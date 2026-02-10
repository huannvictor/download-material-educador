import time
import os
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from concurrent.futures import ThreadPoolExecutor
import concurrent.futures

# --- CONFIGURAÇÕES ---
USUARIO = "081.068.954-59"
SENHA = "081068"

URL_LOGIN = "https://formandocidadaos.com.br/formando-digital.php"
URL_ALVO = "https://formandocidadaos.com.br/lista_livro_professor_gestor.php"

# Cria a pasta 'manuais_pdf' no mesmo local onde o script está
PASTA_DOWNLOAD = os.path.join(os.getcwd(), "manuais_pdfs")

# Define quantos downloads podem acontecer ao mesmo tempo
MAX_WORKERS = 4 

if not os.path.exists(PASTA_DOWNLOAD):
    os.makedirs(PASTA_DOWNLOAD)

# --- FUNÇÃO DE DOWNLOAD EM SEGUNDO PLANO ---
def baixar_arquivo_thread(url, caminho_arquivo, cookies, headers):
    try:
        if os.path.exists(caminho_arquivo):
            return f" [Pular] Já existe: {os.path.basename(caminho_arquivo)}"
        
        # Faz o download via streaming (para não ocupar muita memória)
        r = requests.get(url, cookies=cookies, headers=headers, stream=True)
        if r.status_code == 200:
            with open(caminho_arquivo, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
            return f" [Sucesso] Baixado: {os.path.basename(caminho_arquivo)}"
        else:
            return f" [Erro] Status {r.status_code} para {url}"
    except Exception as e:
        return f" [Falha] Erro ao baixar {url}: {e}"

# --- CONFIGURAÇÃO DO MODO HEADLESS (Invisível) ---
chrome_options = Options()
chrome_options.add_argument("--headless=new") 
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--window-size=1920,1080")
chrome_options.add_argument("--log-level=3") # Reduz logs do Chrome no terminal

driver = webdriver.Chrome(options=chrome_options)
executor = ThreadPoolExecutor(max_workers=MAX_WORKERS)
futuros_downloads = []

try:
    print(">>> Iniciando Automação (Modo Headless + Multi-Thread)...")
    print(f">>> Pasta de destino: {PASTA_DOWNLOAD}")
    
    # ---------------------------------------------------------
    # 1. LOGIN
    # ---------------------------------------------------------
    driver.get(URL_LOGIN)
    
    # Preenche CPF (Gestor) e Senha
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "cpf_gestor"))).send_keys(USUARIO)
    driver.find_element(By.ID, "senha_gestor").send_keys(SENHA)
    
    # Clica Entrar
    driver.find_element(By.CSS_SELECTOR, "#login_gestor button[type='submit']").click()
    print(">>> Login enviado. Aguardando acesso...")
    
    # ---------------------------------------------------------
    # 2. ACESSAR PÁGINA DE DOWNLOADS
    # ---------------------------------------------------------
    try:
        WebDriverWait(driver, 10).until(lambda d: URL_ALVO in d.current_url or "area_gestor" in d.current_url)
    except: pass
    
    driver.get(URL_ALVO)

    # ---------------------------------------------------------
    # 3. PREPARAR SESSÃO (Cookies)
    # ---------------------------------------------------------
    cookies_dict = {c['name']: c['value'] for c in driver.get_cookies()}
    headers_dict = {"User-Agent": driver.execute_script("return navigator.userAgent;")}

    # ---------------------------------------------------------
    # 4. MAPEAMENTO DE DISCIPLINAS
    # ---------------------------------------------------------
    select_element = Select(WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.ID, "lista_de_livros"))))
    
    opcoes_info = []
    for opt in select_element.options:
        if "Selecione" not in opt.text:
            opcoes_info.append((opt.text.strip(), opt.get_attribute("value")))

    print(f">>> Encontradas {len(opcoes_info)} opções/disciplinas.")
    print(">>> Iniciando varredura...")

    # ---------------------------------------------------------
    # 5. LOOP DE NAVEGAÇÃO E EXTRAÇÃO
    # ---------------------------------------------------------
    for nome_serie, valor_serie in opcoes_info:
        try:
            # Seleciona a opção no dropdown
            select_obj = Select(driver.find_element(By.ID, "lista_de_livros"))
            select_obj.select_by_value(valor_serie)
            
            # --- LÓGICA DE ESTABILIDADE (SEGURANÇA) ---
            # O loop abaixo verifica a cada 0.5s se novos arquivos apareceram na tabela.
            # Só avança quando o número de arquivos parar de mudar (estabilizar).
            qtd_anterior = -1
            estavel_count = 0
            elementos = []
            
            for _ in range(20): # Tenta por até 10 segundos
                elementos = driver.find_elements(By.CSS_SELECTOR, "#tbody-table a.btn-warning")
                qtd_atual = len(elementos)
                
                # Verifica se a quantidade mudou
                if qtd_atual > 0 and qtd_atual == qtd_anterior:
                    estavel_count += 1
                else:
                    estavel_count = 0 # Reseta se mudou
                
                # Se ficou estável por 3 checagens (1.5s), confirma.
                if estavel_count >= 3:
                    break
                
                qtd_anterior = qtd_atual
                time.sleep(0.5)

            if not elementos:
                 print(f" -- {nome_serie}: Nenhum arquivo detectado.")
                 continue

            # --- ENVIA PARA DOWNLOAD EM SEGUNDO PLANO ---
            count_local = 0
            for link in elementos:
                url_pdf = link.get_attribute("href")
                if url_pdf:
                    nome_arq = url_pdf.split("/")[-1]
                    # Limpa nome da série para não dar erro no Windows
                    safe_serie = "".join(x for x in nome_serie if x.isalnum() or x in " -_")
                    nome_final = f"Prof_{safe_serie}_{nome_arq}"
                    caminho_completo = os.path.join(PASTA_DOWNLOAD, nome_final)
                    
                    # Adiciona tarefa na fila
                    future = executor.submit(baixar_arquivo_thread, url_pdf, caminho_completo, cookies_dict, headers_dict)
                    futuros_downloads.append(future)
                    count_local += 1
            
            print(f" [OK] {nome_serie}: {count_local} arquivos enviados para fila.")

        except Exception as e:
            print(f" [ERRO] Falha ao processar {nome_serie}: {e}")

    # ---------------------------------------------------------
    # 6. FINALIZAÇÃO
    # ---------------------------------------------------------
    print("\n>>> Navegação concluída! Aguardando término dos downloads...")
    
    # Mostra o resultado de cada download conforme eles terminam
    for future in concurrent.futures.as_completed(futuros_downloads):
        print(future.result())

finally:
    executor.shutdown(wait=True)
    driver.quit()
    print("\n>>> Processo finalizado com sucesso!")
