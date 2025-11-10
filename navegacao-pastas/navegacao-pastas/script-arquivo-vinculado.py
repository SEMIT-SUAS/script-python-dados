import os
import csv
from tika import parser  # pip install tika
import uuid
import hashlib

ROOT = r"C:\Users\marim\OneDrive\Imagens\Documentos\Arquivos Paulo\projetos\DADOS ONEDRIVE"
OUTPUT_CSV = "extracao-arquivo.csv"
EXT_WHITE = {".pdf", ".docx", ".txt", ".html", ".md"}

with open(OUTPUT_CSV, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["nome_arquivo","path_arquivo","tipo_mime","tamanho_bytes","hash_md5","ocr_status","conteudo_ocr"])

    for dirpath, dirnames, filenames in os.walk(ROOT):
        print(dirpath, dirnames, filenames)  # debug opcional

        for name in filenames:
            nome_arquivo = name
            meu_uuid = str(uuid.uuid4())
            path_arquivo = "uploads/" + meu_uuid + "_" + name
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
                # parsed = parser.from_file(path)
                # text = parsed.get("content") or ""
                # snippet = text.strip().replace("\n", " ")[:1000]
                writer.writerow([nome_arquivo,path_arquivo,tipo_mime,tamanho_bytes,hash_md5,ocr_status,conteudo_ocr])
            except Exception as e:
                writer.writerow([nome_arquivo,path_arquivo,tipo_mime,tamanho_bytes,hash_md5,ocr_status,conteudo_ocr, f"ERROR: {e}"])

print("Pronto — resultados salvos em", OUTPUT_CSV)
