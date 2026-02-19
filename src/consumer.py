import pika
import os
from dotenv import load_dotenv

load_dotenv()


def on_msg_received(ch, method, properties, body):
    print(f"received new msg: {body}")


# env vars
amqp_host = os.getenv("RABBITMQ_HOST")
amqp_port = int(os.getenv("RABBITMQ_PORT"))
amqp_user = os.getenv("RABBITMQ_USER")
amqp_pass = os.getenv("RABBITMQ_PASS")

# connection
credentials = pika.PlainCredentials(amqp_user, amqp_pass)
connection_params = pika.ConnectionParameters(
    host=amqp_host, port=amqp_port, virtual_host="/", credentials=credentials
)
connection = pika.BlockingConnection(connection_params)

# create channel
channel = connection.channel()

# queue
# Note: Ensure this queue name matches your producer (e.g., "letterbox" vs "letter-box")
channel.queue_declare(queue="letter-box")

# consume
channel.basic_consume(
    queue="letter-box", auto_ack=True, on_message_callback=on_msg_received
)

print("Start Consuming...")
channel.start_consuming()
