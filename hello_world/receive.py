import sys

from pika import BlockingConnection, ConnectionParameters
from pika.adapters.blocking_connection import BlockingChannel
from pika.channel import Channel
from pika.spec import Basic, BasicProperties

from hello_world.config import RabbitMQConfig, read_config

CONFIG_FILE: str = './config.json'

WAITING: str = '[*] Aguardando mensagens. Para sair aperte CTRL+C'
RECIEVED: str = "[x] Recebido '{}'"
SHUTDOWN: str = 'Desligando...'


def on_message_received(channel: Channel, method: Basic.Deliver, properties: BasicProperties, body: bytes) -> None:
    message: str = body.decode()
    print(RECIEVED.format(message))


def main() -> None:
    config: RabbitMQConfig = read_config(CONFIG_FILE)

    connection = BlockingConnection(ConnectionParameters(host=config.host))
    channel: BlockingChannel = connection.channel()

    channel.queue_declare(queue=config.queue)

    channel.basic_consume(queue=config.queue, on_message_callback=on_message_received, auto_ack=True)

    print(WAITING)
    channel.start_consuming()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print(SHUTDOWN)
        sys.exit()
