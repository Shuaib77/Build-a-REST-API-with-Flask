#!/usr/bin/env python3
"""
Demo script for User Management REST API
This script demonstrates API testing without running the Flask server
"""

import json
from datetime import datetime

def demo_api_concepts():
    """Demonstrate REST API concepts and Flask functionality"""
    print("🚀 User Management REST API - Demo Mode")
    print("=" * 60)
    print("This demo shows REST API concepts and request/response examples\n")

def demo_flask_routes():
    """Demonstrate Flask route concepts"""
    print("🛠 Flask Routes Demo")
    print("=" * 40)

    routes = [
        {
            "method": "GET",
            "endpoint": "/users",
            "description": "Retrieve all users",
            "parameters": "?page=1&per_page=10 (optional)"
        },
        {
            "method": "GET", 
            "endpoint": "/users/<id>",
            "description": "Get specific user by ID",
            "parameters": "id: integer (path parameter)"
        },
        {
            "method": "POST",
            "endpoint": "/users",
            "description": "Create new user",
            "parameters": "JSON body with user data"
        },
        {
            "method": "PUT",
            "endpoint": "/users/<id>", 
            "description": "Update existing user",
            "parameters": "id: integer, JSON body with updates"
        },
        {
            "method": "DELETE",
            "endpoint": "/users/<id>",
            "description": "Delete user by ID", 
            "parameters": "id: integer (path parameter)"
        }
    ]

    print("📍 Available API Endpoints:")
    for route in routes:
        print(f"   {route['method']:6} {route['endpoint']:15} - {route['description']}")
        if route['parameters']:
            print(f"          Parameters: {route['parameters']}")

    return routes

def demo_http_methods():
    """Demonstrate HTTP methods and their usage"""
    print("\n🌐 HTTP Methods Demo")
    print("=" * 40)

    methods = {
        "GET": {
            "purpose": "Retrieve/Read data",
            "idempotent": True,
            "safe": True,
            "example": "GET /users - Get all users"
        },
        "POST": {
            "purpose": "Create new resource",
            "idempotent": False,
            "safe": False,
            "example": "POST /users - Create new user"
        },
        "PUT": {
            "purpose": "Update/Replace resource",
            "idempotent": True,
            "safe": False,
            "example": "PUT /users/1 - Update user 1"
        },
        "DELETE": {
            "purpose": "Remove resource",
            "idempotent": True,
            "safe": False,
            "example": "DELETE /users/1 - Delete user 1"
        }
    }

    print("📡 HTTP Methods Explained:")
    for method, details in methods.items():
        print(f"\n   {method}:")
        print(f"     Purpose: {details['purpose']}")
        print(f"     Idempotent: {details['idempotent']}")
        print(f"     Safe: {details['safe']}")
        print(f"     Example: {details['example']}")

def demo_request_response_examples():
    """Demonstrate API request and response formats"""
    print("\n📋 Request/Response Examples")
    print("=" * 40)

    # POST request example
    print("\n1. CREATE USER (POST /users)")
    print("   Request:")
    create_request = {
        "name": "Alice Johnson",
        "email": "alice.johnson@example.com",
        "age": 28,
        "department": "Product Management"
    }
    print("   " + json.dumps(create_request, indent=4).replace('\n', '\n   '))

    print("\n   Response (201 Created):")
    create_response = {
        "error": False,
        "data": {
            "id": 4,
            "name": "Alice Johnson", 
            "email": "alice.johnson@example.com",
            "age": 28,
            "department": "Product Management",
            "created_at": "2025-09-26T19:05:00",
            "updated_at": "2025-09-26T19:05:00"
        },
        "message": "User created successfully with ID 4",
        "timestamp": "2025-09-26T19:05:00"
    }
    print("   " + json.dumps(create_response, indent=4).replace('\n', '\n   '))

    # GET request example
    print("\n\n2. GET ALL USERS (GET /users)")
    print("   Request: GET /users?page=1&per_page=5")
    print("\n   Response (200 OK):")
    get_response = {
        "error": False,
        "data": {
            "users": [
                {
                    "id": 1,
                    "name": "John Doe",
                    "email": "john.doe@example.com", 
                    "age": 28,
                    "department": "Engineering"
                },
                {
                    "id": 2,
                    "name": "Jane Smith",
                    "email": "jane.smith@example.com",
                    "age": 25,
                    "department": "Marketing"
                }
            ],
            "total": 2,
            "page": 1,
            "per_page": 5,
            "pages": 1
        },
        "timestamp": "2025-09-26T19:10:00"
    }
    print("   " + json.dumps(get_response, indent=4).replace('\n', '\n   '))

    # Error response example
    print("\n\n3. ERROR RESPONSE (404 Not Found)")
    print("   Request: GET /users/999")
    print("\n   Response (404 Not Found):")
    error_response = {
        "error": True,
        "message": "User with ID 999 not found",
        "timestamp": "2025-09-26T19:15:00"
    }
    print("   " + json.dumps(error_response, indent=4).replace('\n', '\n   '))

