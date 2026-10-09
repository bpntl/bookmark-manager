import pytest
from fastapi.testclient import TestClient


@pytest.fixture()
def bookmark():
    """Generates test data for creating a new bookmark."""

    return {
        "name": "Startpage Search",
        "address": "https://www.startpage.com/",
        "description": "Startpage Search",
        "type": "website",
        "status": "added",
    }


@pytest.fixture()
def bookmark_update():
    """Generates test data for updating a bookmark."""

    return {
        "status": "archived",
    }


def test_create_bookmark(test_client: TestClient, bookmark: dict[str, str]) -> None:

    response = test_client.post("/bookmarks", json=bookmark, )

    assert response.status_code == 200

    content = response.json()

    assert content["name"] == bookmark["name"]
    assert content["address"] == bookmark["address"]
    assert content["description"] == bookmark["description"]
    assert content["type"] == bookmark["type"]
    assert content["status"] == bookmark["status"]

    assert "id" in content
    assert "date_added" in content
    assert "date_modified" in content


def test_get_bookmark(test_client: TestClient, bookmark: dict[str, str]):
    response = test_client.get("/bookmarks/1")

    assert response.status_code == 200

    content = response.json()

    assert content["id"] == 1
    assert content["name"] == bookmark["name"]
    assert content["address"] == bookmark["address"]
    assert content["description"] == bookmark["description"]
    assert content["type"] == bookmark["type"]
    assert content["status"] == bookmark["status"]

    assert "date_added" in content
    assert "date_modified" in content


def test_get_bookmark_not_found(test_client: TestClient):
    response = test_client.get("/bookmarks/333")

    assert response.status_code == 404
    assert response.json()["detail"] == "Bookmark with the given id doesn't exist"


def test_get_bookmarks(test_client: TestClient):
    response = test_client.get("/bookmarks")

    assert response.status_code == 200

    content = response.json()

    assert isinstance(content, list)


def test_update_bookmark(test_client: TestClient, bookmark: dict[str, str], bookmark_update: dict[str, str]):
    response = test_client.patch("/bookmarks/1", json=bookmark_update, )

    assert response.status_code == 200

    content = response.json()

    assert content["id"] == 1
    assert content["name"] == bookmark["name"]
    assert content["address"] == bookmark["address"]
    assert content["description"] == bookmark["description"]
    assert content["type"] == bookmark["type"]

    assert "date_added" in content
    assert "date_modified" in content

    assert content["status"] == bookmark_update["status"]
    assert content["date_modified"] > content["date_added"]


def test_delete_bookmark(test_client: TestClient):
    response = test_client.delete("/bookmarks/1")
    assert response.status_code == 200

    response = test_client.get("/bookmarks/1")
    assert response.status_code == 404
