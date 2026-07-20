from email.mime import message
import json
import pika
import os
from dotenv import load_dotenv

load_dotenv()

from app.models.request import Request

class Publisher:

    def publish(self, request: Request) -> None:
        payload = {
            "id": request.id,
            "requested_by": request.requested_by,
            "provider": request.provider,
            "resource_type": request.resource_type,
            "configuration": request.configuration,
            "location": request.location,
            "project_id": request.project_id,
            "end_date": str(request.end_date),
            "status": request.status,
        }

        message = json.dumps(payload)

        credentials = pika.PlainCredentials("admin", "admin")
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=os.getenv("RABBITMQ_HOST"), port=int(os.getenv("RABBITMQ_PORT")), credentials=credentials)
        )

        channel = connection.channel()

        channel.queue_declare(queue="resource_requests", durable=True)
        print("Publishing message...", flush=True)
        print(message, flush=True)
        channel.basic_publish(
            exchange="",
            routing_key="resource_requests",
            body=message,
            properties=pika.BasicProperties(
                delivery_mode=pika.DeliveryMode.Persistent,
            ),
        )
        print("Message published.", flush=True)

        connection.close()