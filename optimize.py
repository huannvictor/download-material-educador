import time
import os
import subprocess
import concurrent.futures
from concurrent.futures import ProcessPoolExecutor

# --- CONFIGURAÇÕES ---
PASTA_DOWNLOAD = os.path.join(os.getcwd(), "manuais_pdfs")
PASTA_DESTINO_OTIMIZACAO = os.path.join(os.getcwd(), "manuais_otimizados")
# Caminho corrigido conforme sua instalação (10.06.0)
CAMINHO_GHOSTSCRIPT = r"C:\Program Files\gs\gs10.06.0\bin\gswin64c.exe"
MODO_COMPRESSAO = "/ebook"
# Usa o número de processadores disponíveis para máxima performance
MAX_WORKERS = os.cpu_count()

os.makedirs(PASTA_DOWNLOAD, exist_ok=True)
os.makedirs(PASTA_DESTINO_OTIMIZACAO, exist_ok=True)

def comprimir_pdf(caminhos):
    """
    Função que executa a compressão de um único arquivo.
    Recebe uma tupla (caminho_entrada, caminho_saida).
    """
    entrada, saida = caminhos
    try:
        tam_orig = os.path.getsize(entrada)
        cmd = [
            CAMINHO_GHOSTSCRIPT, "-sDEVICE=pdfwrite", "-dCompatibilityLevel=1.4",
            f"-dPDFSETTINGS={MODO_COMPRESSAO}", "-dNOPAUSE", "-dQUIET", "-dBATCH",
            f"-sOutputFile={saida}", entrada
        ]
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        tam_novo = os.path.getsize(saida)
        economia_mb = (tam_orig - tam_novo) / (1024 * 1024)
        reducao_pct = (1 - (tam_novo / tam_orig)) * 100 if tam_orig > 0 else 0
        
        return {
            "sucesso": True,
            "nome": os.path.basename(entrada),
            "economia_mb": economia_mb,
            "reducao_pct": reducao_pct
        }
    except Exception as e:
        return {"sucesso": False, "nome": os.path.basename(entrada), "erro": str(e)}

if __name__ == "__main__":
    print("\n>>> INICIANDO OTIMIZADOR DE PDFS (MODO PARALELO) <<<")
    print(f"Origem:  {PASTA_DOWNLOAD}")
    print(f"Destino: {PASTA_DESTINO_OTIMIZACAO}")
    print(f"Workers: {MAX_WORKERS} (Processamento simultâneo)")
    print("-" * 60)

    if not os.path.exists(CAMINHO_GHOSTSCRIPT):
        print(f"X ERRO CRÍTICO: Ghostscript não encontrado em: {CAMINHO_GHOSTSCRIPT}")
        exit()

    arquivos = [f for f in os.listdir(PASTA_DOWNLOAD) if f.lower().endswith('.pdf')]
    
    if not arquivos:
        print("Nenhum arquivo PDF encontrado para processar.")
    else:
        tarefas = []
        for nome in arquivos:
            tarefas.append((
                os.path.join(PASTA_DOWNLOAD, nome),
                os.path.join(PASTA_DESTINO_OTIMIZACAO, nome)
            ))

        sucessos = 0
        total_economizado = 0

        # O Image do fluxo de threads ajudaria a visualizar como os 4 workers pegam os arquivos da fila.
        # 
        with ProcessPoolExecutor(max_workers=MAX_WORKERS) as executor:
            futuros = [executor.submit(comprimir_pdf, t) for t in tarefas]
            
            for i, futuro in enumerate(concurrent.futures.as_completed(futuros), 1):
                res = futuro.result()
                if res["sucesso"]:
                    sucessos += 1
                    total_economizado += max(0, res["economia_mb"])
                    status = f"{res['reducao_pct']:.1f}% menor" if res['economia_mb'] > 0 else "Sem redução"
                    print(f"[{i}/{len(arquivos)}] [OK] {res['nome']} | {status}")
                else:
                    print(f"[{i}/{len(arquivos)}] [FALHA] {res['nome']} | Erro: {res['erro']}")

        print("-" * 60)
        print(">>> RESUMO FINAL <<<")
        print(f"Arquivos processados: {sucessos}/{len(arquivos)}")
        print(f"Espaço total liberado: {total_economizado:.2f} MB")
        print(f"Local: {PASTA_DESTINO_OTIMIZACAO}")