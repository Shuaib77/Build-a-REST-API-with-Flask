{
  "info": {
    "name": "User Management REST API",
    "description": "Complete API testing collection for Flask user management system",
    "version": "1.0.0"
  },
  "item": [
    {
      "name": "Get API Info",
      "request": {
        "method": "GET",
        "url": "http://localhost:5000/",
        "description": "Get API documentation and available endpoints"
      }
    },
    {
      "name": "Health Check",
      "request": {
        "method": "GET",
        "url": "http://localhost:5000/health",
        "description": "Check if API is running properly"
      }
    },
    {
      "name": "Get All Users",
      "request": {
        "method": "GET",
        "url": "http://localhost:5000/users",
        "description": "Retrieve all users with pagination"
      }
    },
    {
      "name": "Get User by ID",
      "request": {
        "method": "GET",
        "url": "http://localhost:5000/users/1",
        "description": "Get specific user by ID"
      }
    },
    {
      "name": "Create New User",
      "request": {
        "method": "POST",
        "url": "http://localhost:5000/users",
        "header": [
          {
            "key": "Content-Type",
            "value": "application/json"
          }
        ],
        "body": {
          "mode": "raw",
          "raw": "{\n  \"name\": \"Alice Johnson\",\n  \"email\": \"alice@example.com\",\n  \"age\": 28,\n  \"department\": \"Product Management\"\n}"
        },
        "description": "Create a new user with required fields"
      }
    },
    {
      "name": "Update User",
      "request": {
        "method": "PUT",
        "url": "http://localhost:5000/users/1",
        "header": [
          {
            "key": "Content-Type",
            "value": "application/json"
          }
        ],
        "body": {
          "mode": "raw",
          "raw": "{\n  \"name\": \"Alice Smith\",\n  \"department\": \"Engineering\"\n}"
        },
        "description": "Update existing user fields"
      }
    },
    {
      "name": "Delete User",
      "request": {
        "method": "DELETE",
        "url": "http://localhost:5000/users/1",
        "description": "Delete user by ID"
      }
    },
    {
      "name": "Reset Sample Data",
      "request": {
        "method": "POST",
        "url": "http://localhost:5000/reset",
        "description": "Reset database to initial sample users"
      }
    }
  ]
}
