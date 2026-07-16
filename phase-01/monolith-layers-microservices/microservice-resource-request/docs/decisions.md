# Architecture Decisions

This document records the architectural decisions adopted for the Resource Provisioning System project.

The purpose of these decisions is to keep the project consistent during its evolution and avoid architectural drift as new features are introduced.

---

# AD-001 - Event-Driven Architecture

## Decision

The system adopts an asynchronous Event-Driven Architecture.

Services communicate exclusively through RabbitMQ events.

No service performs direct HTTP calls to another service for business operations.

## Rationale

- Loose coupling
- Independent scalability
- Easier provider expansion
- Better fault isolation

---

# AD-002 - Service Ownership

## Decision

Each microservice has a single responsibility.

### Request Service

- Receives provisioning requests.
- Performs structural payload validation.
- Persists the request.
- Publishes the RequestCreated event.

### Provision Service

- Consumes provisioning requests.
- Validates provider-specific business rules.
- Simulates resource provisioning.
- Publishes the provisioning result.

### Notification Service

- Consumes provisioning events.
- Registers notifications.
- Does not contain provisioning logic.

## Rationale

Each service must have a well-defined responsibility and remain independent from the internal implementation of other services.

---

# AD-003 - Database per Microservice

## Decision

Each microservice owns its own database.

No database is shared.

No service is allowed to query another service's database.

## Rationale

This prevents the creation of a distributed monolith and preserves service autonomy.

---

# AD-004 - Provider-Agnostic Request Service

## Decision

The Request Service must remain provider-agnostic.

It must not contain Azure, AWS or GCP business logic.

Provider-specific validation belongs exclusively to the Provision Service.

## Rationale

Adding a new cloud provider must not require changes in the Request Service.

---

# AD-005 - Structural vs Business Validation

## Decision

Validation responsibilities are separated.

### Request Service

Responsible for:

- Valid JSON
- Required fields
- Field types

### Provision Service

Responsible for:

- Provider validation
- Resource validation
- Configuration validation
- Business rules

## Rationale

Business rules belong to the domain responsible for executing them.

---

# AD-006 - Event Contracts

## Decision

Services communicate only through event contracts.

Services never depend on another service's implementation.

## Rationale

Only event schemas are shared.

Internal implementations remain isolated.

---

# AD-007 - HTTP Response Strategy

## Decision

POST /requests returns HTTP 202 Accepted.

The request is accepted for asynchronous processing.

It does not indicate that the requested cloud resource has already been provisioned.

## Rationale

The API creates a provisioning request, not the final cloud resource.

---

# AD-008 - Request Lifecycle

## Decision

A provisioning request follows the lifecycle:

Pending

↓

Provisioning

↓

Completed

or

Pending

↓

Provisioning

↓

Failed

## Rationale

Provisioning is asynchronous and may succeed or fail after the request has been accepted.

---

# AD-009 - Docker First

## Decision

The project must be executable through Docker Compose.

The official execution method is:

docker compose up --build

Development outside Docker is allowed only as a convenience.

## Rationale

The repository must be easily reproducible by anyone cloning it.

---

# AD-010 - Project Extensibility

## Decision

The architecture must allow additional cloud providers without modifying existing services unrelated to provisioning.

Future providers should integrate by implementing new provisioning components.

## Rationale

The architecture must remain open for extension while minimizing changes to existing services.

---

# AD-011 - Service Independence

## Decision

No microservice may know internal implementation details of another microservice.

Communication occurs exclusively through published events.

## Rationale

Services evolve independently while preserving stable integration contracts.

---

# AD-012 - Project Objective

## Decision

This repository represents a production-inspired reference implementation of an asynchronous resource provisioning platform.

The goal is not only to satisfy the academic challenge but also to provide a maintainable, extensible and reproducible architecture.

## Rationale

Architectural consistency has priority over implementing unnecessary features.