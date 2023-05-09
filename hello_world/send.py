from pika import BlockingConnection, ConnectionParameters
from pika.adapters.blocking_connection import BlockingChannel

from hello_world.config import read_config, RabbitMQConfig

CONFIG_FILE: str = './config.json'

MESSAGE: str = 'Hello, World!'

SENT: str = "[x] Enviado '{}'"


def main() -> None:
    config: RabbitMQConfig = read_config(CONFIG_FILE)

    connection = BlockingConnection(ConnectionParameters(host=config.host))
    channel: BlockingChannel = connection.channel()

    channel.queue_declare(queue=config.queue)

    channel.basic_publish(exchange='', routing_key=config.routing_key, body=MESSAGE.encode())
    print(SENT.format(MESSAGE))
    
    connection.close()


if __name__ == '__main__':
    main()
