# Cloud Resource Provisioning Platform

Projeto desenvolvido como parte da pós-graduação em DevOps & Cloud Architecture (FIAP).

O objetivo é demonstrar uma arquitetura baseada em microsserviços para processamento assíncrono de solicitações de provisionamento de recursos em provedores de nuvem.

> O projeto possui caráter educacional e não realiza provisionamento real de recursos. O foco está na arquitetura, comunicação entre serviços e desacoplamento utilizando mensageria.

---

# Arquitetura

O fluxo da aplicação é composto por três microsserviços e um broker RabbitMQ.

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

Cada serviço possui responsabilidade única.

| Serviço | Responsabilidade |
|----------|------------------|
| service-request | Recebe requisições HTTP, valida o payload e publica a mensagem na fila |
| service-provision | Consome mensagens da fila e simula o provisionamento |
| service-notification | Consome o resultado do provisionamento e registra a notificação |
| RabbitMQ | Broker responsável pela comunicação assíncrona |

---

# Tecnologias

- Python 3.13
- FastAPI
- RabbitMQ
- Docker
- Docker Compose
- Pydantic
- Uvicorn

---

# Estrutura do projeto

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

# Fluxo

1. O cliente envia uma requisição HTTP.

2. O **service-request**

- valida o payload;
- gera um identificador;
- publica a mensagem no RabbitMQ.

3. O **service-provision**

- consome a mensagem;
- simula o provisionamento;
- publica o resultado em outra fila.

4. O **service-notification**

- consome o resultado;
- registra a notificação.

Todo o processamento ocorre de forma assíncrona.

---

# Exemplo de requisição

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

Resposta:

```http
HTTP/1.1 202 Accepted
```

---

# Variáveis de ambiente

Cada microsserviço possui seu próprio arquivo `.env`.

Exemplo:

```
RABBITMQ_HOST=rabbitmq
RABBITMQ_PORT=5672
RABBITMQ_USER=guest
RABBITMQ_PASSWORD=guest
```

---

# Executando

```bash
docker compose up --build
```

Swagger:

```
http://localhost:8000/docs
```

---