@echo off
REM Script para rodar o Divulgador Inteligente
echo Iniciando Divulgador Inteligente...
echo.

REM Garante que o script rode a partir da pasta do projeto
cd /d "%~dp0"

if not exist .env (
    echo ERRO: Arquivo .env nao encontrado!
    echo Copie .env.example para .env e preencha as credenciais.
    pause
    exit /b 1
)

if exist venv (
    call venv\Scripts\activate.bat
) else (
    echo AVISO: Ambiente virtual nao encontrado. Usando o Python do sistema.
    echo Para criar o ambiente virtual, execute install.bat.
    echo.
)

where py >nul 2>&1
if errorlevel 1 (
    python main.py
) else (
    py main.py
)
pause
