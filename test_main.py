# test_main.py
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from .main import app
from .database import get_db
from .models import Base

# Configurar um banco de dados SQLite para testes
SQLALCHEMY_DATABASE_URL = "sqlite:///./note.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Usar a base de dados de teste
Base.metadata.create_all(bind=engine)

# Dependência de teste
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

@pytest.fixture
def db():
    # Cria uma nova sessão de banco de dados para cada teste
     Base.metadata.create_all(bind=engine)
     db = TestingSessionLocal()
     try:
         yield db
     finally:
         db.close()
         Base.metadata.drop_all(bind=engine)

def test_create_task(db):
    response = client.post("/tasks/", json={"id": 1, "title": "Tarefa", "description": "Tarefa 1", "status": "Concluida", "createdAt": "2024-06-10T22:31:01.202Z" })
    assert response.status_code == 200
    data = response.json()
#    assert data["id"] == 1    
#    assert data["title"] == "Tarefa"
#    assert data["email"] == "Tarefa 1"
#    assert data["Status"] == "Concluida"
#    assert data["created"] == "2024-06-10T22:31:01.202Z"


def test_read_task(db):
    response = client.get("/tasks/", json={"title": "Tarefa", "description": "Tarefa 1", "status": "Concluida"})
    assert response.status_code == 200
    user_id = response.json()["0"]

    response = client.get(f"/tasks/{user_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Tarefa"
    assert data["description"] == "Tarefa 1"
    assert data["status"] == "Concluida"

def test_read_task_not_found(db):
    response = client.get("/tasks/0")
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "User not found"
