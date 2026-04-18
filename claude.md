# Development Instructions

# Claude Development Best Practices

This document outlines the production and development best practices to follow when writing code. Adherence to these guidelines ensures maintainable, scalable, and professional code.

---

## 0. Plan, Then Execute Workflow

**CRITICAL: Always follow the "Plan, Then Execute" approach before writing any code.**

### Planning Phase

Before writing any code, create a detailed plan:

1. **Understand Requirements**: Break down the task into clear requirements
2. **Design Architecture**: Decide on project structure, components, and their interactions
3. **Identify Dependencies**: List all required packages and external services
4. **Define Interfaces**: Specify API endpoints, function signatures, and data schemas
5. **Plan Testing Strategy**: Determine what needs to be tested and how
6. **Document Approach**: Write down the implementation strategy

### Execution Phase

Only after planning is complete:

1. **Set Up Environment**: Create project structure and install dependencies
2. **Write Tests First** (TDD): Implement tests based on planned specifications
3. **Implement Code**: Write minimal code to pass tests
4. **Refactor**: Improve code quality while keeping tests green
5. **Document**: Add docstrings and update README
6. **Review**: Verify code meets all planned requirements

### Planning Template

Before starting any feature or project, document:

- TASK: Brief description
- REQUIREMENTS: List all requirements as checkboxes
- ARCHITECTURE: Components needed, data flow, external dependencies
- TEST STRATEGY: Unit tests and integration tests needed
- IMPLEMENTATION STEPS: Numbered step-by-step approach

**Never skip the planning phase.** It saves time, reduces bugs, and ensures clear direction.

---

## 1. PEP 8 Conventions

Follow PEP 8 style guide strictly:

- Use 4 spaces for indentation (no tabs)
- Maximum line length: 79 characters for code, 72 for comments
- Naming conventions:
  - `snake_case` for functions and variables
  - `PascalCase` for class names
  - `UPPER_CASE` for constants
- Two blank lines between top-level functions/classes
- One blank line between class methods
- Group imports: standard library → third-party → local
- Avoid wildcard imports (`from module import *`)

Use tools like `ruff` or `flake8` for automatic enforcement.

---

## 2. Docstrings

Use docstrings for all public modules, classes, functions, and methods. Use Google-style or NumPy-style consistently.

### Format Requirements

- Document the purpose of the function/class
- List all parameters with their types and descriptions
- Specify return type and what is returned
- Document any exceptions that may be raised
- Keep docstrings concise but informative

For classes, document the class purpose and key attributes. Keep docstrings concise but informative.

---

## 3. Project Structure

Maintain a clean and organized directory structure with the following components:

### Directory Structure

```
project_root/
├── main.py                 # Main application entry point (FastAPI factory)
├── config/                 # Configuration files directory
│   └── prompt.yaml        # Prompt configuration file
├── data/                   # Data storage and artifacts
├── tests/                  # Test suite containing unit and integration tests
└── src/                    # Source code directory
    ├── components/         # Reusable components and building blocks
    ├── services/           # Business logic layer (class-based services)
    ├── routers/            # API endpoint definitions and route handlers (FastAPI)
    ├── schemas/            # Schema definitions for data validation and serialization
    │   ├── pydantic/       # Pydantic models for request/response validation
    │   └── sqlalchemy/     # SQLAlchemy ORM models for database interactions
    ├── models/             # Machine learning and deep learning model definitions
    ├── pipelines/          # Data processing and ML pipeline implementations
    ├── dependencies/       # Dependency injection utilities and reusable dependencies
    ├── core/               # Core configuration, application setup, and shared utilities
    ├── prompts/            # Prompt templates directory
    │   ├── react_prompts.json    # ReAct (Reasoning + Acting) prompt templates
    │   └── cot_prompts.json      # Chain-of-Thought prompt templates
    ├── constants.py        # Application-wide constants
    ├── utils.py            # Utility functions and helpers
    ├── run.py              # Project runner script
    └── llms.py             # LLM-related code and utilities
```

