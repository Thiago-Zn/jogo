@echo off
REM Script de instalação e execução automática do jogo "Atravessar a Rua" para Windows

title Atravessar a Rua - Instalador
color 0A

echo ========================================================
echo    ATRAVESSAR A RUA - Instalador Automatico
echo ========================================================
echo.

REM Verifica se Python está instalado
echo [1/4] Verificando Python...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [X] Python nao encontrado!
    echo.
    echo Por favor, instale Python 3.7 ou superior:
    echo https://www.python.org/downloads/
    echo.
    echo Durante a instalacao, marque a opcao:
    echo "Add Python to PATH"
    pause
    exit /b 1
)

for /f "tokens=*" %%i in ('python --version') do set PYTHON_VERSION=%%i
echo [OK] Python encontrado: %PYTHON_VERSION%
echo.

REM Verifica se pip está instalado
echo [2/4] Verificando pip...
python -m pip --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [X] pip nao encontrado!
    echo Instalando pip...
    python -m ensurepip --default-pip
)
echo [OK] pip encontrado
echo.

REM Instala pygame-ce
echo [3/4] Instalando/verificando Pygame-CE...
python -c "import pygame" >nul 2>&1
if %errorlevel% neq 0 (
    echo Instalando Pygame-CE...
    if exist requirements.txt (
        python -m pip install -r requirements.txt
    ) else (
        python -m pip install pygame-ce
    )
) else (
    for /f "tokens=*" %%i in ('python -c "import pygame; print(pygame.version.ver)"') do set PYGAME_VERSION=%%i
    echo [OK] Pygame-CE ja instalado (versao %PYGAME_VERSION%)
)
echo.

REM Verifica se o arquivo do jogo existe
echo [4/4] Verificando arquivos do jogo...
if not exist "atravessar_rua.py" (
    echo [X] Arquivo atravessar_rua.py nao encontrado!
    echo Certifique-se de estar no diretorio correto.
    pause
    exit /b 1
)
echo [OK] Arquivo do jogo encontrado
echo.

echo ========================================================
echo          INSTALACAO CONCLUIDA COM SUCESSO!
echo ========================================================
echo.
echo Controles do jogo:
echo   Setas do teclado : Mover o sapo
echo   ESPACO          : Iniciar/Reiniciar
echo   ESC             : Menu/Sair
echo.
echo Objetivo:
echo   Atravesse a rua sem ser atingido pelos carros!
echo.
echo ========================================================
echo.

REM Pergunta se deseja executar o jogo
set /p resposta="Deseja executar o jogo agora? (S/n): "
if /i "%resposta%"=="" goto executar
if /i "%resposta%"=="s" goto executar
if /i "%resposta%"=="S" goto executar

echo.
echo Para jogar depois, execute:
echo   python atravessar_rua.py
echo.
echo Divirta-se!
pause
exit /b 0

:executar
echo.
echo Iniciando o jogo...
echo.
timeout /t 1 >nul
python atravessar_rua.py
