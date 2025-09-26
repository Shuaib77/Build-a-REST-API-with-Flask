# Build-a-REST-API-with-Flask
Create a REST API that manages user data with full CRUD operations
# User Management REST API

**Python Developer Internship - Task 4**  
**Company**: Elevate Labs  
**Objective**: Create a REST API that manages user data with Flask.

## 📝 Project Description

This is a RESTful API built with Flask that provides complete user data management functionality. The API supports all CRUD operations (Create, Read, Update, Delete) and stores user data in memory using Python dictionaries. It includes comprehensive error handling, data validation, and follows REST API best practices.

## ✨ Features

### Core REST Operations
- **GET /users** - Retrieve all users with pagination
- **GET /users/<id>** - Get specific user by ID
- **POST /users** - Create new user
- **PUT /users/<id>** - Update existing user
- **DELETE /users/<id>** - Delete user by ID

### Advanced Features
- **Data Validation**: Email format, required fields, data types
- **Error Handling**: Comprehensive HTTP status codes and error messages
- **Pagination**: Support for page and per_page parameters
- **Duplicate Prevention**: Email uniqueness validation
- **Timestamps**: Automatic created_at and updated_at tracking
- **Health Check**: /health endpoint for API monitoring
- **API Documentation**: Self-documenting root endpoint

## 🛠 Technologies Used

- **Framework**: Flask 2.3+
- **Language**: Python 3.6+
- **Storage**: In-memory dictionary (as specified)
- **Data Format**: JSON for requests and responses
- **Testing**: Postman/curl compatible

## 📦 Installation

### Prerequisites
```bash
# Ensure you have Python 3.6+ installed
python --version
```

### Install Dependencies
```bash
# Install Flask
pip install Flask

# Or install from requirements file
pip install -r requirements.txt
```

## 🚀 How to Run

1. **Start the API server**:
   ```bash
   python app.py
   ```

2. **Access the API**:
   - Base URL: `http://localhost:5000`
   - API Documentation: `http://localhost:5000/`
   - Health Check: `http://localhost:5000/health`

3. **Stop the server**: Press `Ctrl+C`

## 📋 API Endpoints

### 1. Get All Users
```http
GET /users
```

**Response:**
```json
{
  "error": false,
  "data": {
    "users": [
      {
        "id": 1,
        "name": "John Doe",
        "email": "john.doe@example.com",
        "age": 28,
        "department": "Engineering",
        "created_at": "2025-09-26T19:00:00",
        "updated_at": "2025-09-26T19:00:00"
      }
    ],
    "total": 1,
    "page": 1,
    "per_page": 10
  },
  "timestamp": "2025-09-26T19:00:00"
}
```

### 2. Get User by ID
```http
GET /users/1
```

**Response:**
```json
{
  "error": false,
  "data": {
    "id": 1,
    "name": "John Doe",
    "email": "john.doe@example.com",
    "age": 28,
    "department": "Engineering",
    "created_at": "2025-09-26T19:00:00",
    "updated_at": "2025-09-26T19:00:00"
  },
  "timestamp": "2025-09-26T19:00:00"
}
```

### 3. Create New User
```http
POST /users
Content-Type: application/json

{
  "name": "Alice Wilson",
  "email": "alice@example.com",
  "age": 26,
  "department": "Design"
}
```

**Response:**
```json
{
  "error": false,
  "data": {
    "id": 4,
    "name": "Alice Wilson",
    "email": "alice@example.com",
    "age": 26,
    "department": "Design",
    "created_at": "2025-09-26T19:05:00",
    "updated_at": "2025-09-26T19:05:00"
  },
  "message": "User created successfully with ID 4",
  "timestamp": "2025-09-26T19:05:00"
}
```

### 4. Update User
```http
PUT /users/1
Content-Type: application/json

{
  "name": "John Smith",
  "age": 29
}
```

### 5. Delete User
```http
DELETE /users/1
```

## 🧪 Testing with curl

### Get all users
```bash
curl -X GET http://localhost:5000/users
```

### Create a user
```bash
curl -X POST http://localhost:5000/users \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test User",
    "email": "test@example.com",
    "age": 25,
    "department": "Testing"
  }'
```

