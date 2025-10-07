import base64
import hashlib, sys, math, secrets

class RsaCrypto:
    def __init__(self):
        self.oaep_k = 4096//8 # tamanho da chave pública em bytes
        self.oaep_hLen = hashlib.sha3_512().digest_size # tamanho do output SHA-3 512 em bytes

    def OS2IP(self, data: bytes) -> int:
        return int.from_bytes(data, 'big')

    def I2OSP(self, number: int, numberLen: int) -> bytes:
        if number >= pow(256, numberLen):
            raise ValueError('The number is too large to perform a conversion')

        return number.to_bytes(numberLen, 'big')



    def MGF1(self, mgfSeed: bytearray, maskLen: int) -> bytearray:
        if maskLen > pow(2,32)*self.oaep_hLen:
            raise ValueError('The mask length is too long to be used on MGF1')

        T_data = bytearray()
        i = 0

        while i < maskLen:
            C_bstr = self.I2OSP(i, 4)
            concat = bytearray()
            concat.extend(mgfSeed)
            concat.extend(bytearray(C_bstr))
            seed_hash = bytearray(hashlib.sha3_512(bytes(concat)).digest())
            T_data.extend(seed_hash)

            i += 1

        return T_data[0:maskLen]


    def padMessage(self, message: bytearray, L="") -> bytes:

        # Verifica se o tamanho do bloco é válido
        mLen = len(message)

        if mLen > self.oaep_k - (2*self.oaep_hLen) - 2:
            raise ValueError('The message length is too long to be padded using OAEP')

        PsLen = self.oaep_k - mLen - (2*self.oaep_hLen) - 2

        # Hash do label
        lHas = bytearray(hashlib.sha3_512(L.encode('utf-8')).digest())

        # Valor de PS com PsLen zeros
        PS = bytearray(PsLen)

        # Concatenação de valores
        DB = bytearray()
        DB.extend(lHas)
        DB.extend(PS)
        DB.extend(bytearray(b'\x01'))
        DB.extend(message)

        # Chamadas MGF
        seed = secrets.token_bytes(self.oaep_hLen)
        DB_mask = self.MGF1(bytearray(seed), self.oaep_k - self.oaep_hLen - 1)
        masked_DB = bytes(a ^ b for a, b in zip(DB, DB_mask))
        seed_mask = self.MGF1(bytearray(masked_DB), self.oaep_hLen)
        masked_seed = bytes(a ^ b for a, b in zip(seed, seed_mask))

        # Mensagem codificada
        EM = bytearray()
        EM.extend(bytearray(b'\x00'))
        EM.extend(bytearray(masked_seed))
        EM.extend(bytearray(masked_DB))

        return bytes(EM)

    def unpadMessage(self, EM: bytearray, L="") -> bytes:

        # Hash do label
        lHas = bytearray(hashlib.sha3_512(L.encode('utf-8')).digest())

        # Separação de EM
        offset = 1
        Y = EM[0]

        if Y != 0:
            raise ValueError('The message cant be decoded')

        masked_seed = EM[offset:offset+self.oaep_hLen]
        offset += self.oaep_hLen

        masked_DB = EM[offset:offset+(self.oaep_k - self.oaep_hLen - 1)]


        # Chamadas MGF
        seed_mask = self.MGF1(masked_DB, self.oaep_hLen)
        seed = bytes(a ^ b for a, b in zip(masked_seed, seed_mask))
        DB_mask = self.MGF1(bytearray(seed), self.oaep_k - self.oaep_hLen - 1)
        DB = bytearray(a ^ b for a, b in zip(masked_DB, DB_mask))

        # Separação de DB
        lHas2 = DB[0:self.oaep_hLen]

        if lHas != lHas2:
            raise ValueError('The message cant be decoded')

        index = self.oaep_hLen
        while (index < len(DB)):
            if DB[index] == 1:
                break
            index += 1

        else:
            raise ValueError('The message cant be decoded')

        return bytes(DB[index+1:len(DB)])

    def encrypt(self, message: bytearray, e: int, n: int) -> bytes:
        EM = self.padMessage(message)
        m = self.OS2IP(EM)

        crypt_m = pow(m, e, n)

        return self.I2OSP(crypt_m, self.oaep_k)

    def decrypt(self, ciphertext: bytearray, d: int, n: int, L="") -> bytes:
        ctn = self.OS2IP(ciphertext)

        EM_num = pow(ctn, d, n)

        EM = self.I2OSP(EM_num, self.oaep_k)

        return self.unpadMessage(bytearray(EM))

# Função para calcular hash SHA-3
def calculate_sha3_hash(message):
    if isinstance(message, str):
        message = message.encode('utf-8')
    sha3 = hashlib.sha3_256()
    sha3.update(message)
    return bytearray(sha3.digest())

# Função para assinar mensagem
def sign_message(message, d, n):
    rsa_crypt = RsaCrypto()

    message_hash = calculate_sha3_hash(message)
    signature = rsa_crypt.encrypt(message_hash, d, n)
    return signature

# Função para verificar assinatura
def verify_signature(message, signature, e, n):
    rsa_crypt = RsaCrypto()

    message_hash = calculate_sha3_hash(message)
    decrypted_hash = rsa_crypt.decrypt(signature, e, n)

    return message_hash == decrypted_hash

# Função para formatar documento assinado em BASE64
def format_signed_document(message, signature):
    # Converter assinatura para bytes e depois para BASE64
    #signature_bytes = signature.to_bytes((signature.bit_length() + 7) // 8, 'big')
    signature_b64 = base64.b64encode(signature).decode('utf-8')
    
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
        #signature = int.from_bytes(signature_bytes, 'big')
        
        return message, signature_bytes
    
    except Exception as e:
        raise ValueError(f"Erro ao fazer parsing do documento assinado: {str(e)}")
