# RabbitMQ

Exemplo de uso do RabbitMQ. Inspirado no [exemplo](https://www.rabbitmq.com/tutorials/tutorial-one-python.html) da
documentação oficial.

# Uso

1. Instale e configure o RabbitMQ na sua máquina com a fila `hello` e routing key `hello`
2. Instale as dependências do `requirements.txt`
3. Em um terminal rode `python send.py`
4. Em outro terminal rode `python recieve.py`

Para mandar outra mensagem, basta rodar `python send.py` novamente no mesmo terminal ou em outro (se em outro, um novo
produtor é criado). A mensagem pode ser modificada ao alterar a constante `MESSAGE` no arquivo `send.py`.

Para criar um novo consumidor, basta abrir outro terminal e executar `python recieve.py` novamente. 