### Update a user
```bash
curl -X PUT http://localhost:5000/users/1 \
  -H "Content-Type: application/json" \
  -d '{"name": "Updated Name"}'
```

### Delete a user
```bash
curl -X DELETE http://localhost:5000/users/1
```

## 🧪 Testing with Postman

1. **Import the API endpoints into Postman**
2. **Set base URL**: `http://localhost:5000`
3. **Test each endpoint**:
   - GET requests: Just send the request
   - POST/PUT requests: Set `Content-Type: application/json` and add body data
   - Check response status codes and JSON format

## 🔧 Implementation Details

### Data Structure
Users are stored in memory using this structure:
```python
users_db = {
    1: {
        "id": 1,
        "name": "John Doe",
        "email": "john.doe@example.com", 
        "age": 28,
        "department": "Engineering",
        "created_at": "2025-09-26T19:00:00",
        "updated_at": "2025-09-26T19:00:00"
    }
}
```

### HTTP Status Codes
- **200 OK**: Successful GET, PUT operations
- **201 Created**: Successful POST operations
- **400 Bad Request**: Validation errors, invalid data
- **404 Not Found**: User or endpoint not found
- **405 Method Not Allowed**: Invalid HTTP method
- **500 Internal Server Error**: Server errors

### Error Response Format
```json
{
  "error": true,
  "message": "Error description",
  "timestamp": "2025-09-26T19:00:00"
}
```

### Success Response Format
```json
{
  "error": false,
  "data": { /* response data */ },
  "message": "Optional success message",
  "timestamp": "2025-09-26T19:00:00"
}
```

## 🎯 Learning Outcomes

This project demonstrates mastery of:

### Flask Framework
- **Route Definition**: @app.route() decorators
- **HTTP Methods**: GET, POST, PUT, DELETE handling
- **Request Handling**: request.get_json(), request.args
- **Response Generation**: jsonify() for JSON responses
- **Error Handling**: Custom error handlers

### REST API Principles
- **Resource-based URLs**: /users, /users/<id>
- **HTTP Methods**: Proper use of GET, POST, PUT, DELETE
- **Status Codes**: Appropriate HTTP response codes
- **JSON Format**: Consistent request/response structure
- **Stateless**: Each request contains all needed information

### Data Management
- **CRUD Operations**: Create, Read, Update, Delete
- **Data Validation**: Input validation and sanitization
- **Error Handling**: Comprehensive error management
- **Data Persistence**: In-memory storage simulation

## 🔍 Interview Questions Preparation

### Flask Basics
- **What is Flask?** - Lightweight Python web framework for building web applications and APIs
- **Flask Route?** - Decorator that binds URL endpoints to Python functions
- **Run Flask App?** - `flask run` or `python app.py` with `app.run()`

### REST & HTTP
- **What is REST?** - Representational State Transfer, architectural style for web services
- **GET vs POST?** - GET retrieves data, POST creates/submits data
- **Status Codes?** - 200 (OK), 201 (Created), 404 (Not Found), 400 (Bad Request), 500 (Server Error)

### Technical Details
- **request.json?** - Flask property to access JSON data from request body
- **What is JSON?** - JavaScript Object Notation, lightweight data interchange format
- **Test API?** - Use Postman, curl, or automated testing frameworks
- **Database vs Memory?** - Yes, can use SQLite, PostgreSQL, MongoDB instead of in-memory storage

## 📁 Project Structure

```
flask-rest-api/
├── app.py              # Main Flask application
├── requirements.txt    # Dependencies
├── README.md          # Project documentation
├── test_api.py        # API tests
├── postman_collection.json  # Postman collection
└── demo_requests.py   # Demo script
```

## 🤝 Contributing

This project is part of the Elevate Labs internship program. Suggestions for improvements welcome!

## 📄 License

Educational project created for learning purposes.

---

**Author**: [Your Name]  
**Date**: September 26, 2025  
**Task**: Python Developer Internship - Task 4  
**Company**: Elevate Labs  
**Submission Deadline**: 10:00 PM IST
