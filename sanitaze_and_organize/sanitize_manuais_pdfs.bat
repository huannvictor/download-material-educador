@echo off
setlocal

:: -----------------------------------------------------------------------------
:: CONFIGURACAO
:: -----------------------------------------------------------------------------
SET "ALVO=%~dp0..\manuais_pdfs"

echo Navegando para: %ALVO%
cd /d "%ALVO%"

if %errorlevel% neq 0 (
    echo [ERRO] Nao foi possivel encontrar o diretorio especificado.
    pause
    exit /b
)

echo.
echo -----------------------------------------------------------------------------
echo INICIANDO LIMPEZA TOTAL (Removendo 'Prof_' e codigos estranhos)
echo -----------------------------------------------------------------------------
echo.

:: O comando abaixo chama o PowerShell pelo caminho completo para evitar erro de "nao reconhecido"
"%SystemRoot%\System32\WindowsPowerShell\v1.0\powershell.exe" -NoProfile -ExecutionPolicy Bypass -Command "Get-ChildItem *.pdf | ForEach-Object { $original = $_.Name; $novo = $original -replace '^Prof_', '' -replace '_[a-f0-9]{32}\.pdf$', '.pdf'; if ($original -ne $novo) { $caminho = $_.DirectoryName; $testeNome = $novo; $cont = 1; while (Test-Path (Join-Path $caminho $testeNome)) { $base = [System.IO.Path]::GetFileNameWithoutExtension($novo); $ext = [System.IO.Path]::GetExtension($novo); $testeNome = '{0} ({1}){2}' -f $base, $cont, $ext; $cont++ }; Write-Host 'Renomeando:' $original ' -> ' $testeNome; Rename-Item -LiteralPath $_.FullName -NewName $testeNome } }"

echo.
echo -----------------------------------------------------------------------------
echo Concluido! Verifique a pasta.
echo -----------------------------------------------------------------------------
pause