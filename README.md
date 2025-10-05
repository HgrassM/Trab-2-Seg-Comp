---
title: "Trabalho de Implementação 2 - Gerador e Verificador de Assinaturas Digitais RSA"
author: "H. de M. O. Lima – 211055281, L. P. Torres – 222011623, and M. N. Miyata – 180126890"
abstract: "Este trabalho apresenta a implementação de um gerador e verificador de assinaturas digitais utilizando o algoritmo RSA. O objetivo é garantir a autenticidade e integridade das mensagens trocadas entre as partes envolvidas. A implementação inclui a geração de chaves públicas e privadas, a assinatura digital de mensagens e a verificação dessas assinaturas. O trabalho também discute os desafios enfrentados durante o desenvolvimento e as soluções adotadas para superá-los."
keywords: ["Assinaturas Digitais", "RSA", "Criptografia"]
bibliography: ["references.bib"]
---

# Introdução

O RSA (Rivest-Shamir-Adleman) é um algoritmo de criptografia assimétrica, em que são utilizadas duas chaves distintas: uma chave pública para criptografar mensagens e uma chave privada para descriptografá-las. O surgimento do RSA foi
importante para resolver o problema de enviar uma mensagem criptografada sem que o remetente e o destinatário precisem compartilhar uma chave secreta previamente @VeritasRSA.

O presente trabalho foi implementado em três partes: (1) geração de chaves públicas e privadas, (2) assinatura digital de mensagens e (3) verificação de assinaturas digitais e descriptografia de mensagens. A seguir, cada uma dessas partes é discutida em detalhes.

# Geração de Chaves

A geração de chaves se baseia no conceito de "trapdoor one-way function", ou seja, uma função que é fácil de calcular em uma direção, mas quase impossível de inverter sem uma informação secreta (a "trapdoor"). No caso do RSA, a função é
baseada na multiplicação de dois números primos grandes @katz2014introduction.

Neste trabalho, os números primos gerados são de 2048 bits, ou seja, possuem aproximadamente 617 dígitos decimais. Para gerar esses números, são combinados dois métodos: (1) o "Sieve of Sundaram" para eliminar rapidamente números divisíveis por primos pequenos, e (2) o "Miller-Rabin Primality Test" para verificar a primalidade dos números restantes. Como o algoritmo de Miller-Rabin é mais custoso, ele é aplicado apenas a um subconjunto dos números gerados pelo Sieve of Sundaram.

## Sieve of Sundaram
O código implementado gera um número aleatório $n$ de 2048 bits e utiliza o Sieve of Sundaram para gerar uma lista de números primos menores que $n$. O Sieve of Sundaram elimina números da forma $i + j + 2ij$, onde $1 \le i \le j$, resultando em uma lista de números que podem ser convertidos em primos utilizando a fórmula $2i + 1$. Abaixo está a implementação do Sieve of Sundaram:

```python
def genPrimesList(nlimit):
    new_nlimit = (nlimit-1) // 2

    mark_table = [True for i in range(new_nlimit+1)]
    primes_list = []

    for i in range(1, new_nlimit+1):
        j = i
        while (i + j + 2*i*j) <= new_nlimit:
            mark_table[i + j + 2*i*j] = False
            j += 1

    if nlimit > 2:
        primes_list.append(2)

    for i in range(1, new_nlimit+1):
        if mark_table[i]:
            primes_list.append(2*i + 1)

    return primes_list
```

## Miller-Rabin Primality Test
Depois de filtrar os números com o Sieve of Sundaram, o código aplica o Miller-Rabin Primality Test para verificar a primalidade dos números restantes. O teste é um algoritmo probabilístico que determina se um número é composto ou provavelmente primo e segue os passos descritos abaixo:

1. Escolher um número ímpar $n > 3$ e um número de iterações $k$.
2. Cortar imediatamente se $n$ é um número par.
3. Decompor $n-1$ na forma $2^s \cdot d$, onde $d$ é ímpar, e $s$ é o número de fatores de 2 em $n-1$, ou seja, quantas vezes $n-1$ pode ser dividido por 2.
4. Testar 40 vezes com bases aleatórias $a$ no intervalo $[2, n-2]$:
   - Calcular $x = a^d \pmod{n}$.
   - Se $x$ é 1 ou $n-1$, continuar para a próxima iteração.
   - Repetir $s-1$ vezes:
     - Calcular $x = x^2 \pmod{n}$.
     - Se $x$ é $n-1$, continuar para a próxima iteração.
   - Se nenhuma das condições acima for satisfeita, retornar FALSO ($n$ é composto).

As etapas do Miller-Rabin Primality Test são implementadas no seguinte código:

```python
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
```