import pika
import json
import requests

# Function to calculate the factorial of a number
def calculate_factorial(n):
    result = 1
    if n > 1:
        for i in range(1, n+1):
            result = result * i
    return result

# Create a callback function
def callback(ch, method, properties, body):
    body = json.loads(body)
    request_id = body['request_id']
    print('Received request with ID: ', request_id)
    input = body['input']
    output = calculate_factorial(input)
    # Update the status to done
    requests.post('http://localhost:5000/factorial/update', json={'id': request_id, 'status': 'done', 'output': output})

def start_consumer():
    # Create connection
    connection = pika.BlockingConnection(pika.URLParameters('amqp://guest:guest@localhost:5672/'))
    channel = connection.channel()
    # Create queue . For now queue name is factorial_process
    channel.queue_declare(queue='factorial_process', durable=True)
    # Listen to the queue and 
    # call the callback function on receiving a message
    channel.basic_consume(queue='factorial_process', on_message_callback=callback, auto_ack=True)
    # Start consuming
    channel.start_consuming()

if __name__ == '__main__':
    start_consumer()