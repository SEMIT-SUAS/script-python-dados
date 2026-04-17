import os
import re
import uuid
import hashlib
import shutil
import mimetypes
import psycopg2
from datetime import date

# ==============================================================================
# CONFIGURAÇÕES DE CAMINHOS
# ==============================================================================
DIRETORIO_ORIGEM   = os.path.join("test", "assets", "drive_d", "PROCESSOS 2021")
DIRETORIO_DESTINO  = os.path.join("test", "assets", "uploads")
ARQUIVO_SQL        = os.path.join("test", "database", "seeders", "registro_processos_2021.sql")
ARQUIVO_IGNORADOS  = os.path.join("test", "logs", "arquivos_ignorados_2021.txt")

PATH_BASE_BANCO = "/home/suas/Arquivo-digital-inteligente/uploads"

# Configurações do Banco de Dados Local (para continuidade da chave_lote)
DB_CONFIG = {
    "host": "localhost",
    "port": 5435,
    "user": "postgres",
    "password": "postgres",
    "dbname": "db_adi_test"
}

# ==============================================================================
# CONFIGURAÇÕES DE PRODUÇÃO (Auditadas)
# ==============================================================================
ID_ESTADO_CONSERVACAO  = 6
ID_DISCO_SERVIDOR      = 23
ID_PASTA_DIGITAL       = 13
ID_TIPO_PROCESSO       = 1
ID_TIPO_DIARIO         = 7

TEXTO_OCR_PENDENTE = "OCR pendente para processamento posterior"
ORIGEM_CARGA = "Digitalizado"
OPCAO_OCR_PADRAO = "false"

# ==============================================================================
# REGEX v3.0: Ultra Flexível (Captura Nº, PROCESSO, espaços variados)
# ==============================================================================
PADRAO_NOME = re.compile(
    r"06[\.\s]*00\s*-?\s*(.*?)\s*(?:N[ºº]|N\.?\s*E\.?|NE|PROCESSO DE .*? Nº|PROCESSO Nº|PROC[A-Z\.]*|PORCESSO)\s*(.*?)\.pdf",
    re.IGNORECASE
)

# ==============================================================================
# FUNÇÕES
# ==============================================================================

def obter_ultimo_index_lote() -> int:
    """Consulta o banco de dados para encontrar o último index de chave_lote (ex: L20 -> 20)."""
    print("[*] Verificando estado atual do banco para continuidade de lote...")
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        # Busca o maior valor numérico após o 'L' na chave_lote
        cur.execute("SELECT chave_lote FROM volumes WHERE chave_lote LIKE 'L%'")
        rows = cur.fetchall()
        
        max_idx = 0
        for (lote,) in rows:
            try:
                # Extrai apenas os números após o 'L' usando regex
                match = re.search(r'L(\d+)', lote)
                if match:
                    idx = int(match.group(1))
                    if idx > max_idx:
                        max_idx = idx
            except:
                continue
                
        cur.close()
        conn.close()
        
        if max_idx > 0:
            print(f"[+] Último lote detectado: L{max_idx}. Iniciando a partir de L{max_idx + 1}.")
        else:
            print("[!] Nenhum lote prévio detectado ou banco vazio. Iniciando de L1.")
        return max_idx
    except Exception as e:
        print(f"[!] Aviso: Não foi possível conectar ao banco local ({e}). Iniciando de L1.")
        return 0

def calcular_hash_md5(caminho_arquivo: str) -> str:
    if os.path.getsize(caminho_arquivo) == 0:
        return hashlib.md5(os.path.basename(caminho_arquivo).encode()).hexdigest()
    hash_md5 = hashlib.md5()
    with open(caminho_arquivo, "rb") as f:
        for bloco in iter(lambda: f.read(4096), b""):
            hash_md5.update(bloco)
    return hash_md5.hexdigest()

def escapar_sql(valor: str) -> str:
    return str(valor).replace("'", "''") if valor else ""

def montar_bloco_sql(titulo, id_tipo, nome_original, path_banco, tamanho, hash_val, chave_lote, mime_type, nome_secretaria) -> str:
    """Gera bloco SQL com CRIAÇÃO DINÂMICA DE SECRETARIA e Vínculo Duplo."""
    # numero_volume agora é NULL conforme padrão de amostra do banco
    return f"""DO $$
DECLARE v_id_sec INT;
DECLARE v_id_vol INT;
DECLARE v_id_arq INT;
BEGIN
    -- 1. Garante que a secretaria exista (Criação Dinâmica)
    INSERT INTO secretarias (nome_secretaria) 
    VALUES ('{escapar_sql(nome_secretaria)}') 
    ON CONFLICT (nome_secretaria) DO NOTHING;
    
    SELECT id INTO v_id_sec FROM secretarias WHERE nome_secretaria = '{escapar_sql(nome_secretaria)}';

    -- 2. Inserção do Volume (numero_volume fixado como NULL)
    INSERT INTO volumes (
        titulo, numero_volume, data_documento, id_tipo_documental, id_secretaria, id_discos_servidores,
        id_pastas_digitais, id_estado_conservacao, ativo, origem, opcao_ocr, chave_lote
    ) VALUES (
        '{escapar_sql(titulo)}', NULL, '2021-01-01', {id_tipo}, v_id_sec, 
        {ID_DISCO_SERVIDOR}, {ID_PASTA_DIGITAL}, {ID_ESTADO_CONSERVACAO}, true, '{escapar_sql(ORIGEM_CARGA)}', '{OPCAO_OCR_PADRAO}', '{escapar_sql(chave_lote)}'
    ) RETURNING id INTO v_id_vol;

    -- 3. Inserção do Arquivo Digital
    INSERT INTO arquivos_digitais (
        nome_arquivo, path_arquivo, tipo_mime, tamanho_bytes, hash_md5, ocr_status, conteudo_ocr, id_volume, chave_lote
    ) VALUES (
        '{escapar_sql(nome_original)}', '{escapar_sql(path_banco)}', '{escapar_sql(mime_type)}', {tamanho}, '{hash_val}', 
        false, '{escapar_sql(TEXTO_OCR_PENDENTE)}', v_id_vol, '{escapar_sql(chave_lote)}'
    ) RETURNING id INTO v_id_arq;

    -- 4. Vínculo Reverso
    UPDATE volumes SET id_arquivos_digitais = v_id_arq WHERE id = v_id_vol;
END $$;
"""