### Directory Descriptions

**Root Level:**
- `main.py`: Main application entry point (FastAPI factory)
- `config/`: Configuration files directory
- `data/`: Data storage and artifacts
- `tests/`: Test suite containing unit and integration tests

**Source Code (src/):**
- `components/`: Reusable components and building blocks
- `services/`: Business logic layer (class-based services)
- `routers/`: API endpoint definitions and route handlers (FastAPI)
- `schemas/pydantic/`: Pydantic models for request/response validation
- `schemas/sqlalchemy/`: SQLAlchemy ORM models for database interactions
- `models/`: Machine learning and deep learning model definitions
- `pipelines/`: Data processing and ML pipeline implementations
- `dependencies/`: Dependency injection utilities and reusable dependencies
- `core/`: Core configuration, application setup, and shared utilities
- `prompts/`: Prompt templates directory
- `constants.py`: Application-wide constants
- `utils.py`: Utility functions and helpers
- `run.py`: Project runner script
- `llms.py`: LLM-related code and utilities

---

## 3.1. Package Management with uv

**Use uv for fast, reliable Python package management.**

### Setup and Usage

Key commands:

- Install uv using the official installation script
- Create virtual environment with `uv venv`
- Activate environment (platform-specific activation)
- Install dependencies with `uv pip install -r requirements.txt`
- Add new packages with `uv pip install package-name`
- Sync dependencies with `uv sync` (for pyproject.toml)
- Generate requirements.txt with `uv pip freeze`

### Project Setup with uv

Workflow:

1. Initialize new project with `uv init`
2. Install production dependencies (fastapi, uvicorn, sqlalchemy, pydantic, pytest)
3. Install dev dependencies (black, ruff, pytest-cov)
4. Lock dependencies to requirements.txt

**Always use uv instead of pip for faster and more reliable dependency management.**

---

## 4. Test-Driven Development (TDD)

Follow the Red-Green-Refactor cycle:

1. **Red**: Write a failing test first
2. **Green**: Write minimal code to pass the test
3. **Refactor**: Improve code while keeping tests green

### Unit Tests

Unit tests should:

- Test individual components in isolation
- Use fixtures for test setup
- Test both success and failure cases
- Have descriptive test names
- Assert specific expected outcomes
- Use pytest.raises for exception testing

### Integration Tests

Integration tests should:

- Test API endpoints end-to-end
- Use TestClient for FastAPI applications
- Verify HTTP status codes
- Validate response structure
- Test authentication and authorization flows

**Always write tests before implementation. Test coverage should be >80%.**

---

## 5. Dockerfile

Create optimized, multi-stage Dockerfiles using uv:

### Dockerfile Structure

**Builder Stage:**

- Use python:3.12-slim as base
- Install uv from official image
- Copy requirements.txt and install dependencies with uv
- Install system dependencies if needed

**Final Stage:**

- Use python:3.12-slim as base
- Copy Python dependencies from builder stage
- Copy application code
- Create non-root user for security
- Set appropriate user permissions
- Expose application port
- Add health check endpoint
- Set CMD to run uvicorn

### Key Features

- Multi-stage build reduces final image size
- Non-root user for security
- Health check for container orchestration
- Minimal attack surface with slim base image

---

## 6. Docker Compose

Use docker-compose.yml only when explicitly needed for multi-container setups.

### Structure Requirements

**API Service:**

- Build from Dockerfile
- Expose appropriate ports
- Set environment variables (DATABASE_URL, REDIS_URL)
- Define dependencies on other services
- Mount volumes for development

**Database Service:**

- Use official PostgreSQL Alpine image
- Set environment variables for credentials
- Mount volume for data persistence
- Connect to application network

**Cache Service (Redis):**

- Use official Redis Alpine image
- Connect to application network
- Optional volume for persistence

**Volumes:**

- Define named volumes for database persistence

**Networks:**

- Create custom bridge network for service communication

---

## 7. main.py

Structure the main application file cleanly with these components:

