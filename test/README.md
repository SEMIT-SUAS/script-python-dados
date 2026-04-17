# Ambiente de Testes - Documentação e Registro

Este diretório contém a infraestrutura e os scripts necessários para simular o ambiente de produção do sistema **ADI** (Arquivo Digital Inteligente) localmente, permitindo testes de migração e registro de documentos sem risco à base original.

## 🏗️ Infraestrutura (Docker)

O ambiente utiliza **Docker** para subir uma instância do PostgreSQL 17.

- **Porta Local**: `5435`
- **Banco de Dados**: `db_adi_test`
- **Usuário/Senha**: `postgres` / `postgres`
- **Volumes Mapeados**:
    - `./uploads-test`: Simula a pasta de uploads do servidor de produção (mapeado para `/home/suas/Arquivo-digital-inteligente/uploads` no container).

**Como subir o ambiente:**
```powershell
cd test
docker compose up -d
```

---

## 🛠️ Ferramentas e Scripts (`/scripts`)

### 1. Estrutura de Amostragem (`/scripts/utils/`)
- **`utils/script-amostra-banco.py`**: Motor autônomo para reset e população do ambiente. 
    - **Ação**: Executa o `DROP SCHEMA`, recria a estrutura usando **exclusivamente** o `test/database/dumps/dll.sql` e insere 20 registros referenciais da produção.
    - **Segurança**: Opera em modo **READ-ONLY** na produção para auditoria de IDs.

### 2. Robôs de Migração (`/scripts/migration/*.py`)

A migração é dividida em dois passos para maior controle:

**Passo A: Geração do SQL**
- **`script-processos-2021.py`**: Robô que varre os arquivos e gera o script SQL.
    - **Local de Origem**: `test/assets/drive_d/PROCESSOS 2021/`
    - **Saída SQL**: `test/database/seeders/registro_processos_2021.sql`
    - **Execução**: `python ./test/scripts/migration/script-processos-2021.py`

**Passo B: Injeção no Banco (Execução)**
- **`executar_migracao_final.py`**: Motor de injeção que lê o arquivo SQL gerado e o executa contra o banco no Docker.
    - **Ação**: Executa a carga em uma **transação atômica** (commit único), garantindo a integridade dos 10.537 registros.
    - **Execução**: `python ./test/scripts/migration/executar_migracao_final.py`

---

## 🔍 Como Validar os Testes

1. **DBeaver**: Conecte no `localhost:5435`.
2. **Logs**: Verifique o diretório `test/logs/` para relatórios detalhados (`arquivos_ignorados_2021.txt`).
3. **Padrão de Dados**: Verifique se os novos registros seguem a sequência correta de `L[número]` na coluna `chave_lote`.

---

## 🛡️ Guia de Segurança
- **MODO LEITURA**: Todos os scripts que acessam a produção (`10.0.0.53`) estão configurados com `readonly=True` ou utilizam ferramentas de dump de estrutura (schema-only), garantindo a integridade dos dados originais.
- **ISOLAMENTO**: O ambiente de teste é isolado via Docker. Nunca aponte scripts de escrita (`INSERT`/`UPDATE`) para o host de produção.
