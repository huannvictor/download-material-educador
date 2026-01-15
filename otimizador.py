import os
import subprocess
import time

# --- CONFIGURAÇÕES ---
# Pasta onde estão os PDFs originais (baixados pelo outro script)
PASTA_ORIGEM = os.path.join(os.getcwd(), "manuais_pdfs")

# Pasta onde os PDFs comprimidos serão salvos
PASTA_DESTINO = os.path.join(os.getcwd(), "manuais_otimizados")

# Caminho do executável do Ghostscript (CONFIRA NO SEU COMPUTADOR)
CAMINHO_GHOSTSCRIPT = r"C:\Program Files\gs\gs10.06.0\bin\gswin64c.exe"

# Configuração de Qualidade vs Tamanho
# /ebook   = 150 dpi (Recomendado: boa leitura, tamanho pequeno)
# /screen  = 72 dpi (Qualidade baixa, tamanho minúsculo - bom apenas para visualização rápida)
# /printer = 300 dpi (Alta qualidade, tamanho maior)
MODO_COMPRESSAO = "/ebook"

# --- FUNÇÃO DE COMPRESSÃO ---
def comprimir_pdf(arquivo_entrada, arquivo_saida):
    try:
        cmd = [
            CAMINHO_GHOSTSCRIPT,
            "-sDEVICE=pdfwrite",
            "-dCompatibilityLevel=1.4",
            f"-dPDFSETTINGS={MODO_COMPRESSAO}",
            "-dNOPAUSE", 
            "-dQUIET", 
            "-dBATCH",
            f"-sOutputFile={arquivo_saida}",
            arquivo_entrada
        ]
        
        # Executa o comando sem abrir janelas
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return True
    except Exception as e:
        print(f"[ERRO GHOSTSCRIPT] {e}")
        return False

# --- BLOCO PRINCIPAL ---
if __name__ == "__main__":
    # Verifica se o Ghostscript existe
    if not os.path.exists(CAMINHO_GHOSTSCRIPT):
        print("X ERRO CRÍTICO: Ghostscript não encontrado!")
        print(f"  Verifique o caminho: {CAMINHO_GHOSTSCRIPT}")
        print("  Instale em: https://ghostscript.com/releases/gsdnld.html")
        exit()

    # Cria pasta de destino se não existir
    if not os.path.exists(PASTA_DESTINO):
        os.makedirs(PASTA_DESTINO)

    print(">>> INICIANDO OTIMIZADOR DE PDFS <<<")
    print(f"Origem:  {PASTA_ORIGEM}")
    print(f"Destino: {PASTA_DESTINO}")
    print("-" * 50)

    # Lista arquivos
    arquivos = [f for f in os.listdir(PASTA_ORIGEM) if f.lower().endswith('.pdf')]
    total_arquivos = len(arquivos)
    
    if total_arquivos == 0:
        print("Nenhum arquivo PDF encontrado na pasta de origem.")
        exit()

    sucessos = 0
    economizado_total_mb = 0

    for i, nome_arq in enumerate(arquivos, 1):
        caminho_full_origem = os.path.join(PASTA_ORIGEM, nome_arq)
        caminho_full_destino = os.path.join(PASTA_DESTINO, nome_arq)

        # Pega tamanho original
        tam_orig = os.path.getsize(caminho_full_origem)
        
        print(f"[{i}/{total_arquivos}] Processando: {nome_arq}...", end="\r")

        # Chama a compressão
        if comprimir_pdf(caminho_full_origem, caminho_full_destino):
            # Calcula estatísticas
            tam_novo = os.path.getsize(caminho_full_destino)
            reducao = (1 - (tam_novo / tam_orig)) * 100
            economia_mb = (tam_orig - tam_novo) / (1024 * 1024)
            economizado_total_mb += economia_mb
            
            # Mostra resultado apenas se valeu a pena (reduziu algo)
            if tam_novo < tam_orig:
                print(f" [OK] {nome_arq} | -{reducao:.1f}% ({economia_mb:.2f} MB a menos)")
            else:
                print(f" [=]  {nome_arq} | Não houve redução significativa.")
            
            sucessos += 1
        else:
            print(f" [FALHA] Não foi possível comprimir {nome_arq}")

    print("-" * 50)
    print(">>> PROCESSO FINALIZADO <<<")
    print(f"Arquivos processados: {sucessos}/{total_arquivos}")
    print(f"Espaço total economizado: {economizado_total_mb:.2f} MB")
    print(f"Verifique a pasta: {PASTA_DESTINO}")