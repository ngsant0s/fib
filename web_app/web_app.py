from flask import Flask, request, jsonify
import redis
import psycopg2

app = Flask(__name__)

#Conectar ao cache Redis
redis_host = 'cache'
redis_port = 6379
redis_db = 0
redis_conn = redis.Redis(host=redis_host,
                            port=redis_port,
                            db=redis_db)


#Conectar ao postgresQL
postgres_host = 'database'
postgres_port = 5432
postgres_dbname = 'database'
postgres_user = 'postgres'
postgres_password = 'mypasswd'
postgres_conn = psycopg2.connect(host=postgres_host,
                            port=postgres_port,
                            dbname=postgres_dbname,
                            user=postgres_user,
                            password=postgres_password)

#Função para calcular o N fibonacci
def fibonacci(number, redis_conn, postgres_conn) -> int:
    '''Fibonacci N digit calculation'''
    if number < 2:
        fib_number =  number
        return number

    #Checar se o valor esta no Redis
    fib_number = redis_conn.get(number)
    if fib_number is not None:
        return int(fib_number)

    #Checar se o valor esta no PostgresSQL
    cursor = postgres_conn.cursor()
    cursor.execute("SELECT fib_value FROM fibonacci_numbers WHERE digit = %s", (number,))
    row = cursor.fetchone()
    if row is not None:
        fib_number = row[0]
        redis_write(number, fib_number)
        return fib_number

    #Se não estiver, calcular
    fib_number = fibonacci(number - 1, redis_conn, postgres_conn) + fibonacci(number - 2, redis_conn, postgres_conn)
    postgres_write(number, fib_number, postgres_conn)
    redis_write(number, fib_number)
    return fib_number

#Escreve os 10 primeiros digitos no redis cache
def redis_cache_write(redis_conn, postgres_conn):
    '''Write the ten first numbers in redis cache'''
    for i in range(1, 11):
        fib_number = fibonacci(i, redis_conn, postgres_conn)
        redis_conn.set(f"fib_{i}", fib_number)

#Escreve as buscas subsequentes repetidas no cache
def redis_write(number, value):
    redis_conn.set(number, value)

#Inserção no PostgresSQL
def postgres_write(number, fib_number, postgres_conn):
    cursor = postgres_conn.cursor()
    cursor.execute(f"INSERT INTO fibonacci_numbers (digit, fib_value) VALUES ({number}, {fib_number})")
    postgres_conn.commit()

#Rota para calcular o valor
@app.route('/fibonacci', methods=['POST'])
def calculate_fibonacci():
    data = request.json
    number = data.get('number')

    if number is None:
        return jsonify({'error':'Invalid request data'}), 400
    
    try:
        number = int(number)
    except ValueError:
        return jsonify({'error':'Invalid request data'}), 400
    
    if number < 0:
        return jsonify({'error':'Ivalid input.'})
    
    result = fibonacci(number, redis_conn, postgres_conn)
    return jsonify({'result': result})

if __name__ =='__main__':
    app.run(debug=True)