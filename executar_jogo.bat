@echo off
REM Script simples para executar o jogo "Atravessar a Rua v2.0"
REM Para Windows - Versão usando Pygame-CE

echo ========================================
echo   🐸 ATRAVESSAR A RUA v2.0 🐸
echo   Versao melhorada com Pygame-CE
echo ========================================
echo.

REM Verifica se pygame-ce está instalado
python -c "import pygame" >nul 2>&1
if %errorlevel% neq 0 (
    echo [INFO] Pygame-CE nao esta instalado!
    echo.
    echo Instalando Pygame-CE...
    python -m pip install pygame-ce
    if %errorlevel% neq 0 (
        echo.
        echo [ERRO] Falha ao instalar Pygame-CE.
        echo.
        echo Tente instalar manualmente:
        echo   python -m pip install pygame-ce
        echo.
        pause
        exit /b 1
    )
    echo [OK] Pygame-CE instalado com sucesso!
    echo.
)

echo Iniciando o jogo v2.0...
echo.
python atravessar_rua.py

if %errorlevel% neq 0 (
    echo.
    echo [ERRO] O jogo nao pode ser executado.
    echo.
    echo Verifique se:
    echo   1. Pygame-CE esta instalado: python -m pip install pygame-ce
    echo   2. Python esta no PATH
    echo   3. Todos os arquivos estao presentes
    echo.
)
pause
