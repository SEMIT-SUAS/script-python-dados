import os
import csv
# from tika import parser  # pip install tika
import uuid
import hashlib
import shutil

ROOT = r"/home/docs-onedrive/ARQUIVO SEMAD"
OUTPUT_SQL = "extracao-arquivo.sql"
EXT_WHITE = {".pdf", ".docx", ".txt", ".html", ".md"}

with open(OUTPUT_SQL, "w", newline="", encoding="utf-8") as f:
    f.write("-- INSERTS para tabela de arquivos\n\n")
    # writer = csv.writer(f)
    # writer.writerow(["nome_arquivo","path_arquivo","tipo_mime","tamanho_bytes","hash_md5","ocr_status","conteudo_ocr","chave_lote"])

    sum = 283

    for dirpath, dirnames, filenames in os.walk(ROOT):
        # print(dirpath, dirnames, filenames)  # debug opcional

        for name in filenames:
            # print(dirpath.replace("\\", "/") + "/")  # Mostra o caminho completo do arquivo
            sum+=1
            chave_lote = "L" + str(sum)
            nome_arquivo = name
            meu_uuid = str(uuid.uuid4())
            path_arquivo = "/home/suas/Arquivo-digital-inteligente/uploads/" + meu_uuid + "_" + name
            path = os.path.join(dirpath, name)
            ext = os.path.splitext(name)[1].lower()
            tipo_mime = "application/pdf"  # Exemplo fixo, ajustar conforme necessário
            tamanho_bytes = os.path.getsize(path)
            nome_bytes = nome_arquivo.encode('utf-8')
            hash_md5 = hashlib.md5(nome_bytes).hexdigest()
            ocr_status = "false"
            conteudo_ocr = "OCR pendente para processamento posterior"

            # PROCESSO = 9,
            # DOSSIÊ = 12, 
            # OFICÍO = 13, 
            # DIARIO OFICIAL = 14, 
            # MEMORANDO = 15 

            # if ext in EXT_WHITE:
            #     # Detecta se a pasta atual ou alguma acima é "DOSSIÊS"
            #     if "DOSSI" in dirpath.upper():
            #         titulo = f"Dossiês - {name}"
            #         id_tipo_documental = 12
            #     elif "PROCESSOS" in dirpath.upper():
            #         titulo = f"Processos - {name}"
            #         id_tipo_documental = 9
            #     elif "OFICIO" in dirpath.upper():
            #         titulo = f"Ofício - {name}"
            #         id_tipo_documental = 13
            #     elif "DIARIO OFICIAL" in dirpath.upper():
            #         titulo = f"Diário Oficial - {name}"
            #         id_tipo_documental = 14
            #     elif "MEMORANDO" in dirpath.upper():
            #         titulo = f"Memorando - {name}"
            #         id_tipo_documental = 15
            #     else:
            #         titulo = name  # ou "Outro - {name}" se quiser deixar explícito

                    #ORG: TITULO, DATA DOCUMENTO, ID_TIPO_DOCUMENTAL, ID_ESTADO_CONSERVACAO,
                    #ID_SECRETARIA, ID_DISCO_SERVIDOR,
                    #ID_OBSERVACAO_PASTA, ATIVO, OPCAO_OCR,
                    #ORIGEM

            try:
                os.rename(dirpath.replace("\\", "/") + "/" + name, 'home/suas/Arquivo-digital-inteligente/' + path_arquivo)
            except Exception as e:
                print(f"Erro ao mover arquivo {name}: {e}")
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
