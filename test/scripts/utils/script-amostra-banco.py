import psycopg2
from psycopg2 import sql
import os
import uuid
import sys
import shutil

# CONFIGURAÇÃO DE LOGS
LOG_FILE = os.path.join("test", "logs", "logs.txt")

def log(mensagem):
    try:
        print(mensagem)
    except UnicodeEncodeError:
        # Fallback para console Windows
        print(str(mensagem).encode('ascii', 'replace').decode('ascii'))
        
    con_msg = str(mensagem)
    # A primeira mensagem da execução (que contém 'Iniciando' ou 'SMART') limpa o arquivo
    mode = "w" if "SMART REFERENTIAL" in con_msg or "[*] Limpando arquivos" in con_msg else "a"
    with open(LOG_FILE, mode, encoding="utf-8") as f:
        f.write(con_msg + "\n")

# CONFIGURAÇÕES DE CONEXÃO
DB_ORIGEM = {
    "host": "10.0.0.53",
    "port": 5432,
    "database": "adi",
    "user": "postgres",
    "password": "Su4s_!@#"
}

DB_DESTINO = {
    "host": "localhost",
    "port": 5435,
    "database": "db_adi_test",
    "user": "postgres",
    "password": "postgres"
}

LIMITE_SEMENTE = 20
ESQUEMA = "public"
ARQUIVO_DDL = os.path.join("test", "database", "dumps", "dll.sql")
UPLOADS_DIR = os.path.join("test", "assets", "uploads")

def encontrar_arquivo_ddl():
    paths = [
        ARQUIVO_DDL, 
        os.path.join("..", ARQUIVO_DDL), 
        os.path.join("test", ARQUIVO_DDL),
        os.path.join("..", "..", ARQUIVO_DDL)
    ]
    for p in paths:
        if os.path.exists(p): return p
    return None

def mapear_fks(cur):
    query = """
    SELECT
        kcu.table_name, 
        kcu.column_name, 
        ccu.table_name AS foreign_table
    FROM information_schema.table_constraints AS tc 
    JOIN information_schema.key_column_usage AS kcu ON tc.constraint_name = kcu.constraint_name AND tc.table_schema = kcu.table_schema
    JOIN information_schema.constraint_column_usage AS ccu ON ccu.constraint_name = tc.constraint_name AND ccu.table_schema = tc.table_schema
    WHERE tc.constraint_type = 'FOREIGN KEY' AND tc.table_schema = %s
    """
    cur.execute(query, (ESQUEMA,))
    relacoes = {}
    for row in cur.fetchall():
        tab, col, f_tab = row
        if tab not in relacoes: relacoes[tab] = {}
        relacoes[tab][col] = f_tab
    return relacoes

def buscar_pk(cur, tabela):
    cur.execute("""
        SELECT kcu.column_name
        FROM information_schema.table_constraints tc
        JOIN information_schema.key_column_usage kcu ON tc.constraint_name = kcu.constraint_name
        WHERE tc.constraint_type = 'PRIMARY KEY' 
          AND tc.table_name = %s 
          AND tc.table_schema = %s
    """, (tabela, ESQUEMA))
    row = cur.fetchone()
    return row[0] if row else 'id'

def executar_ddl_no_destino(conn):
    path = encontrar_arquivo_ddl()
    if not path: return False
    # Usamos encoding='utf-8-sig' para lidar com possível BOM (Byte Order Mark automaticamente
    with open(path, "r", encoding="utf-8-sig") as f:
        ddl_content = f.read()
    
    # PASSO 1: Limpeza seletiva de arquivos de teste (Preservando .gitkeep)
    if os.path.exists(UPLOADS_DIR):
        log(f"[*] Limpando arquivos de upload anteriores em {UPLOADS_DIR}...")
        for item in os.listdir(UPLOADS_DIR):
            if item == ".gitkeep": continue
            item_path = os.path.join(UPLOADS_DIR, item)
            try:
                if os.path.isfile(item_path): os.remove(item_path)
                elif os.path.isdir(item_path): shutil.rmtree(item_path)
            except Exception as e:
                log(f"  [!] Erro ao remover {item}: {e}")
    
    old_autocommit = conn.autocommit
    try:
        conn.autocommit = True
        cur = conn.cursor()
        log("[*] Aplicando estrutura no Docker...")
        cur.execute("DROP SCHEMA IF EXISTS public CASCADE; CREATE SCHEMA public;")
        cur.execute(ddl_content)
        return True
    except Exception as e:
        log(f"Erro no DDL: {e}")
        return False
    finally:
        if conn:
            conn.autocommit = old_autocommit

