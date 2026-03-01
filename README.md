Leave Management System – Backend API
Overview

This project is a backend REST API for managing employee leave requests.
It supports:

Creating leave requests

Viewing all leave requests

Approving or rejecting requests

Preventing duplicate processing

Validating date logic

The goal was to design a clean, modular backend architecture that reflects production-ready structure while remaining lightweight.
Architecture

The application follows a modular Flask application factory pattern:
backend/
├── app/
│   ├── __init__.py        # App factory
│   ├── extensions.py      # DB initialization
│   ├── models/            # SQLAlchemy models
│   └── routes/            # Blueprints
├── migrations/            # Alembic migrations
├── run.py                 # Entry point
├── requirements.txt
└── Procfile
Key architectural principles:

Separation of concerns (routes vs models vs configuration)

App factory pattern for scalability

Blueprint-based routing

Database abstraction using SQLAlchemy ORM

Controlled state transitions (Pending → Approved/Rejected)

Key Technical Decisions
1. Flask App Factory Pattern

Used to allow:

Testability

Scalability

Environment-based configuration

Extension initialization separation

2. SQLAlchemy ORM

Chosen over raw SQL to:

Abstract DB engine

Enable migrations

Support future scaling to PostgreSQL

3. Leave Status as Controlled State

Status transitions are restricted:

Only Pending requests can be approved/rejected

Prevents duplicate processing

Protects data integrity

4. Migrations (Alembic)

Used for:

Version-controlled schema changes

Safe production deployment

Reproducible DB setup

5. Production WSGI (Gunicorn)

The development server is not production-safe.
Gunicorn ensures:

Multi-worker support

Proper request handling

Deployment readiness
| Method | Endpoint             | Description     |
| ------ | -------------------- | --------------- |
| POST   | /leaves/             | Create leave    |
| GET    | /leaves/all          | List all leaves |
| PUT    | /leaves/<id>/approve | Approve leave   |
| PUT    | /leaves/<id>/reject  | Reject leave    |
Data Validation

End date must not be before start date

Leave cannot be approved/rejected twice

Required fields enforced

Known Limitations

No authentication layer

No pagination (can be added easily)

No concurrency locking

No role-based authorization

Extension Opportunities

Add JWT authentication

Introduce role-based approval

Add pagination and filtering

Add concurrency protection

Convert status to Enum type

Add audit logging
