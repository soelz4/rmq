import pika
import os
from dotenv import load_dotenv

# 1. Load environment variables from .env file
load_dotenv()

# 2. Get variables (good practice to set defaults or handle missing vars)
amqp_host = os.getenv("RABBITMQ_HOST")
amqp_port = int(os.getenv("RABBITMQ_PORT"))  # Convert string to int
amqp_user = os.getenv("RABBITMQ_USER")
amqp_pass = os.getenv("RABBITMQ_PASS")

# connection
credentials = pika.PlainCredentials(amqp_user, amqp_pass)
connection_params = pika.ConnectionParameters(
    host=amqp_host, port=amqp_port, virtual_host="/", credentials=credentials
)
connection = pika.BlockingConnection(connection_params)

# channel
channel = connection.channel()
channel.queue_declare(queue="letter-box")

# msg
msg = "Hello World, this is a Message from Producer :))"

channel.basic_publish(exchange="", routing_key="letter-box", body=msg)

print(f"sent message: {msg}")

connection.close()
