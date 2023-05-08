import pika
import sys

HOST: str = 'localhost'

QUEUE: str = 'hello'

WAITING: str = '[*] Aguardando mensagens. Para sair aperte CTRL+C'
RECIEVED: str = "[x] Recebido '{}'"
SHUTDOWN: str = 'Desligando...'


def on_message_received(ch, method, properties, body):
    print(RECIEVED.format(body))


def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=HOST))
    channel = connection.channel()

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
