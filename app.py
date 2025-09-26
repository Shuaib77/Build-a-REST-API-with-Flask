#!/usr/bin/env python3
"""
User Management REST API with Flask
Elevate Labs Python Developer Internship - Task 4

A RESTful API that manages user data with full CRUD operations
(Create, Read, Update, Delete) using Flask framework.

Author: Python Developer Intern
Date: September 26, 2025
"""

from flask import Flask, request, jsonify
from datetime import datetime
import json
import os

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

    sample_users = [
        {
            "name": "John Doe",
            "email": "john.doe@example.com",
            "age": 28,
            "department": "Engineering"
        },
        {
            "name": "Jane Smith", 
            "email": "jane.smith@example.com",
            "age": 25,
            "department": "Marketing"
        },
        {
            "name": "Mike Johnson",
            "email": "mike.johnson@example.com", 
            "age": 32,
            "department": "Sales"
        }
    ]

    for user_data in sample_users:
        user_data.update({
            "id": user_counter,
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat()
        })
        users_db[user_counter] = user_data
        user_counter += 1

# Helper functions
def validate_user_data(data, is_update=False):
    """Validate user data for required fields"""
    required_fields = ['name', 'email']
    if not is_update:
        required_fields.extend(['age'])

    errors = []

    for field in required_fields:
        if field not in data or not data[field]:
            errors.append(f"'{field}' is required")

    # Email validation (basic)
    if 'email' in data and data['email']:
        if '@' not in data['email'] or '.' not in data['email']:
            errors.append("Invalid email format")

    # Age validation
    if 'age' in data and data['age'] is not None:
        if not isinstance(data['age'], int) or data['age'] < 0:
            errors.append("Age must be a positive integer")

    return errors

def get_user_by_id(user_id):
    """Get user by ID from the database"""
    return users_db.get(user_id)

def create_error_response(message, status_code):
    """Create standardized error response"""
    return jsonify({
        "error": True,
        "message": message,
        "timestamp": datetime.now().isoformat()
    }), status_code

def create_success_response(data, message=None, status_code=200):
    """Create standardized success response"""
    response = {
        "error": False,
        "data": data,
        "timestamp": datetime.now().isoformat()
    }
    if message:
        response["message"] = message
    return jsonify(response), status_code

# API Routes

@app.route('/', methods=['GET'])
def api_home():
    """API home endpoint with welcome message and available endpoints"""
    endpoints = {
        "welcome": "User Management REST API",
        "version": "1.0.0",
        "endpoints": {
            "GET /": "API information",
            "GET /users": "Get all users",
            "GET /users/<id>": "Get user by ID", 
            "POST /users": "Create new user",
            "PUT /users/<id>": "Update user by ID",
            "DELETE /users/<id>": "Delete user by ID",
            "GET /health": "API health check"
        },
        "sample_request": {
            "POST /users": {
                "name": "John Doe",
                "email": "john@example.com",
                "age": 30,
                "department": "Engineering"
            }
        },
        "total_users": len(users_db)
    }
    return create_success_response(endpoints)

@app.route('/health', methods=['GET'])
def health_check():
    """API health check endpoint"""
    health_data = {
        "status": "healthy",
        "api_version": "1.0.0",
        "total_users": len(users_db),
        "uptime": "running"
    }
    return create_success_response(health_data)

@app.route('/users', methods=['GET'])
def get_all_users():
    """GET endpoint to retrieve all users"""
    try:
        # Support for pagination (optional enhancement)
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)

        users_list = list(users_db.values())

        if not users_list:
            return create_success_response(
                {"users": [], "total": 0},
                "No users found"
            )

        # Simple pagination
        start_idx = (page - 1) * per_page
        end_idx = start_idx + per_page
        paginated_users = users_list[start_idx:end_idx]

        response_data = {
            "users": paginated_users,
            "total": len(users_list),
            "page": page,
            "per_page": per_page,
            "pages": (len(users_list) + per_page - 1) // per_page
        }

        return create_success_response(response_data)

    except Exception as e:
        return create_error_response(f"Internal server error: {str(e)}", 500)

