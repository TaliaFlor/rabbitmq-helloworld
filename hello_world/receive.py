import sys

from pika import BlockingConnection, ConnectionParameters
from pika.adapters.blocking_connection import BlockingChannel
from pika.channel import Channel
from pika.spec import Basic, BasicProperties

HOST: str = 'localhost'

QUEUE: str = 'hello'

ENCODING: str = 'utf-8'

WAITING: str = '[*] Aguardando mensagens. Para sair aperte CTRL+C'
RECIEVED: str = "[x] Recebido '{}'"
SHUTDOWN: str = 'Desligando...'


def on_message_received(channel: Channel, method: Basic.Deliver, properties: BasicProperties, body: bytes) -> None:
    message: str = body.decode(ENCODING)
    print(RECIEVED.format(message))


def main() -> None:
    connection = BlockingConnection(ConnectionParameters(host=HOST))
    channel: BlockingChannel = connection.channel()

    channel.queue_declare(queue=QUEUE)

    channel.basic_consume(queue=QUEUE, on_message_callback=on_message_received, auto_ack=True)

    print(WAITING)
    channel.start_consuming()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print(SHUTDOWN)
        sys.exit()
