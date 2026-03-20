import os
import re
from PyPDF2 import PdfReader

ROOT = r"C:/Users/Administrador/Documents/Paulo/Arquivos-SEMAD/Diario/arquivos_full"
OUTPUT_SQL = "extracao-volumes.sql"
EXT_WHITE = {".pdf"}

contador = 0

# Função para converter romano para inteiro
def romano_para_int(romano):
    valores = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100}
    total = 0
    prev = 0
    for letra in reversed(romano.upper()):
        valor = valores.get(letra, 0)
        if valor < prev:
            total -= valor
        else:
            total += valor
        prev = valor
    return total

# Função para extrair número da edição do nome do PDF
def extrair_numero_edicao(nome):
    nome_lower = nome.lower()

    patterns = [
        r'edica[oõ]?-?\s*(\d+)',  # edicao-123 ou edicao 123
        r'n[ºo]\s*(\d+)',         # n° 123 ou no 123
        r'numero\s*(\d+)',        # numero 123
        r'(\d+)'                   # último recurso: qualquer número
    ]

    for pattern in patterns:
        match = re.search(pattern, nome_lower)
        if match:
            return match.group(1)

    return "0"

# Função para extrair data de dentro do PDF
def extrair_data_pdf(caminho_pdf):
    try:
        reader = PdfReader(caminho_pdf)
        texto = ""
        for page in reader.pages:
            texto += page.extract_text() or ""

        # Regex para datas numéricas ou por extenso
        patterns = [
            r'(\d{1,2})[\/\-](\d{1,2})[\/\-](\d{4})',                  # dd/mm/yyyy ou dd-mm-yyyy
            r'(\d{1,2}) de (\w+) de (\d{4})'                          # 10 de março de 2023
        ]

        meses = {
            'janeiro':'01','fevereiro':'02','março':'03','marco':'03','abril':'04','maio':'05','junho':'06',
            'julho':'07','agosto':'08','setembro':'09','outubro':'10','novembro':'11','dezembro':'12'
        }

        for pattern in patterns:
            match = re.search(pattern, texto, re.IGNORECASE)
            if match:
                if len(match.groups()) == 3:
                    d, m, a = match.groups()
                    if m.isalpha():
                        m = meses.get(m.lower(), '01')
                    dia = d.zfill(2)
                    mes = m.zfill(2)
                    return f"{a}-{mes}-{dia}"

        return None
    except Exception as e:
        print(f"Erro lendo PDF {caminho_pdf}: {e}")
        return None

# Script principal
with open(OUTPUT_SQL, "w", encoding="utf-8") as f:
    f.write("-- INSERTS para tabela de volumes\n\n")

    for dirpath, dirnames, filenames in os.walk(ROOT):
        ano_pasta = os.path.basename(dirpath)
        if not ano_pasta.isdigit():
            continue  # pula pastas que não são anos

        for name in filenames:
            ext = os.path.splitext(name)[1].lower()
            if ext in EXT_WHITE:
                contador += 1
                chave_lote = f"L{contador}"

                numero = extrair_numero_edicao(name)
                caminho_arquivo = os.path.join(dirpath, name)

                data_extraida = extrair_data_pdf(caminho_arquivo)
                data_documento = data_extraida if data_extraida else f"{ano_pasta}-01-01"

                titulo = f"DIARIO OFICIAL nº {numero} ANO {ano_pasta}"

                # IDs padrão conforme solicitado
                id_tipo_documental = 7
                id_estado_conservacao = 6
                id_secretaria = 1
                id_discos_servidores = 23
                id_pastas_digitais = 13
                ativo = True
                opcao_ocr = False
                origem = "Digitalizado"

                titulo_escaped = titulo.replace("'", "''")

                insert_sql = f"""INSERT INTO volumes 
(titulo, data_documento, id_tipo_documental, id_estado_conservacao, id_secretaria, id_discos_servidores, id_pastas_digitais, ativo, opcao_ocr, origem, chave_lote)
VALUES ('{titulo_escaped}', '{data_documento}', {id_tipo_documental}, {id_estado_conservacao}, {id_secretaria}, {id_discos_servidores}, {id_pastas_digitais}, {str(ativo).lower()}, {str(opcao_ocr).lower()}, '{origem}', '{chave_lote}');\n"""

                f.write(insert_sql)

print("Pronto — resultados salvos em", OUTPUT_SQL)