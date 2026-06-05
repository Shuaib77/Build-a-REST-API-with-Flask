"""
Shared utilities for the User Management REST API.

Provides reusable helpers for response building, validation,
request parsing, and error handling used across the application.
"""

from datetime import datetime
from functools import wraps

from flask import jsonify, request

from constants import REQUIRED_FIELDS_CREATE, REQUIRED_FIELDS_UPDATE


# --- Timestamp helper ---

def get_timestamp():
    """Return the current UTC time as an ISO-8601 string."""
    return datetime.now().isoformat()


# --- Response builders ---

def create_error_response(message, status_code):
    """Create a standardized JSON error response."""
    return jsonify({
        "error": True,
        "message": message,
        "timestamp": get_timestamp(),
    }), status_code


def create_success_response(data, message=None, status_code=200):
    """Create a standardized JSON success response."""
    response = {
        "error": False,
        "data": data,
        "timestamp": get_timestamp(),
    }
    if message:
        response["message"] = message
    return jsonify(response), status_code


# --- Validation ---

def validate_user_data(data, is_update=False):
    """Validate user data and return a list of error strings (empty if valid)."""
    required_fields = REQUIRED_FIELDS_UPDATE if is_update else REQUIRED_FIELDS_CREATE
    errors = []

    for field in required_fields:
        if field not in data or not data[field]:
            errors.append(f"'{field}' is required")

    if "email" in data and data["email"]:
        if "@" not in data["email"] or "." not in data["email"]:
            errors.append("Invalid email format")

    if "age" in data and data["age"] is not None:
        if not isinstance(data["age"], int) or data["age"] < 0:
            errors.append("Age must be a positive integer")

    return errors


# --- Request parsing ---

def parse_json_request():
    """Parse and validate an incoming JSON request body.

    Returns:
        tuple: ``(data, None)`` on success, or ``(None, error_response)`` on
        failure where *error_response* is a Flask response tuple ready to be
        returned from a view.
    """
    if not request.is_json:
        return None, create_error_response("Request must contain JSON data", 400)

    data = request.get_json()
    if not data:
        return None, create_error_response("Request body is empty", 400)

    return data, None


# --- Email uniqueness ---

def check_email_unique(users_db, email, exclude_user_id=None):
    """Return an error response if *email* is already taken, else ``None``.

    Args:
        users_db: The in-memory user dict.
        email: Email address to check.
        exclude_user_id: User ID to skip (used when updating a user's own record).
    """
    for uid, user in users_db.items():
        if user["email"] == email and uid != exclude_user_id:
            return create_error_response("User with this email already exists", 400)
    return None


# --- Error-handling decorator ---

def handle_errors(func):
    """Decorator that wraps a view in a ``try / except`` returning a 500."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            return create_error_response(
                f"Internal server error: {str(e)}", 500
            )
    return wrapper
