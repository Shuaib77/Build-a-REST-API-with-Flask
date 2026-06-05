#!/usr/bin/env python3
"""
User Management REST API with Flask
Elevate Labs Python Developer Internship - Task 4

A RESTful API that manages user data with full CRUD operations
(Create, Read, Update, Delete) using Flask framework.

Author: Python Developer Intern
Date: September 26, 2025
"""

from flask import Flask, request

from constants import (
    API_VERSION,
    DEFAULT_PER_PAGE,
    SAMPLE_USERS,
    UPDATABLE_FIELDS,
)
from utils import (
    check_email_unique,
    create_error_response,
    create_success_response,
    get_timestamp,
    handle_errors,
    parse_json_request,
    validate_user_data,
)

# Initialize Flask application
app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

# In-memory storage for users (as specified in requirements)
users_db = {}
user_counter = 1


# Sample data for demonstration
def initialize_sample_data():
    """Initialize some sample users for testing"""
    global user_counter, users_db

    for user_data in SAMPLE_USERS:
        timestamp = get_timestamp()
        user_record = {
            **user_data,
            "id": user_counter,
            "created_at": timestamp,
            "updated_at": timestamp,
        }
        users_db[user_counter] = user_record
        user_counter += 1


# Helper function
def get_user_by_id(user_id):
    """Get user by ID from the database"""
    return users_db.get(user_id)


def find_user_or_404(user_id):
    """Look up a user and return ``(user, None)`` or ``(None, 404_response)``."""
    user = get_user_by_id(user_id)
    if not user:
        return None, create_error_response(f"User with ID {user_id} not found", 404)
    return user, None


# API Routes

@app.route('/', methods=['GET'])
@handle_errors
def api_home():
    """API home endpoint with welcome message and available endpoints"""
    endpoints = {
        "welcome": "User Management REST API",
        "version": API_VERSION,
        "endpoints": {
            "GET /": "API information",
            "GET /users": "Get all users",
            "GET /users/<id>": "Get user by ID",
            "POST /users": "Create new user",
            "PUT /users/<id>": "Update user by ID",
            "DELETE /users/<id>": "Delete user by ID",
            "GET /health": "API health check",
        },
        "sample_request": {
            "POST /users": {
                "name": "John Doe",
                "email": "john@example.com",
                "age": 30,
                "department": "Engineering",
            }
        },
        "total_users": len(users_db),
    }
    return create_success_response(endpoints)


@app.route('/health', methods=['GET'])
@handle_errors
def health_check():
    """API health check endpoint"""
    health_data = {
        "status": "healthy",
        "api_version": API_VERSION,
        "total_users": len(users_db),
        "uptime": "running",
    }
    return create_success_response(health_data)


@app.route('/users', methods=['GET'])
@handle_errors
def get_all_users():
    """GET endpoint to retrieve all users"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', DEFAULT_PER_PAGE, type=int)

    users_list = list(users_db.values())

    if not users_list:
        return create_success_response(
            {"users": [], "total": 0},
            "No users found",
        )

    start_idx = (page - 1) * per_page
    end_idx = start_idx + per_page
    paginated_users = users_list[start_idx:end_idx]

    response_data = {
        "users": paginated_users,
        "total": len(users_list),
        "page": page,
        "per_page": per_page,
        "pages": (len(users_list) + per_page - 1) // per_page,
    }

    return create_success_response(response_data)


@app.route('/users/<int:user_id>', methods=['GET'])
@handle_errors
def get_user(user_id):
    """GET endpoint to retrieve a specific user by ID"""
    user, err = find_user_or_404(user_id)
    if err:
        return err

    return create_success_response(user)


@app.route('/users', methods=['POST'])
@handle_errors
def create_user():
    """POST endpoint to create a new user"""
    data, err = parse_json_request()
    if err:
        return err

    validation_errors = validate_user_data(data)
    if validation_errors:
        return create_error_response(
            f"Validation errors: {'; '.join(validation_errors)}", 400
        )

    email_err = check_email_unique(users_db, data['email'])
    if email_err:
        return email_err

    global user_counter
    timestamp = get_timestamp()
    new_user = {
        "id": user_counter,
        "name": data['name'],
        "email": data['email'],
        "age": data['age'],
        "department": data.get('department', ''),
        "created_at": timestamp,
        "updated_at": timestamp,
    }

    users_db[user_counter] = new_user
    user_counter += 1

    return create_success_response(
        new_user,
        f"User created successfully with ID {new_user['id']}",
        201,
    )


@app.route('/users/<int:user_id>', methods=['PUT'])
@handle_errors
def update_user(user_id):
    """PUT endpoint to update an existing user"""
    user, err = find_user_or_404(user_id)
    if err:
        return err

    data, err = parse_json_request()
    if err:
        return err

    validation_errors = validate_user_data(data, is_update=True)
    if validation_errors:
        return create_error_response(
            f"Validation errors: {'; '.join(validation_errors)}", 400
        )

    if 'email' in data and data['email'] != user['email']:
        email_err = check_email_unique(users_db, data['email'], exclude_user_id=user_id)
        if email_err:
            return email_err

    for field in UPDATABLE_FIELDS:
        if field in data:
            user[field] = data[field]

    user['updated_at'] = get_timestamp()

    return create_success_response(
        user,
        f"User with ID {user_id} updated successfully",
    )


@app.route('/users/<int:user_id>', methods=['DELETE'])
@handle_errors
def delete_user(user_id):
    """DELETE endpoint to remove a user"""
    _, err = find_user_or_404(user_id)
    if err:
        return err

    deleted_user = users_db.pop(user_id)

    return create_success_response(
        {"deleted_user": deleted_user},
        f"User with ID {user_id} deleted successfully",
    )


# Error handlers
@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return create_error_response("Endpoint not found", 404)


@app.errorhandler(405)
def method_not_allowed(error):
    """Handle 405 errors"""
    return create_error_response("Method not allowed for this endpoint", 405)


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return create_error_response("Internal server error", 500)


# Development utilities
@app.route('/reset', methods=['POST'])
@handle_errors
def reset_data():
    """Reset all data to initial state (development only)"""
    global users_db, user_counter
    users_db = {}
    user_counter = 1
    initialize_sample_data()

    return create_success_response(
        {"total_users": len(users_db)},
        "Database reset successfully",
    )


if __name__ == '__main__':
    initialize_sample_data()

    print("Starting User Management REST API...")
    print("Sample users loaded for testing")
    print(f"API will be available at: http://localhost:5000")
    print(f"API documentation at: http://localhost:5000/")
    print("\nAvailable endpoints:")
    print("   GET    /users        - Get all users")
    print("   GET    /users/<id>   - Get user by ID")
    print("   POST   /users        - Create new user")
    print("   PUT    /users/<id>   - Update user")
    print("   DELETE /users/<id>   - Delete user")
    print("\nPress Ctrl+C to stop the server")

    app.run(debug=True, host='0.0.0.0', port=5000)
