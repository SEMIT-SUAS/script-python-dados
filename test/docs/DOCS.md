# Manual Técnico: Robô de Migração

Este documento descreve o funcionamento interno do script `script-processos-2021.py`, atualizado para suportar continuidade automática de lotes e alinhamento rigoroso com a produção.

## 1. Varredura e Mapeamento (Scan)

O robô percorre recursivamente o diretório de origem (`test/assets/drive_d/PROCESSOS 2021`).

- Identifica arquivos `.pdf`.
- Captura o nome da **pasta pai** (ex: SEPLAN, SECOM) para utilizá-lo dinamicamente como o nome da Secretaria no banco de dados.

## 2. Extração de Metadados

Utiliza uma expressão regular ultra-flexível para capturar informações mesmo em nomes de arquivos fora do padrão estrito:

- **Padrão**: Identifica códigos estruturais (ex: `06.00`), o **Título/Categoria** do documento e o número da **NE/Processo**.
- **Fallback**: Caso um arquivo não combine com o padrão, ele é registrado no log de ignorados para revisão manual.

## 3. Sincronização e Chave de Lote (DB Sync)

O robô agora se conecta ao banco de dados local para garantir a continuidade:

- **Consulta Dinâmica**: O script executa `SELECT MAX(chave_lote)` para descobrir o último index processado (ex: `L20`).
- **Continuidade**: A nova migração inicia automaticamente a partir do próximo número (ex: `L21`), evitando duplicidade de chaves.
- **Formato**: `L[Contador]` gravado nas tabelas `volumes` e `arquivos_digitais`.

## 4. Padronização de Campos (Mirror Produção)

Para total compatibilidade com o sistema ADI:

- **Conteúdo OCR**: Inserção do texto padrão `"OCR pendente para processamento posterior"`.
- **numero_volume**: Definido explicitamente como **`NULL`**, conforme o padrão observado nas amostras oficiais do banco.
- **IDs Oficiais**: Usa IDs pré-definidos para `id_estado_conservacao` (6), `id_discos_servidores` (23) e `id_pastas_digitais` (13).

## 5. Integridade de Dados

- **Hashing MD5**: Calculado em tempo real para garantir a integridade do arquivo.
- **UUID**: Cada arquivo recebe um prefixo UUID único no sistema de arquivos para evitar colisões de nomes.
- **MIME Type**: Detecção automática via biblioteca `mimetypes`.

## 6. Logs e Relatórios

Ao final da execução, o script gera um relatório em `test/logs/arquivos_ignorados_2021.txt` listando todos os arquivos que não puderam ser processados e o motivo (ERRO SISTEMA ou PADRAO INVALIDO).

## 7. Execução no Banco (Motor de Injeção)

Após a geração do arquivo `.sql`, a carga final é realizada pelo script **`executar_migracao_final.py`**:
- **Conexão**: PostgreSQL Docker (`port 5435`).
- **Transacionalidade**: O script executa um **commit único (Transação Atômica)** para todo o lote de registros. Isso garante que, em caso de falha, o banco não fique em um estado inconsistente ("tudo ou nada").
- **Integridade**: Valida a existência do arquivo gerado em `test/database/seeders/` antes de iniciar.
