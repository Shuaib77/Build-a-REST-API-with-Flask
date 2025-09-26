# Git Workflow for User Management REST API

## Step-by-Step GitHub Repository Setup

### 1. Create GitHub Repository
1. Go to https://github.com
2. Click "New repository" (+ icon)
3. Repository name: `flask-user-management-api`
4. Description: "User Management REST API with Flask - Elevate Labs Task 4"
5. Make it **Public**
6. ✅ Add README file (we'll replace it)
7. Add .gitignore: Python
8. Click "Create repository"

### 2. Clone Repository Locally
```bash
git clone https://github.com/YOUR_USERNAME/flask-user-management-api.git
cd flask-user-management-api
```

### 3. Add Project Files
Copy these files to your repository folder:
- app.py (main Flask application)
- requirements.txt (dependencies)
- README.md (comprehensive documentation)
- demo.py (demo script)
- test_api.py (test cases)
- setup.md (setup instructions)
- postman_requests.py (API testing examples)
- postman_collection.json (Postman collection)

### 4. Update .gitignore
```bash
# Add Flask-specific exclusions to .gitignore
echo "# Flask specific" >> .gitignore
echo "instance/" >> .gitignore  
echo "*.pyc" >> .gitignore
echo "__pycache__/" >> .gitignore
echo ".env" >> .gitignore
echo "venv/" >> .gitignore
echo ".venv/" >> .gitignore
echo "" >> .gitignore
echo "# IDE files" >> .gitignore
echo ".vscode/" >> .gitignore
echo ".idea/" >> .gitignore
echo "*.swp" >> .gitignore
echo "*.swo" >> .gitignore
```

### 5. Git Commands
```bash
# Check status
git status

# Add all project files
git add .

# Commit with comprehensive message
git commit -m "feat: Complete User Management REST API with Flask

Core Features:
- Full CRUD operations (GET, POST, PUT, DELETE)
- User data management with in-memory storage
- Comprehensive input validation and error handling
- RESTful API design following best practices
- JSON request/response format throughout

Technical Implementation:
- Flask framework with route decorators
- HTTP status codes (200, 201, 400, 404, 405, 500)
- Request handling with request.get_json()
- JSON responses using jsonify()
- Custom error handlers for all scenarios
- Data persistence using Python dictionaries
- Automatic timestamp tracking (created_at, updated_at)

API Endpoints:
- GET /users - Retrieve all users with pagination
- GET /users/<id> - Get specific user by ID
- POST /users - Create new user with validation
- PUT /users/<id> - Update existing user fields  
- DELETE /users/<id> - Remove user by ID
- GET /health - API health check endpoint
- POST /reset - Reset to sample data (development)

Data Features:
- User fields: id, name, email, age, department
- Email uniqueness validation
- Required field validation (name, email, age)
- Age must be positive integer
- Email format validation

Testing & Documentation:
- Complete test suite covering all functionality
- Demo script for offline concept demonstration
- Postman collection for interactive API testing
- Comprehensive setup instructions
- curl command examples for all endpoints

Development Tools:
- Flask development server with auto-reload
- Debug mode for detailed error messages
- Sample data initialization
- Request/response logging"

# Push to GitHub
git push origin main
```

### 6. Verify Repository
Check your GitHub repository has:
- ✅ app.py (main Flask application)
- ✅ requirements.txt (Flask dependency)
- ✅ README.md with comprehensive API documentation
- ✅ All testing and demo files
- ✅ Postman collection for API testing
- ✅ Clean commit history with detailed message
- ✅ .gitignore excludes Python cache files

### 7. Test Repository Completeness
```bash
# Clone to test directory
git clone https://github.com/YOUR_USERNAME/flask-user-management-api.git test-api
cd test-api

# Install dependencies
pip install -r requirements.txt

# Test demo (offline)
python demo.py

# Test the API
python app.py
# (In another terminal)
curl http://localhost:5000/users
```

### 8. Submit to Elevate Labs
Copy your repository URL and submit:
`https://github.com/YOUR_USERNAME/flask-user-management-api`

## Flask Project File Management

### Files TO Commit
- ✅ app.py (main Flask application)
- ✅ requirements.txt (dependencies)
- ✅ README.md (documentation)
- ✅ demo.py, test_api.py (testing files)
- ✅ setup.md (setup instructions)
- ✅ postman_collection.json (API testing)
- ✅ .gitignore (exclusion rules)

### Files NOT TO Commit
- ❌ __pycache__/ (Python cache)
- ❌ *.pyc (compiled Python files)
- ❌ .env (environment variables)
- ❌ venv/ or .venv/ (virtual environments)
- ❌ instance/ (Flask instance folder)
- ❌ .vscode/, .idea/ (IDE settings)

### Flask-Specific Considerations
- Flask runs on port 5000 by default
- No database files to exclude (using in-memory storage)
- Debug mode creates additional cache files
- Virtual environments should not be committed

## Advanced Git Operations

### Professional Commit Messages for Flask
```bash
# Feature additions
git commit -m "feat: Add user validation for email uniqueness"
git commit -m "feat: Implement pagination for GET /users endpoint"

# Bug fixes
git commit -m "fix: Handle missing Content-Type header in POST requests"
git commit -m "fix: Return 404 for non-existent user updates"

# API improvements
git commit -m "api: Add timestamp fields to user records"
git commit -m "api: Implement consistent error response format"

# Documentation
git commit -m "docs: Add Postman collection for API testing"
git commit -m "docs: Update README with curl examples"

# Testing
git commit -m "test: Add comprehensive test suite for all endpoints"
git commit -m "test: Add input validation test cases"
```

### Branch Strategy (Optional)
```bash
# Create feature branches for enhancements
git checkout -b feature/add-user-search
git add .
git commit -m "feat: Add search functionality for users"
git push origin feature/add-user-search

# Merge back to main
git checkout main
git merge feature/add-user-search
git push origin main
```

### Repository Maintenance
```bash
# Update documentation
git add README.md setup.md
git commit -m "docs: Update API documentation with new examples"

# Add new endpoints
git add app.py test_api.py
git commit -m "feat: Add user search endpoint with filters"

# Version tagging (optional)
git tag -a v1.0.0 -m "Complete User Management REST API v1.0.0"
git push origin v1.0.0
```

## Quality Assurance Checklist

### Before Committing
- ✅ Flask app starts without errors
- ✅ All endpoints return expected responses
- ✅ Test suite passes completely
- ✅ Documentation is up to date
- ✅ Postman collection works correctly
- ✅ No sensitive data in code
- ✅ Code follows Python PEP 8 style

### Repository Structure Check
```
flask-user-management-api/
├── app.py                    # ✅ Main Flask application
├── requirements.txt          # ✅ Dependencies
├── README.md                 # ✅ Comprehensive docs
├── demo.py                   # ✅ Demo script
├── test_api.py              # ✅ Test suite
├── setup.md                  # ✅ Setup instructions
├── postman_requests.py       # ✅ Testing examples
├── postman_collection.json   # ✅ Postman collection
├── .gitignore               # ✅ Exclusion rules
└── .git/                    # Git metadata
```

### Final Testing Workflow
```bash
# 1. Fresh repository clone
git clone <your-repo> fresh-test && cd fresh-test

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run tests
python test_api.py  # Should pass all tests

# 4. Start Flask server
python app.py  # Should start without errors

# 5. Test endpoints (in new terminal)
curl http://localhost:5000/health  # Should return health status
curl http://localhost:5000/users   # Should return sample users
```

## Submission Best Practices

### Repository URL Format
```
https://github.com/YOUR_USERNAME/flask-user-management-api
```

### Documentation Quality
- README.md displays properly on GitHub
- All code blocks have syntax highlighting
- API endpoints are clearly documented
- Installation steps are tested and work
- Examples are copy-pasteable

### Professional Presentation
- Clear repository description
- Proper naming convention (flask-user-management-api)
- Clean commit history without debugging commits
- Professional README with badges (optional)
- Tagged releases for versions (optional)

### Submission Timing
- Complete before 10:00 PM IST deadline
- Leave buffer time for final testing
- Push all changes before submission
- Verify repository is public and accessible

---

**Repository Summary:**
- **Purpose**: User Management REST API with Flask
- **Features**: Complete CRUD operations, data validation, error handling
- **Testing**: Comprehensive test suite, demo script, Postman collection
- **Quality**: Professional documentation, clean code, best practices
- **Status**: Production-ready for evaluation

This creates a professional, complete Flask REST API project! 🚀
