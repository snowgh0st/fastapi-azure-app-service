import os
import pyodbc
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv() # Load environment variables from .env

app = FastAPI()

# Allow frontend to communicate with API (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Change to your deployed frontend domain in production
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database Connection Helper
def get_db_connection():
    server = os.getenv("SQL_SERVER")
    database = os.getenv("SQL_DB")
    username = os.getenv("SQL_USER")
    password = os.getenv("SQL_PASSWORD")
    driver = os.getenv("SQL_DRIVER")

    conn_str = f"DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}"
    return pyodbc.connect(conn_str)

# Pydantic Model
class Client(BaseModel):
    ClientCode: str
    ClientName: str

# CREATE
@app.post("/clients/")
def create_client(client: Client):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Clients (ClientCode, ClientName) VALUES (?, ?)", client.ClientCode, client.ClientName)
        conn.commit()
        conn.close()
        return {"message": "Client created successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# READ ALL
@app.get("/clients/")
def get_clients():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT ClientCode, ClientName FROM Clients")
    rows = cursor.fetchall()
    conn.close()
    return [{"ClientCode": row[0], "ClientName": row[1]} for row in rows]

# UPDATE
@app.put("/clients/{client_code}")
def update_client(client_code: str, client: Client):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE Clients SET ClientName = ? WHERE ClientCode = ?", client.ClientName, client_code)
    conn.commit()
    conn.close()
    return {"message": "Client updated successfully"}

# DELETE
@app.delete("/clients/{client_code}")
def delete_client(client_code: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Clients WHERE ClientCode = ?", client_code)
    conn.commit()
    conn.close()
    return {"message": "Client deleted successfully"}
