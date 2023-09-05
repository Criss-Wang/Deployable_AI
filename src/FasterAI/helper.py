import json
import pika
import uuid
import redis

redis_instance = redis.Redis(host='localhost', port=6379)
redis_instance.select(0)

def publish_to_rabbitMQ(data):
    # Create connection
    connection = pika.BlockingConnection(pika.URLParameters('amqp://guest:guest@localhost:5672/'))
    channel = connection.channel()
    # Create queue . For now queue name is factorial_process
    channel.queue_declare(queue='factorial_process', durable=True)
    # Publish the message to the queue
    channel.basic_publish(exchange='', routing_key='factorial_process', body=json.dumps(data))
    # Close the connection
    connection.close()

def create_request(input):
    # Generate a random ID
    random_id = str(uuid.uuid4())
    # Store the request in Redis
    redis_instance.set(random_id, json.dumps({'input': input, 'status': 'processing', 'output': ''}))
    # Publish the request to RabbitMQ
    publish_to_rabbitMQ({'request_id': random_id, 'input': input})
    # Return the request ID
    return random_id

def get_request(request_id):
    request_data = redis_instance.get(request_id)
    if request_data:
        return json.loads(request_data)
    return None

def update_request(request_id, status, output):
    request_details = get_request(request_id)
    redis_instance.set(request_id, json.dumps({'input': request_details['input'], 'status': status, 'output': output}))