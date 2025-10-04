from sign_verify import DigitalSignature
import os
import time
import json
import glob

def example_file_signing():
    """Exemplo de assinatura de arquivo"""
    print("=== EXEMPLO PRÁTICO: ASSINATURA DE ARQUIVO ===")
    
    timestamp = int(time.time())
    
    # Nomes de arquivo
    filename = f"documento_importante_{timestamp}.txt"
    signed_filename = f"documento_assinalado_{timestamp}.txt"
    keys_filename = f"chaves_completas_{timestamp}.json"
    public_key_filename = f"chave_publica_{timestamp}.json"
    
    try:
        # Inicializar sistema de assinatura - isso gera novas chaves
        print("Gerando novas chaves RSA...")
        ds = DigitalSignature()
        
        # Salvar as chaves COMPLETAS para uso futuro (assinar e verificar)
        if ds.save_keys_to_file(keys_filename):
            print(f"✓ Chaves completas salvas em: {keys_filename}")
        
        # Salvar apenas a chave pública (apenas para verificação)
        if ds.save_public_key_only(public_key_filename):
            print(f"✓ Chave pública salva em: {public_key_filename}")
        
        # Criar um arquivo de exemplo
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("CONTRATO IMPORTANTE\n")
            f.write("===================\n")
            f.write("Este documento representa um acordo legal importante.\n")
            f.write("Data: 2024-01-01\n")
            f.write("Partes envolvidas: Alice e Bob\n")
            f.write(f"ID do documento: {timestamp}\n")
        
        # Ler o conteúdo do arquivo
        with open(filename, 'r', encoding='utf-8') as f:
            file_content = f.read()
        
        print(f"\n1. Assinando o arquivo: {filename}")
        
        # Assinar o conteúdo do arquivo
        signed_document = ds.sign_document(file_content)
        
        # Salvar documento assinado
        with open(signed_filename, 'w', encoding='utf-8') as f:
            f.write(signed_document)
        
        print(f"✓ Documento assinado salvo em: {signed_filename}")
        
        # 🔄 **VERIFICAÇÃO IMEDIATA COM AS MESMAS CHAVES**
        print("\n" + "="*50)
        print("VERIFICAÇÃO IMEDIATA (com as mesmas chaves)")
        print("="*50)
        
        # Verificar com a mesma instância (mesmas chaves)
        is_valid, verified_content = ds.verify_document(signed_document)
        print(f"✓ Assinatura válida: {is_valid}")
        
        if is_valid:
            print("✓ O documento é autêntico e não foi alterado!")
        else:
            print("✗ Problema na verificação!")
        
        return filename, signed_filename, keys_filename, public_key_filename
        
    except Exception as e:
        print(f"❌ Erro durante o processo: {e}")
        import traceback
        traceback.print_exc()
        return None, None, None, None

def find_matching_key_file(signed_filename):
    """Encontra o arquivo de chaves correspondente ao arquivo assinado"""
    # Extrair timestamp do arquivo assinado
    try:
        timestamp = signed_filename.split('_')[-1].split('.')[0]
        
        # Procurar por arquivos de chaves com o mesmo timestamp
        patterns = [
            f"chave_publica_{timestamp}.json",
            f"chaves_completas_{timestamp}.json"
        ]
        
        for pattern in patterns:
            if os.path.exists(pattern):
                return pattern
        
        # Se não encontrou por timestamp, procurar qualquer arquivo de chaves
        key_files = glob.glob("chave_publica_*.json") + glob.glob("chaves_*.json")
        if key_files:
            print(f"⚠️  Não encontrado chave com timestamp {timestamp}, usando: {key_files[0]}")
            return key_files[0]
            
        return None
    except:
        return None

def verify_existing_file():
    """Verificar um arquivo assinado existente"""
    print("\n=== VERIFICAÇÃO DE ARQUIVO EXISTENTE ===")
    
    signed_file = input("Digite o caminho do arquivo assinado: ").strip()
    
    if not os.path.exists(signed_file):
        print("❌ Arquivo assinado não encontrado!")
        return
    
    # Tentar encontrar automaticamente o arquivo de chaves correspondente
    key_file = find_matching_key_file(signed_file)
    
    if not key_file:
        print("❌ Nenhum arquivo de chaves correspondente encontrado automaticamente.")
        key_file = input("Digite o caminho do arquivo de chaves JSON: ").strip()
    
    if not os.path.exists(key_file):
        print("❌ Arquivo de chaves não encontrado!")
        print("Arquivos de chaves disponíveis:")
        key_files = glob.glob("chaves_*.json") + glob.glob("chave_publica_*.json")
        for kf in key_files:
            print(f"  - {kf}")
        return
    
    try:
        print(f"Carregando chaves de: {key_file}")
        ds = DigitalSignature(key_file=key_file)
        
        with open(signed_file, 'r', encoding='utf-8') as f:
            signed_content = f.read()
        
        print("Verificando assinatura...")
        is_valid, verified_content = ds.verify_document(signed_content)
        
        print(f"✓ Assinatura válida: {is_valid}")
        
        if is_valid:
            print("✅ Documento íntegro e autêntico!")
            print("\nConteúdo verificado:")
            print(verified_content)
        else:
            print("❌ Documento corrompido ou assinatura inválida!")
            print("\nPossíveis causas:")
            print("- Arquivo de chaves incorreto")
            print("- Documento foi alterado após assinatura")
            print("- Problema na formatação do documento assinado")
            
    except Exception as e:
        print(f"❌ Erro na verificação: {e}")

