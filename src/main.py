from rsa import genprimes, keygen, crypto
from sign_verify import DigitalSignature

def test_part1():
    """Teste da Parte I: Geração de chaves e cifração básica"""
    print("=== PARTE I: GERAÇÃO DE CHAVES E CIFRAÇÃO ===")
    
    keys = keygen.generateKeys()
    print(f"As chaves RSA geradas são:\n e: {keys['e']}\n d: {keys['d']}\n n: {keys['n']}\n")

    # Teste de cifração/decifração
    plaintext = 12345
    ciphertext = crypto.dummyEncrypt(plaintext, keys["e"], keys["n"])
    decrypted = crypto.dummyDecrypt(ciphertext, keys["d"], keys["n"])

    print(f"Texto original: {plaintext}")
    print(f"Texto cifrado: {ciphertext}")
    print(f"Texto decifrado: {decrypted}")
    print(f"Decifração correta: {plaintext == decrypted}\n")

    return keys

def test_part2_part3():
    """Teste das Partes II e III: Assinatura e Verificação Digital"""
    print("\n=== PARTE II e III: ASSINATURA E VERIFICAÇÃO DIGITAL ===")
    
    # Criar instância de assinatura digital
    ds = DigitalSignature()
    
    # Mensagem de teste
    test_message = "Esta é uma mensagem importante que precisa ser assinada digitalmente."
    
    print("1. Assinando a mensagem...")
    # Parte II: Assinar o documento
    signed_doc = ds.sign_document(test_message)
    print("Documento assinado gerado com sucesso!")
    print(f"Documento assinado (primeiras 200 caracteres):\n{signed_doc[:200]}...\n")
    
    print("2. Verificando a assinatura...")
    # Parte III: Verificar a assinatura
    is_valid, recovered_message = ds.verify_document(signed_doc)
    
    print(f"Mensagem recuperada: {recovered_message}")
    print(f"Assinatura válida: {is_valid}\n")
    
    print("3. Testando verificação com mensagem alterada...")
    # Teste: tentar verificar com mensagem alterada
    tampered_doc = signed_doc.replace("importante", "MODIFICADA")
    is_valid_tampered, tampered_message = ds.verify_document(tampered_doc)
    
    print(f"Assinatura válida para mensagem modificada: {is_valid_tampered}")
    print(f"Isso demonstra a integridade da assinatura digital!\n")

def test_hash_function():
    """Teste da função de hash SHA-3"""
    print("\n=== TESTE DA FUNÇÃO HASH SHA-3 ===")
    
    test_string = "Mensagem de teste para hash"
    hash_result = crypto.calculate_sha3_hash(test_string)
    
    print(f"Mensagem: {test_string}")
    print(f"Hash SHA3-256 (como inteiro): {hash_result}")
    print(f"Tamanho do hash em bits: {hash_result.bit_length()}\n")

if __name__ == "__main__":
    # Executar todos os testes
    keys = test_part1()
    test_hash_function()
    test_part2_part3()