@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """GET endpoint to retrieve a specific user by ID"""
    try:
        user = get_user_by_id(user_id)

        if not user:
            return create_error_response(f"User with ID {user_id} not found", 404)

        return create_success_response(user)

    except Exception as e:
        return create_error_response(f"Internal server error: {str(e)}", 500)

@app.route('/users', methods=['POST'])
def create_user():
    """POST endpoint to create a new user"""
    try:
        # Check if request contains JSON data
        if not request.is_json:
            return create_error_response("Request must contain JSON data", 400)

        data = request.get_json()

        if not data:
            return create_error_response("Request body is empty", 400)

        # Validate user data
        validation_errors = validate_user_data(data)
        if validation_errors:
            return create_error_response(f"Validation errors: {'; '.join(validation_errors)}", 400)

        # Check if email already exists
        for existing_user in users_db.values():
            if existing_user['email'] == data['email']:
                return create_error_response("User with this email already exists", 400)

        # Create new user
        global user_counter
        new_user = {
            "id": user_counter,
            "name": data['name'],
            "email": data['email'],
            "age": data['age'],
            "department": data.get('department', ''),
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat()
        }

        users_db[user_counter] = new_user
        user_counter += 1

        return create_success_response(
            new_user, 
            f"User created successfully with ID {new_user['id']}", 
            201
        )

    except Exception as e:
        return create_error_response(f"Internal server error: {str(e)}", 500)

@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    """PUT endpoint to update an existing user"""
    try:
        # Check if user exists
        user = get_user_by_id(user_id)
        if not user:
            return create_error_response(f"User with ID {user_id} not found", 404)

        # Check if request contains JSON data
        if not request.is_json:
            return create_error_response("Request must contain JSON data", 400)

        data = request.get_json()

        if not data:
            return create_error_response("Request body is empty", 400)

        # Validate user data (for updates, fields are optional)
        validation_errors = validate_user_data(data, is_update=True)
        if validation_errors:
            return create_error_response(f"Validation errors: {'; '.join(validation_errors)}", 400)

        # Check if email already exists (if email is being updated)
        if 'email' in data and data['email'] != user['email']:
            for existing_user in users_db.values():
                if existing_user['email'] == data['email']:
                    return create_error_response("User with this email already exists", 400)

        # Update user fields
        updatable_fields = ['name', 'email', 'age', 'department']
        for field in updatable_fields:
            if field in data:
                user[field] = data[field]

        user['updated_at'] = datetime.now().isoformat()

        return create_success_response(
            user,
            f"User with ID {user_id} updated successfully"
        )

    except Exception as e:
        return create_error_response(f"Internal server error: {str(e)}", 500)

@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    """DELETE endpoint to remove a user"""
    try:
        # Check if user exists
        user = get_user_by_id(user_id)
        if not user:
            return create_error_response(f"User with ID {user_id} not found", 404)

        # Delete user
        deleted_user = users_db.pop(user_id)

        return create_success_response(
            {"deleted_user": deleted_user},
            f"User with ID {user_id} deleted successfully"
        )

    except Exception as e:
        return create_error_response(f"Internal server error: {str(e)}", 500)

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
def reset_data():
    """Reset all data to initial state (development only)"""
    global users_db, user_counter
    users_db = {}
    user_counter = 1
    initialize_sample_data()

    return create_success_response(
        {"total_users": len(users_db)},
        "Database reset successfully"
    )

if __name__ == '__main__':
    # Initialize sample data
    initialize_sample_data()

    print("🚀 Starting User Management REST API...")
    print("📋 Sample users loaded for testing")
    print("🌐 API will be available at: http://localhost:5000")
    print("📖 API documentation at: http://localhost:5000/")
    print("\n🔧 Available endpoints:")
    print("   GET    /users        - Get all users")
    print("   GET    /users/<id>   - Get user by ID") 
    print("   POST   /users        - Create new user")
    print("   PUT    /users/<id>   - Update user")
    print("   DELETE /users/<id>   - Delete user")
    print("\n⏹️  Press Ctrl+C to stop the server")

    # Run the Flask application
    app.run(debug=True, host='0.0.0.0', port=5000)
