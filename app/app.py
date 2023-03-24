import redis
#mport psycopg2

#Função para calcular o N fibonacci
def fibonacci(number, redis_conn) -> int:
    '''Fibonacci N digit calculation'''
    if number < 2:
        fib_number =  number
        return number


    #Checagem se o numero ja esta escrito no redis
    fib_number = redis_conn.get(number)
    if fib_number is not None:
        return int(fib_number)


    fib_number = fibonacci(number - 1, redis_conn) + fibonacci(number - 2, redis_conn)
    
    redis_write(number, fib_number, redis_conn)
    return fib_number

#Escreve os 10 primeiros digitos no redis cache
def redis_cache_write(redis_conn):
    '''Write the ten first numbers in redis cache'''
    for i in range(1, 11):
        fib_number = fibonacci(i, redis_conn)
        redis_conn.set(f"fib_{i}", fib_number)

#Escreve as buscas subsequentes repetidas no cache
def redis_write(number, value, redis_conn):
    redis_conn.set(number, value)

if __name__ == '__main__':
    #Definindo valor estatico inicial para 'number' "
    number: int = 0

    #Conectar ao cache Redis
    redis_host = 'cache'
    redis_port = 6379
    redis_db = 0
    redis_conn = redis.Redis(host=redis_host,
                             port=redis_port,
                             db=redis_db)



    #Inicialização dos 10 primeiros digitos no redis cache
    redis_cache_write(redis_conn)

    KEEP_RUNNING = True
    print("LOOP BEGIN")
    while KEEP_RUNNING:
        #Seleção de um digito para calculo
        try:
            print("----------")
            n_aux = input("Qual digito da sequencia de Fibonacci deseja?\n").strip()
            number = int(n_aux)
            print("----------")
            print(f"Digito informado: {number}")
        except EOFError:
            print("Erro: entrada de dados interrompida, o programa sera encerrado")
            break
        #Verificação se o digito informado é valido
        if number < 0:
            print("\nCaractere Invalido! Por favor informe um valor inteiro positivo.\n")
        else:        
            print(f"O digito {number} da sequencia e:", fibonacci(number, redis_conn))


        #Escolha do usuario se ira calcular mais numeros
        answer = int(input("Deseja calcular mais algum numero?\n1 -> Sim / 2 -> Nao\n"))
        if answer == 1:
            continue
        else:
            KEEP_RUNNING = False


    #Fechar a conexão com o Redis e o PostgresSQL
    redis_conn.close()