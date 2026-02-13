import json
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Configurações do Navegador
options = webdriver.ChromeOptions()
options.add_argument("--disable-notifications")
options.add_argument("--start-maximized")
# Remova o comentário abaixo apenas se tudo estiver funcionando bem
# options.add_argument("--headless") 

driver = webdriver.Chrome(options=options)

def get_terabox_links(url, session_cookie):
    try:
        # 1. Acessa o domínio para injetar o cookie
        driver.get("https://www.terabox.com")
        time.sleep(2)
        
        driver.delete_all_cookies()
        driver.add_cookie({
            'name': 'ndus',
            'value': session_cookie,
            'domain': '.terabox.com',
            'path': '/'
        })
        
        # 2. Acessa a pasta compartilhada
        print(f"Acessando: {url}")
        driver.get(url)
        
        # 3. Espera explícita pelo carregamento da lista
        wait = WebDriverWait(driver, 20)
        # Espera até que o corpo da página e algum elemento de lista apareçam
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        
        print("Aguardando renderização dos itens...")
        time.sleep(8) # Tempo para o JavaScript carregar a lista de arquivos

        # 4. Rolagem para carregar itens (Lazy Load)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)

        # 5. Captura de links usando XPaths variados para maior robustez
        # Tenta pegar tanto links diretos quanto spans dentro de containers de nomes
        seletores = [
            "//div[contains(@class, 'file-name')]//a",
            "//a[contains(@href, '/s/')]",
            "//div[contains(@class, 'item-name')]//a"
        ]
        
        links_encontrados = []
        
        for seletor in seletores:
            elementos = driver.find_elements(By.XPATH, seletor)
            for el in elementos:
                try:
                    nome = el.text.strip()
                    link = el.get_attribute('href')
                    
                    if link and "/s/" in link and nome:
                        # Evita duplicatas na lista
                        if not any(item['link'] == link for item in links_encontrados):
                            links_encontrados.append({"nome": nome, "link": link})
                            print(f"[Sucesso] {nome} -> {link}")
                except:
                    continue
        
        return links_encontrados

    except Exception as e:
        print(f"Erro durante a execução: {e}")
        return []
    finally:
        driver.quit()

def salvar_dados(dados, arquivo="links_terabox.json"):
    with open(arquivo, "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=4, ensure_ascii=False)
    print(f"\nTotal de {len(dados)} links salvos em {arquivo}")

# --- CONFIGURAÇÃO ---
LINK_ALVO = "https://www.terabox.com/portuguese/main?category=all&path=%2FMANUAL%20EDUCADOR%20-%20FORMANDO%20CIDADAOS"
# Certifique-se de capturar o 'ndus' atualizado no seu navegador (F12 > Application > Cookies)
MEU_COOKIE_NDUS = "YTjaMr3teHuihdYZtSqptrv0uFLdIz3NyOdsk9lS"

# --- EXECUÇÃO ---
resultado = get_terabox_links(LINK_ALVO, MEU_COOKIE_NDUS)

if resultado:
    salvar_dados(resultado)
else:
    print("\nNenhum link foi extraído. Verifique se a página carregou os arquivos visualmente.")