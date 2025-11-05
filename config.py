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

# ==================== ALEATORIEDADE E SEMENTES ====================
# Seed padrão para permitir execuções determinísticas. Use None para aleatório.
DEFAULT_SEED = 20240125

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

# ==================== CONFIGURAÇÕES DE DIFICULDADE PROGRESSIVA ====================
# Aumenta gradualmente para manter o jogo divertido por 30+ minutos
NIVEL_MAXIMO_DIFICULDADE = 20  # Após este nível, a dificuldade estabiliza
DIFICULDADE_MAXIMA = 2.5  # Multiplicador máximo de dificuldade (evita velocidades impossíveis)

# Distância em pixels percorridos para subir um nível (baseado no offset da câmera)
DISTANCIA_POR_NIVEL = 800

# Ajuste temporal da dificuldade - marcos em segundos
DIFICULDADE_INTERVALO_TEMPO = 45
MAX_MARCOS_TEMPO = 10

# Multiplicadores por nível/marco para velocidade
VELOCIDADE_MULTIPLICADOR_BASE = 1.0
VELOCIDADE_MULTIPLICADOR_POR_NIVEL = 0.08
VELOCIDADE_MULTIPLICADOR_POR_MARCO = 0.05
VELOCIDADE_MULTIPLICADOR_MAX = DIFICULDADE_MAXIMA

# Multiplicadores por nível/marco para spawn rate (quanto maior, mais spawns)
SPAWN_MULTIPLICADOR_BASE = 1.0
SPAWN_MULTIPLICADOR_POR_NIVEL = 0.06
SPAWN_MULTIPLICADOR_POR_MARCO = 0.05
SPAWN_MULTIPLICADOR_MAX = 2.75

# Intervalos e limites dos spawns de carros
CAR_SPAWN_INTERVALO_RANGE = (1.4, 2.8)
CAR_SPAWN_INTERVALO_MIN = 0.6
CAR_SPAWN_INTERVALO_MAX = 3.0
CARROS_POR_FAIXA_INICIAL = 2
CARROS_POR_FAIXA_MAX = 5

# Velocidade base das faixas
CAR_VELOCIDADE_BASE_RANGE = (2.0, 4.5)
RIO_VELOCIDADE_BASE_RANGE = (1.5, 3.5)

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


# ==================== FUNÇÕES AUXILIARES DE DIFICULDADE ====================
def _calcular_multiplicador(base, incremento_nivel, incremento_marco, nivel, marcos, limite):
    """Calcula um multiplicador limitado por nível e marcos de tempo."""
    nivel_progressao = max(0, int(nivel) - 1)
    valor = base + incremento_nivel * nivel_progressao + incremento_marco * max(0, marcos)
    return min(valor, limite)


def obter_multiplicador_velocidade(nivel=1, marcos=0):
    """Retorna o multiplicador de velocidade para o nível/marcos atuais."""
    return _calcular_multiplicador(
        VELOCIDADE_MULTIPLICADOR_BASE,
        VELOCIDADE_MULTIPLICADOR_POR_NIVEL,
        VELOCIDADE_MULTIPLICADOR_POR_MARCO,
        nivel,
        marcos,
        VELOCIDADE_MULTIPLICADOR_MAX,
    )


def obter_multiplicador_spawn(nivel=1, marcos=0):
    """Retorna o multiplicador de spawn rate para o nível/marcos atuais."""
    return _calcular_multiplicador(
        SPAWN_MULTIPLICADOR_BASE,
        SPAWN_MULTIPLICADOR_POR_NIVEL,
        SPAWN_MULTIPLICADOR_POR_MARCO,
        nivel,
        marcos,
        SPAWN_MULTIPLICADOR_MAX,
    )


def calcular_spawn_intervalo(intervalo_base, nivel=1, marcos=0):
    """Calcula o intervalo de spawn ajustado, respeitando limites configurados."""
    multiplicador = max(1.0, obter_multiplicador_spawn(nivel, marcos))
    intervalo = intervalo_base / multiplicador
    return max(CAR_SPAWN_INTERVALO_MIN, min(intervalo, CAR_SPAWN_INTERVALO_MAX))


def calcular_nivel_por_distancia(distancia):
    """Determina o nível baseado na distância percorrida."""
    if distancia <= 0:
        return 1
    nivel = 1 + int(distancia // max(1, DISTANCIA_POR_NIVEL))
    return min(nivel, NIVEL_MAXIMO_DIFICULDADE)

