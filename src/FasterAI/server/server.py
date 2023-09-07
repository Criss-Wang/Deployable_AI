from flask_socketio import emit, Namespace

from helper import create_request, get_result, get_cached_result, update_request
from setup import socketio

import json
"""

- Redis to store the data of requests
- Deleting the processed request records from the database as they have no use
- Make the consumer/worker dockerize so it can be easy to run multiple consumers using Amazon EKS, ECS, or other services
TODO:
Things we have done:
- TTL
- persistence with RDB
- Caching request data to Redis
- Avoided long polling with WebSocket, creating separate namespaces for workers and client
"""
# route to queue the request
class FactorialNamespace(Namespace):
    def on_connect(self):
        print('Client connected')

    def on_disconnect(self):
        print('Client disconnected')

    def on_calculate_factorial(self, data):
        # do calculation only if data is not available
        id, result = get_cached_result(data)
        if not id:
            id = create_request(data)
            emit('factorial_id', id)
        else:
            emit('factorial_result', {"id": id, "result": result})

    def on_get_factorial_result(self, id):
        result = get_result(id)
        result = json.dumps({'id': id, 'result': result['result']})
        emit('factorial_result', result)

# WebSocket event handler to update the result
@socketio.on('update_factorial_result')
def update_factorial_result(data):
    id = data['id']
    result = int(data['result'])
    update_request(id, result)

