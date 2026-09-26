import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, delete
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database import Base, get_db
from app.main import app
from app.models import Article


TEST_DATABASE_URL = "sqlite://"

test_engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)

TestingSessionLocal = sessionmaker(
    bind=test_engine,
    autoflush=False,
    autocommit=False
)

Base.metadata.create_all(bind=test_engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


@pytest.fixture(autouse=True)
def clean_database():
    with TestingSessionLocal() as db:
        db.execute(delete(Article))
        db.commit()

    yield


def create_test_article():
    response = client.post(
        "/articles",
        json={
            "title": "Test article",
            "source_url": "https://example.com/test",
            "municipality": "Naklo",
            "status": "draft"
        }
    )

    assert response.status_code == 201
    return response.json()


def test_health_check():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_create_article():
    data = create_test_article()

    assert data["title"] == "Test article"
    assert data["municipality"] == "Naklo"
    assert data["status"] == "draft"
    assert "id" in data
    assert "created_at" in data


def test_create_article_validation_error():
    response = client.post(
        "/articles",
        json={
            "title": "A",
            "source_url": "not-a-url",
            "municipality": "X",
            "status": "wrong"
        }
    )

    assert response.status_code == 422


def test_get_article():
    article = create_test_article()

    response = client.get(f"/articles/{article['id']}")

    assert response.status_code == 200
    assert response.json()["id"] == article["id"]
    assert response.json()["title"] == "Test article"


def test_update_article():
    article = create_test_article()

    response = client.patch(
        f"/articles/{article['id']}",
        json={"status": "published"}
    )

    assert response.status_code == 200
    assert response.json()["status"] == "published"

    check_response = client.get(f"/articles/{article['id']}")

    assert check_response.status_code == 200
    assert check_response.json()["status"] == "published"


def test_delete_article():
    article = create_test_article()

    response = client.delete(f"/articles/{article['id']}")

    assert response.status_code == 204

    check_response = client.get(f"/articles/{article['id']}")

    assert check_response.status_code == 404
    assert check_response.json() == {"detail": "Article not found"}


def test_get_missing_article():
    response = client.get("/articles/999999")

    assert response.status_code == 404
    assert response.json() == {"detail": "Article not found"}