### Application Factory Pattern

Create a factory function that:

- Initializes FastAPI application
- Configures application metadata (title, version, docs URLs)
- Implements lifespan context manager for startup/shutdown events
- Adds middleware (CORS, authentication, logging)
- Includes routers with appropriate prefixes and tags
- Returns configured application instance

### Lifespan Management

Use asynccontextmanager for:

- Database connection initialization on startup
- Resource allocation
- Cleanup and disconnection on shutdown
- Connection pool management

### Health Check Endpoint

Implement health check endpoint that:

- Returns application status
- Includes version information
- Can be used for container orchestration
- Verifies critical dependencies

### Main Entry Point

Include conditional main block:

- Uses uvicorn to run the application
- Configures host and port
- Enables reload for development
- Can specify worker count for production

---

## 8. Object-Oriented Programming and Design Patterns

### SOLID Principles

Follow SOLID principles:

- **S**ingle Responsibility: One class, one purpose
- **O**pen/Closed: Open for extension, closed for modification
- **L**iskov Substitution: Subclasses should be interchangeable
- **I**nterface Segregation: Many specific interfaces over one general
- **D**ependency Inversion: Depend on abstractions, not concretions

### Singleton Pattern

Implement Singleton pattern for shared resources:

- Use class-level instance variable
- Implement thread-safe instantiation with locks
- Override **new** method to control instance creation
- Initialize resources only once in **init**
- Common use cases: database connections, configuration managers, logging

### Service Layer Pattern

Encapsulate business logic in service classes:

- Separate concerns: routing → service → data access
- Keep routers thin, services focused
- Use dependency injection for testability
- Services should handle business logic only
- One service per domain entity or business concept

---

## 9. Code Simplicity and Readability

### Key Principles

1. **Keep It Simple**: Write clear, straightforward code
2. **Avoid Deep Nesting**: Use early returns to reduce complexity
3. **Meaningful Names**: Use descriptive variable and function names
4. **DRY Principle**: Don't Repeat Yourself - extract reusable functions
5. **Single Responsibility**: Each function should do one thing well
6. **Limit Function Length**: Keep functions under 50 lines when possible
7. **Prefer Composition**: Build complex behavior from simple components
8. **Clear Control Flow**: Make the logic path obvious
9. **Limit File Length**: Each file should be ideally within 200-300 lines of code.

### Guidelines

- Use early returns to flatten nested conditionals
- Extract complex conditionals into named functions
- Break large functions into smaller, focused ones
- Use meaningful variable names that explain intent
- Avoid clever one-liners that sacrifice readability
- Write code for humans first, computers second

**Remember**: Code is read more often than written. Prioritize clarity over cleverness.

---

## 10. README File

Create a concise, informative README without emojis.

### Required Sections

**Project Overview:**

- Project name and brief description
- Purpose and key features

**Prerequisites:**

- Python version requirement (3.11+)
- uv package manager
- Database requirements (PostgreSQL, Redis if applicable)

**Installation:**

- Install uv with official script
- Clone repository instructions
- Setup virtual environment with uv
- Install dependencies using uv pip
- Environment configuration (.env setup)
- Database migrations
- Start application

**Usage:**

- API base URL
- Swagger UI and ReDoc documentation URLs
- Key endpoints or features

**Testing:**

- Run all tests
- Run unit tests
- Run integration tests

**Development:**

- Linting commands
- Formatting commands
- Clean up commands

**Project Structure:**

- Brief directory layout explanation
- Purpose of main directories

**Contributing:**

- Fork and branch workflow
- Test requirements
- Pull request process

**License and Contact:**

- License type
- Maintainer contact information

---

## 11. Makefile

Create a comprehensive Makefile using uv for package management.

### Required Targets

**Help Target:**

- Display all available targets with descriptions
- Use awk to parse inline documentation

**Installation Targets:**

- `install`: Install all dependencies (production + dev) with uv
- `install-prod`: Install production dependencies only
- `sync`: Sync dependencies using uv sync

