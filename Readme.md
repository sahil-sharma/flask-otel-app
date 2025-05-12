# Flask CRUD App with OpenTelemetry, JWT Authentication, and Prometheus Metrics

This is a Flask-based CRUD application with JWT authentication and metrics collection using Prometheus. It also integrates OpenTelemetry for distributed tracing. The application supports multiple routes for user management and item handling, while providing tracing and monitoring capabilities.

## Features
- **JWT Authentication**: Secure login and signup functionality with JWT tokens.
- **CRUD Operations**: Create and retrieve items.
- **Prometheus Metrics**: Exposes metrics for Prometheus monitoring.
- **Distributed Tracing**: Collects and exports traces using OpenTelemetry.
- **Database**: PostgreSQL integration for persistent storage.

## Prerequisites
Before you begin, ensure you have the following installed:
- Python 3.x
- Docker (for running Jaeger or Zipkin)
- Postgres database or connection to one
- Helm (for Kubernetes deployment, if needed)

## Installation

1. **Clone the Repository**

   ```bash
   git clone https://github.com/yourusername/flask-crud-app.git
   cd flask-crud-app
   pip install -r requirements.txt
   python3 app.py
   ```

📡 **API Endpoints**

## 1. GET / - Display Welcome Message
- Description: Returns a simple welcome message.
- Authentication: Not Required

## 2. POST /login - User Login
- Description: Logs in a user and returns a JWT token.
- Authentication: Not Required
- Headers:
```bash
"Content-Type: application/json"
```
- Request Body:
```bash
{
  "username": "user1",
  "password": "pass123"
}
```
- Response:
```bash
{
  "token": "<JWT_TOKEN>"
}
```

## 3. POST /signup
- Description: Registers a new user.
- Authentication: Not required
- Headers:
```bash
"Content-Type: application/json"
```
- Request Body:
```bash
{
  "username": "newuser",
  "password": "newpass"
}
```

## 4. POST /items
- Description: Adds a new item.
- Authentication: ✅ JWT required
- Headers:
```bash
"Content-Type: application/json"
"Authorization: Bearer <JWT_TOKEN>"
```
- Request Body:
```bash
{
  "name": "ItemName",
  "description": "ItemDescription"
}
```
- Response Body:
```bash
{
  "Item added successfully."
}
```

## 5. GET /items
- Description: Retrieves all items.
- Authentication: ✅ JWT required
- Headers:
- Headers:
```bash
"Content-Type: application/json"
"Authorization: Bearer <JWT_TOKEN>"
```
- Response Body:
```bash
{
  "name": "ItemName1",
  "description": "ItemDescription1",
  "name": "ItemName2",
  "description": "ItemDescription2"
  ...
}
```

## 6. GET /external
- Description: Makes an external API request to httpbin.org.
- Authentication: ✅ JWT required
- Headers:
```bash
"Content-Type: application/json"
"Authorization: Bearer <JWT_TOKEN>"
```
- Response Body:
```bash
HTTP 200 OK
```

# Example Usage
## Login to get JWT token:
```bash
curl -X POST http://localhost:5000/login \
-H "Content-Type: application/json" \
-d '{"username":"user1", "password":"pass123"}'
```

## Access protected endpoint:
```bash
curl -X GET http://localhost:5000/items \
-H "Authorization: Bearer <your_jwt_token>"
```