def sincronizar_sequences(cur_origem, cur_destino, tabela):
    cur_origem.execute("""
        SELECT column_name FROM information_schema.columns 
        WHERE table_schema = 'public' AND table_name = %s AND column_default LIKE 'nextval%%'
    """, (tabela,))
    for col in [r[0] for r in cur_origem.fetchall()]:
        cur_origem.execute("SELECT pg_get_serial_sequence(%s, %s)", (tabela, col))
        row = cur_origem.fetchone()
        if row and row[0]:
            seq_name = row[0]
            cur_origem.execute(sql.SQL("SELECT last_value FROM {}").format(sql.Identifier(*seq_name.split("."))))
            val = cur_origem.fetchone()[0]
            cur_destino.execute(sql.SQL("SELECT setval({}, %s)").format(sql.Literal(seq_name)), (val,))

def upsert_registros(cur_origem, cur_destino, tabela, ids, fks, cache, profundidade=0):
    if not ids or profundidade > 6: return 
    
    if tabela not in cache: cache[tabela] = set()
    ids_novos = [i for i in ids if i not in cache[tabela]]
    if not ids_novos: return
    
    # Nome único de savepoint para evitar colisões em recursão profunda
    sp_name = f"sp_{tabela}_{uuid.uuid4().hex[:8]}"
    cur_destino.execute(sql.SQL("SAVEPOINT {}").format(sql.Identifier(sp_name)))
    
    try:
        pk_col = buscar_pk(cur_origem, tabela)
        cur_origem.execute(
            sql.SQL("SELECT * FROM {} WHERE {} IN %s").format(sql.Identifier(tabela), sql.Identifier(pk_col)),
            (tuple(ids_novos),)
        )
        colunas = [desc[0] for desc in cur_origem.description]
        rows = cur_origem.fetchall()
        if not rows: 
            cur_destino.execute(sql.SQL("RELEASE SAVEPOINT {}").format(sql.Identifier(sp_name)))
            return
        
        # Resolve dependências (PAIS) primeiro
        tabela_fks = fks.get(tabela, {})
        for row in rows:
            for i, col in enumerate(colunas):
                if col in tabela_fks and row[i] is not None:
                    upsert_registros(cur_origem, cur_destino, tabela_fks[col], [row[i]], fks, cache, profundidade + 1)

        # Insere após os pais existirem
        log(f"{'  ' * profundidade}└─ {tabela}: +{len(rows)} registro(s)")
        query_insert = sql.SQL("INSERT INTO {} ({}) VALUES ({}) ON CONFLICT ({}) DO NOTHING").format(
            sql.Identifier(tabela),
            sql.SQL(", ").join(map(sql.Identifier, colunas)),
            sql.SQL(", ").join(sql.Placeholder() * len(colunas)),
            sql.Identifier(pk_col)
        )
        for row in rows:
            cur_destino.execute(query_insert, row)
            idx_pk = colunas.index(pk_col)
            cache[tabela].add(row[idx_pk])
        
        cur_destino.execute(sql.SQL("RELEASE SAVEPOINT {}").format(sql.Identifier(sp_name)))
            
    except Exception as e:
        cur_destino.execute(sql.SQL("ROLLBACK TO SAVEPOINT {}").format(sql.Identifier(sp_name)))
        log(f"Erro ignorado em '{tabela}': {e}")

