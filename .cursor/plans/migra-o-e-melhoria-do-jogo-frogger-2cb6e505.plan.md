<!-- 2cb6e505-1618-4eed-b9ca-1469a55952c1 be98963d-47f8-4f54-b11c-1fc5e03d39c7 -->
# Plano de Transformação Completa do Jogo - Versão HD e Infinita

## Objetivo

Transformar o jogo atual em uma experiência profissional HD com modo infinito, geração procedimental, sistema de progressão contínua, animações polidas, sons/música, e qualidade visual premium. Jogo adaptado para tela cheia em resoluções HD.

## 1. Sistema de Scroll Progressivo e Estrada Expandida

### 1.1 Modificações na Configuração

- Arquivo: `config.py`
- Aumentar ALTURA_TELA para 900px (ou configurável)
- Adicionar sistema de scroll vertical
- Variável de progresso do nível (0-100%)
- Configuração de comprimento da estrada por nível

### 1.2 Sistema de Câmera/Scroll

- Arquivo: `game/camera.py` (novo)
- Classe Camera que acompanha o jogador
- Scroll suave quando jogador avança
- Área de spawn de novos elementos conforme scroll
- Gerenciamento de posição relativa vs absoluta

### 1.3 Expansão Dinâmica da Estrada

- Modificar `atravessar_rua.py` - método `desenhar_fundo()`
- Estrada se expande conforme jogador avança
- Novas faixas aparecem dinamicamente
- Sistema de "zones" que aparecem progressivamente

## 2. Sistema de Geração Procedimental Infinita

### 2.1 Geração Aleatória de Faixas

- Arquivo: `game/procedural_generator.py` (novo)
- Geração aleatória de faixas de carros
- Geração aleatória de áreas de rio
- Padrões variados (densidade, velocidade, direção)
- Sistema de "chunks" que são gerados conforme scroll
- Seed aleatória para variabilidade

### 2.2 Sistema de Progressão Infinita

- Dificuldade aumenta gradualmente e infinitamente
- Velocidade dos carros aumenta com distância percorrida
- Densidade de obstáculos aumenta progressivamente
- Novos tipos de obstáculos aparecem em distâncias maiores
- Sistema de "milhas" ou "metros" percorridos

### 2.3 Sistema de Transição e Animações

- Arquivo: `ui/transition.py` (novo)
- Animações suaves de carregamento
- Transições entre telas (fade in/out)
- Efeitos de partículas ao completar seções
- Feedback visual de progresso
- Sistema de loading screen

## 3. Sistema de Rio com Troncos e Tartarugas

### 3.1 Entidades do Rio

- Arquivo: `entities/tronco.py` (novo)
- Classe Tronco que se move na água
- Permite que jogador suba nele
- Diferentes tamanhos

- Arquivo: `entities/tartaruga.py` (novo)
- Classe Tartaruga que mergulha e emerge
- Ciclo de mergulho/emersão
- Colisão apenas quando emersa

- Arquivo: `entities/lilypad.py` (novo)
- Nenúfares como plataformas estáticas
- Pontos de segurança no rio

### 3.2 Sistema de Água

- Modificar `atravessar_rua.py` - método `desenhar_fundo()`
- Área de rio entre faixas de carros
- Animação de água (ondas, reflexos)
- Efeito visual de profundidade

### 3.3 Física do Rio

- Arquivo: `game/river_physics.py` (novo)
- Jogador é carregado por troncos
- Movimento relativo quando em tronco
- Dano ao cair na água

## 4. Menu Profissional com Mouse

### 4.1 Sistema de Botões

- Arquivo: `ui/button.py` (novo)
- Classe Button com estados (normal, hover, clicked)
- Feedback visual (cores, sombras, animações)
- Sistema de callbacks

### 4.2 Menu Principal Redesenhado

- Arquivo: `ui/menu.py` - reescrever completamente
- Botões clicáveis:
- Novo Jogo
- Seleção de Nível
- Configurações
- Tela Cheia
- Sair
- Background animado
- Logo/título destacado
- Estatísticas visíveis

### 4.3 Menu de Seleção de Nível

- Arquivo: `ui/level_select.py` (novo)
- Grid de 5 níveis com preview visual
- Indicadores de progresso
- Estrelas/badges de conquista
- Níveis bloqueados/desbloqueados

### 4.4 Menu de Configurações

- Arquivo: `ui/settings.py` (novo)
- Toggle tela cheia
- Volume de som (se implementado)
- Dificuldade
- Controles

## 5. Sistema de Tela Cheia

### 5.1 Configuração de Display

- Arquivo: `config.py`
- Variáveis para modo janela/tela cheia
- Resolução configurável

### 5.2 Implementação de Tela Cheia

