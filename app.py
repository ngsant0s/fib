import redis

#Conectar ao cache Redis
redis_host = 'localhost'
redis_port = 6379
redis_db = 0
redis_conn = redis.Redis(host=redis_host, port=redis_port, db=redis_db)

#Função para calcular o N fibonacci
def fibonacci(number) -> int:
    '''Fibonacci N digit calculation'''
    if number < 2:
        return number 
    return fibonacci(number - 1) + fibonacci(number - 2)

#Escreve os 10 primeiros digitos no redis cache
def redis_cache_write():
    '''Write the ten first numbers in redis cache'''
    for i in range(1, 11):
        fib_number = fibonacci(i)
        redis_conn.set(f"fib_{i}", fib_number)

if __name__ == '__main__':

    #Inicialização dos 10 primeiros digitos no redis cache
    redis_cache_write()

    #Seleção de um digito para calculo
    number = int(input("Qual digito da sequencia de Fibonacci deseja?\n"))

    #Condição de loop
    END_PROGRAM = 0
    while not END_PROGRAM:

        #Verificação se o digito informado é valido
        if number < 0:
            print("\nCaractere Invalido! Por favor informe um valor inteiro positivo.\n")
        else:        
            print(f"O digito {number} da sequencia e:", fibonacci(number))

        #Escolha do usuario se ira calcular mais numeros
        answer = int(input("Deseja calcular mais algum numero?\n1 -> Sim / 2 -> Nao\n"))
        if answer == 1:
            number = int(input("Qual digito da sequencia de Fibonacci deseja?\n"))
        else: END_PROGRAM = 1