def demo_status_codes():
    """Demonstrate HTTP status codes"""
    print("\n🔢 HTTP Status Codes Demo") 
    print("=" * 40)

    status_codes = {
        200: {
            "name": "OK",
            "usage": "Successful GET, PUT requests",
            "example": "GET /users/1 returns user data"
        },
        201: {
            "name": "Created", 
            "usage": "Successful POST requests",
            "example": "POST /users creates new user"
        },
        400: {
            "name": "Bad Request",
            "usage": "Invalid data, validation errors",
            "example": "POST /users with missing required fields"
        },
        404: {
            "name": "Not Found",
            "usage": "Resource doesn't exist",
            "example": "GET /users/999 when user 999 doesn't exist"
        },
        405: {
            "name": "Method Not Allowed",
            "usage": "Invalid HTTP method for endpoint",
            "example": "PATCH /users when only PUT is supported"
        },
        500: {
            "name": "Internal Server Error",
            "usage": "Server-side errors",
            "example": "Database connection failure"
        }
    }

    print("📊 Status Codes Used in API:")
    for code, details in status_codes.items():
        print(f"\n   {code} {details['name']}:")
        print(f"     Usage: {details['usage']}")
        print(f"     Example: {details['example']}")

def demo_data_validation():
    """Demonstrate data validation concepts"""
    print("\n✅ Data Validation Demo")
    print("=" * 40)

    validation_rules = [
        {
            "field": "name",
            "rules": ["Required", "Non-empty string"],
            "valid": "John Doe",
            "invalid": ["", None, 123]
        },
        {
            "field": "email", 
            "rules": ["Required", "Valid email format", "Unique"],
            "valid": "user@example.com",
            "invalid": ["invalid-email", "", "existing@example.com"]
        },
        {
            "field": "age",
            "rules": ["Required for creation", "Positive integer"],
            "valid": 25,
            "invalid": [-5, "twenty", None]
        },
        {
            "field": "department",
            "rules": ["Optional", "String"],
            "valid": "Engineering",
            "invalid": [123, True]
        }
    ]

    print("🔍 Validation Rules:")
    for rule in validation_rules:
        print(f"\n   {rule['field'].upper()}:")
        print(f"     Rules: {', '.join(rule['rules'])}")
        print(f"     Valid: {rule['valid']}")
        print(f"     Invalid: {rule['invalid']}")

def demo_testing_methods():
    """Demonstrate API testing approaches"""
    print("\n🧪 API Testing Methods Demo")
    print("=" * 40)

    testing_tools = [
        {
            "tool": "curl",
            "description": "Command-line HTTP client",
            "example": 'curl -X GET http://localhost:5000/users'
        },
        {
            "tool": "Postman",
            "description": "GUI-based API testing tool",
            "example": "Import endpoints and test interactively"
        },
        {
            "tool": "Python requests",
            "description": "Programmatic API testing",
            "example": "import requests; requests.get('http://localhost:5000/users')"
        },
        {
            "tool": "Browser",
            "description": "For GET requests only",
            "example": "Navigate to http://localhost:5000/users"
        }
    ]

    print("🔧 Testing Tools:")
    for tool in testing_tools:
        print(f"\n   {tool['tool']}:")
        print(f"     Description: {tool['description']}")
        print(f"     Example: {tool['example']}")

    # Sample curl commands
    print("\n📝 Sample curl Commands:")
    curl_commands = [
        'curl -X GET "http://localhost:5000/users"',
        'curl -X POST "http://localhost:5000/users" -H "Content-Type: application/json" -d '{"name":"Test User","email":"test@example.com","age":25}'',
        'curl -X PUT "http://localhost:5000/users/1" -H "Content-Type: application/json" -d '{"name":"Updated Name"}'',
        'curl -X DELETE "http://localhost:5000/users/1"'
    ]

    for i, cmd in enumerate(curl_commands, 1):
        print(f"\n   {i}. {cmd}")

def run_complete_demo():
    """Run the complete Flask REST API demo"""
    demo_api_concepts()
    demo_flask_routes()
    demo_http_methods()
    demo_request_response_examples()
    demo_status_codes()
    demo_data_validation()
    demo_testing_methods()

    print("\n" + "=" * 60)
    print("🎯 Demo Summary:")
    print("  ✅ Flask routes and decorators explained")
    print("  ✅ HTTP methods (GET, POST, PUT, DELETE) covered")
    print("  ✅ Request/response JSON format demonstrated")
    print("  ✅ HTTP status codes and their usage shown")
    print("  ✅ Data validation rules explained")
    print("  ✅ API testing methods and tools covered")
    print("=" * 60)

    print("\n🏃‍♂️ To run the actual API:")
    print("   1. Install Flask: pip install Flask")
    print("   2. Start server: python app.py")
    print("   3. Access API: http://localhost:5000")
    print("   4. Test endpoints with curl or Postman")

if __name__ == "__main__":
    run_complete_demo()
