# Script de Captura Automatica do DDL da Producao (Schema-Only)
# Este script usa o container docker local para rodar o pg_dump contra o servidor de producao

$PROD_HOST = "10.0.0.53"
$PROD_USER = "postgres"
$PROD_DB   = "adi"
$OUTPUT    = "test/database/dumps/dll_producao.sql"
$CONTAINER = "pg_adi_test"

Write-Host "`n[*] Iniciando captura de DDL da Producao ($PROD_HOST)..." -ForegroundColor Cyan

# Define a senha para o pg_dump rodar sem pedir interaçao
$PGPASSWORD = "Su4s_!@#"

# Executa o comando via Docker
# -s = --schema-only (nao traz dados, apenas estrutura)
try {
    Write-Host "[*] Executando pg_dump via Docker container: $CONTAINER..." -ForegroundColor Gray
    
    # Criamos o comando usando a variavel de ambiente PGPASSWORD
    docker exec -e PGPASSWORD=$PGPASSWORD $CONTAINER pg_dump -h $PROD_HOST -U $PROD_USER -s $PROD_DB > $OUTPUT
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "`n[OK] DDL capturado com sucesso!" -ForegroundColor Green
        Write-Host "Arquivo gerado: $OUTPUT" -ForegroundColor Green
        
        # Opcional: Contar as linhas
        $lines = (Get-Content $OUTPUT).Count
        Write-Host "Total de linhas capturadas: $lines" -ForegroundColor Gray
    } else {
        Write-Host "`n[ERRO] Erro ao capturar DDL. Verifique se o container $CONTAINER esta rodando." -ForegroundColor Red
    }
} catch {
    Write-Host "`n[ERRO] Erro inesperado: $_" -ForegroundColor Red
}
