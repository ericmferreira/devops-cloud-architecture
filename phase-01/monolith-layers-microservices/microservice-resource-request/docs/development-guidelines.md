# Development Guidelines

This document defines the development conventions adopted for the project.

These conventions should remain consistent across every microservice.

---

# Naming Conventions

## Directory Names

Use **kebab-case**.

Examples:

service-request
service-provision
service-notification

---

## Python Modules

Use **snake_case**.

Examples:

main.py
database.py
request_service.py

---

## Python Classes

Use **PascalCase**.

Examples:

Request
ProvisionResult
NotificationRepository

---

## Functions

Use **snake_case**.

Functions should describe actions.

Examples:

create_request()
get_request()
list_requests()
publish_event()

Avoid generic names such as:

process()
handler()
execute()

---

## Variables

Use **snake_case**.

Examples:

request_id
resource_group
resource_type
cloud_provider

---

## Constants

Use **UPPER_SNAKE_CASE**.

Examples:

DEFAULT_TIMEOUT

MAX_RETRIES

API_VERSION

---

# Project Language

All technical content must be written in English.

Includes:

- Code
- Variables
- Functions
- Classes
- Comments
- Documentation
- Commit messages

---

# Project Structure

Each microservice follows the same structure.

service-name/

app/

data/

Dockerfile

requirements.txt

.env.example

---

# main.py

The purpose of main.py is only to bootstrap the application.

Avoid placing business logic inside main.py.

Business logic belongs to dedicated modules.

---

# API Design

REST endpoints should use plural nouns.

Examples:

POST /requests

GET /requests

GET /requests/{id}

Avoid verbs in endpoint names.

---

# HTTP Status Codes

Use the most appropriate HTTP status code.

Examples:

202 Accepted

400 Bad Request

404 Not Found

422 Unprocessable Entity

429 Too Many Requests

500 Internal Server Error

---

# Microservice Responsibilities

Each service must have a single responsibility.

No service should:

- Access another service's database.
- Depend on another service's implementation.
- Execute business rules belonging to another service.

---

# Event Communication

Services communicate exclusively through RabbitMQ.

Never invoke another microservice directly for business operations.

---

# Database Ownership

Each microservice owns its own database.

No shared databases.

No cross-service queries.

---

# Docker

The official execution method is:

docker compose up --build

Every service must be executable through Docker.

---

# Git

Commits follow the Conventional Commits specification.

Examples:

feat:

fix:

docs:

build:

refactor:

test:

chore:

ci:

---

# General Principles

Keep functions small.

Keep classes focused.

Prefer composition over duplication.

Write readable code before clever code.

If a responsibility grows, extract it into a new module.

Architecture decisions have priority over implementation convenience.