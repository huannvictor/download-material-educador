import os
import subprocess
from concurrent.futures import ProcessPoolExecutor # Novo: para paralelismo

# --- CONFIGURAÇÕES ---
PASTA_ORIGEM = os.path.join(os.getcwd(), "manuais_pdfs")
PASTA_DESTINO = os.path.join(os.getcwd(), "manuais_otimizados")
CAMINHO_GHOSTSCRIPT = r"C:\Program Files\gs\gs10.06.0\bin\gswin64c.exe"
MODO_COMPRESSAO = "/ebook"

def comprimir_individual(nome_arq):
    """Função isolada para ser executada em paralelo"""
    caminho_full_origem = os.path.join(PASTA_ORIGEM, nome_arq)
    caminho_full_destino = os.path.join(PASTA_DESTINO, nome_arq)
    
    tam_orig = os.path.getsize(caminho_full_origem)
    
    cmd = [
        CAMINHO_GHOSTSCRIPT,
        "-sDEVICE=pdfwrite",
        "-dCompatibilityLevel=1.4",
        f"-dPDFSETTINGS={MODO_COMPRESSAO}",
        "-dNOPAUSE", "-dQUIET", "-dBATCH",
        f"-sOutputFile={caminho_full_destino}",
        caminho_full_origem
    ]

    try:
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        tam_novo = os.path.getsize(caminho_full_destino)
        economia_mb = (tam_orig - tam_novo) / (1024 * 1024)
        return True, nome_arq, economia_mb
    except:
        return False, nome_arq, 0

if __name__ == "__main__":
    if not os.path.exists(CAMINHO_GHOSTSCRIPT):
        print(f"X ERRO: Verifique o caminho do Ghostscript.")
        exit()

    if not os.path.exists(PASTA_DESTINO):
        os.makedirs(PASTA_DESTINO)

    arquivos = [f for f in os.listdir(PASTA_ORIGEM) if f.lower().endswith('.pdf')]
    
    print(f">>> INICIANDO OTIMIZADOR MULTI-CORE ({len(arquivos)} arquivos) <<<")

    economizado_total_mb = 0
    sucessos = 0

    # O segredo está aqui: o Pool decide quantos processos rodar (geralmente 1 por núcleo)
    with ProcessPoolExecutor() as executor:
        resultados = list(executor.map(comprimir_individual, arquivos))

    for status, nome, economia in resultados:
        if status:
            sucessos += 1
            economizado_total_mb += economia
            print(f" [OK] {nome} | Economia: {economia:.2f} MB")
        else:
            print(f" [FALHA] {nome}")

    print("-" * 50)
    print(f"Finalizado: {sucessos}/{len(arquivos)} processados.")
    print(f"Total economizado: {economizado_total_mb:.2f} MB")