import os
import shutil
import re
import logging

# Configuração de log
logging.basicConfig(
    filename='organizacao.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    encoding='utf-8'
)

def setup_directories(base_path):
    """Cria o diretório base se não existir."""
    if not os.path.exists(base_path):
        os.makedirs(base_path)

def get_kit(filename):
    """Determina o KIT com base no nome do arquivo."""
    name_lower = filename.lower()
    
    # Regras para COMPLEMENTARES (Prioridade alta)
    complementares_keywords = ["manual do educador", "formação continuada", "guia do professor"]
    if any(keyword in name_lower for keyword in complementares_keywords):
        return "COMPLEMENTARES"

    # Regras para KIT A
    kit_a_keywords = [
        "linguagem", "matemática", "natureza e sociedade", "língua portuguesa", 
        "gramática", "história", "geografia", "ciências", "cidadania moral e ética"
    ]
    # Verifica palavras exatas ou parciais significativas
    for keyword in kit_a_keywords:
        # Usando regex para garantir que não pegue partes de outras palavras indesejadas, 
        # mas permitindo flexibilidade (ex: "matemática" em "linguagem matemática...")
        if re.search(re.escape(keyword), name_lower): 
            return "KIT A"

    # Regras para KIT B
    kit_b_keywords = [
        "caligrafia", "tabuada", "arte", "artes", "inglês", "english", "atividades de desenho", "atividades lúdicas"
    ]
    for keyword in kit_b_keywords:
        if re.search(re.escape(keyword), name_lower):
            return "KIT B"

    # Regras para KIT C
    kit_c_keywords = [
        "trabalhando com a literatura", "atividades de reforço", "oficina de negócios", "produção de texto"
    ]
    for keyword in kit_c_keywords:
        if re.search(re.escape(keyword), name_lower):
            return "KIT C"

    return None

def get_serie(filename):
    """Extrai a série do nome do arquivo."""
    # Padrão para "X ano" ou "X anos" ou "Educação Infantil"
    # Ex: "1 ano - ...", "2 anos - ...", "Educação Infantil - ..."
    
    # Tenta capturar o padrão no início do arquivo
    match = re.match(r"^(\d+\s*anos?|educação infantil)", filename, re.IGNORECASE)
    if match:
        return match.group(1).title() # Retorna "1 Ano", "2 Anos", etc.
    
    return None

def organize_files(source_dir, output_dir):
    """Organiza os arquivos PDF."""
    
    if not os.path.exists(source_dir):
        print(f"Erro: Diretório de origem '{source_dir}' não encontrado.")
        return

    # Lista arquivos
    try:
        files = [f for f in os.listdir(source_dir) if os.path.isfile(os.path.join(source_dir, f)) and f.lower().endswith('.pdf')]
    except Exception as e:
        print(f"Erro ao listar arquivos: {e}")
        return

    count_moved = 0
    count_error = 0
    
    print(f"Iniciando organização de {len(files)} arquivos...")

    for filename in files:
        serie = get_serie(filename)
        kit = get_kit(filename)
        
        if serie and kit:
            # Caminho de destino
            dest_folder = os.path.join(output_dir, serie, kit)
            os.makedirs(dest_folder, exist_ok=True)
            
            src_path = os.path.join(source_dir, filename)
            dest_path = os.path.join(dest_folder, filename)
            
            try:
                shutil.move(src_path, dest_path)
                count_moved += 1
                # print(f"Movido: {filename} -> {dest_folder}")
            except Exception as e:
                logging.error(f"Erro ao mover '{filename}': {e}")
                print(f"Erro ao mover '{filename}': {e}")
        else:
            reason = []
            if not serie: reason.append("Série não identificada")
            if not kit: reason.append("Kit não identificado")
            
            logging.warning(f"Não classificado: '{filename}' - Motivo: {', '.join(reason)}")
            count_error += 1

    print("-" * 30)
    print(f"Processo concluído.")
    print(f"Arquivos organizados: {count_moved}")
    print(f"Arquivos não classificados: {count_error}")
    print(f"Verifique 'organizacao.log' para detalhes.")

if __name__ == "__main__":
    SOURCE_DIR = "./manuais_otimizados"
    OUTPUT_DIR = "./saida"
    
    # Gera lista_arquivos.txt conforme solicitado (apenas para registro)
    try:
        if os.path.exists(SOURCE_DIR):
            with open("lista_arquivos.txt", "w", encoding="utf-8") as f:
                for item in os.listdir(SOURCE_DIR):
                    f.write(f"{item}\n")
    except Exception as e:
        print(f"Aviso: Não foi possível gerar lista_arquivos.txt: {e}")

    organize_files(SOURCE_DIR, OUTPUT_DIR)