def verify_with_any_key():
    """Tentar verificar com qualquer arquivo de chaves disponível"""
    print("\n=== VERIFICAÇÃO COM CHAVE AUTOMÁTICA ===")
    
    signed_file = input("Digite o caminho do arquivo assinado: ").strip()
    
    if not os.path.exists(signed_file):
        print("❌ Arquivo assinado não encontrado!")
        return
    
    # Procurar arquivos de chaves no diretório atual
    key_files = glob.glob("chaves_*.json") + glob.glob("chave_publica_*.json")
    
    if not key_files:
        print("❌ Nenhum arquivo de chaves encontrado!")
        print("Os arquivos de chaves devem ter extensão .json")
        return
    
    print("Arquivos de chaves encontrados:")
    for i, key_file in enumerate(key_files, 1):
        print(f"{i}. {key_file}")
    
    try:
        choice = int(input(f"Escolha um arquivo de chaves (1-{len(key_files)}): "))
        selected_key_file = key_files[choice-1]
        
        print(f"Usando chaves de: {selected_key_file}")
        ds = DigitalSignature(key_file=selected_key_file)
        
        with open(signed_file, 'r', encoding='utf-8') as f:
            signed_content = f.read()
        
        is_valid, verified_content = ds.verify_document(signed_content)
        
        print(f"✓ Assinatura válida: {is_valid}")
        
        if is_valid:
            print("✅ Documento íntegro e autêntico!")
        else:
            print("❌ Assinatura inválida com estas chaves!")
            
    except (ValueError, IndexError):
        print("❌ Escolha inválida!")
    except Exception as e:
        print(f"❌ Erro na verificação: {e}")

def list_signed_files():
    """Listar arquivos assinados e suas chaves correspondentes"""
    print("\n=== ARQUIVOS ASSINADOS E CHAVES ===")
    current_dir = os.getcwd()
    
    # Encontrar todos os arquivos assinados
    signed_files = glob.glob("documento_assinalado_*.txt")
    key_files = glob.glob("chaves_*.json") + glob.glob("chave_publica_*.json")
    
    if not signed_files:
        print("Nenhum arquivo assinado encontrado.")
        return
    
    print("Arquivos assinados encontrados:")
    for i, file in enumerate(signed_files, 1):
        matching_key = find_matching_key_file(file)
        key_status = "✅" if matching_key else "❌"
        key_name = matching_key if matching_key else "NÃO ENCONTRADA"
        print(f"{i}. {file} {key_status} {key_name}")
    
    return signed_files

def cleanup_files():
    """Remover arquivos de exemplo"""
    print("\n=== LIMPEZA DE ARQUIVOS ===")
    
    files_to_remove = (
        glob.glob("documento_importante_*.txt") +
        glob.glob("documento_assinalado_*.txt") +
        glob.glob("chaves_*.json") +
        glob.glob("chave_publica_*.json") +
        glob.glob("teste_*.txt")
    )
    
    if not files_to_remove:
        print("Nenhum arquivo para remover.")
        return
    
    print("Arquivos encontrados:")
    for file in files_to_remove:
        print(f"  - {file}")
    
    confirm = input("\nDeseja remover todos estes arquivos? (s/N): ").strip().lower()
    if confirm == 's':
        for file in files_to_remove:
            try:
                os.remove(file)
                print(f"✓ Removido: {file}")
            except Exception as e:
                print(f"❌ Erro ao remover {file}: {e}")
        print("✅ Limpeza concluída!")
    else:
        print("Limpeza cancelada.")

def menu():
    """Menu interativo"""
    while True:
        print("\n" + "="*50)
        print("SISTEMA DE ASSINATURA DIGITAL")
        print("="*50)
        print("1. Criar e assinar novo documento")
        print("2. Verificar arquivo assinado existente")
        print("3. Verificar arquivo assinado (selecionar chave)")
        print("4. Listar arquivos assinados e chaves")
        print("5. Limpar arquivos de exemplo")
        print("6. Sair")
        
        choice = input("\nEscolha uma opção (1-6): ").strip()
        
        if choice == '1':
            original, signed, keys, public = example_file_signing()
            if original and signed and keys:
                print(f"\n✅ Processo concluído! Arquivos criados:")
                print(f"  - Original: {original}")
                print(f"  - Assinado: {signed}")
                print(f"  - Chaves completas: {keys}")
                print(f"  - Chave pública: {public}")
        
        elif choice == '2':
            verify_existing_file()
        
        elif choice == '3':
            verify_with_any_key()
        
        elif choice == '4':
            list_signed_files()
        
        elif choice == '5':
            cleanup_files()
        
        elif choice == '6':
            print("Saindo...")
            break
        
        else:
            print("❌ Opção inválida!")

if __name__ == "__main__":
    menu()