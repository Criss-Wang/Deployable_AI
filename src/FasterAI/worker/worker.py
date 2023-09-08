import pika
import json
import socketio
import sys

from functools import partial

sys.set_int_max_str_digits(0)


# Function to calculate the factorial of a number
def calculate_factorial(n):
    result = 1
    if n > 1:
        for i in range(1, n+1):
            result = result * i
    return result


# Create a callback function
def callback(ch, method, properties, body, sio):
    body = json.loads(body)
    request_id = body['request_id']
    print('Received request with ID: ', request_id)
    data = body['data']
    result = calculate_factorial(int(data))
    result = str(result)
    # Update the status to done
    sio.emit('update_factorial_result', {
        'id': request_id,
        'result': result
    })


def start_consumer(sio):
    url_params = pika.URLParameters('amqp://guest:guest@rabbitmq:5672/')
    # Create connection
    connection = pika.BlockingConnection(url_params)
    channel = connection.channel()
    channel.exchange_declare(exchange="deployable_ai", exchange_type='direct')

    # Create queue . For now queue name is factorial_process
    channel.queue_declare(queue='deployable_ai', durable=True)

    channel.queue_bind(exchange='deployable_ai',
                       queue='deployable_ai',
                       routing_key='deployable_ai')
    # Listen to the queue and
    # call the callback function on receiving a message
    channel.basic_consume(
        queue='deployable_ai',
        on_message_callback=partial(callback, sio=sio),
        auto_ack=True
    )
    # Start consuming
    channel.start_consuming()


if __name__ == '__main__':
    # Initialize the Socket.IO client
    sio = socketio.Client()

    @sio.on('connect')
    def on_connect():
        print('Connected to WebSocket server')

    @sio.on('disconnect')
    def on_disconnect():
        print('Disconnected from WebSocket server')

    # Connect to the Flask-SocketIO server
    sio.connect('http://server:5000')

    # Start the RabbitMQ consumer with the Socket.IO client as an argument
    start_consumer(sio)