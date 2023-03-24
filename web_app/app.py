from flask import Flask, request, render_template
from flask_redis import Redis
import json


app = Flask(__name__, template_folder='templates')
app.config['REDIS_URL'] = 'redis://cache:6379/0'

redis_cache = Redis(app)

def fibonacci(number) -> list:
    '''Fibonacci N digit calculation'''
    if number < 0:
        return []

    fib_sequence = [0,1]
    for i in range(2, number + 1):
        fib_sequence.append(fib_sequence[i - 1] + fib_sequence[i - 2])

    return fib_sequence


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        number = int(request.form['number'])
        result = fibonacci(int(number))
        data = {"number": number, "fibonacci": result}
        
        if result is None:
            result = fibonacci(int(number))
            data = {"number": number, "fibonacci": result}
            redis_cache.set(number, json.dumps(data))

        return render_template('index.html', result=result)
    return render_template('index.html')


@app.route('/calculate', methods=['POST'])
def calculate():
    if request.method == 'POST':
        number=request.form['number']
        result = fibonacci(int(number))
        data = {"number": number, "fibonacci": result}

        redis_cache.set(number, json.dumps(data))

        return render_template('index.html', result=result, number=number)
    return render_template('index.html')

if __name__ =='__main__':
    app.run(host='0.0.0.0', port=5000, portdebug=True)