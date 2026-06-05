"""
Unit tests for the User Management REST API (app.py).

Uses Flask's built-in test client to exercise every route, validation path,
and helper function. Run with:
    pytest tests/ --cov=app --cov-report=term-missing
"""

import json
import pytest

from app import (
    app,
    initialize_sample_data,
    validate_user_data,
    get_user_by_id,
    create_error_response,
    create_success_response,
    users_db,
)


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def client():
    """Create a fresh test client with sample data for each test."""
    import app as app_module

    app.config["TESTING"] = True
    # Reset state before each test
    app_module.users_db = {}
    app_module.user_counter = 1
    initialize_sample_data()

    with app.test_client() as client:
        yield client

    # Cleanup
    app_module.users_db = {}
    app_module.user_counter = 1


@pytest.fixture
def empty_client():
    """Test client with no users in the database."""
    import app as app_module

    app.config["TESTING"] = True
    app_module.users_db = {}
    app_module.user_counter = 1

    with app.test_client() as client:
        yield client

    app_module.users_db = {}
    app_module.user_counter = 1


# ---------------------------------------------------------------------------
# Helper function tests
# ---------------------------------------------------------------------------

class TestValidateUserData:
    """Tests for validate_user_data helper."""

    def test_valid_full_user(self):
        data = {"name": "Alice", "email": "alice@example.com", "age": 30}
        assert validate_user_data(data) == []

    def test_missing_name(self):
        data = {"email": "a@b.com", "age": 20}
        errors = validate_user_data(data)
        assert any("'name' is required" in e for e in errors)

    def test_missing_email(self):
        data = {"name": "Bob", "age": 20}
        errors = validate_user_data(data)
        assert any("'email' is required" in e for e in errors)

    def test_missing_age(self):
        data = {"name": "Bob", "email": "b@c.com"}
        errors = validate_user_data(data)
        assert any("'age' is required" in e for e in errors)

    def test_empty_name(self):
        data = {"name": "", "email": "a@b.com", "age": 20}
        errors = validate_user_data(data)
        assert any("'name' is required" in e for e in errors)

    def test_invalid_email_no_at(self):
        data = {"name": "X", "email": "invalid", "age": 20}
        errors = validate_user_data(data)
        assert any("Invalid email" in e for e in errors)

    def test_invalid_email_no_dot(self):
        data = {"name": "X", "email": "user@nodot", "age": 20}
        errors = validate_user_data(data)
        assert any("Invalid email" in e for e in errors)

    def test_negative_age(self):
        data = {"name": "X", "email": "x@y.com", "age": -1}
        errors = validate_user_data(data)
        assert any("Age must be a positive integer" in e for e in errors)

    def test_non_int_age(self):
        data = {"name": "X", "email": "x@y.com", "age": "twenty"}
        errors = validate_user_data(data)
        assert any("Age must be a positive integer" in e for e in errors)

    def test_update_mode_allows_missing_age(self):
        data = {"name": "X", "email": "x@y.com"}
        errors = validate_user_data(data, is_update=True)
        assert errors == []

    def test_update_mode_still_requires_name_email(self):
        data = {"age": 20}
        errors = validate_user_data(data, is_update=True)
        assert any("'name' is required" in e for e in errors)
        assert any("'email' is required" in e for e in errors)


class TestGetUserById:
    """Tests for get_user_by_id helper."""

    def test_existing_user(self, client):
        user = get_user_by_id(1)
        assert user is not None
        assert user["name"] == "John Doe"

    def test_nonexistent_user(self, client):
        assert get_user_by_id(999) is None


# ---------------------------------------------------------------------------
# Route tests: Home & Health
# ---------------------------------------------------------------------------

class TestHomeEndpoint:
    def test_home_returns_200(self, client):
        resp = client.get("/")
        assert resp.status_code == 200

    def test_home_contains_endpoints(self, client):
        resp = client.get("/")
        data = resp.get_json()
        assert data["error"] is False
        assert "endpoints" in data["data"]

    def test_home_reports_total_users(self, client):
        resp = client.get("/")
        data = resp.get_json()
        assert data["data"]["total_users"] == 3


