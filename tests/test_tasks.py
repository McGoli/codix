from datetime import date

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database import Base, get_db
from app.main import app

SQLALCHEMY_DATABASE_URL = "sqlite:///./test_tasks.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


def test_create_task():
    response = client.post(
        "/tasks",
        json={
            "title": "Nouvelle tâche",
            "description": "Description",
            "status": "à faire",
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Nouvelle tâche"
    assert data["status"] == "à faire"


def test_read_tasks():
    response = client.get("/tasks")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1


def test_update_task():
    response = client.post(
        "/tasks",
        json={
            "title": "Tâche à mettre à jour",
            "status": "à faire",
        },
    )
    task_id = response.json()["id"]

    update_response = client.put(
        f"/tasks/{task_id}",
        json={
            "title": "Tâche mise à jour",
            "status": "en cours",
            "date_limite": date.today().isoformat(),
        },
    )
    assert update_response.status_code == 200
    updated_task = update_response.json()
    assert updated_task["title"] == "Tâche mise à jour"
    assert updated_task["status"] == "en cours"
    assert updated_task["date_limite"] == date.today().isoformat()


def test_delete_task():
    response = client.post(
        "/tasks",
        json={
            "title": "Tâche à supprimer",
            "status": "à faire",
        },
    )
    task_id = response.json()["id"]

    delete_response = client.delete(f"/tasks/{task_id}")
    assert delete_response.status_code == 204

    get_response = client.get(f"/tasks/{task_id}")
    assert get_response.status_code == 404