def processar_lote():
    os.makedirs(DIRETORIO_DESTINO, exist_ok=True)
    os.makedirs(os.path.dirname(ARQUIVO_SQL), exist_ok=True)
    
    print(f"[*] Iniciando Migracao em: {DIRETORIO_ORIGEM}")
    
    # Busca index inicial no banco
    offset_lote = obter_ultimo_index_lote()
    
    todos_arquivos = []
    for root, _, files in os.walk(DIRETORIO_ORIGEM):
        pasta_pai = os.path.basename(root)
        for nome in files:
            if nome.lower().endswith(".pdf"):
                todos_arquivos.append((os.path.join(root, nome), pasta_pai, nome))

    print(f"[*] Total de PDFs encontrados: {len(todos_arquivos)}")

    count_sucesso = 0
    ignorados = []

    with open(ARQUIVO_SQL, "w", encoding="utf-8") as f_sql:
        f_sql.write(f"-- SCRIPT (MOTOR UNIVERSAL) - {date.today()}\n")
        f_sql.write(f"-- Continuidade automatica de Chave Lote ativada.\n\n")

        for i, (caminho, pasta_pai, nome_original) in enumerate(todos_arquivos, 1):
            
            # 💡 IDENTIFICAÇÃO DINÂMICA
            if "diário oficial" in nome_original.lower() or "diario oficial" in nome_original.lower():
                id_tipo = ID_TIPO_DIARIO
                titulo = nome_original.replace(".pdf", "")
                ne_numero = "N/A"
            else:
                id_tipo = ID_TIPO_PROCESSO
                match = PADRAO_NOME.search(nome_original)
                if not match:
                    ignorados.append(f"PADRAO INVALIDO | {pasta_pai} | {nome_original}")
                    continue
                
                categoria_ext, ne_val = match.groups()
                ne_numero = ne_val.strip() if ne_val else "N/A"
                titulo_limpo = categoria_ext.strip().replace("  ", " ")
                titulo = f"[{pasta_pai}] {titulo_limpo} - {ne_numero}"

            # 🛠️ PROCESSAMENTO
            meu_uuid = str(uuid.uuid4())
            hash_val = calcular_hash_md5(caminho)
            tamanho  = os.path.getsize(caminho)
            
            # Cálculo dinâmico da chave_lote baseada no offset do banco
            chave_lote = f"L{offset_lote + i}"
            
            mime_type = mimetypes.guess_type(caminho)[0] or "application/pdf"
            
            novo_nome = f"{meu_uuid}_{nome_original}"
            path_banco = f"{PATH_BASE_BANCO}/{novo_nome}"

            nome_sec = pasta_pai if pasta_pai not in ["DIGITALIZADOS", "PROCESSOS 2021", "D"] else "SEMAD"

            try:
                shutil.copy2(caminho, os.path.join(DIRETORIO_DESTINO, novo_nome))
                sql_block = montar_bloco_sql(titulo, id_tipo, nome_original, path_banco, tamanho, hash_val, chave_lote, mime_type, nome_sec)
                f_sql.write(sql_block + "\n")
                count_sucesso += 1
            except Exception as e:
                ignorados.append(f"ERRO SISTEMA | {nome_original} | {str(e)}")

    # 📝 RELATÓRIO
    if ignorados:
        with open(ARQUIVO_IGNORADOS, "w", encoding="utf-8") as f_log:
            f_log.write(f"RELATORIO DE ARQUIVOS IGNORADOS - {date.today()}\n")
            f_log.write(f"Total de arquivos nao capturados: {len(ignorados)}\n")
            f_log.write("-" * 50 + "\n")
            f_log.write("\n".join(ignorados))

    print(f"\n[+] CONCLUIDO:")
    print(f"   - Capturados: {count_sucesso} (Inciando de L{offset_lote + 1} ate L{offset_lote + count_sucesso})")
    print(f"   - Ignorados: {len(ignorados)} (Ver {ARQUIVO_IGNORADOS})")
    print(f"[*] SQL Universal Pronto: {ARQUIVO_SQL}")

if __name__ == "__main__":
    processar_lote()