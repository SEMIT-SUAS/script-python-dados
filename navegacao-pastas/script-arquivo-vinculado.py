import os
import csv
# from tika import parser  # pip install tika
import uuid
import hashlib
import shutil

def calcular_md5(caminho):
    hash_md5 = hashlib.md5()
    with open(caminho, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

ROOT = r"/home/suas/Arquivos-SEMAD/Diario/arquivos_full"
OUTPUT_SQL = "extracao-arquivo.sql"
EXT_WHITE = {".pdf"}

os.makedirs("/home/suas/Arquivos-SEMAD/Diario/arquivos_full", exist_ok=True)

with open(OUTPUT_SQL, "w", newline="", encoding="utf-8") as f:
    f.write("-- INSERTS para tabela de arquivos\n\n")
    # writer = csv.writer(f)
    # writer.writerow(["nome_arquivo","path_arquivo","tipo_mime","tamanho_bytes","hash_md5","ocr_status","conteudo_ocr","chave_lote"])

    contador = 0

    for ano in sorted(os.listdir(ROOT), key=int):  # 🔥 ordena anos corretamente
        caminho_ano = os.path.join(ROOT, ano)

        if not os.path.isdir(caminho_ano) or not ano.isdigit():
            continue

        for dirpath, dirnames, filenames in os.walk(caminho_ano):
            dirnames.sort()     # 🔥 ordena subpastas
            filenames.sort()    # 🔥 ordena arquivos

            for name in filenames:
                ext = os.path.splitext(name)[1].lower()

                if ext not in EXT_WHITE:
                    continue  # 🔥 IGNORA NÃO PDF

                contador += 1
                chave_lote = "L" + str(contador)

                nome_arquivo = name
                meu_uuid = str(uuid.uuid4())
                path_arquivo = r"/home/suas/Arquivo-digital-inteligente/uploads/" + meu_uuid + "_" + name
                path = os.path.join(dirpath, name)

                ext = os.path.splitext(name)[1].lower()

                import mimetypes
                tipo_mime = mimetypes.guess_type(path)[0] or "application/octet-stream"

                tamanho_bytes = os.path.getsize(path)
                hash_md5 = calcular_md5(path)
                ocr_status = "false"
                conteudo_ocr = "OCR pendente para processamento posterior"

                try:
                    os.makedirs(os.path.dirname(path_arquivo), exist_ok=True)
                    shutil.copy2(path, path_arquivo)
                except Exception as e:
                    print(f"Erro ao copiar arquivo {name}: {e}")
                    continue
                try:
                    # Escape de aspas simples para PostgreSQL
                    nome_arquivo_escaped = nome_arquivo.replace("'", "''")
                    path_arquivo_escaped = path_arquivo.replace("'", "''")
                    tipo_mime_escaped = tipo_mime.replace("'", "''")
                    hash_md5_escaped = hash_md5.replace("'", "''")
                    ocr_status_escaped = ocr_status.replace("'", "''")
                    conteudo_ocr_escaped = conteudo_ocr.replace("'", "''")
                    chave_lote_escaped = chave_lote.replace("'", "''")
                    
                    insert_sql = f"""INSERT INTO arquivos_digitais (nome_arquivo, path_arquivo, tipo_mime, tamanho_bytes, hash_md5, ocr_status, conteudo_ocr, chave_lote) 
                    VALUES ('{nome_arquivo_escaped}', '{path_arquivo_escaped}', '{tipo_mime_escaped}', {tamanho_bytes}, '{hash_md5_escaped}', '{ocr_status_escaped}', '{conteudo_ocr_escaped}', '{chave_lote_escaped}');\n"""
                    
                    f.write(insert_sql)
                    
                except Exception as e:
                    # Em caso de erro, ainda gera o INSERT com informações básicas
                    nome_arquivo_escaped = nome_arquivo.replace("'", "''") if nome_arquivo else ''
                    path_arquivo_escaped = path_arquivo.replace("'", "''") if path_arquivo else ''
                    tipo_mime_escaped = tipo_mime.replace("'", "''") if tipo_mime else ''
                    hash_md5_escaped = hash_md5.replace("'", "''") if hash_md5 else ''
                    ocr_status_escaped = ocr_status.replace("'", "''") if ocr_status else ''
                    conteudo_ocr_escaped = f"ERROR: {str(e)}".replace("'", "''")
                    chave_lote_escaped = chave_lote.replace("'", "''") if chave_lote else ''
                    
                    insert_sql = f"""INSERT INTO arquivos_digitais (nome_arquivo, path_arquivo, tipo_mime, tamanho_bytes, hash_md5, ocr_status, conteudo_ocr, chave_lote) 
                    VALUES ('{nome_arquivo_escaped}', '{path_arquivo_escaped}', '{tipo_mime_escaped}', {tamanho_bytes}, '{hash_md5_escaped}', '{ocr_status_escaped}', '{conteudo_ocr_escaped}', '{chave_lote_escaped}');\n"""
                    
                    f.write(insert_sql)

print("Pronto — resultados salvos em", OUTPUT_SQL)
