# Meeting Room Management System

### Specification/Description
> A meeting room management system application to assist our company to easily book meeting rooms.


### Technologies🧑‍💻
- Python 3.14
- FastAPI
- Pydantic
- Postgresql
- sqlalchemy
- Uvicorn
- uv


## Project Structure

```text
Meeting Room Management System
│
├── app/
│   ├── main.py
│   ├── auth/
│   ├── database/
│   ├── dependencies/
│   ├── models/
│   ├── routes/
│   ├── schemas/
│   └── services/
│
├── .env
├── .gitignore
├── pyproject.toml
├── uv.lock
└── README.md
```

### Installation
1. clone/download the project
    ```bash
        git clone https://github.com/TERRENCEKGETEDI/Meeting-Room-Management-System.git
    ```
2. Download and Install the required tools
   - Python 3.14
   - PostgreSQL v18
   - uv
  
3. Install project dependencies
   - `uv` will create virtual environment and install the dependencies
    ```bash
        uv sync
    ```

> Configure environment variables
```bash
    DB_NAME=db_name
    DB_USER=db_username
    DB_PASSWORD=password
    DB_HOST=localhost
    DB_PORT=5432
    SECRETE_KEY=my_secrete_key
```

### Usage
- Run the FastAPI application with
    ```bash
        uv run uvicorn app.main:app --reload
    ```
- The API will be available at
    ```bash
        http://localhost:8000
    ```
- Swagger
    ```bash
        http://localhost:8000/docs
    ```
- for FastAPI documentation

### Features
- creates a room
- edits a room
- delete a room
- list room
- list rooms by filtering with capacity

### Get latest changes
- To retrieve the latest changes from the main branch:
```bash
   git pull origin main
```
