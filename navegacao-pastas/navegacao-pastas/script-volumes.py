import os
import csv
from tika import parser  # pip install tika

ROOT = r"C:\Users\marim\OneDrive\Imagens\Documentos\Arquivos Paulo\projetos\DADOS ONEDRIVE"
OUTPUT_CSV = "extracao-volumes.csv"
EXT_WHITE = {".pdf", ".docx", ".txt", ".html", ".md"}

with open(OUTPUT_CSV, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["titulo","data_documento","id_tipo_documental","id_estado_conservacao","id_secretaria","id_discos_servidores","id_pastas_digitais","ativo","opcao_ocr","origem"])# "text_snippet"])

    for dirpath, dirnames, filenames in os.walk(ROOT):
        print(dirpath, dirnames, filenames)  # debug opcional

        for name in filenames:
            path = os.path.join(dirpath, name)
            ext = os.path.splitext(name)[1].lower()

            # PROCESSO = 9,
            # DOSSIÊ = 12, 
            # OFICÍO = 13, 
            # DIARIO OFICIAL = 14, 
            # MEMORANDO = 15 

            if ext in EXT_WHITE:
                # Detecta se a pasta atual ou alguma acima é "DOSSIÊS"
                if "DOSSI" in dirpath.upper():
                    titulo = f"Dossiês - {name}"
                    id_tipo_documental = 12
                elif "PROCESSOS" in dirpath.upper():
                    titulo = f"Processos - {name}"
                    id_tipo_documental = 9
                elif "OFICIO" in dirpath.upper():
                    titulo = f"Ofício - {name}"
                    id_tipo_documental = 13
                elif "DIARIO OFICIAL" in dirpath.upper():
                    titulo = f"Diário Oficial - {name}"
                    id_tipo_documental = 14
                elif "MEMORANDO" in dirpath.upper():
                    titulo = f"Memorando - {name}"
                    id_tipo_documental = 15
                else:
                    titulo = name  # ou "Outro - {name}" se quiser deixar explícito

                    #ORG: TITULO, DATA DOCUMENTO, ID_TIPO_DOCUMENTAL, ID_ESTADO_CONSERVACAO,
                    #ID_SECRETARIA, id_discos_servidores,
                    #id_pastas_digitais, ATIVO, OPCAO_OCR,
                    #ORIGEM

                #Data documento 
                data_documento = "2025-11-10"
                id_estado_conservacao = 8
                id_secretaria = 37
                id_discos_servidores = 25
                id_pastas_digitais = 14
                ativo = "true"
                opcao_ocr = "false"
                origem = "Digitalizado"

                try:
                    parsed = parser.from_file(path)
                    text = parsed.get("content") or ""
                    snippet = text.strip().replace("\n", " ")[:1000]
                    writer.writerow([titulo,data_documento,id_tipo_documental,id_estado_conservacao,id_secretaria,id_discos_servidores,id_pastas_digitais,ativo,opcao_ocr,origem])# snippet])
                except Exception as e:
                    writer.writerow([titulo,data_documento,id_tipo_documental,id_estado_conservacao,id_secretaria,id_discos_servidores,id_pastas_digitais,ativo,opcao_ocr,origem, f"ERROR: {e}"])

print("Pronto — resultados salvos em", OUTPUT_CSV)