- Modificar `atravessar_rua.py` - método `__init__()`
- Usar `pygame.FULLSCREEN` flag
- Toggle com F11 ou menu
- Preservar proporções (aspect ratio)

### 5.3 Adaptação de UI

- Todas as UI precisam escalar para tela cheia
- Fontes responsivas
- Elementos posicionados proporcionalmente

## 6. Melhorias Visuais Significativas

### 6.1 Elementos Decorativos

- Arquivo: `entities/decorative.py` (novo)
- Classe Árvore (vários tipos)
- Classe Pedra/Rocha
- Classe Cacto
- Classe Palmeira
- Sistema de parallax para profundidade

### 6.2 Melhorias no Cenário

- Modificar `atravessar_rua.py` - método `desenhar_fundo()`
- Background com múltiplas camadas
- Efeitos de parallax scrolling
- Partículas e efeitos atmosféricos
- Sombras e iluminação melhoradas

### 6.3 Animações

- Arquivo: `game/animations.py` (novo)
- Animações de transição suaves
- Efeitos de partículas
- Animações de UI (botões, menus)

### 6.4 Sprites Melhorados

- Modificar `entities/jogador.py`
- Sprite mais detalhado do sapo
- Múltiplos frames de animação
- Modificar `entities/carro.py`
- Carros mais variados e detalhados
- Diferentes tipos de veículos por nível

## 7. Estrutura de Arquivos Expandida

### Arquivos a Criar:

- `game/camera.py` - Sistema de câmera/scroll
- `game/scenarios.py` - Definição de cenários
- `game/river_physics.py` - Física do rio
- `entities/tronco.py` - Troncos flutuantes
- `entities/tartaruga.py` - Tartarugas
- `entities/lilypad.py` - Nenúfares
- `entities/decorative.py` - Elementos decorativos
- `ui/button.py` - Sistema de botões
- `ui/level_select.py` - Seleção de nível
- `ui/settings.py` - Menu de configurações
- `ui/transition.py` - Animações de transição
- `game/animations.py` - Sistema de animações

### Arquivos a Modificar:

- `config.py` - Adicionar configurações de scroll, cenários, tela cheia
- `atravessar_rua.py` - Integrar scroll, cenários, rio, tela cheia
- `ui/menu.py` - Reescrever com botões e mouse
- `entities/jogador.py` - Melhorar sprite e animações
- `entities/carro.py` - Variedade de veículos

## 8. Ordem de Implementação

### Fase 1: Sistema Base Expandido

1. Expandir `config.py` com novas configurações
2. Criar sistema de câmera/scroll
3. Implementar scroll progressivo na estrada
4. Aumentar altura da tela e adaptar coordenadas

### Fase 2: Sistema de Cenários

1. Criar `game/scenarios.py`
2. Definir os 5 cenários únicos
3. Implementar sistema de transição
4. Integrar cenários no loop principal

### Fase 3: Sistema de Rio

1. Criar entidades do rio (troncos, tartarugas, nenúfares)
2. Implementar física do rio
3. Adicionar área de rio no cenário
4. Integrar colisões e movimento relativo

### Fase 4: Menu Profissional

1. Criar sistema de botões com mouse
2. Redesenhar menu principal
3. Criar menu de seleção de nível
4. Criar menu de configurações

### Fase 5: Tela Cheia e UI

1. Implementar toggle de tela cheia
2. Adaptar todas as UI para escalar
3. Adicionar opção no menu

### Fase 6: Melhorias Visuais

1. Adicionar elementos decorativos
2. Melhorar sprites e animações
3. Implementar efeitos visuais
4. Polimento final

## 9. Melhorias de Gameplay Adicionais

- Sistema de progressão entre níveis
- Desbloqueio de níveis
- Sistema de conquistas
- Melhor feedback visual
- Sons e música (opcional, mas recomendado)

## 10. Testes e Validação

- Testar scroll em todos os cenários
- Validar física do rio
- Testar menu com mouse
- Verificar tela cheia em diferentes resoluções
- Performance com muitos elementos na tela
- Testar transições entre níveis

### To-dos

- [x] Criar estrutura de pastas (entities/, game/, ui/, utils/) e arquivos __init__.py
- [x] Criar config.py com todas as constantes e configurações
- [x] Migrar classe Jogador para entities/jogador.py usando pygame-ce
- [x] Migrar classe Carro para entities/carro.py usando pygame-ce
- [x] Criar game/game_state.py com gerenciador de estados
- [x] Criar game/collision.py com sistema de detecção de colisão
- [x] Criar ui/menu.py, ui/hud.py e ui/game_over.py
- [x] Reescrever atravessar_rua.py com loop principal pygame-ce
- [x] Atualizar requirements.txt para pygame-ce
- [x] Atualizar scripts .bat para pygame-ce
- [x] Testar instalação e execução no Windows
- [x] Atualizar README.md e COMO_JOGAR.md