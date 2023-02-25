def fibonacci(number) -> int:
    if number < 2:
        return number 
    return fibonacci(number - 1) + fibonacci(number - 2)

if __name__ == '__main__':
    number = int(input("Qual digito da sequencia de Fibonacci deseja?\n"))
    print(f"O digito {number} da sequencia e:", fibonacci(number))