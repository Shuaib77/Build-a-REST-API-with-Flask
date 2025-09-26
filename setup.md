# Setup Instructions for User Management REST API

## Quick Start Guide

### Prerequisites
- Python 3.6 or higher installed on your system
- Command line/terminal access
- Text editor (VS Code recommended)
- Postman or curl for API testing (optional)

### Installation Steps

1. **Check Python Installation**
   ```bash
   python --version
   # or
   python3 --version
   ```

2. **Download/Clone the Project**
   ```bash
   # If using git
   git clone <your-repo-url>
   cd flask-rest-api

   # Or download files manually and place them in a folder
   ```

3. **Install Flask**
   ```bash
   # Install Flask (only dependency needed)
   pip install Flask

   # Or install from requirements file
   pip install -r requirements.txt
   ```

4. **Project Files Structure**
   ```
   flask-rest-api/
   ├── app.py              # Main Flask application
   ├── requirements.txt    # Python dependencies
   ├── demo.py            # Demo script
   ├── test_api.py        # Test cases
   ├── README.md          # Documentation
   ├── setup.md           # This file
   └── postman_requests.py # API testing examples
   ```

### Running the Application

#### Method 1: Start the Flask Server
```bash
python app.py
```

Expected output:
```
🚀 Starting User Management REST API...
📋 Sample users loaded for testing
🌐 API will be available at: http://localhost:5000
📖 API documentation at: http://localhost:5000/
...
 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:5000
 * Running on http://[::1]:5000
```

#### Method 2: Run Demo (Offline)
```bash
python demo.py
```

#### Method 3: Run Tests
```bash
python test_api.py
```

### Testing the API

Once the server is running, you can test it using various methods:

#### Using curl (Command Line)
```bash
# Get all users
curl -X GET http://localhost:5000/users

# Get specific user
curl -X GET http://localhost:5000/users/1

# Create new user
curl -X POST http://localhost:5000/users \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test User",
    "email": "test@example.com", 
    "age": 25,
    "department": "Testing"
  }'

# Update user
curl -X PUT http://localhost:5000/users/1 \
  -H "Content-Type: application/json" \
  -d '{"name": "Updated Name"}'

# Delete user
curl -X DELETE http://localhost:5000/users/1
```

#### Using Web Browser (GET requests only)
- Navigate to `http://localhost:5000/` for API documentation
- Navigate to `http://localhost:5000/users` to see all users
- Navigate to `http://localhost:5000/users/1` to see user with ID 1

#### Using Postman
1. **Download and install Postman** from https://www.postman.com/downloads/
2. **Create a new collection** called "User Management API"
3. **Add requests** for each endpoint:

   **GET All Users:**
   - Method: GET
   - URL: http://localhost:5000/users

   **CREATE User:**
   - Method: POST  
   - URL: http://localhost:5000/users
   - Headers: Content-Type: application/json
   - Body (raw JSON):
     ```json
     {
       "name": "Jane Doe",
       "email": "jane@example.com",
       "age": 27,
       "department": "Marketing"
     }
     ```

   **UPDATE User:**
   - Method: PUT
   - URL: http://localhost:5000/users/1
   - Headers: Content-Type: application/json
   - Body (raw JSON):
     ```json
     {
       "name": "Updated Name",
       "department": "New Department"
     }
     ```

### API Endpoints Reference

| Method | Endpoint | Description | Request Body |
|--------|----------|-------------|--------------|
| GET | `/` | API documentation | None |
| GET | `/health` | Health check | None |
| GET | `/users` | Get all users | None |
| GET | `/users/<id>` | Get user by ID | None |
| POST | `/users` | Create new user | JSON with name, email, age |
| PUT | `/users/<id>` | Update user | JSON with fields to update |
| DELETE | `/users/<id>` | Delete user | None |
| POST | `/reset` | Reset to sample data | None |

### Expected Response Format

**Success Response:**
```json
{
  "error": false,
  "data": { /* response data */ },
  "message": "Optional success message",
  "timestamp": "2025-09-26T19:00:00"
}
```

**Error Response:**
```json
{
  "error": true,
  "message": "Error description",
  "timestamp": "2025-09-26T19:00:00"
}
```

### Troubleshooting

#### Common Issues and Solutions

**Problem**: "Address already in use" error
```bash
# Solution: Kill existing Flask processes
# On Windows:
netstat -ano | findstr :5000
taskkill /PID <process_id> /F

# On Mac/Linux:
lsof -ti:5000 | xargs kill -9
```

**Problem**: "Module 'flask' not found"
```bash
# Solution: Install Flask
pip install Flask

# Check installation
python -c "import flask; print(flask.__version__)"
```

**Problem**: Cannot access API from other devices
```bash
# Solution: API runs on 0.0.0.0, check firewall
# Make sure port 5000 is not blocked
```

**Problem**: JSON data not being accepted
```bash
# Solution: Make sure Content-Type header is set
curl -H "Content-Type: application/json" -X POST ...
```

**Problem**: 405 Method Not Allowed
```bash
# Solution: Check HTTP method matches endpoint
# GET /users ✅, POST /users ✅, PATCH /users ❌
```

### Development Tips

#### Debugging
- Set `debug=True` in app.run() for detailed error messages
- Use print statements to debug request data
- Check Flask console output for errors

#### Testing Best Practices
1. Start with GET requests to verify server is running
2. Test POST to create users before testing other operations
3. Use different user IDs to avoid conflicts
4. Check HTTP status codes in responses

#### Sample Test Workflow
```bash
# 1. Start server
python app.py

# 2. Test health check
curl http://localhost:5000/health

# 3. Get initial users
curl http://localhost:5000/users

# 4. Create new user
curl -X POST http://localhost:5000/users -H "Content-Type: application/json" -d '{"name":"Test","email":"test@example.com","age":25}'

# 5. Verify creation
curl http://localhost:5000/users
```

### Performance Considerations

#### Memory Usage
- All data stored in memory (dictionary)
- Data is lost when server restarts
- Suitable for development and small datasets
- For production, consider database integration

#### Concurrent Requests
- Flask development server handles one request at a time
- For production, use WSGI server like Gunicorn
- Current implementation is thread-safe for read operations

### Security Notes

#### Development vs Production
- Current setup is for development only
- No authentication implemented
- CORS not configured
- Debug mode enabled

#### Data Validation
- Basic email format validation
- Required field validation
- Age must be positive integer
- No SQL injection risk (no database used)

### Next Steps

After successful setup:
1. Test all endpoints with curl or Postman
2. Verify error handling by sending invalid data
3. Check response format consistency
4. Customize user fields as needed
5. Submit GitHub repository as required

### Flask Configuration Options

You can modify these settings in app.py:
```python
# Change port
app.run(port=8000)

# Disable debug mode
app.run(debug=False)

# Restrict to localhost only
app.run(host='127.0.0.1')
```
