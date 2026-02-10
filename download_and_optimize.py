import time
import os
import requests
import re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from concurrent.futures import ThreadPoolExecutor
import concurrent.futures
import subprocess

# --- CONFIGURAÇÕES DE DOWNLOAD ---
USUARIO = "081.068.954-59"
SENHA = "081068"

URL_LOGIN = "https://formandocidadaos.com.br/formando-digital.php"
URL_ALVOS = [
    "https://formandocidadaos.com.br/lista_pdf_gestor.php",
    "https://formandocidadaos.com.br/lista_livro_professor_gestor.php"
]

PASTA_DOWNLOAD = os.path.join(os.getcwd(), "manuais_pdfs")
MAX_WORKERS = 4 

# --- CONFIGURAÇÕES DE OTIMIZAÇÃO ---
PASTA_ORIGEM_OTIMIZACAO = PASTA_DOWNLOAD
PASTA_DESTINO_OTIMIZACAO = os.path.join(os.getcwd(), "manuais_otimizados")
CAMINHO_GHOSTSCRIPT = r"C:\Program Files\gs\gs10.060.0\bin\gswin64c.exe"
MODO_COMPRESSAO = "/ebook"

os.makedirs(PASTA_DOWNLOAD, exist_ok=True)
os.makedirs(PASTA_DESTINO_OTIMIZACAO, exist_ok=True)

# --- FUNÇÕES AUXILIARES ---

def gerar_nome_unico(caminho_base):
    """Verifica se o arquivo existe e adiciona (1), (2) para evitar duplicados."""
    if not os.path.exists(caminho_base):
        return caminho_base
    
    nome, extensao = os.path.splitext(caminho_base)
    contador = 1
    while os.path.exists(f"{nome} ({contador}){extensao}"):
        contador += 1
    return f"{nome} ({contador}){extensao}"

