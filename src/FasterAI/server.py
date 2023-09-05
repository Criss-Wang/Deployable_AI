from flask import Flask, request

from helper import create_request, get_request, update_request

# create the Flask app
app = Flask(__name__) 

# route to queue the request
@app.route('/factorial', methods=['GET'])
def factorial_handler():
    no = int(request.args.get('no'))
    id = create_request(no)
    return id

# route to get the result
@app.route('/factorial/result', methods=['GET'])
def factorial_result_handler():
    id = request.args.get('id')
    result = get_request(id)
    return result

# route to update the result
@app.route('/factorial/update', methods=['POST'])
def factorial_update_handler():
    body = request.get_json()
    id = body['id']
    status = body['status']
    output = body['output']
    update_request(id, status, output)
    return 'OK'

if __name__ == '__main__':
    app.run(debug=False)