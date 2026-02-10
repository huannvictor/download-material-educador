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

PASTA_DOWNLOAD = os.path.join(os.getcwd(), "manuais_pdfs")
MAX_WORKERS = 4 

# --- CONFIGURAÇÕES DE OTIMIZAÇÃO ---
PASTA_ORIGEM_OTIMIZACAO = PASTA_DOWNLOAD
PASTA_DESTINO_OTIMIZACAO = os.path.join(os.getcwd(), "manuais_otimizados")
CAMINHO_GHOSTSCRIPT = r"C:\Program Files\gs\gs10.06.0\bin\gswin64c.exe"
MODO_COMPRESSAO = "/ebook"

os.makedirs(PASTA_DOWNLOAD, exist_ok=True)
os.makedirs(PASTA_DESTINO_OTIMIZACAO, exist_ok=True)

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