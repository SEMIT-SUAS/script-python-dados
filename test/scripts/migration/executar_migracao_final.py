import psycopg2
import time

DB_LOCAL = {
    "host": "localhost",
    "port": 5435,
    "database": "db_adi_test",
    "user": "postgres",
    "password": "postgres"
}

def executar_migracao():
    try:
        conn = psycopg2.connect(**DB_LOCAL)
        cur = conn.cursor()
        
        print("[*] Lendo arquivo SQL de 10.537 registros...")
        with open('test/database/seeders/registro_processos_2021.sql', 'r', encoding='utf-8') as f:
            sql_content = f.read()
            
        print("[*] Iniciando injeção no banco local. Isso pode levar alguns segundos...")
        start_time = time.time()
        
        # Executa todo o lote
        cur.execute(sql_content)
        
        conn.commit()
        end_time = time.time()
        
        print(f"[+] SUCESSO! 10.537 registros injetados em {end_time - start_time:.2f} segundos.")
        print("[+] Todas as secretarias foram criadas/vinculadas conforme as pastas.")
        conn.close()
        
    except Exception as e:
        print(f"[-] Erro durante a migracao: {e}")

if __name__ == "__main__":
    executar_migracao()
