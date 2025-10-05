import random, math

#Gera um número aleatório de tamanho "size" em bits
def genNumber(size):
    return random.randrange((2**(size-1))+1, (2**size)-1)

#Gera uma lista de números primos menores que o número n (Sieve of Sundaram)
def genPrimesList(nlimit):
    new_nlimit = (nlimit-1) // 2

    mark_table = [True for i in range(new_nlimit+1)]
    primes_list = []

    #Marca como False os números da forma i + j + 2*i*j tal que 1 <= i <= j
    for i in range(1, len(mark_table)):
        j = i
        while ((i + j + 2*i*j) <= new_nlimit):
            mark_table[i + j + 2*i*j] = False
            j += 1

    #Recupera da tabela os números marcados como True e os tranforma em n = 2*n + 1
    index = 1
    while (index < len(mark_table)):
        if mark_table[index]:
            primes_list.append(2*index + 1)

        index += 1

    return primes_list

#Teste primitivo para checagem de número primo (Sieve of Sundaram)
def lowPrimeTest(prime_number_candidate, matrix_size):
    p_list = genPrimesList(matrix_size)

    #Divide o cadidato a número primo pelos primos menores que ele
    for prime in p_list:
        if (prime_number_candidate % prime == 0):
            return False

    return True

#Teste iterativo de Miller-Rabin para checar se o número é primo
def millerRabin(prime_number_candidate, iterations):
    if prime_number_candidate % 2 == 0:
        return False

    d = prime_number_candidate - 1
    s = 0

    while (d % 2 == 0):
        d //= 2
        s += 1

    for _ in range(iterations):
        a = random.randrange(2, prime_number_candidate - 1)
        x = pow(a, d, prime_number_candidate)

        if x == 1 or x == prime_number_candidate - 1:
            continue

        for _ in range(s - 1):
            x = pow(x, 2, prime_number_candidate)

            if x == prime_number_candidate - 1:
                break
        else:
            return False

    return True

#Gera um número primo suficientemente grande para o RSA
def genPrimeNumber(bit_size):
    while (True):
        prime_candidate = genNumber(bit_size)

        if lowPrimeTest(prime_candidate, bit_size):
            if millerRabin(prime_candidate, 40):
                return prime_candidate
            else:
                continue
        else:
            continue





