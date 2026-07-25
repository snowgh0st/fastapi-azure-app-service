# 🌐 FastAPI for Azure App Service

A modern FastAPI backend for a full-stack CRUD application that manages client records in a PostgreSQL database hosted on Google Cloud Platform.

> ℹ️ This repository is only 1 of 3 components that make up the complete application. It serves as the backend service, while the frontend lives at https://github.com/snowgh0st/frontend-vercel and the webhook service lives at https://github.com/snowgh0st/webhook-azure-function.

## 🧩 What This Backend Does

- Exposes RESTful CRUD endpoints for client records
- Connects to PostgreSQL using FastAPI and Python
- Supports create, read, update, patch, and delete operations
- Includes CORS support for frontend integration
- Handles database errors with retry logic and clear API responses

## 🛠️ Tech Stack

- Python
- FastAPI
- pyodbc
- PostgreSQL
- Tenacity

## ⚙️ Getting Started

1. Create and activate a virtual environment
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set the required environment variables for your database connection:
   - SQL_SERVER
   - SQL_DATABASE
   - SQL_USER
   - SQL_PASSWORD
   - SQL_DRIVER
4. Run the API locally:
   ```bash
   uvicorn index:app --reload
   ```

## 📡 API Overview

The backend provides endpoints for managing clients, including:

- POST /clients/
- GET /clients/
- PUT /clients/{client_code}
- PATCH /clients/{client_code}
- DELETE /clients/{client_code}

## 🔗 Related Repositories

- Frontend: https://github.com/snowgh0st/frontend-vercel
- Webhook: https://github.com/snowgh0st/webhook-azure-function

## 📄 License

This project is licensed under the MIT License. See the LICENSE file for more details.
