# Python Backend Learning Examples

Basic Python backend code to help you understand core concepts. All examples are simple and well-commented.

## Files Included

### 1. `app.py` - Flask API Server
A simple task management API with CRUD operations.

**Key Concepts:**
- Routes and HTTP methods (GET, POST, PUT, DELETE)
- Request/response handling
- Error handling and validation
- Status codes (200, 201, 404, 400)

**Key Functions:**
- `GET /tasks` - Get all tasks
- `GET /tasks/<id>` - Get single task
- `POST /tasks` - Create new task
- `PUT /tasks/<id>` - Update task
- `DELETE /tasks/<id>` - Delete task
- `GET /health` - Health check

### 2. `database.py` - Database Layer
SQLite database operations with context managers.

**Key Concepts:**
- Database connections
- Context managers (`with` statement)
- SQL queries
- CRUD operations
- Connection pooling

**Methods:**
- `get_all_tasks()` - Fetch all records
- `get_task_by_id(id)` - Fetch single record
- `create_task(title)` - Insert record
- `update_task(id, ...)` - Update record
- `delete_task(id)` - Delete record

### 3. `auth_example.py` - Authentication
JWT token-based authentication.

**Key Concepts:**
- JWT tokens
- Authorization headers
- Decorators for middleware
- Token validation

**Functions:**
- `generate_token(user_id)` - Create JWT token
- `verify_token(token)` - Decode and validate token
- `@token_required` - Decorator to protect routes

### 4. `test_api.sh` - Testing Script
Curl commands to test all API endpoints.

### 5. `requirements.txt` - Dependencies
Python packages needed to run the app.

## Getting Started

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the Server
```bash
python app.py
```

The server will start on `http://localhost:5000`

### 3. Test the API

Using curl (from `test_api.sh`):
```bash
# Get all tasks
curl -X GET http://localhost:5000/tasks

# Create a task
curl -X POST http://localhost:5000/tasks \
  -H "Content-Type: application/json" \
  -d '{"title": "My Task"}'

# Update a task
curl -X PUT http://localhost:5000/tasks/1 \
  -H "Content-Type: application/json" \
  -d '{"completed": true}'

# Delete a task
curl -X DELETE http://localhost:5000/tasks/1
```

Or using Python:
```python
import requests

# Create a task
response = requests.post('http://localhost:5000/tasks', 
                        json={'title': 'Learn Python'})
print(response.json())
```

## Key Learning Points

### HTTP Methods
- **GET**: Retrieve data (safe, cacheable)
- **POST**: Create new data (not idempotent)
- **PUT**: Update existing data (idempotent)
- **DELETE**: Remove data (idempotent)

### Status Codes
- **200**: OK - Request succeeded
- **201**: Created - Resource created successfully
- **400**: Bad Request - Invalid input
- **404**: Not Found - Resource doesn't exist
- **500**: Server Error

### REST API Principles
1. Use nouns for resources (not verbs)
2. Use HTTP methods for actions
3. Return appropriate status codes
4. Include resource IDs in URLs
5. Return JSON responses

### Security Tips
- Always validate input
- Use HTTPS in production
- Store secrets in environment variables
- Use authentication for protected routes
- Use CORS for cross-origin requests

## Next Steps

1. **Database Integration**: Modify `app.py` to use `database.py` instead of in-memory storage
2. **Error Handling**: Add try-catch blocks for database errors
3. **Validation**: Use libraries like `marshmallow` or Pydantic for data validation
4. **Testing**: Write unit tests using `pytest`
5. **Deployment**: Learn to deploy to Heroku, AWS, or DigitalOcean
6. **Async**: Explore async Python with `asyncio` or `async` frameworks
7. **Documentation**: Add Swagger/OpenAPI documentation

## Common Patterns

### Pattern 1: Pagination
```python
@app.route('/tasks?page=1&limit=10', methods=['GET'])
def get_tasks():
    page = request.args.get('page', 1, type=int)
    limit = request.args.get('limit', 10, type=int)
    # Implement pagination logic
```

### Pattern 2: Filtering
```python
@app.route('/tasks?completed=true', methods=['GET'])
def filter_tasks():
    completed = request.args.get('completed', type=bool)
    # Filter results based on parameter
```

### Pattern 3: Error Wrapper
```python
def error_handler(status_code, message):
    return jsonify({"error": message, "code": status_code}), status_code
```

## Resources for Learning

- Flask Documentation: https://flask.palletsprojects.com/
- REST API Best Practices: https://restfulapi.net/
- HTTP Status Codes: https://developer.mozilla.org/en-US/docs/Web/HTTP/Status
- JWT Tokens: https://jwt.io/
- SQLite Documentation: https://www.sqlite.org/docs.html
