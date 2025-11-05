"""
Configurações e constantes do jogo
"""

# ==================== CORES ====================
PRETO = (0, 0, 0)
BRANCO = (255, 255, 255)
VERDE = (34, 177, 76)
VERDE_ESCURO = (20, 120, 50)
VERMELHO = (237, 28, 36)
AZUL = (0, 162, 232)
AMARELO = (255, 242, 0)
LARANJA = (255, 127, 39)
ROXO = (163, 73, 164)
CINZA = (127, 127, 127)
CINZA_ESCURO = (64, 64, 64)
ASFALTO = (50, 50, 50)
VERDE_GRAMA = (76, 175, 80)
VERDE_GRAM_ESCURO = (56, 142, 60)

# ==================== DIMENSÕES MODERNAS ====================
# Resolução HD moderna (16:9) - padrão para jogos pixel art
LARGURA_TELA = 1280  # HD moderno
ALTURA_TELA = 720    # HD moderno (16:9)
TITULO = "🐸 Atravessar a Rua v3.0 - Frogger Infinito"

# ==================== CONFIGURAÇÕES DO JOGO ====================
FPS = 60
VELOCIDADE_JOGADOR = 32  # Velocidade em pixels por frame (1 célula por frame = movimento fluido)

# ==================== SISTEMA DE GRID/TABULEIRO MODERNO ====================
# Tile size de 32px é padrão para jogos pixel art modernos
TAMANHO_CELL = 32  # Tamanho de cada célula do grid (32x32 pixels) - PADRÃO MODERNO
GRID_LARGURA = LARGURA_TELA // TAMANHO_CELL  # 40 células horizontais
GRID_ALTURA = ALTURA_TELA // TAMANHO_CELL    # 22 células verticais

# Todos os tamanhos devem ser múltiplos de 32 para alinhamento perfeito
TAMANHO_JOGADOR = 32  # 1 célula (32x32)
TAMANHO_CARRO_LARGURA = 64  # 2 células (64x32)
TAMANHO_CARRO_ALTURA = 32   # 1 célula (32x32)

# ==================== CONFIGURAÇÕES DE JOGABILIDADE ====================
VIDAS_INICIAIS = 3
VIDAS_MAXIMAS = 5
PONTOS_BASE = 100
BONUS_TEMPO_MAX = 100
BONUS_NIVEL = 50
AUMENTO_VELOCIDADE_NIVEL = 0.3
CARROS_POR_FIXA_INICIAL = 2

# ==================== CONFIGURAÇÕES DE DIFICULDADE PROGRESSIVA ====================
# Aumenta gradualmente para manter o jogo divertido por 30+ minutos
NIVEL_MAXIMO_DIFICULDADE = 20  # Após este nível, a dificuldade estabiliza

# ==================== CONFIGURAÇÕES DE FAIXAS ====================
# Formato: (y, velocidade_base, direcao)
# direcao: 1 = direita, -1 = esquerda
FAIXAS = [
    (150, 2, 1),
    (210, 3, -1),
    (270, 2.5, 1),
    (330, 3.5, -1),
    (390, 3, 1),
    (450, 4, -1),
]

CORES_CARROS = [VERMELHO, AZUL, LARANJA, ROXO, AMARELO]

# ==================== CONFIGURAÇÕES DE ÁREAS DE DESCANSO ====================
# Áreas seguras que aparecem periodicamente para o jogador planejar
INTERVALO_DESAFIOS_PARA_DESCANSO = 5  # Base: aparece a cada 5 desafios
VARIACAO_INTERVALO_DESAFIOS = 1  # Pode variar entre 5 e 6 (5 + VARIACAO)
ALTURA_AREA_DESCANSO = 96  # 3 células (96px) - múltiplo de 32
COR_AREA_DESCANSO = VERDE_GRAMA  # Cor principal
COR_AREA_DESCANSO_DETALHE = VERDE_GRAM_ESCURO  # Cor para textura

# ==================== CONFIGURAÇÕES DE SCROLL E CÂMERA ====================
# Sistema de scroll progressivo para jogo infinito
VELOCIDADE_SCROLL = 2  # Velocidade base do scroll automático
ALTURA_CHUNK = 320  # 10 células (320px) - múltiplo de 32
DISTANCIA_GERACAO_CHUNK = 400  # Distância para gerar novo chunk
MARGEM_REMOCAO_CHUNK = -200  # Margem para remover chunks antigos