class TestHealthEndpoint:
    def test_health_returns_200(self, client):
        resp = client.get("/health")
        assert resp.status_code == 200

    def test_health_status_healthy(self, client):
        resp = client.get("/health")
        data = resp.get_json()
        assert data["data"]["status"] == "healthy"


# ---------------------------------------------------------------------------
# Route tests: GET /users
# ---------------------------------------------------------------------------

class TestGetAllUsers:
    def test_returns_all_sample_users(self, client):
        resp = client.get("/users")
        data = resp.get_json()
        assert resp.status_code == 200
        assert data["data"]["total"] == 3
        assert len(data["data"]["users"]) == 3

    def test_pagination_page_1(self, client):
        resp = client.get("/users?page=1&per_page=2")
        data = resp.get_json()
        assert len(data["data"]["users"]) == 2
        assert data["data"]["page"] == 1
        assert data["data"]["per_page"] == 2

    def test_pagination_page_2(self, client):
        resp = client.get("/users?page=2&per_page=2")
        data = resp.get_json()
        assert len(data["data"]["users"]) == 1

    def test_empty_database(self, empty_client):
        resp = empty_client.get("/users")
        data = resp.get_json()
        assert resp.status_code == 200
        assert data["data"]["total"] == 0
        assert data["data"]["users"] == []


# ---------------------------------------------------------------------------
# Route tests: GET /users/<id>
# ---------------------------------------------------------------------------

class TestGetUser:
    def test_existing_user(self, client):
        resp = client.get("/users/1")
        data = resp.get_json()
        assert resp.status_code == 200
        assert data["data"]["name"] == "John Doe"

    def test_nonexistent_user_returns_404(self, client):
        resp = client.get("/users/999")
        data = resp.get_json()
        assert resp.status_code == 404
        assert data["error"] is True
        assert "999" in data["message"]


# ---------------------------------------------------------------------------
# Route tests: POST /users
# ---------------------------------------------------------------------------

class TestCreateUser:
    def test_create_valid_user(self, client):
        payload = {
            "name": "New User",
            "email": "new@example.com",
            "age": 25,
            "department": "QA",
        }
        resp = client.post("/users", json=payload)
        data = resp.get_json()
        assert resp.status_code == 201
        assert data["data"]["name"] == "New User"
        assert data["data"]["email"] == "new@example.com"
        assert "created_at" in data["data"]

    def test_create_user_without_department(self, client):
        payload = {"name": "No Dept", "email": "nodept@example.com", "age": 22}
        resp = client.post("/users", json=payload)
        data = resp.get_json()
        assert resp.status_code == 201
        assert data["data"]["department"] == ""

    def test_create_user_missing_fields(self, client):
        payload = {"name": "Incomplete"}
        resp = client.post("/users", json=payload)
        assert resp.status_code == 400
        data = resp.get_json()
        assert data["error"] is True

    def test_create_user_invalid_email(self, client):
        payload = {"name": "Bad Email", "email": "nope", "age": 20}
        resp = client.post("/users", json=payload)
        assert resp.status_code == 400

    def test_create_user_duplicate_email(self, client):
        payload = {
            "name": "Dup",
            "email": "john.doe@example.com",
            "age": 30,
        }
        resp = client.post("/users", json=payload)
        assert resp.status_code == 400
        data = resp.get_json()
        assert "already exists" in data["message"]

    def test_create_user_non_json_request(self, client):
        resp = client.post(
            "/users",
            data="not json",
            content_type="text/plain",
        )
        assert resp.status_code == 400
        data = resp.get_json()
        assert "JSON" in data["message"]

    def test_create_user_empty_body(self, client):
        resp = client.post(
            "/users",
            data=json.dumps(None),
            content_type="application/json",
        )
        assert resp.status_code == 400

    def test_create_user_negative_age(self, client):
        payload = {"name": "Young", "email": "young@x.com", "age": -5}
        resp = client.post("/users", json=payload)
        assert resp.status_code == 400


# ---------------------------------------------------------------------------
# Route tests: PUT /users/<id>
# ---------------------------------------------------------------------------

