import redis
import psycopg2

#Função para calcular o N fibonacci
def fibonacci(number, redis_conn, postgres_conn) -> int:
    '''Fibonacci N digit calculation'''
    if number < 2:
        fib_number =  number
        return number


    #Checagem se o numero ja esta escrito no redis
    fib_number = redis_conn.get(number)
    if fib_number is not None:
        return int(fib_number)


    #Checagem se o numero esta no postgres
    cursor = postgres_conn.cursor()
    cursor.execute("SELECT digit FROM fibonacci_numbers WHERE digit = %s", (number,))
    row = cursor.fetchone()
    if row is not None:
        fib_number = row[0]
        redis_write(number, fib_number)
        return fib_number


    fib_number = fibonacci(number - 1, redis_conn, postgres_conn) + fibonacci(number - 2, redis_conn, postgres_conn)
    postgres_write(number, fib_number, postgres_conn)
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

def postgres_write(number, fib_number, postgres_conn):
    cursor = postgres_conn.cursor()
    cursor.execute(f"INSERT INTO fibonacci_numbers (digit, fib_value) VALUES ({number}, {fib_number})")
    postgres_conn.commit()


if __name__ == '__main__':

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


    #Inicialização dos 10 primeiros digitos no redis cache
    redis_cache_write(redis_conn, postgres_conn)

    KEEP_RUNNING = True
    while KEEP_RUNNING:
        #Seleção de um digito para calculo
        try:
            number = int(input("Qual digito da sequencia de Fibonacci deseja?\n").strip())
            print(f"Digito informado: {number}")
        except EOFError:
            print("Erro: entrada de dados interrompida, o programa sera encerrado")
            break
        #Verificação se o digito informado é valido
        if number < 0:
            print("\nCaractere Invalido! Por favor informe um valor inteiro positivo.\n")
        else:        
            print(f"O digito {number} da sequencia e:", fibonacci(number, redis_conn, postgres_conn))


        #Escolha do usuario se ira calcular mais numeros
        answer = int(input("Deseja calcular mais algum numero?\n1 -> Sim / 2 -> Nao\n"))
        if answer == 1:
            continue
        else:
            KEEP_RUNNING = False


    #Fechar a conexão com o Redis e o PostgresSQL
    redis_conn.close()
    postgres_conn.close()