from rsa import crypto, keygen
import json
import os

class DigitalSignature:
    def __init__(self, keys=None, key_file=None):
        if key_file and os.path.exists(key_file):
            # Carregar chaves de arquivo existente
            self.keys = self._load_keys_from_file(key_file)
        elif keys is None:
            # Gerar novas chaves
            self.keys = keygen.generateKeys()
        else:
            self.keys = keys
    
    def _load_keys_from_file(self, key_file):
        """Carrega chaves de um arquivo JSON"""
        try:
            with open(key_file, 'r', encoding='utf-8') as f:
                keys_data = json.load(f)
            
            # Verificar se é o formato antigo (apenas e, n) ou novo (e, d, n)
            if 'e' in keys_data and 'n' in keys_data:
                if 'd' in keys_data:
                    # Formato completo (e, d, n)
                    return keys_data
                else:
                    # Formato apenas público (e, n) - não serve para assinar, mas pode verificar
                    return keys_data
            else:
                raise ValueError("Formato de arquivo de chaves inválido")
                
        except Exception as e:
            raise ValueError(f"Erro ao carregar chaves do arquivo {key_file}: {e}")
    
    def save_keys_to_file(self, key_file):
        """Salva as chaves COMPLETAS (e, d, n) em um arquivo JSON"""
        try:
            with open(key_file, 'w', encoding='utf-8') as f:
                json.dump(self.keys, f, indent=2)
            return True
        except Exception as e:
            print(f"Erro ao salvar chaves: {e}")
            return False
    
    def save_public_key_only(self, key_file):
        """Salva apenas a chave pública (e, n) em um arquivo JSON"""
        try:
            public_key = {"e": self.keys["e"], "n": self.keys["n"]}
            with open(key_file, 'w', encoding='utf-8') as f:
                json.dump(public_key, f, indent=2)
            return True
        except Exception as e:
            print(f"Erro ao salvar chave pública: {e}")
            return False
    
    def sign_document(self, message):
        """
        Parte II: Assinatura digital
        1. Cálculo de hash da mensagem (SHA-3)
        2. Assinatura do hash com chave privada
        3. Formatação em BASE64
        """
        print("Assinando mensagem...")
        signature = crypto.sign_message(message, self.keys["d"], self.keys["n"])
        print("Assinatura gerada, formatando documento...")
        signed_document = crypto.format_signed_document(message, signature)
        return signed_document
    
    def verify_document(self, signed_document):
        """
        Parte III: Verificação de assinatura
        1. Parsing do documento assinado
        2. Decifração da assinatura com chave pública
        3. Verificação do hash
        """
        print("Fazendo parsing do documento assinado...")
        message, signature = crypto.parse_signed_document(signed_document)
        print("Parsing concluído, verificando assinatura...")
        
        is_valid = crypto.verify_signature(message, signature, self.keys["e"], self.keys["n"])
        
        return is_valid, message

    def get_public_key(self):
        return {"e": self.keys["e"], "n": self.keys["n"]}
    
    def get_private_key(self):
        return {"d": self.keys["d"], "n": self.keys["n"]}