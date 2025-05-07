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
