"""
Shared constants for the User Management REST API.

Centralizes configuration values, sample data, and field definitions
used across app.py, demo.py, and test_api.py.
"""

API_VERSION = "1.0.0"

DEFAULT_PER_PAGE = 10

UPDATABLE_FIELDS = ["name", "email", "age", "department"]

REQUIRED_FIELDS_CREATE = ["name", "email", "age"]

REQUIRED_FIELDS_UPDATE = ["name", "email"]

SAMPLE_USERS = [
    {
        "name": "John Doe",
        "email": "john.doe@example.com",
        "age": 28,
        "department": "Engineering",
    },
    {
        "name": "Jane Smith",
        "email": "jane.smith@example.com",
        "age": 25,
        "department": "Marketing",
    },
    {
        "name": "Mike Johnson",
        "email": "mike.johnson@example.com",
        "age": 32,
        "department": "Sales",
    },
]
