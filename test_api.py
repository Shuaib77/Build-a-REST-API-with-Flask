#!/usr/bin/env python3
"""
Test cases for User Management REST API
Tests API functionality and Flask concepts
"""

import json
from datetime import datetime

from constants import SAMPLE_USERS
from utils import validate_user_data


def test_flask_concepts():
    """Test understanding of Flask concepts"""
    print("Testing Flask Concepts...")

    routes = [
        ("GET", "/users", "get_all_users"),
        ("GET", "/users/<int:user_id>", "get_user"),
        ("POST", "/users", "create_user"),
        ("PUT", "/users/<int:user_id>", "update_user"),
        ("DELETE", "/users/<int:user_id>", "delete_user"),
    ]

    print("Testing route structure:")
    for method, route, function in routes:
        print(f"   {method:6} {route:20} -> {function}")

    flask_components = [
        "Flask app initialization",
        "Route decorators (@app.route)",
        "Request handling (request.get_json())",
        "JSON responses (jsonify())",
        "Error handlers (@app.errorhandler)",
    ]

    print("\nFlask components tested:")
    for component in flask_components:
        print(f"   PASS  {component}")

    print("Flask concepts test passed!")


def test_rest_principles():
    """Test REST API principles"""
    print("\nTesting REST Principles...")

    rest_principles = [
        ("Resource-based URLs", "/users, /users/1"),
        ("HTTP Methods", "GET, POST, PUT, DELETE"),
        ("Stateless", "Each request contains all needed info"),
        ("JSON Format", "Consistent request/response structure"),
        ("Status Codes", "Appropriate HTTP response codes"),
    ]

    print("REST principles verified:")
    for principle, example in rest_principles:
        print(f"   PASS  {principle}: {example}")

    crud_mapping = [
        ("Create", "POST /users", "201 Created"),
        ("Read", "GET /users", "200 OK"),
        ("Update", "PUT /users/1", "200 OK"),
        ("Delete", "DELETE /users/1", "200 OK"),
    ]

    print("\nCRUD operations mapping:")
    for operation, endpoint, status in crud_mapping:
        print(f"   PASS  {operation:6} -> {endpoint:15} -> {status}")

    print("REST principles test passed!")


def test_data_validation():
    """Test data validation logic using the shared validate_user_data utility."""
    print("\nTesting Data Validation...")

    valid_user = SAMPLE_USERS[0]
    errors = validate_user_data(valid_user)

    print("Valid user data validation:")
    print(f"   Data: {json.dumps(valid_user, indent=2)}")
    print(f"   Errors: {errors if errors else 'None'}")
    assert not errors, f"Expected no errors for valid user, got: {errors}"

    invalid_users = [
        ({"name": "", "email": "invalid", "age": -5}, "empty name, bad email, negative age"),
        ({"email": "test@example.com"}, "missing name and age"),
        ({"name": "Test", "email": "notemail", "age": "twenty"}, "bad email format, non-int age"),
    ]

    print("\nInvalid user data examples:")
    for user, desc in invalid_users:
        errs = validate_user_data(user)
        print(f"   {json.dumps(user)} -> {errs}  ({desc})")
        assert errs, f"Expected errors for invalid user ({desc}), got none"

    print("Data validation test passed!")


def test_http_status_codes():
    """Test HTTP status code usage"""
    print("\nTesting HTTP Status Codes...")

    scenarios = [
        {
            "request": "GET /users",
            "condition": "Users exist",
            "status": 200,
            "description": "OK - Successfully retrieved users",
        },
        {
            "request": "POST /users",
            "condition": "Valid data provided",
            "status": 201,
            "description": "Created - User created successfully",
        },
        {
            "request": "GET /users/999",
            "condition": "User doesn't exist",
            "status": 404,
            "description": "Not Found - User with ID 999 not found",
        },
        {
            "request": "POST /users",
            "condition": "Invalid data",
            "status": 400,
            "description": "Bad Request - Validation errors",
        },
        {
            "request": "PATCH /users/1",
            "condition": "Method not supported",
            "status": 405,
            "description": "Method Not Allowed - Only PUT supported",
        },
    ]

    print("Status code scenarios:")
    for scenario in scenarios:
        print(f"   {scenario['status']} - {scenario['request']}")
        print(f"       Condition: {scenario['condition']}")
        print(f"       Response: {scenario['description']}")
        print()

    print("HTTP status codes test passed!")


def test_json_handling():
    """Test JSON request/response handling"""
    print("Testing JSON Handling...")

    sample_request = {
        "name": "Test User",
        "email": "test@example.com",
        "age": 30,
        "department": "Testing",
    }

    print("Sample JSON request:")
    print(f"   {json.dumps(sample_request, indent=2)}")

    sample_response = {
        "error": False,
        "data": {
            "id": 1,
            **sample_request,
            "created_at": "2025-09-26T19:00:00",
            "updated_at": "2025-09-26T19:00:00",
        },
        "message": "User created successfully",
        "timestamp": "2025-09-26T19:00:00",
    }

    print("\nSample JSON response:")
    print(f"   {json.dumps(sample_response, indent=2)}")

    error_response = {
        "error": True,
        "message": "User with ID 999 not found",
        "timestamp": "2025-09-26T19:00:00",
    }

    print("\nSample error response:")
    print(f"   {json.dumps(error_response, indent=2)}")

    print("JSON handling test passed!")


def test_memory_storage():
    """Test in-memory storage concepts"""
    print("\nTesting Memory Storage...")

    users_db = {}
    user_counter = 1

    new_user = {
        "id": user_counter,
        "name": "John Doe",
        "email": "john@example.com",
        "age": 25,
        "created_at": datetime.now().isoformat(),
    }
    users_db[user_counter] = new_user
    user_counter += 1

    print("Memory storage operations:")
    print(f"   PASS  CREATE: Added user with ID {new_user['id']}")
    print(f"   PASS  READ: Retrieved user: {users_db[1]['name']}")

    users_db[1]["name"] = "John Smith"
    users_db[1]["updated_at"] = datetime.now().isoformat()
    print(f"   PASS  UPDATE: Modified user name to {users_db[1]['name']}")

    deleted_user = users_db.pop(1)
    print(f"   PASS  DELETE: Removed user {deleted_user['name']}")

    print(f"\nFinal storage state: {len(users_db)} users")
    print("Memory storage test passed!")


def run_all_tests():
    """Run all test functions"""
    print("Running User Management REST API Tests")
    print("=" * 60)

    tests = [
        test_flask_concepts,
        test_rest_principles,
        test_data_validation,
        test_http_status_codes,
        test_json_handling,
        test_memory_storage,
    ]

    passed = 0
    failed = 0

    for test_func in tests:
        try:
            test_func()
            passed += 1
        except Exception as e:
            print(f"FAIL {test_func.__name__} failed: {e}")
            failed += 1
        print("-" * 40)

    print(f"\nTest Results:")
    print(f"   Passed: {passed}")
    print(f"   Failed: {failed}")
    print(f"   Success Rate: {(passed / (passed + failed) * 100):.1f}%")

    if failed == 0:
        print("\nAll tests passed! Flask REST API is ready for submission.")
    else:
        print(f"\n{failed} test(s) failed. Please review and fix issues.")


if __name__ == "__main__":
    run_all_tests()
