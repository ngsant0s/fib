def fibonacci(number) -> int:
    '''Fibonacci N digit calculation'''
    if number < 2:
        return number 
    return fibonacci(number - 1) + fibonacci(number - 2)

if __name__ == '__main__':

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