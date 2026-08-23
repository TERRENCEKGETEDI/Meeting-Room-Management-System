# Meeting Room Management System

### Specification/Description
> A meeting room management system application to assist our company to easily book meeting rooms.


### Technologies🧑‍💻
- FastAPI
- Postgresql
- sqlalchemy.


## Project Structure

```text
Meeting Room Management System
│
├── app/
│   ├── main.py
│   ├── models/
│   ├── schemas/
│   ├── routes/
│   └── database/
│
├── .env
├── .gitignore
├── requirements.txt
└── README.md
```

### Installation
- clone/download the project
```bash
    git clone https://github.com/TERRENCEKGETEDI/Meeting-Room-Management-System.git
```
- download python v3.14.6
- download postgres v18
- download pip v26.1.2
- activate virtual environment
```bash
    python3 -m venv .venv
    source .venv/bin/activate
```
- install the project dependencies requirement.txt
```bash
    pip install -r requirements.txt
```
> create the .env file with the following variables
```bash
    DB_NAME=db_name
    DB_USER=db_username
    DB_PASSWORD=password
    DB_HOST=localhost
    DB_PORT=5432
```

### Usage
```bash
    uvicorn app.main:app --reload
```
- and visit the broswer at:
```bash
    http://localhost:8000/[paths][parameters]
```
- OR
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
```bash
   git pull origin main
```