**Testing Targets:**

- `test`: Run all tests with coverage reports
- `test-unit`: Run unit tests only
- `test-integration`: Run integration tests only
- `test-watch`: Run tests in watch mode

**Linting and Formatting Targets:**

- `lint`: Run ruff or flake8 checks
- `lint-fix`: Auto-fix linting issues
- `format`: Format code with black and ruff
- `format-check`: Check formatting without changes

**Application Targets:**

- `run`: Run application in development mode with reload
- `run-prod`: Run application in production mode with workers

**Database Targets:**

- `migrate`: Run database migrations
- `migrate-create`: Create new migration with message prompt
- `migrate-rollback`: Rollback last migration

**Docker Targets:**

- `docker-build`: Build Docker image
- `docker-run`: Run Docker container
- `docker-compose-up`: Start docker-compose services
- `docker-compose-down`: Stop docker-compose services

**Utility Targets:**

- `clean`: Remove all generated files and caches
- `requirements`: Generate requirements.txt from uv
- `pre-commit`: Run format, lint, and test in sequence

### Variables to Define

- PYTHON, UV, PYTEST, BLACK, RUFF
- DOCKER_IMAGE, DOCKER_TAG
- Any project-specific paths or configurations

---

## Additional Best Practices

### Environment Variables

Never hardcode sensitive information:

- Use python-dotenv to load environment variables
- Store all sensitive data in .env file
- Provide .env.example template
- Access variables using os.getenv()
- Set sensible defaults for non-sensitive configs
- Document all required environment variables

### Logging

Use structured logging instead of print statements:

- Configure logging at application startup
- Use appropriate log levels (DEBUG, INFO, WARNING, ERROR, CRITICAL)
- Include contextual information in logs
- Log exceptions with stack traces using exc_info=True
- Use logger per module with **name**
- Consider structured logging for production (JSON format)
- Dont use emojis
- Dont create extra md files

### Error Handling

Create custom exceptions and handle errors gracefully:

- Define base application exception class
- Create specific exception classes for different error types
- Use try-except blocks appropriately
- Return meaningful HTTP status codes in APIs
- Log errors before raising or returning
- Provide user-friendly error messages
- Never expose internal errors to end users

### Type Hints

Always use type hints for better code clarity:

- Add type hints to all function parameters
- Specify return types for all functions
- Use typing module for complex types (List, Dict, Optional, Union)
- Use type hints for class attributes
- Consider using mypy for static type checking
- Document types in docstrings if complex

---

## Summary

Following these best practices ensures professional, production-ready applications:

### Core Principles

1. **Plan Before Execute**: Always create a detailed plan before writing code
2. **Use uv**: Fast, reliable package management
3. **Follow PEP 8**: Consistent code style
4. **TDD Approach**: Write tests first, then implement
5. **Clean Architecture**: Well-organized project structure
6. **OOP & Patterns**: SOLID principles and design patterns
7. **Simple Code**: Readable, maintainable, and clear
8. **Documentation**: Comprehensive docstrings and README
9. **Automation**: Makefile for common tasks

**Remember**: Always plan first, keep code simple, and prioritize clarity over cleverness.

## Project Context

The application is a Vision Language Model (VLM) Evaluation Pipeline designed as part of a larger Food Calorie Counter product. Its primary role is to evaluate and compare multiple VLMs for their effectiveness in food item classification tasks. This repository focuses solely on the model evaluation layer—testing various VLMs, aggregating their results, computing custom evaluation metrics, and identifying the best-performing model for downstream food recognition tasks. The system provides a data-driven approach to model selection before integrating the chosen VLM into the production pipeline.

## Current Task

The current task is to implement and test a comprehensive VLM evaluation pipeline that processes a directory of food images, runs inference across multiple vision-language models, concatenates and analyzes results, and produces detailed performance metrics. The goal is to establish a reliable and repeatable model evaluation framework that enables informed decision-making for selecting the optimal VLM for food classification tasks.

## Notes