class TestUpdateUser:
    def test_update_name(self, client):
        payload = {"name": "Updated Name", "email": "john.doe@example.com"}
        resp = client.put("/users/1", json=payload)
        data = resp.get_json()
        assert resp.status_code == 200
        assert data["data"]["name"] == "Updated Name"

    def test_update_email(self, client):
        payload = {"name": "John Doe", "email": "newemail@example.com"}
        resp = client.put("/users/1", json=payload)
        data = resp.get_json()
        assert resp.status_code == 200
        assert data["data"]["email"] == "newemail@example.com"

    def test_update_nonexistent_user(self, client):
        payload = {"name": "Ghost", "email": "ghost@x.com"}
        resp = client.put("/users/999", json=payload)
        assert resp.status_code == 404

    def test_update_duplicate_email(self, client):
        payload = {"name": "Jane Smith", "email": "john.doe@example.com"}
        resp = client.put("/users/2", json=payload)
        assert resp.status_code == 400
        data = resp.get_json()
        assert "already exists" in data["message"]

    def test_update_non_json_request(self, client):
        resp = client.put(
            "/users/1",
            data="not json",
            content_type="text/plain",
        )
        assert resp.status_code == 400

    def test_update_empty_body(self, client):
        resp = client.put(
            "/users/1",
            data=json.dumps(None),
            content_type="application/json",
        )
        assert resp.status_code == 400

    def test_update_sets_updated_at(self, client):
        payload = {"name": "Time Check", "email": "john.doe@example.com"}
        resp = client.put("/users/1", json=payload)
        data = resp.get_json()
        assert "updated_at" in data["data"]

    def test_update_invalid_email_format(self, client):
        payload = {"name": "X", "email": "bademail"}
        resp = client.put("/users/1", json=payload)
        assert resp.status_code == 400


# ---------------------------------------------------------------------------
# Route tests: DELETE /users/<id>
# ---------------------------------------------------------------------------

class TestDeleteUser:
    def test_delete_existing_user(self, client):
        resp = client.delete("/users/1")
        data = resp.get_json()
        assert resp.status_code == 200
        assert "deleted_user" in data["data"]
        assert data["data"]["deleted_user"]["id"] == 1

    def test_delete_nonexistent_user(self, client):
        resp = client.delete("/users/999")
        assert resp.status_code == 404

    def test_delete_removes_from_db(self, client):
        client.delete("/users/1")
        resp = client.get("/users/1")
        assert resp.status_code == 404


# ---------------------------------------------------------------------------
# Route tests: POST /reset
# ---------------------------------------------------------------------------

class TestResetEndpoint:
    def test_reset_restores_sample_data(self, client):
        # Delete all users first
        client.delete("/users/1")
        client.delete("/users/2")
        client.delete("/users/3")
        # Reset
        resp = client.post("/reset")
        data = resp.get_json()
        assert resp.status_code == 200
        assert data["data"]["total_users"] == 3


# ---------------------------------------------------------------------------
# Error handler tests
# ---------------------------------------------------------------------------

class TestErrorHandlers:
    def test_404_unknown_route(self, client):
        resp = client.get("/nonexistent")
        assert resp.status_code == 404
        data = resp.get_json()
        assert data["error"] is True

    def test_405_method_not_allowed(self, client):
        resp = client.patch("/users/1")
        assert resp.status_code == 405
        data = resp.get_json()
        assert data["error"] is True


# ---------------------------------------------------------------------------
# Response format tests
# ---------------------------------------------------------------------------

class TestResponseFormat:
    def test_success_response_has_timestamp(self, client):
        resp = client.get("/health")
        data = resp.get_json()
        assert "timestamp" in data

    def test_error_response_has_timestamp(self, client):
        resp = client.get("/users/999")
        data = resp.get_json()
        assert "timestamp" in data

    def test_success_response_structure(self, client):
        resp = client.get("/users/1")
        data = resp.get_json()
        assert "error" in data
        assert "data" in data
        assert data["error"] is False

    def test_error_response_structure(self, client):
        resp = client.get("/users/999")
        data = resp.get_json()
        assert "error" in data
        assert "message" in data
        assert data["error"] is True
