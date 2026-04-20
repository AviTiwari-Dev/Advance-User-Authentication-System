# Advanced FastAPI User Management Service

This project is an asynchronous user management API built with FastAPI, SQLAlchemy, PostgreSQL, and AsyncPG. It focuses on authentication, account lifecycle management, input validation, and secure token handling for applications that need a solid backend foundation for user accounts.

The codebase is organized around clear layers for endpoints, dependencies, operations, models, configuration, and utilities, which makes it a useful starting point for production-style backend services as well as a good reference project for learning modern Python API design.

## What This Application Does

The service handles the core workflows required by many products:

- User registration with validated profile data
- Secure login with password verification
- Access-token based authentication for protected endpoints
- Refresh-token issuance with database-backed storage
- Logout using refresh-token invalidation
- Authenticated profile lookup through a `me` endpoint
- Username updates for authenticated users
- Automatic table creation during application startup

## Why This Project Is Useful

This repository is useful if you are building:

- SaaS products that need account creation and session management
- Internal platforms that require a reusable authentication service
- Backend systems that need a clean FastAPI + PostgreSQL structure
- Demo or portfolio projects that should show more than CRUD basics
- A foundation for features such as email verification, password reset, role-based access control, and audit logging

It already demonstrates patterns that matter in real systems: async database access, structured validation, layered architecture, security-focused token workflows, and operational safeguards for transient database failures.

## Implemented Features

### Authentication and Session Management

- Signup flow that creates a user profile, email record, and credential record in one database transaction
- Login flow that validates credentials and returns a short-lived bearer access token
- Refresh token generation with a unique token identifier (`jti`)
- Refresh tokens stored as hashes instead of plain values
- Refresh token cookie configured as `HttpOnly`, `Secure`, and `SameSite=Strict`
- Logout flow that removes the stored refresh token associated with the current user
- Access token validation through a reusable dependency

### User Profile Management

- `GET /user-profile/me` for fetching the currently authenticated user
- `PATCH /user-profile/username` for changing the username of the logged-in user
- Automatic username generation during signup

### Data Validation

- Email validation using Pydantic email types
- Password constraints for length and allowed characters
- Name validation with field-level constraints
- Validation rule enforcing `last_name` when `middle_name` is supplied
- Lower-casing for selected string-based inputs
- Strict request models that forbid unexpected fields

### Reliability and Operational Behavior

- Async SQLAlchemy engine and sessions for non-blocking database access
- Exponential retry logic around transient database failures in signup and login flows
- Connection pool settings controlled through environment variables
- Startup lifecycle hook that creates tables from SQLAlchemy metadata

## Advanced-Level Features

This project goes beyond a basic FastAPI starter in several ways:

- Async-first architecture using FastAPI, SQLAlchemy 2.x async APIs, and AsyncPG
- Token separation with explicit `access` and `refresh` token types
- Refresh-token rotation logic implemented in the codebase
- Hashed refresh-token persistence rather than storing raw tokens
- Argon2 password hashing with an application-level pepper
- UUIDv7 identifiers for records, which are useful for sortability and modern distributed systems
- Layered domain structure that separates routers, endpoint handlers, database operations, utilities, and models
- PostgreSQL schema separation for `user_profile` and `auth` domains
- OpenAPI documentation exposed through customized Swagger and ReDoc routes

## Tech Stack

### Frameworks and Runtime

- FastAPI
- Uvicorn
- Python

### Database and ORM

- PostgreSQL
- SQLAlchemy 2.x
- AsyncPG

### Validation and Settings

- Pydantic v2
- pydantic-settings
- email-validator

### Security

- Argon2 via `argon2-cffi`
- JWT handling with `python-jose`
- Secure cookie configuration for refresh tokens

## Project Structure

```text
src/
	main.py                    FastAPI application entrypoint
	bases/                     Declarative ORM bases
	config/                    Environment and settings management
	dependencies/              Reusable FastAPI dependencies
	endpoints/                 Route handlers grouped by feature
	engines/                   SQLAlchemy engine definitions
	enums/                     Shared enumerations
	models/
		data_storage/            SQLAlchemy ORM models
		data_validation/         Pydantic request and response models
	operations/                Database-focused business operations
	routers/                   APIRouter definitions
	session_factories/         Async session factories
	utilities/                 Hashing, token, and username helpers
docs/
	architecture.md            High-level architecture notes
```

