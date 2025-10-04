import base64
import hashlib

# Função de criptografia para TESTE sem padding
def dummyEncrypt(message, e, n):
    return pow(message, e, n)

def dummyDecrypt(cipher_text, d, n):
    return pow(cipher_text, d, n)

# Função para calcular hash SHA-3
def calculate_sha3_hash(message):
    if isinstance(message, str):
        message = message.encode('utf-8')
    sha3 = hashlib.sha3_256()
    sha3.update(message)
    return int.from_bytes(sha3.digest(), 'big')

# Função para assinar mensagem
def sign_message(message, d, n):
    message_hash = calculate_sha3_hash(message)
    signature = dummyEncrypt(message_hash, d, n)
    return signature

# Função para verificar assinatura
def verify_signature(message, signature, e, n):
    message_hash = calculate_sha3_hash(message)
    decrypted_hash = dummyDecrypt(signature, e, n)
    return message_hash == decrypted_hash

# Função para formatar documento assinado em BASE64
def format_signed_document(message, signature):
    # Converter assinatura para bytes e depois para BASE64
    signature_bytes = signature.to_bytes((signature.bit_length() + 7) // 8, 'big')
    signature_b64 = base64.b64encode(signature_bytes).decode('utf-8')
    
    # Formatar documento com delimitadores claros
    formatted = f"MESSAGE_START\n{message}\nMESSAGE_END\nSIGNATURE_START\n{signature_b64}\nSIGNATURE_END"
    return formatted

# Função para fazer parsing do documento assinado
def parse_signed_document(signed_document):
    try:
        lines = signed_document.strip().split('\n')
        
        # Encontrar os índices dos delimitadores
        message_start_idx = -1
        message_end_idx = -1
        signature_start_idx = -1
        signature_end_idx = -1
        
        for i, line in enumerate(lines):
            if line == "MESSAGE_START":
                message_start_idx = i
            elif line == "MESSAGE_END":
                message_end_idx = i
            elif line == "SIGNATURE_START":
                signature_start_idx = i
            elif line == "SIGNATURE_END":
                signature_end_idx = i
        
        # Verificar se todos os delimitadores foram encontrados
        if -1 in [message_start_idx, message_end_idx, signature_start_idx, signature_end_idx]:
            raise ValueError("Formato de documento assinado inválido: delimitadores ausentes")
        
        # Extrair mensagem
        message_lines = lines[message_start_idx + 1:message_end_idx]
        message = '\n'.join(message_lines)
        
        # Extrair assinatura
        signature_b64 = ''.join(lines[signature_start_idx + 1:signature_end_idx])
        
        if not signature_b64:
            raise ValueError("Assinatura não encontrada no documento")
        
        # Decodificar assinatura
        signature_bytes = base64.b64decode(signature_b64)
        signature = int.from_bytes(signature_bytes, 'big')
        
        return message, signature
    
    except Exception as e:
        raise ValueError(f"Erro ao fazer parsing do documento assinado: {str(e)}")