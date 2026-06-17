import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pyodbc
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# Get database credentials
SERVER = os.getenv("SQL_SERVER")
DATABASE = os.getenv("SQL_DATABASE")
USER = os.getenv("SQL_USER")
PASSWORD = os.getenv("SQL_PASSWORD")
DRIVER = "{ODBC Driver 18 for SQL Server}"

connection_string = f"Driver={DRIVER};Server=tcp:{SERVER},1433;Database={DATABASE};Uid={USER};Pwd={PASSWORD};Encrypt=yes;TrustServerCertificate=yes;ConnectionTimeout=30;"

def get_db_connection():
    return pyodbc.connect(connection_string)

# Pydantic schema for request validation
class Client(BaseModel):
    ClientCode: str
    ClientName: str

@app.get("/clients")
def get_clients():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT ClientCode, ClientName FROM Clients")
        rows = cursor.fetchall()
        
        clients = [{"ClientCode": row[0], "ClientName": row[1]} for row in rows]
        conn.close()
        return clients
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/clients")
def add_client(client: Client):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Clients (ClientCode, ClientName) VALUES (?, ?)", (client.ClientCode, client.ClientName))
        conn.commit()
        conn.close()
        return {"message": "Client added successfully", "client": client}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

