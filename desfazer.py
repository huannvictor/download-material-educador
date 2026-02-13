import os
import shutil

def undo_organization(source_dir, dest_dir):
    """
    Move todos os arquivos PDF de 'source_dir' (recursivamente) de volta para 'dest_dir'.
    Remove diretórios vazios após a movimentação.
    """
    if not os.path.exists(source_dir):
        print(f"Diretório fonte '{source_dir}' não encontrado.")
        return

    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)

    print(f"Movendo arquivos de '{source_dir}' para '{dest_dir}'...")
    count = 0

    for root, dirs, files in os.walk(source_dir, topdown=False):
        for file in files:
            if file.lower().endswith('.pdf'):
                src_path = os.path.join(root, file)
                dest_path = os.path.join(dest_dir, file)
                
                # Evitar sobrescrever se já existir (adiciona sufixo se necessário)
                if os.path.exists(dest_path):
                    base, ext = os.path.splitext(file)
                    counter = 1
                    while os.path.exists(dest_path):
                        dest_path = os.path.join(dest_dir, f"{base}_restore_{counter}{ext}")
                        counter += 1
                
                try:
                    shutil.move(src_path, dest_path)
                    count += 1
                    # print(f"Restaurado: {file}")
                except Exception as e:
                    print(f"Erro ao mover {file}: {e}")
        
        # Tenta remover diretório se estiver vazio
        try:
            if not os.listdir(root):
                os.rmdir(root)
                # print(f"Diretório removido: {root}")
        except Exception as e:
            pass # Ignora erros ao remover diretório

    print(f"Concluído. {count} arquivos restaurados para '{dest_dir}'.")

if __name__ == "__main__":
    # Configuração
    SOURCE_DIR = "./MANUAL EDUCADOR - FORMANDO CIDADAOS" # Pasta onde os arquivos estão agora
    DEST_DIR = "./manuais_otimizados"       # Pasta original
    
    confirm = input(f"Isso moverá TODOS os PDFs de '{SOURCE_DIR}' para '{DEST_DIR}'. Continuar? (s/n): ")
    if confirm.lower() == 's':
        undo_organization(SOURCE_DIR, DEST_DIR)
    else:
        print("Operação cancelada.")
