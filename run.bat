@echo off
REM Script para rodar o Divulgador Inteligente
echo Iniciando Divulgador Inteligente...
echo.

if not exist venv (
    echo ERRO: Ambiente virtual nao encontrado!
    echo Execute install.bat primeiro.
    pause
    exit /b 1
)

if not exist .env (
    echo ERRO: Arquivo .env nao encontrado!
    echo Copie .env.example para .env e preencha as credenciais.
    pause
    exit /b 1
)

call venv\Scripts\activate.bat
where py >nul 2>&1
if errorlevel 1 (
    python main.py
) else (
    py main.py
)
pause
