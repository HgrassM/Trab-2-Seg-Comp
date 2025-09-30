import math, copy

# Função de utilidade para charmichael
def doesExponentHoldsForIntegerList(a_list, number, exponent):

    for a in a_list:
        if (a**exponent) % number != 1:
            return False

    return True

# Função de charmichael
def charmichael(n):
    a_list = []
    exponent = 1

    # Achar todos os números 'a' coprimos de 'n'
    for i in range(n-1):
        if math.gcd(n, i+1) == 1:
            a_list.append(i+1)

    # Testar expoentes
    while not doesExponentHoldsForIntegerList(a_list, n, exponent):
        exponent += 1

    return exponent