def baixar_arquivo_thread(url, caminho_arquivo, cookies, headers):
    try:
        r = requests.get(url, cookies=cookies, headers=headers, stream=True)
        if r.status_code == 200:
            with open(caminho_arquivo, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
            return f" [Sucesso] Baixado: {os.path.basename(caminho_arquivo)}"
        return f" [Erro] Status {r.status_code} para {url}"
    except Exception as e:
        return f" [Falha] Erro ao baixar {url}: {e}"

def comprimir_pdf(arquivo_entrada, arquivo_saida):
    try:
        cmd = [
            CAMINHO_GHOSTSCRIPT, "-sDEVICE=pdfwrite", "-dCompatibilityLevel=1.4",
            f"-dPDFSETTINGS={MODO_COMPRESSAO}", "-dNOPAUSE", "-dQUIET", "-dBATCH",
            f"-sOutputFile={arquivo_saida}", arquivo_entrada
        ]
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return True
    except:
        return False

# --- BLOCO PRINCIPAL ---
if __name__ == "__main__":
    chrome_options = Options()
    chrome_options.add_argument("--headless=new") 
    driver = webdriver.Chrome(options=chrome_options)
    executor = ThreadPoolExecutor(max_workers=MAX_WORKERS)
    futuros_downloads = []

    try:
        print(">>> Iniciando Automação...")
        driver.get(URL_LOGIN)
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "cpf_gestor"))).send_keys(USUARIO)
        driver.find_element(By.ID, "senha_gestor").send_keys(SENHA)
        driver.find_element(By.CSS_SELECTOR, "#login_gestor button[type='submit']").click()
        
        WebDriverWait(driver, 10).until(lambda d: URL_LOGIN not in d.current_url)
        cookies_dict = {c['name']: c['value'] for c in driver.get_cookies()}
        headers_dict = {"User-Agent": driver.execute_script("return navigator.userAgent;")}

        for url_alvo_single in URL_ALVOS:
            driver.get(url_alvo_single)
            
            select_element = Select(WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.ID, "lista_de_livros"))))
            opcoes_info = [(opt.text.strip(), opt.get_attribute("value")) for opt in select_element.options if "Selecione" not in opt.text]

            for nome_serie, valor_serie in opcoes_info:
                try:
                    select_obj = Select(driver.find_element(By.ID, "lista_de_livros"))
                    select_obj.select_by_value(valor_serie)
                    
                    # Espera a tabela atualizar após a seleção
                    time.sleep(1.5) 
                    
                    # Procura os links de download
                    elementos = driver.find_elements(By.CSS_SELECTOR, "#tbody-table a.btn-warning")
                    
                    count_local = 0
                    for link in elementos:
                        url_pdf = link.get_attribute("href")
                        if url_pdf:
                            # Limpeza: Remove hash, prefixo e caracteres inválidos
                            safe_name = re.sub(r'[^\w\s-]', '', nome_serie).strip()
                            caminho_base = os.path.join(PASTA_DOWNLOAD, f"{safe_name}.pdf")
                            
                            # Garante nome único para evitar conflitos entre categorias
                            caminho_final = gerar_nome_unico(caminho_base)
                            
                            future = executor.submit(baixar_arquivo_thread, url_pdf, caminho_final, cookies_dict, headers_dict)
                            futuros_downloads.append(future)
                            count_local += 1
                    
                    print(f" [OK] {nome_serie}: {count_local} arquivos na fila.")
                except Exception as e:
                    print(f" [ERRO] Falha em {nome_serie}: {e}")

        for future in concurrent.futures.as_completed(futuros_downloads):
            print(future.result())

    finally:
        executor.shutdown(wait=True)
        driver.quit()

    # --- OTIMIZAÇÃO DE PDFS ---
    print("\n>>> INICIANDO OTIMIZADOR DE PDFS <<<")
    print(f"Origem:  {PASTA_ORIGEM_OTIMIZACAO}")
    print(f"Destino: {PASTA_DESTINO_OTIMIZACAO}")
    print("-" * 50)

    if not os.path.exists(CAMINHO_GHOSTSCRIPT):
        print("X ERRO CRÍTICO: Ghostscript não encontrado!")
        print(f"  Verifique o caminho: {CAMINHO_GHOSTSCRIPT}")
        print("  Instale em: https://ghostscript.com/releases/gsdnld.html")
        exit()

    arquivos_para_otimizar = [f for f in os.listdir(PASTA_ORIGEM_OTIMIZACAO) if f.lower().endswith('.pdf')]
    total_arquivos_otimizar = len(arquivos_para_otimizar)
    
    if total_arquivos_otimizar == 0:
        print("Nenhum arquivo PDF encontrado na pasta de origem para otimizar.")
    else:
        sucessos_otimizacao = 0
        economizado_total_mb = 0

        for i, nome_arq in enumerate(arquivos_para_otimizar, 1):
            caminho_full_origem = os.path.join(PASTA_ORIGEM_OTIMIZACAO, nome_arq)
            caminho_full_destino = os.path.join(PASTA_DESTINO_OTIMIZACAO, nome_arq)

            if not os.path.exists(caminho_full_origem):
                print(f" [AVISO] Arquivo {nome_arq} não encontrado na origem, pulando otimização.")
                continue

            tam_orig = os.path.getsize(caminho_full_origem)
            
            print(f"[{i}/{total_arquivos_otimizar}] Otimizando: {nome_arq}...", end="\r")

            if comprimir_pdf(caminho_full_origem, caminho_full_destino):
                tam_novo = os.path.getsize(caminho_full_destino)
                reducao = (1 - (tam_novo / tam_orig)) * 100
                economia_mb = (tam_orig - tam_novo) / (1024 * 1024)
                economizado_total_mb += economia_mb
                
                if tam_novo < tam_orig:
                    print(f" [OK] {nome_arq} | -{reducao:.1f}% ({economia_mb:.2f} MB a menos)")
                else:
                    print(f" [=]  {nome_arq} | Não houve redução significativa.")
                
                sucessos_otimizacao += 1
            else:
                print(f" [FALHA] Não foi possível otimizar {nome_arq}")

        print("-" * 50)
        print(">>> PROCESSO DE OTIMIZAÇÃO FINALIZADO <<<")
        print(f"Arquivos otimizados: {sucessos_otimizacao}/{total_arquivos_otimizar}")
        print(f"Espaço total economizado: {economizado_total_mb:.2f} MB")
        print(f"Verifique a pasta: {PASTA_DESTINO_OTIMIZACAO}")