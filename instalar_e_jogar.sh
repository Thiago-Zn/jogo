#!/bin/bash

# Script de instalação e execução automática do jogo "Atravessar a Rua"

echo "╔════════════════════════════════════════════════════════╗"
echo "║   🐸 ATRAVESSAR A RUA - Instalador Automático 🐸      ║"
echo "╚════════════════════════════════════════════════════════╝"
echo ""

# Cores
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Função para verificar se um comando existe
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Verifica se Python está instalado
echo -e "${BLUE}[1/4]${NC} Verificando Python..."
if command_exists python3; then
    PYTHON_CMD=python3
    PYTHON_VERSION=$(python3 --version)
    echo -e "${GREEN}✓${NC} Python encontrado: $PYTHON_VERSION"
elif command_exists python; then
    PYTHON_CMD=python
    PYTHON_VERSION=$(python --version)
    echo -e "${GREEN}✓${NC} Python encontrado: $PYTHON_VERSION"
else
    echo -e "${RED}✗${NC} Python não encontrado!"
    echo "Por favor, instale Python 3.7 ou superior:"
    echo "  Ubuntu/Debian: sudo apt-get install python3"
    echo "  macOS: brew install python3"
    echo "  Windows: https://www.python.org/downloads/"
    exit 1
fi

# Verifica se pip está instalado
echo ""
echo -e "${BLUE}[2/4]${NC} Verificando pip..."
if command_exists pip3; then
    PIP_CMD=pip3
    echo -e "${GREEN}✓${NC} pip encontrado"
elif command_exists pip; then
    PIP_CMD=pip
    echo -e "${GREEN}✓${NC} pip encontrado"
else
    echo -e "${RED}✗${NC} pip não encontrado!"
    echo "Instalando pip..."
    $PYTHON_CMD -m ensurepip --default-pip
fi

# Instala pygame
echo ""
echo -e "${BLUE}[3/4]${NC} Instalando/verificando Pygame..."

# Verifica se pygame já está instalado
if $PYTHON_CMD -c "import pygame" 2>/dev/null; then
    PYGAME_VERSION=$($PYTHON_CMD -c "import pygame; print(pygame.version.ver)")
    echo -e "${GREEN}✓${NC} Pygame já instalado (versão $PYGAME_VERSION)"
else
    echo "Instalando Pygame..."
    if [ -f "requirements.txt" ]; then
        $PIP_CMD install -r requirements.txt
    else
        $PIP_CMD install pygame
    fi

    # Verifica se a instalação foi bem-sucedida
    if $PYTHON_CMD -c "import pygame" 2>/dev/null; then
        echo -e "${GREEN}✓${NC} Pygame instalado com sucesso!"
    else
        echo -e "${RED}✗${NC} Erro ao instalar Pygame"
        exit 1
    fi
fi

# Verifica se o arquivo do jogo existe
echo ""
echo -e "${BLUE}[4/4]${NC} Verificando arquivos do jogo..."
if [ -f "atravessar_rua.py" ]; then
    echo -e "${GREEN}✓${NC} Arquivo do jogo encontrado"
else
    echo -e "${RED}✗${NC} Arquivo atravessar_rua.py não encontrado!"
    echo "Certifique-se de estar no diretório correto."
    exit 1
fi

# Tudo pronto!
echo ""
echo "╔════════════════════════════════════════════════════════╗"
echo "║          ✅ INSTALAÇÃO CONCLUÍDA COM SUCESSO!         ║"
echo "╚════════════════════════════════════════════════════════╝"
echo ""
echo -e "${YELLOW}🎮 Controles do jogo:${NC}"
echo "  ↑ ↓ ← → : Mover o sapo"
echo "  ESPAÇO  : Iniciar/Reiniciar"
echo "  ESC     : Menu/Sair"
echo ""
echo -e "${YELLOW}🎯 Objetivo:${NC}"
echo "  Atravesse a rua sem ser atingido pelos carros!"
echo ""

# Pergunta se deseja executar o jogo
echo -e "${GREEN}Deseja executar o jogo agora? (S/n)${NC}"
read -r resposta

if [ -z "$resposta" ] || [ "$resposta" = "s" ] || [ "$resposta" = "S" ]; then
    echo ""
    echo "🚀 Iniciando o jogo..."
    echo ""
    sleep 1
    $PYTHON_CMD atravessar_rua.py
else
    echo ""
    echo "Para jogar depois, execute:"
    echo "  $PYTHON_CMD atravessar_rua.py"
    echo ""
    echo "Divirta-se! 🎉"
fi
