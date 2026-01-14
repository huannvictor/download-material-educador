import time
import os
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# --- CONFIGURAÇÕES ---
USUARIO = "081.068.954-59"
SENHA = "081068"

URL_LOGIN = "https://formandocidadaos.com.br/formando-digital.php"
URL_ALVO = "https://formandocidadaos.com.br/lista_livro_professor_gestor.php"

# Caminho da pasta ajustado conforme seu último pedido
PASTA_DOWNLOAD = os.path.join(os.getcwd(), "manuais_pdf") 

if not os.path.exists(PASTA_DOWNLOAD):
    os.makedirs(PASTA_DOWNLOAD)

# --- CONFIGURAÇÃO DO MODO HEADLESS ---
chrome_options = Options()
chrome_options.add_argument("--headless=new") 
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--window-size=1920,1080")
chrome_options.add_argument("--log-level=3")

driver = webdriver.Chrome(options=chrome_options)

try:
    print(">>> Iniciando em modo oculto (Headless)...")
    print(f">>> Pasta de destino: {PASTA_DOWNLOAD}")
    
    # 1. LOGIN
    driver.get(URL_LOGIN)
    
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "cpf_gestor"))).send_keys(USUARIO)
    driver.find_element(By.ID, "senha_gestor").send_keys(SENHA)
    driver.find_element(By.CSS_SELECTOR, "#login_gestor button[type='submit']").click()
    
    print(">>> Login enviado. Aguardando acesso...")
    
    # 2. ACESSAR ÁREA DE DOWNLOADS
    try:
        WebDriverWait(driver, 10).until(lambda d: URL_ALVO in d.current_url or "area_gestor" in d.current_url)
    except:
        pass 
        
    driver.get(URL_ALVO)

    # 3. PREPARAR SESSÃO DE DOWNLOAD
    cookies_selenium = driver.get_cookies()
    session = requests.Session()
    for cookie in cookies_selenium:
        session.cookies.set(cookie['name'], cookie['value'])
    header_ua = {"User-Agent": driver.execute_script("return navigator.userAgent;")}
    session.headers.update(header_ua)

    # 4. ITERAR SOBRE AS SÉRIES
    select_element = Select(WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.ID, "lista_de_livros"))))
    opcoes_info = []
    
    for opt in select_element.options:
        if "Selecione" not in opt.text:
            opcoes_info.append((opt.text.strip(), opt.get_attribute("value")))

    print(f">>> Encontradas {len(opcoes_info)} opções de Manuais. Iniciando downloads...")

    for nome_serie, valor_serie in opcoes_info:
        try:
            select_obj = Select(driver.find_element(By.ID, "lista_de_livros"))
            
            # --- PONTO CRÍTICO DA CORREÇÃO ---
            select_obj.select_by_value(valor_serie)
            
            # Pausa de 3 segundos para garantir que a tabela anterior suma 
            # e a nova carregue COMPLETA com todos os arquivos
            time.sleep(3) 

            # Garante que pelo menos um botão apareceu antes de tentar ler a lista
            try:
                WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#tbody-table .btn-warning")))
            except:
                print(f" [AVISO] {nome_serie}: Nenhum arquivo encontrado (Time out).")
                continue

            # Agora pega a lista de botões atualizada
            links_elementos = driver.find_elements(By.CSS_SELECTOR, "#tbody-table a.btn-warning")
            urls_para_baixar = [link.get_attribute("href") for link in links_elementos]

            print(f" [OK] {nome_serie}: {len(urls_para_baixar)} arquivos identificados.")

            for url_pdf in urls_para_baixar:
                if not url_pdf: continue
                
                nome_arquivo = url_pdf.split("/")[-1]
                safe_serie = "".join(x for x in nome_serie if x.isalnum() or x in " -_")
                nome_final = f"Prof_{safe_serie}_{nome_arquivo}"
                caminho_completo = os.path.join(PASTA_DOWNLOAD, nome_final)

                if not os.path.exists(caminho_completo):
                    # Tenta baixar
                    try:
                        r = session.get(url_pdf)
                        with open(caminho_completo, 'wb') as f:
                            f.write(r.content)
                    except Exception as e:
                         print(f"      Erro no download: {e}")
                
        except Exception as e:
            print(f" [ERRO] Falha ao processar {nome_serie}: {e}")

finally:
    driver.quit()
    print("\n>>> Processo finalizado!")
