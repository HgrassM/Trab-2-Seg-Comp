# Função de criptografia para TESTE sem padding
def dummyEncrypt(message, e, n):
    return pow(message, e, n)

def dummyDecrypt(cipher_text, d, n):
    return pow(cipher_text, d, n)
