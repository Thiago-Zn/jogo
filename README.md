# 🐸 Atravessar a Rua v2.0 - Frogger Style

Um jogo completo inspirado no clássico Frogger, desenvolvido em Python com **Pygame-CE** - biblioteca moderna, compatível e performática.

![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)
![Pygame-CE](https://img.shields.io/badge/Pygame--CE-2.5.0+-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## 🎯 Objetivo do Jogo

Controle um simpático sapo que precisa atravessar uma rua movimentada cheia de carros em alta velocidade! Chegue até o topo sem ser atingido para avançar de nível. Quanto mais rápido você chegar, mais pontos você ganha!

## ✨ Características v2.0

### 🚀 Melhorias da Versão 2.0
- ✅ **Biblioteca Pygame-CE** - Compatível com Python 3.14+
- ✅ **Código Modular** - Estrutura organizada em módulos
- ✅ **Melhor compatibilidade** - Funciona com Python 3.7+ até 3.14
- ✅ **Suporte a WASD** - Além das setas direcionais
- ✅ **Gráficos melhorados** - Renderização otimizada
- ✅ **Performance otimizada** - Melhor uso de recursos
- ✅ **Arquitetura limpa** - Fácil de manter e expandir

### Funcionalidades Principais
- 🎮 **Controle suave e responsivo** via teclas direcionais ou WASD
- 🚗 **Carros com movimento automático** em múltiplas faixas
- 💥 **Sistema de colisão preciso**
- 🎯 **Sistema de níveis progressivos** com dificuldade crescente
- 🏆 **Sistema de pontuação** com bônus de tempo
- ❤️ **Sistema de vidas** (ganha uma vida extra a cada nível)
- 🎨 **Interface visual agradável** com cores vibrantes
- 🔄 **Animações suaves** a 60 FPS

### Recursos Extras
- 📊 **HUD completo** mostrando pontos, nível, vidas e tempo
- 🏁 **Tela de menu** profissional
- 💀 **Tela de game over** com estatísticas
- 🔄 **Reinício rápido** com tecla de espaço
- 📈 **Melhor pontuação** salva durante a sessão
- ⏱️ **Temporizador** para aumentar a tensão
- 🎨 **Gráficos desenhados em código** (sem dependência de assets externos)

## 🚀 Como Jogar

### Instalação Rápida

#### Opção 1: Script Automático (Recomendado)

**Windows:**
```bash
executar_jogo.bat
```

#### Opção 2: Instalação Manual

1. **Instale as dependências**
   ```bash
   pip install -r requirements.txt
   ```
   
   Ou instale o Pygame-CE diretamente:
   ```bash
   pip install pygame-ce
   ```

2. **Execute o jogo**
   ```bash
   python atravessar_rua.py
   ```

### Controles

| Tecla | Ação |
|-------|------|
| **↑** ou **W** | Mover para cima |
| **↓** ou **S** | Mover para baixo |
| **←** ou **A** | Mover para esquerda |
| **→** ou **D** | Mover para direita |
| **ESPAÇO** | Iniciar jogo / Jogar novamente |
| **ESC** | Voltar ao menu / Sair |

## 🎮 Mecânicas do Jogo

### Sistema de Pontuação
- **100 pontos** por atravessar a rua com sucesso
- **Bônus de tempo** (até 100 pontos extras por velocidade)
- **Bônus de nível** (50 pontos × nível atual)

### Sistema de Níveis
- Cada nível aumenta a **velocidade dos carros** em 30%
- Mais **carros aparecem** em níveis superiores
- Você **ganha uma vida extra** ao completar cada nível (máximo de 5 vidas)

### Dificuldade Progressiva
- **Nível 1**: 2 carros por faixa, velocidade normal
- **Nível 2+**: Mais carros, velocidade aumentada
- **Nível 5+**: Desafio extremo para jogadores habilidosos!

## 🏗️ Estrutura do Projeto

```
jogo/
├── atravessar_rua.py      # Arquivo principal (entry point)
├── config.py              # Configurações e constantes
├── entities/              # Entidades do jogo
│   ├── __init__.py
│   ├── jogador.py         # Classe Jogador
│   └── carro.py           # Classe Carro
├── game/                  # Lógica do jogo
│   ├── __init__.py
│   ├── game_state.py      # Gerenciador de estados
│   └── collision.py       # Sistema de colisão
├── ui/                    # Interface do usuário
│   ├── __init__.py
│   ├── menu.py            # Tela de menu
│   ├── hud.py             # Heads-up display
│   └── game_over.py       # Tela de game over
├── utils/                 # Utilitários
│   ├── __init__.py
│   └── colors.py          # Paleta de cores
├── requirements.txt       # Dependências (Pygame-CE)
├── executar_jogo.bat      # Script de execução (Windows)
├── instalar_e_jogar.bat   # Instalador completo (Windows)
├── README.md              # Este arquivo
└── COMO_JOGAR.md          # Guia de jogo detalhado
```

## 💻 Requisitos do Sistema

- **Python**: 3.7 até 3.14 (recomendado 3.9+)
- **Pygame-CE**: 2.5.0 ou superior
- **Sistema Operacional**: Windows
- **Memória**: 100 MB RAM
- **Processador**: Qualquer processador moderno

## 📝 Dicas para Jogar

1. **Observe o padrão** dos carros antes de atravessar
2. **Não tenha pressa** - planeje seus movimentos
3. **Use todo o espaço** - você pode se mover horizontalmente
4. **Tempo é pontuação** - mas segurança em primeiro lugar!
5. **Pratique** - cada nível ensina novos padrões

## 🧪 Testes e Modo Determinístico

Para validar rapidamente se o jogo inicializa corretamente em ambientes sem interface gráfica, execute o teste de sanidade:

```bash
USE_LANE_CONFIG=1 SDL_VIDEODRIVER=dummy python -m pytest tests/sanity_run.py
```

- `USE_LANE_CONFIG=1`: força o uso do layout determinístico definido em `config.FAIXAS`, ideal para cenários de CI.
- `SDL_VIDEODRIVER=dummy`: permite que o Pygame-CE rode em modo headless.

## 🔄 Migração da v1.0 para v2.0

### Mudanças Principais
- **Biblioteca**: Arcade → Pygame-CE (compatibilidade Python 3.14)
- **Arquitetura**: Código monolítico → Estrutura modular
- **Controles**: Setas → Setas + WASD
- **Performance**: Melhorada significativamente
- **Compatibilidade**: Suporte completo a Python 3.14

### Melhorias Arquiteturais
- **Separação de responsabilidades**: Entities, Game, UI, Utils
- **Código mais limpo**: Fácil de manter e expandir
- **Reutilização**: Componentes modulares
- **Testabilidade**: Estrutura permite testes unitários

## 🐛 Resolução de Problemas

### "ModuleNotFoundError: No module named 'pygame'"
```bash
pip install pygame-ce
# ou
python -m pip install pygame-ce
```

### "Python 3.14 não funciona"
O jogo agora funciona perfeitamente com Python 3.14 usando Pygame-CE!

### "O jogo não abre"
- Certifique-se de ter um ambiente gráfico (não funciona em servidores sem GUI)
- Teste se o pygame está funcionando:
```bash
python -c "import pygame; print(pygame.version.ver)"
```

## 📜 Licença

Este projeto é de código aberto e está disponível sob a licença MIT.

## 🎉 Divirta-se!

Boa sorte atravessando a rua! Tente alcançar o nível 10! 🏆

---

**Desenvolvido com 🤖 + ❤️**

**Versão 2.0 - Agora com Pygame-CE e código modular!**
