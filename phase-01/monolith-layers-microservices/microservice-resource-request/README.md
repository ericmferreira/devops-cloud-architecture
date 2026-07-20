# Cloud Resource Provisioning Platform

![Python](https://img.shields.io/badge/Python-3.13-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115-green)
![RabbitMQ](https://img.shields.io/badge/RabbitMQ-Message_Broker-orange)
![Docker](https://img.shields.io/badge/Docker-Containerized-blue)
![License](https://img.shields.io/badge/License-MIT-yellow)

Project developed as part of the **FIAP DevOps & Cloud Architecture** postgraduate program.

The goal of this project is to demonstrate an event-driven microservices architecture for asynchronous cloud resource provisioning requests.

> This project is intended for educational purposes only. It does not provision real cloud resources. Its primary focus is on software architecture, asynchronous communication, and service decoupling through message-based workflows.

---

# Architecture

The application consists of three independent microservices communicating exclusively through a RabbitMQ message broker.

```
                  HTTP Request
                        │
                        ▼
              service-request
                        │
                        ▼
             RabbitMQ (Queue)
                        │
                        ▼
            service-provision
                        │
                        ▼
             RabbitMQ (Queue)
                        │
                        ▼
          service-notification
```

Each service is responsible for a single business capability.

| Service | Responsibility |
|---------|----------------|
| **service-request** | Receives HTTP requests, validates the payload and publishes events to RabbitMQ. |
| **service-provision** | Consumes provisioning requests and simulates resource provisioning. |
| **service-notification** | Consumes provisioning results and registers notifications. |
| **RabbitMQ** | Message broker responsible for asynchronous communication. |

---

# Technologies

- Python 3.13
- FastAPI
- RabbitMQ
- Docker
- Docker Compose
- Pydantic
- Uvicorn

---

# Project Structure

```
.
├── docker-compose.yml
├── service-request
│   ├── app
│   ├── Dockerfile
│   └── requirements.txt
│
├── service-provision
│   ├── app
│   ├── Dockerfile
│   └── requirements.txt
│
├── service-notification
│   ├── app
│   ├── Dockerfile
│   └── requirements.txt
│
└── docs
```

---

# Request Flow

1. The client submits an HTTP request.

2. **service-request**

- validates the request payload;
- generates a request identifier;
- publishes a `RequestCreated` event to RabbitMQ.

3. **service-provision**

- consumes the request event;
- simulates the provisioning process;
- publishes the provisioning result.

4. **service-notification**

- consumes the provisioning result;
- registers the notification.

The entire provisioning workflow is processed asynchronously.

---

# Example Request

```json
{
  "requested_by": "Eric Ferreira",
  "provider": "azure",
  "resource_type": "storage_account",
  "configuration": {
    "subscription": "Production",
    "resource_group": "rg-demo",
    "location": "eastus",
    "tier": "Standard_LRS"
  }
}
```

Response:

```http
HTTP/1.1 202 Accepted
```

---

# Current Scope

This project currently focuses on demonstrating an event-driven microservices architecture.

The implementation includes:

- HTTP API using FastAPI
- Asynchronous communication through RabbitMQ
- Service decoupling
- Containerized deployment with Docker Compose
- Architecture documentation

Persistent storage is intentionally out of scope for the current phase. The objective is to demonstrate asynchronous communication patterns rather than implementing a complete provisioning platform.

Future iterations may include:

- Dedicated database per microservice
- Request tracking
- Notification history
- Automated tests
- CI/CD pipeline
- Cloud provider integrations

---

# Environment Variables

Each microservice contains its own `.env` file.

Example:

```
RABBITMQ_HOST=rabbitmq
RABBITMQ_PORT=5672
RABBITMQ_USER=guest
RABBITMQ_PASSWORD=guest
```

---

# Running the Project

```bash
docker compose up --build
```

Once the containers are running, the FastAPI Swagger UI is available at:

```
http://localhost:8000/docs
```

---

# Documentation

Additional architectural documentation is available in:

- `ARCHITECTURE.md`