## Database Design

The application separates concerns at the database level using multiple schemas:

- `user_profile.users` stores profile and identity information
- `user_profile.email_addresses` stores email address records
- `auth.credentials` stores hashed passwords
- `auth.invalidated_refresh_tokens` stores hashed refresh tokens and expiry data
- `auth.password_histories` is planned for password history tracking

This structure is useful for maintaining clear domain boundaries and preparing the service for future growth.

## API Surface

### Available Endpoints

![Swagger UI Preview](docs/swagger_ui.png)

| Method | Path | Purpose |
| --- | --- | --- |
| POST | `/user-profile/signup` | Register a new user |
| POST | `/user-profile/login` | Authenticate a user |
| POST | `/user-profile/logout` | Log out the current user |
| GET | `/user-profile/me` | Return the current user |
| PATCH | `/user-profile/username` | Update the current user's username |

### Authentication Flow

1. A user signs up or logs in.
2. The API returns an access token in the response body.
3. The API stores a refresh token in a secure cookie.
4. Protected endpoints use the bearer access token.
5. Logout removes the stored refresh token record and clears the cookie.

### API Documentation Routes

- Swagger UI: `/documentation/Swagger`
- ReDoc: `/documentation/ReDoc`
- OpenAPI JSON: `/documentation/openapi.json`

## Example Requests

### Signup

```json
{
	"first_name": "avi",
	"middle_name": "kumar",
	"last_name": "tiwari",
	"email_address": "avi@example.com",
	"password": "pass@123",
	"date_of_birth": "1998-01-30",
	"gender": "male"
}
```

### Login

```json
{
	"email_address": "avi@example.com",
	"password": "pass@123"
}
```

### Protected Request

```http
GET /user-profile/me
Authorization: Bearer <access_token>
```

## Getting Started

### 1. Create a Virtual Environment

```bash
python -m venv .venv
source .venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install -r dev_requirements.txt
```

### 3. Configure Environment Variables

Create a `.env` file in the project root and set the required values:

```env
DEBUG=True
USER_MANAGEMENT_ENGINE_DATABASE_URL=postgresql+asyncpg://postgres:password@localhost:5432/user_management
USER_MANAGEMENT_ENGINE_ECHO=False
USER_MANAGEMENT_ENGINE_POOL_SIZE=5
USER_MANAGEMENT_ENGINE_MAX_OVERFLOW=10
USER_MANAGEMENT_ENGINE_POOL_TIMEOUT=30
USER_MANAGEMENT_ENGINE_POOL_RECYCLE=1800
USER_MANAGEMENT_ENGINE_FUTURE=True
USERNAME_MAX_LENGTH=32
PASSWORD_PEPPER=change-this-secret
MAX_RETRIES=3
BASE_DELAY=0.1
SECRET_KEY=change-this-jwt-secret
ALGORITHM=HS256
```

### 4. Run the Application

```bash
uvicorn src.main:api --reload
```

The app will create database tables on startup using SQLAlchemy metadata.

## Security Notes

- Passwords are hashed with Argon2 and combined with a pepper before storage
- Refresh tokens are set in secure cookies and stored in hashed form in the database
- Access tokens and refresh tokens are distinguished by a dedicated `type` claim
- Authenticated endpoints validate both token structure and user existence

## Current State and Extension Points

The repository already contains the foundation for a broader authentication platform. Architecture notes mention additional capabilities such as password reset, email verification, and background jobs for email workflows.

There is also refresh-token rotation logic in the codebase. At the moment, the refresh endpoint implementation exists under `src/endpoints/refresh.py`, but endpoint registration should be verified before treating it as active in deployment.

## Good Next Features

- Email verification workflow
- Password reset and password change endpoints
- Role-based authorization
- Rate limiting for authentication endpoints
- Audit logging for login and profile changes
- Automated tests for auth and validation flows
- Docker and CI setup for deployment readiness

## Summary

This project is a strong foundation for a production-minded user management API. It demonstrates secure authentication patterns, async database access, clean modular organization, and room for realistic expansion into a complete identity and account service.
