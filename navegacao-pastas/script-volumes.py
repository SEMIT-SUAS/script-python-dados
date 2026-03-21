import os
import re
from PyPDF2 import PdfReader

ROOT = r"/home/suas/Arquivos-SEMAD/Diario/arquivos_full"
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

    # 🔥 padrão específico do seu arquivo
    match = re.search(r'dom-\d{4}-(\d+)', nome_lower)
    if match:
        return match.group(1).zfill(3)

    # fallback (caso não siga padrão)
    match = re.search(r'(\d+)', nome_lower)
    if match:
        return match.group(1)

    return "000"

# Função para extrair data de dentro do PDF
def extrair_data_pdf(caminho_pdf):
    try:
        reader = PdfReader(caminho_pdf)

        if len(reader.pages) == 0:
            return None

        # 🔥 PEGA SÓ A PRIMEIRA PÁGINA
        texto = reader.pages[0].extract_text() or ""

        if not texto.strip():
            return None

        patterns = [
            r'(\d{1,2})[\/\-](\d{1,2})[\/\-](\d{4})',
            r'(\d{1,2}) de (\w+) de (\d{4})'
        ]

        meses = {
            'janeiro':'01','fevereiro':'02','março':'03','marco':'03','abril':'04',
            'maio':'05','junho':'06','julho':'07','agosto':'08',
            'setembro':'09','outubro':'10','novembro':'11','dezembro':'12'
        }

        for pattern in patterns:
            match = re.search(pattern, texto, re.IGNORECASE)
            if match:
                d, m, a = match.groups()

                if m.isalpha():
                    m = meses.get(m.lower(), '01')

                return f"{a}-{m.zfill(2)}-{d.zfill(2)}"

        return None

    except Exception as e:
        print(f"Erro lendo PDF {caminho_pdf}: {e}")
        return None

# Script principal
with open(OUTPUT_SQL, "w", encoding="utf-8") as f:
    f.write("-- INSERTS para tabela de volumes\n\n")

    for ano in sorted(os.listdir(ROOT)):
        caminho_ano = os.path.join(ROOT, ano)

        if not os.path.isdir(caminho_ano) or not ano.isdigit():
            continue

        # ✅ AGORA ESTÁ DENTRO
        for name in sorted(os.listdir(caminho_ano)):
            ext = os.path.splitext(name)[1].lower()

            if ext in EXT_WHITE:
                contador += 1
                chave_lote = f"L{contador}"

                numero = extrair_numero_edicao(name)
                caminho_arquivo = os.path.join(caminho_ano, name)

                data_extraida = extrair_data_pdf(caminho_arquivo)
                data_documento = data_extraida if data_extraida else f"{ano}-01-01"

                titulo = f"DIARIO OFICIAL nº {numero} ANO {ano}"

                # IDs padrão
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