def clonar_inteligente():
    conn_origem = None
    conn_destino = None
    cache_local = {} 

    try:
        conn_destino = psycopg2.connect(**DB_DESTINO)
        if not executar_ddl_no_destino(conn_destino): return
        
        log("\n" + "="*60)
        log("SMART REFERENTIAL SAMPLER: PRODUCAO -> DOCKER")
        log("="*60)
        
        cur_destino = conn_destino.cursor()
        cur_destino.execute("SET session_replication_role = 'replica';")

        conn_origem = psycopg2.connect(**DB_ORIGEM)
        conn_origem.set_session(readonly=True, autocommit=True)
        cur_origem = conn_origem.cursor()

        # ======================================================================
        # PASSO 0: AUDITORIA DINÂMICA NA PRODUÇÃO (Extração de IDs Reais)
        # ======================================================================
        log("\n[*] Auditando produção para encontrar IDs vitais...")
        
        # 1. Busca IDs de tipos documentais de forma resiliente (Baseado no pesquisar_tipos_prod.py)
        cur_origem.execute("SELECT id, tipo_documento FROM tipos_documentais")
        all_types = {row[1].upper(): row[0] for row in cur_origem.fetchall()}
        
        # Filtra IDs que contenham as palavras-chave (independente de acento ou plural)
        ids_processo = [v for k, v in all_types.items() if 'PROCESSO' in k]
        ids_diario = [v for k, v in all_types.items() if 'DIARIO' in k or 'DIÁRIO' in k]

        # 2. Busca amostra representativa de IDs técnicos de volumes reais
        cur_origem.execute("SELECT id_discos_servidores, id_pastas_digitais, id_estado_conservacao FROM volumes WHERE id_secretaria IS NOT NULL LIMIT 10")
        rows_vol = cur_origem.fetchall()
        
        id_discos  = list({r[0] for r in rows_vol if r[0]})
        id_pastas  = list({r[1] for r in rows_vol if r[1]})
        id_estados = list({r[2] for r in rows_vol if r[2]})

        fks = mapear_fks(cur_origem)
        
        # Consolida os IDs encontrados
        IDS_VIT_MIGRACAO = {
            "estados_conservacao": id_estados,
            "discos_servidores": id_discos,
            "pastas_digitais": id_pastas,
            "tipos_documentais": ids_processo + ids_diario
        }

        log("\n[*] Resultados da Auditoria (High-Fidelity):")
        log(f"  - IDs Processos/Diários: {ids_processo + ids_diario}")
        log(f"  - IDs Discos: {id_discos}")
        log(f"  - IDs Pastas: {id_pastas}")
        log(f"  - IDs Estados: {id_estados}")

        # ======================================================================
        # PASSO 1: GARANTIA DE ALTA FIDELIDADE
        # ======================================================================
        log("\n[*] Garantindo IDs vitais da Produção (Alta Fidelidade)...")
        for tab_vit, ids_vit in IDS_VIT_MIGRACAO.items():
            if not ids_vit:
                log(f"[!] AVISO: {tab_vit} — Nenhum ID vital foi encontrado na auditoria!")
                continue
            
            upsert_registros(cur_origem, cur_destino, tab_vit, ids_vit, fks, cache_local)
            
            # Validação sugerida pelo usuário
            inseridos = len(cache_local.get(tab_vit, set()))
            if inseridos < len(ids_vit):
                log(f"[!] AVISO: {tab_vit} — esperado {len(ids_vit)} ID(s) vital(is), inserido(s) {inseridos}")

        # ======================================================================
        # PASSO 2: AMOSTRAGEM REFERENCIAL GENERICA
        # ======================================================================
        sementes = ["volumes", "servidores", "usuarios"]
        
        log("\n[*] Iniciando amostragem genérica complementar...")

        for sem in sementes:
            pk_sem = buscar_pk(cur_origem, sem)
            cur_origem.execute(sql.SQL("SELECT {} FROM {} LIMIT %s").format(sql.Identifier(pk_sem), sql.Identifier(sem)), (LIMITE_SEMENTE,))
            ids_semente = [r[0] for r in cur_origem.fetchall()]
            if ids_semente:
                upsert_registros(cur_origem, cur_destino, sem, ids_semente, fks, cache_local)

        # Sincronização final de sequences
        log("\n[*] Finalizando integridade...")
        for tab in cache_local.keys():
            sincronizar_sequences(cur_origem, cur_destino, tab)

        cur_destino.execute("SET session_replication_role = 'origin';")
        conn_destino.commit()
        
        log("\n" + "="*60)
        log("AMOSTRAGEM CONCLUÍDA COM SUCESSO!")
        log("-" * 60)
        for t, ids in sorted(cache_local.items()):
            log(f"  - {t.ljust(25)} : {len(ids)} registros")
        log("="*60)

    except Exception as e:
        log(f"[ERRO] ERRO CRÍTICO NA CONEXÃO: {e}")
        if conn_destino: conn_destino.rollback()
    finally:
        if conn_origem:
            try: conn_origem.close()
            except: pass
        if conn_destino:
            try: conn_destino.close()
            except: pass

if __name__ == "__main__":
    confirmacao = input("Iniciar Amostragem Referential Inteligente? (S/N): ")
    if confirmacao.upper() == "S":
        clonar_inteligente()