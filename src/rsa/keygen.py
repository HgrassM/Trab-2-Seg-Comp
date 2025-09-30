import math, copy
import rsa.genprimes as genprimes

# Função de utilidade para charmichael
def doesExponentHoldsForIntegerList(a_list, number, exponent):
    for a in a_list:
        if (a**exponent) % number != 1:
            return False

    return True

# Função de charmichael
def charmichael(n, is_prime):
    """
    Se 'n' for número primo, então pelo pequeno teorema de Fermat, para todo
    número inteiro 'a' coprimo de 'n' 'a**n-1 mod n = 1'.
    """
    if is_prime:
        return n-1

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

def generateE(totient):
    e = 65537

    while (math.gcd(e, totient) != 1 or e == 65537):
        e += 1

    return e

# Encontra o valor 'x' tal que 'ax % m = 1'
def getModularMultiplicativeInverse(a, m):
    return pow(a, -1, m)

# Gera as cahves RSA
def generateKeys():
    # Gerar números p e q primos de 2048 bits
    p = genprimes.genPrimeNumber(2048)
    q = genprimes.genPrimeNumber(2048)

    # Computar n
    n = p*q

    # Computar a função totient
    # Como n = pq, então charmichael(n) = lcm(charmichael(p), charmichael(p))
    totient = math.lcm(charmichael(p, True), charmichael(q, True))

    # Computar e
    e = generateE(totient)

    # Computar d
    d = getModularMultiplicativeInverse(e, totient)

    return {"e": e, "d": d, "n": n}


