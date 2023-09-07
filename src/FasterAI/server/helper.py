import json
import pika
import uuid
import redis

redis_data_instance = redis.Redis(host='redis', port=6379, db=0)
redis_request_instance = redis.Redis(host='redis', port=6379, db=1)

def publish_to_rabbitMQ(data):
    # Create connection
    connection = pika.BlockingConnection(pika.URLParameters('amqp://guest:guest@rabbitmq:5672/'))
    channel = connection.channel()
    # Create queue . For now queue name is factorial_process
    channel.queue_declare(queue='factorial_process', durable=True)
    # Publish the message to the queue
    channel.basic_publish(exchange='', routing_key='factorial_process', body=json.dumps(data))
    # Close the connection
    connection.close()

def create_request(data):
    # Generate a random ID
    random_id = str(uuid.uuid4())
    # Store the request in Redis
    request_info = json.dumps({'data': data, 'result': ''})
    data_info = json.dumps({'id': random_id, 'result': ''})
    redis_request_instance.set(random_id, request_info, ex=3600)  # 1 hour time-to-live 
    redis_data_instance.set(data, data_info, ex=3600)
    # Publish the request to RabbitMQ
    publish_to_rabbitMQ({'request_id': random_id, 'data': data})
    # Return the request ID
    return random_id

def get_cached_result(data):
    if redis_data_instance.exists(data):
        stored_data = redis_data_instance.get(data)
        data_dict = json.loads(stored_data)
        return data_dict.get("id"), data_dict.get("result")
    else:
        return None, None

def get_result(request_id):
    request_data = redis_request_instance.get(request_id)
    if request_data:
        return json.loads(request_data)
    return None

def update_request(request_id, result):
    request_details = get_result(request_id)
    if not request_details:
        print("bad update!")
        return
    data = request_details['data']
    request_result = json.dumps({'data': data, 'result': result})
    data_result = json.dumps({'id': request_id, 'result': result})
    
    redis_request_instance.set(request_id, request_result, ex=3600)  
    redis_data_instance.set(data, data_result, ex=3600)