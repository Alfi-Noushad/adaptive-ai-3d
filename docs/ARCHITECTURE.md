# 3. System Architecture & Request Pipeline

## 3.1 Layered Architecture Pattern
The backend adheres to a strict three-layer design pattern to maintain separation of concerns, enhance testability, and simplify maintainability:

1. **API Layer (`app/api/`)**: Serves as the HTTP entry point. Responsible for request routing, input validation (Pydantic schemas), status code mapping, and response packaging.
2. **Service Layer (`app/services/`)**: Encapsulates core business rules, multi-step operations (e.g., AI inference job triggering, quality report evaluation), and coordination between multiple repositories.
3. **Repository Layer (`app/repositories/`)**: Encapsulates the persistence boundary. Executes SQLAlchemy queries against PostgreSQL, abstracting database operations from business logic.

## 3.2 Dependency Injection
FastAPI's built-in dependency injection (`fastapi.Depends`) manages session lifetimes and resource passing. Database connections are created per-request and automatically closed upon completion, ensuring thread-safe access and straightforward component mocking during testing.

## 3.3 Request Flow: Project Fetch Example
1. **Frontend** submits `GET /projects/{id}` with an authorization bearer token.
2. **API Layer** validates the path parameter and injects the database session.
3. **Service Layer** verifies that the requesting user has access rights to the resource.
4. **Repository Layer** queries the PostgreSQL database via SQLAlchemy ORM.
5. **API Layer** serializes the returned entity into the standard `APIResponse` envelope:
   `{ "status": "success", "message": "...", "data": {...}, "error": null, "timestamp": "..." }`