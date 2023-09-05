from flask import Flask, request

# Function to calculate the factorial of a number
def calculate_factorial(n):
    result = 1
    if n > 1:
        for i in range(1, n+1):
            result = result * i
    return result

# create the Flask app
app = Flask(__name__) 

# route to calculate the factorial of a number
@app.route('/factorial', methods=['GET'])
def factorial_handler():
    no = int(request.args.get('no'))
    result = calculate_factorial(no)
    return str(result)

if __name__ == '__main__':
    app.run(debug=False)