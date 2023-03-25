from flask import Flask, request, render_template
from flask_redis import Redis
import json
import psycopg2

app = Flask(__name__, template_folder='templates')
app.config['REDIS_URL'] = 'redis://cache:6379/0'
app.config['POSTGRES_URL'] = 'postgresql://postgres:mypasswd@localhost:5432/fib_db'

redis_cache = Redis(app)

def fibonacci(number) -> list:
    '''Fibonacci N digit calculation'''
    if number < 0:
        return []

    fib_sequence = [0,1]
    for i in range(2, number + 1):
        fib_sequence.append(fib_sequence[i - 1] + fib_sequence[i - 2])

    return fib_sequence

def postgres_connection():
    '''Returns connection object'''
    return psycopg2.connect(app.config['POSTGRES_URL'])

def postgres_write(number, fib_sequence):
    with get_postgres_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("INSERT INTO fibonacci_numbers (numbers, fib_value) VALUES (%s, %s)", (number, json.dumps(fib_sequence)))

def get_sequence_postgres(number):
    with get_postgres_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT sequence FROM fibonacci_numbers WHERE numbers = %s", (number,))
            result = cur.fetchone()
            if result:
                return json.loads(result[0])

                
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        number = int(request.form['number'])

        result = redis_cache.get(number)
        if result:
            result = json.loads(result)
        else:
            result = get_fibonacci_sequence_from_postgres(number)
            if not result:
                result = fibonacci(int(number))
                data = {"number": number, "fibonacci": result}
                redis_cache.set(number, json.dumps(data))

        return render_template('index.html', result=result)
    return render_template('index.html')


@app.route('/calculate', methods=['POST'])
def calculate():
    if request.method == 'POST':
        number=request.form['number']

        result = redis_cache.get(number)
        if result:
            result = json.loads(result)
        else:
            result = get_fibonacci_sequence_from_postgres(number)
            if not result:

                result = fibonacci(int(number))
                postgres_write(int(number), result)
                data = {"number": number, "fibonacci": result}

        redis_cache.set(number, json.dumps(data))

        return render_template('index.html', result=result, number=number)
    return render_template('index.html')

if __name__ =='__main__':
    app.run(host='0.0.0.0', port=5000, portdebug=True)