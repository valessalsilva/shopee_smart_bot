@echo off
REM Script de instalação para Windows
REM Usa 'py' pois o alias 'python' está desativado nas configurações do Windows
echo ========================================
echo  Divulgador Inteligente - Instalacao
echo ========================================
echo.

REM Verifica Python via 'py' (Windows Launcher)
echo [1/5] Verificando Python...
py --version >nul 2>&1
if errorlevel 1 (
    echo ERRO: Python nao encontrado. Instale de https://python.org
    pause
    exit /b 1
)

REM Cria ambiente virtual
echo [2/5] Criando ambiente virtual...
py -m venv venv
if errorlevel 1 goto :error

REM Ativa o venv
echo [3/5] Ativando ambiente virtual...
call venv\Scripts\activate.bat

REM Instala dependências
echo [4/5] Instalando dependencias...
py -m pip install --upgrade pip
py -m pip install -r requirements.txt
if errorlevel 1 goto :error

REM Copia .env
echo [5/5] Configurando .env...
if not exist .env (
    copy .env.example .env
    echo .env criado! Preencha suas credenciais antes de rodar.
) else (
    echo .env ja existe, mantendo.
)

echo.
echo ========================================
echo  Instalacao concluida com sucesso!
echo ========================================
echo.
echo Proximos passos:
echo 1. Edite o arquivo .env com suas credenciais
echo 2. Execute: .\run.bat
echo.
goto :eof

:error
echo.
echo ERRO durante a instalacao!
echo Dica: verifique se o Python foi instalado corretamente.
pause
exit /b 1
