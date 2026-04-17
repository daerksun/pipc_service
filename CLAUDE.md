# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 🚧 Project Status: IN DEVELOPMENT

This is an incomplete project. The backend API is partially implemented and the frontend is missing.

### What's Implemented ✅
- REST API backend with Python/Cerver framework
- MongoDB database integration with Pymongoose ODM
- Basic CRUD operations for 10 resources
- Docker Compose development environment
- Nginx reverse proxy configuration

### What's Missing ❌
- **Frontend**: Only has a basic test HTML page, needs complete UI
- **Authentication/Authorization**: No JWT or session management
- **Data Validation**: Minimal input validation
- **Tests**: No unit or integration tests
- **API Documentation**: No Swagger/OpenAPI docs
- **Error Handling**: Basic error handling needs improvement

## Development Commands

```bash
# Build Docker image
sh development.sh

# Start all services (MongoDB, Nginx, Python API)
sudo docker compose up

# Rebuild services
sudo docker compose build

# Stop services
sudo docker compose down
```

## Architecture

### Stack
- **Backend**: Python with Cerver HTTP framework
- **Database**: MongoDB (with Pymongoose ODM)
- **Web Server**: Nginx as reverse proxy
- **Containerization**: Docker & Docker Compose

### Service Structure
```
service/
├── main.py           # Entry point, route registration
├── config.py         # Environment configuration
├── db.py            # MongoDB connection and schema setup
├── errors.py        # Error handling definitions
├── models/          # Data models (10 entities)
├── controllers/     # Business logic for each resource
└── routes/          # HTTP route handlers
```

### API Resources
All routes follow pattern: `/api/pipc/[resource]/[action]`

- **organizaciones**: Organizations management
- **usuarios**: User management
- **clientes**: Client management (CRUD complete)
- **establecimientos**: Establishments (CRUD complete)
- **tramites**: Procedures/paperwork (CRUD complete)
- **brigadas**: Brigades (CRUD complete)
- **simulacros**: Drills/simulations (CRUD complete)
- **empleados**: Employees (CRUD complete)
- **programas**: Programs (partial implementation)
- **moral**: Moral persons/entities

### Environment Configuration
- MongoDB URL: Set via `MONGO_URL` environment variable
- API Port: 8080 (internal), exposed via Nginx on port 80
- Upload Path: `/var/uploads`

## Priority Development Tasks

### 1. Complete Frontend
- Choose framework (React/Vue/Angular)
- Create UI components for all API endpoints
- Implement form validation
- Add routing and navigation

### 2. Implement Authentication
- Add JWT token generation and validation
- Create login/logout endpoints
- Implement role-based access control
- Secure all API endpoints

### 3. Enhance Data Validation
- Add input validation in controllers
- Implement request body schemas
- Add field type and constraint validation

### 4. Add Testing
- Unit tests for controllers
- Integration tests for API endpoints
- Database connection tests
- Consider pytest for test framework

### 5. API Documentation
- Implement Swagger/OpenAPI specification
- Document all endpoints with examples
- Add request/response schemas

## Database Schema
Models are defined using Pymongoose with the following entities:
- Brigada, Cliente, Establecimiento, Empleado, Moral
- Organizacion, Programa, Simulacro, Tramite, Usuario

Each model has specific fields defined in `service/models/`

## Docker Services

1. **nginx**: Reverse proxy on port 80
2. **mongo**: MongoDB on port 27017 (admin/12345)
3. **pycerver**: Python API service on port 8080

Network: All services communicate on 'cerver' network

## Notes for Development

- The project uses Cerver, a C-based HTTP server with Python bindings
- File uploads are handled but the load route is commented out
- CORS headers are configured in Nginx for localhost:8080
- The frontend should be developed in `html/` directory or as a separate SPA