# Architecture

## Overview

The Resource Provisioning System is an asynchronous, event-driven platform designed to process cloud resource provisioning requests.

The architecture is composed of independent microservices that communicate exclusively through RabbitMQ.

Each microservice owns its own database and is responsible for a single business capability.

---

# Architecture Principles

* Asynchronous communication.
* Event-driven workflow.
* One database per microservice.
* Provider-agnostic Request Service.
* Independent service ownership.
* Docker-first deployment.

---

# High-Level Architecture

```mermaid
flowchart LR

Client["Client"]

Request["Request Service"]

Rabbit["RabbitMQ"]

Provision["Provision Service"]

Notification["Notification Service"]

RequestDB[("requests.db")]
ProvisionDB[("provision.db")]
NotificationDB[("notification.db")]

Client -->|POST /requests| Request

Request --> RequestDB
Request -->|RequestCreated| Rabbit

Rabbit --> Provision

Provision --> ProvisionDB
Provision -->|ProvisionCompleted / ProvisionFailed| Rabbit

Rabbit --> Notification

Notification --> NotificationDB
```

---

# Request Service

The Request Service is the public entry point of the platform.

Responsibilities:

* Receive provisioning requests.
* Validate payload structure.
* Persist accepted requests.
* Publish RequestCreated events.
* Return HTTP responses.

The Request Service does **not** perform provider-specific validation.

---

# Synchronous Request Flow

The HTTP request lifecycle ends inside the Request Service.

```mermaid
flowchart TD

A["POST /requests"]

B["Validate HTTP request"]

C{"Payload valid?"}

D["Return HTTP Error"]

E["Persist request"]

F["Publish RequestCreated"]

G["Return HTTP 202 Accepted"]

A --> B
B --> C

C -->|No| D
C -->|Yes| E

E --> F
F --> G
```

If the request cannot be accepted, no event is published and no request is persisted.

Typical synchronous responses include:

| HTTP Code | Description                                  |
| --------- | -------------------------------------------- |
| 202       | Request accepted for asynchronous processing |
| 400       | Malformed request                            |
| 415       | Unsupported media type                       |
| 422       | Payload validation failed                    |
| 429       | Rate limit exceeded                          |
| 500       | Unexpected Request Service error             |

---

# Asynchronous Provisioning Flow

After a request has been accepted, processing becomes fully asynchronous.

```mermaid
flowchart TD

A["RequestCreated Event"]

B["Provision Service"]

C{"Business validation"}

D["Provision resource"]

E["Publish ProvisionCompleted"]

F["Publish ProvisionFailed"]

A --> B

B --> C

C -->|Valid| D
D --> E

C -->|Invalid| F
```

Business validation includes provider-specific rules, resource configuration and provisioning constraints.

---

# Notification Flow

The Notification Service consumes provisioning events.

Responsibilities:

* Consume provisioning events.
* Register notification history.
* Persist notification records.

The Notification Service contains no provisioning logic.

---

# Complete Event Flow

```mermaid
sequenceDiagram

participant Client
participant Request
participant RabbitMQ
participant Provision
participant Notification

Client->>Request: POST /requests

Request->>Request: Validate payload

alt Invalid request

Request-->>Client: HTTP Error

else Accepted

Request->>Request: Persist request

Request->>RabbitMQ: Publish RequestCreated

Request-->>Client: HTTP 202 Accepted

RabbitMQ->>Provision: RequestCreated

Provision->>Provision: Validate business rules

alt Provision successful

Provision->>RabbitMQ: ProvisionCompleted

RabbitMQ->>Notification: ProvisionCompleted

Notification->>Notification: Persist notification

else Provision failed

Provision->>RabbitMQ: ProvisionFailed

RabbitMQ->>Notification: ProvisionFailed

Notification->>Notification: Persist notification

end

end
```

---

# Service Responsibilities

| Service              | Responsibility                                                                                     |
| -------------------- | -------------------------------------------------------------------------------------------------- |
| Request Service      | Receive requests, validate payload structure, persist accepted requests and publish events.        |
| Provision Service    | Validate provider-specific business rules, simulate provisioning and publish provisioning results. |
| Notification Service | Consume provisioning events and register notifications.                                            |

---

# Data Ownership

Each microservice owns its own persistence layer.

```mermaid
flowchart LR

Request["Request Service"] --> RequestsDB[("requests.db")]

Provision["Provision Service"] --> ProvisionDB[("provision.db")]

Notification["Notification Service"] --> NotificationDB[("notification.db")]
```

No service is allowed to access another service's database.

---

# Communication Model

Microservices communicate only through RabbitMQ.

```mermaid
flowchart LR

Request --> RabbitMQ

RabbitMQ --> Provision

Provision --> RabbitMQ

RabbitMQ --> Notification
```

No direct service-to-service communication is allowed.

---

# Request Lifecycle

```mermaid
stateDiagram-v2

[*] --> Pending

Pending --> Provisioning

Provisioning --> Completed

Provisioning --> Failed
```

A provisioning request is accepted synchronously and processed asynchronously.

The final state is determined only after the Provision Service completes its processing.
