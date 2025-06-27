# Flask CRUD App with OpenTelemetry, JWT Authentication, Logging, and Prometheus Metrics

This is a Flask-based CRUD application with JWT authentication and metrics collection using Prometheus. It also integrates OpenTelemetry for distributed tracing. The application supports multiple routes for user management and item handling, while providing tracing and monitoring capabilities.

## Note:

```bash
ChatGPT's help has been taken to generate boiler-plate code and for its further improvements.
```

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
- Endpoint: `http://<URL>/`

## 2. POST /login - User Login
- Description: Logs in a user and returns a JWT token.
- Authentication: Not Required
- Endpoint: `http://<URL>/login`
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
- Endpoint: `http://<URL>/signup`
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

## 4. POST /items/create
- Description: Adds a new item.
- Authentication: ✅ JWT required
- Endpoint: `http://<URL>/items/create`
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
- Description: List all items.
- Authentication: ✅ JWT required
- Endpoint: `http://<URL>/items`
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

## 6. GET /items?item_id=id
- Description: List a specific item with ID.
- Authentication: ✅ JWT required
- Endpoint: `http://<URL>/items?item_id=<id>`
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
}
```

## 7. PUT /items/update?item_id=id
- Description: Update specific item with ID.
- Authentication: ✅ JWT required
- Endpoint: `http://<URL>/items/update?item_id=<id>`
- Headers:
```bash
"Content-Type: application/json"
"Authorization: Bearer <JWT_TOKEN>"
```
- Response Body:
```bash
{
  "name": "ItemName1_Update",
  "description": "ItemDescription1_Update",
}
```

## 8. DELETE /items/delete?item_id=id
- Description: Delete specific item with ID.
- Authentication: ✅ JWT required
- Endpoint: `http://<URL>/items/delete?item_id=<id>`
- Headers:
```bash
"Content-Type: application/json"
"Authorization: Bearer <JWT_TOKEN>"
```
- Response Body:
```bash
{
  "Item Deleted."
}
```

## 9. GET /external
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