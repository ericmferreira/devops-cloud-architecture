import pika

print("Iniciando...", flush=True)

credentials = pika.PlainCredentials("admin", "admin")

params = pika.ConnectionParameters(
    host="rabbitmq",
    port=5672,
    virtual_host="/",
    credentials=credentials,
)

print("Criando conexão...", flush=True)

connection = pika.BlockingConnection(params)

print("Conectado!", flush=True)

connection.close()

print("Finalizado.", flush=True)