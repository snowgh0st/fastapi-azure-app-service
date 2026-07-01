import os
import pyodbc
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from contextlib import contextmanager
from tenacity import retry, stop_after_attempt, wait_fixed, retry_if_exception_type

app = FastAPI()

# Allow frontend to communicate with API (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://my-crud-frontend-nu.vercel.app" # Replace with your actual Vercel frontend URL
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Database Connection Helper (Wrapped with Tenacity)
@retry(
    stop=stop_after_attempt(3), 
    wait=wait_fixed(2), 
    retry=retry_if_exception_type(Exception),
    reraise=True # Re-raises exception after final retry so FastAPI can catch it
)
def get_db_connection():
    server = os.environ.get("SQL_SERVER")
    database = os.environ.get("SQL_DATABASE")
    username = os.environ.get("SQL_USER")
    password = os.environ.get("SQL_PASSWORD")
    driver = os.environ.get("SQL_DRIVER")

    conn_str = f"DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}"
    return pyodbc.connect(conn_str)

# Pydantic Model
class Client(BaseModel):
    ClientCode: str
    ClientName: str

@contextmanager
def get_db_cursor():
    conn = get_db_connection()
    try:
        yield conn.cursor()
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


# CREATE
@app.post("/clients/")
def create_client(client: Client):
    try:
        with get_db_cursor() as cursor:
            cursor.execute("INSERT INTO Clients (ClientCode, ClientName) VALUES (?, ?)", client.ClientCode, client.ClientName)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    return {"message": "Client created successfully"}

# READ ALL
@app.get("/clients/")
def get_clients():
    try:
        with get_db_cursor() as cursor:
            cursor.execute("SELECT ClientCode, ClientName FROM Clients")
            columns = [column[0] for column in cursor.description]
            results = [dict(zip(columns, row)) for row in cursor.fetchall()]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return results

# UPDATE
@app.put("/clients/{client_code}")
def update_client(client_code: str, client: Client):
    try:
        with get_db_cursor() as cursor:
            cursor.execute("UPDATE Clients SET ClientName = ? WHERE ClientCode = ?", client.ClientName, client_code)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    return {"message": "Client updated successfully"}

# PATCH
@app.patch("/clients/{client_code}")
def patch_client(client_code: str, client: Client):
    try:
        with get_db_cursor() as cursor:
            cursor.execute("UPDATE Clients SET ClientName = ? WHERE ClientCode = ?", client.ClientName, client_code)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    return {"message": "Client patched successfully"}

# DELETE
@app.delete("/clients/{client_code}")
def delete_client(client_code: str):
    try:
        with get_db_cursor() as cursor:
            cursor.execute("DELETE FROM Clients WHERE ClientCode = ?", client_code)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    return {"message": "Client deleted successfully"}
