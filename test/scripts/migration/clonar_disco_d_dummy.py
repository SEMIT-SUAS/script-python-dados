import os
import shutil

# CONFIGURAÇÕES
# Vamos apontar para a raiz do D: para pegar as pastas principais
ORIGEM_RAIZ = "D:\\"
PASTAS_PARA_CLONAR = ["PROCESSOS 2021", "HD"]
DESTINO_BASE = os.path.join("test", "assets", "drive_d")

def clonar_estrutura_dummy():
    if not os.path.exists(ORIGEM_RAIZ):
        print(f"Erro: Origem {ORIGEM_RAIZ} não encontrada.")
        return

    # Limpeza da pasta de destino para garantir um ambiente "fresco"
    if os.path.exists(DESTINO_BASE):
        print(f"[*] Limpando ambiente anterior em: {DESTINO_BASE}")
        shutil.rmtree(DESTINO_BASE)

    print(f"[*] Iniciando espelhamento de estrutura completa: {PASTAS_PARA_CLONAR}")
    
    total_pastas = 0
    total_arquivos = 0

    for nome_pasta in PASTAS_PARA_CLONAR:
        caminho_origem = os.path.join(ORIGEM_RAIZ, nome_pasta)
        if not os.path.exists(caminho_origem):
            print(f"[!] Pasta nao encontrada: {caminho_origem}")
            continue

        print(f"[*] Processando: {nome_pasta}...")
        for root, dirs, files in os.walk(caminho_origem):
            rel_path = os.path.relpath(root, ORIGEM_RAIZ)
            pasta_destino = os.path.join(DESTINO_BASE, rel_path)

            if not os.path.exists(pasta_destino):
                os.makedirs(pasta_destino)
                total_pastas += 1

            pdf_count_na_pasta = 0
            for name in files:
                if name.lower().endswith(".pdf"):
                    caminho_arquivo = os.path.join(pasta_destino, name)
                    with open(caminho_arquivo, "w") as f:
                        pass
                    total_arquivos += 1
                    pdf_count_na_pasta += 1
            
            if pdf_count_na_pasta > 0:
                print(f"  [+] {rel_path}: {pdf_count_na_pasta} arquivos")

    print("\n" + "="*50)
    print("RESUMO DO ESPELHAMENTO")
    print("="*50)
    print(f"Pastas criadas: {total_pastas}")
    print(f"Arquivos dummy (0kb) criados: {total_arquivos}")
    print(f"Local: {os.path.abspath(DESTINO_BASE)}")
    print("="*50)

if __name__ == "__main__":
    clonar_estrutura_dummy()
