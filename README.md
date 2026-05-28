# 🚀 FastAPI Evolution Roadmap

This repository is an evolutionary project that showcases the development of a REST API using **FastAPI**, progressing from in-memory data handling to relational database persistence, all containerized with **Docker** for immediate deployment.

The goal of this repository is to demonstrate the creation of isolated and clean environments, strict separation of HTTP contracts (POST, PUT, PATCH, DELETE), and production-ready application structures.

## 📂 Repository Structure

The project is divided into independent versions to demonstrate its progression:

*   **`fastapi_memory_v1/`**: Basic REST API that manages tasks using in-memory data structures (lists and dictionaries). Includes basic validation with Pydantic.

*   **`fastapi_sqlite_v2/`**: Version with real data persistence using SQLite. Implements database optimizations (`cursor.rowcount`), strict separation of data models for `PUT` and `PATCH` operations, and protection against empty or null payloads.

*   **`fastapi_postgresql_v3/`** : Version with PostgreSQL persistence managed through the SQLAlchemy 2.0 ORM. Implements dependency injection (Depends), request-scoped session management, strict typing with Pydantic v2 (response_model), partial field updates using setattr, and secure credential handling through environment variables (.env).

## 🛠️ Technologies Used
- **Python** (v3.14-slim)
- **FastAPI** & **Pydantic** (v2)
- **Uvicorn**
- **Docker & Docker Compose** (v3)
- **SQLite** (v2)
- **PostgreSQL** (v3)
- **SQLAlchemy** (v2.0 ORM) (v3)
## 📦 Prerequisites

You only need to have **Docker Desktop** installed on your computer. There is no need to install Python globally, configure virtual environments, or install local databases.

## 🛠️ How to Run the Project (Step by Step)

Choose the version you want to test and execute the following commands in your terminal.

**Clone the Repository**
   ```bash
   git clone https://github.com/DiegoJDArias/fastapi-evolution.git
   cd fastapi-evolution
   ```
**Option A: Run the In-Memory Version (v1)**
   ```bash
   # Enter the version 1 directory
   cd fastapi_memory_v1

   # Build the Docker image
   docker build -t fastapi_memory_v1 .

   # Run the container
   docker run -d -p 8000:8000 fastapi_memory_v1
   ```
**Option B: Run the SQLite Version (v2)**
   ```bash
   # Enter the version 2 directory
   cd fastapi_sqlite_v2

   # Build the Docker image
   docker build -t fastapi_sqlite_v2 .

   # Run the container
   docker run -d -p 8000:8000 fastapi_sqlite_v2
   ```
**Option C: Run the PostgreSQL Version (v3)**
   ```bash
   # Enter the version 3 directory
   cd fastapi_postgresql_v3

   # Copy the environment variables file
   cp .env.example .env

   Open the .env file and fill in the required values.

   # Build the image and start both the API and Database with a single command
   docker-compose up --build
   ```
**Test the API:**

Once the selected version container is running, open your browser and access the auto-generated interactive FastAPI documentation (Swagger UI):

👉 [http://localhost:8000/docs](http://localhost:8000/docs)

💡 *Notes 1: Docker Desktop (Graphical Interface) For v1 and v2, after building the image, it will appear inside Docker Desktop. You can go to the Images tab, search for the desired version `fastapi_memory_v1` or `fastapi_sqlite_v2`, and click the Run button while configuring the local port as `8000`.*

💡 *Notes 2: PostgreSQL Version (v3) Since v3 uses Docker Compose, inside Docker Desktop you will see a unified container stack called `fastapi_postgresql_v3` under the Containers tab. From there, you can start, stop, and monitor both the API and the database together with a single click, without additional configuration.*
