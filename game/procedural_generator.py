"""
Sistema de Geração Procedimental
"""

import json
import random
import pygame
import config
from entities.safe_zone import SafeZone
from entities.tronco import Tronco
# Tartarugas removidas - apenas troncos para simplificar
# Lilypads removidos - apenas troncos


class Chunk:
    """Representa um chunk (pedaço) do mundo"""
    
    def __init__(self, y_inicio, tipo='estrada', dados=None):
        """
        Inicializa um chunk
        
        Args:
            y_inicio: Posição Y inicial do chunk
            tipo: Tipo do chunk ('estrada', 'rio', 'safe_zone')
            dados: Dados específicos do chunk (faixas, velocidades, etc.)
        """
        self.y_inicio = y_inicio
        self.tipo = tipo
        self.dados = dados if dados else {}
        self.altura = self.dados.get('altura', config.ALTURA_CHUNK)
        self.y_fim = y_inicio + self.altura
        self.ativo = True
        
    def __repr__(self):
        return f"Chunk(tipo={self.tipo}, y={self.y_inicio}-{self.y_fim})"


class ProceduralGenerator:
    """Gerenciador de geração procedimental"""
    
    def __init__(self, seed=None):
        """
        Inicializa o gerador procedimental

        Args:
            seed: Seed para geração aleatória (opcional)
        """
        if seed:
            random.seed(seed)

        # Configurações externas de faixas
        self.use_lane_config = getattr(config, 'USE_LANE_CONFIG', False)
        self.lane_config = []
        self.road_lane_defs = []
        self.river_lane_defs = []
        self.road_lane_index = 0
        self.river_lane_index = 0
        if self.use_lane_config:
            self._carregar_lane_config()

        # Lista de chunks ativos
        self.chunks = []
        self.safe_zones = []

        # Controle de geração
        self.proximo_y = 0  # Próxima posição Y para gerar
        self.contador_desafios = 0  # Contador de desafios gerados
        self.ultimo_intervalo = config.INTERVALO_DESAFIOS_PARA_DESCANSO
        self.ultimo_tipo = None  # Tipo do último chunk gerado ('estrada' ou 'rio')

        # Estatísticas
        self.distancia_percorrida = 0
        self.dificuldade_atual = 1.0

        # Pool de chunks reciclados (otimização de memória)
        self.chunk_pool = []
        self.max_pool_size = 50

    def _carregar_lane_config(self):
        """Carrega definições de faixas a partir de arquivo JSON."""
        caminho = getattr(config, 'LANE_CONFIG_PATH', None)
        if not caminho:
            self.use_lane_config = False
            return

        try:
            with open(caminho, 'r', encoding='utf-8') as arquivo:
                dados = json.load(arquivo)
        except FileNotFoundError:
            print(f"[AVISO] Arquivo de configuração de faixas não encontrado: {caminho}. Usando geração padrão.")
            self.use_lane_config = False
            return
        except json.JSONDecodeError as exc:
            print(f"[AVISO] Erro ao ler configuração de faixas ({caminho}): {exc}. Usando geração padrão.")
            self.use_lane_config = False
            return

        self.lane_config = dados.get('lanes', [])
        for lane in self.lane_config:
            lane_type = lane.get('type')
            if lane_type == 'road':
                self.road_lane_defs.append(lane)
            elif lane_type == 'river':
                self.river_lane_defs.append(lane)

        if not self.road_lane_defs and not self.river_lane_defs:
            print(f"[AVISO] Configuração de faixas vazia em {caminho}. Usando geração padrão.")
            self.use_lane_config = False

    def _obter_lane_config(self, lane_type):
        """Retorna próxima configuração de faixa para o tipo informado."""
        if not self.use_lane_config:
            return None

        if lane_type == 'road' and self.road_lane_defs:
            lane = self.road_lane_defs[self.road_lane_index % len(self.road_lane_defs)]
            self.road_lane_index += 1
            return lane
        if lane_type == 'river' and self.river_lane_defs:
            lane = self.river_lane_defs[self.river_lane_index % len(self.river_lane_defs)]
            self.river_lane_index += 1
            return lane
        return None

    def obter_parametros_lane(self, lane_dados):
        """Calcula parâmetros atuais da lane considerando dificuldade."""
        if not lane_dados:
            return {
                'velocidade': 3.0,
                'spawn_intervalo': 2.5,
                'min_gap': 160,
                'entity_width': config.TAMANHO_CARRO_LARGURA,
                'spawn_jitter': 0.5
            }

        base_speed = lane_dados.get('base_speed', lane_dados.get('velocidade', 3.0))
        dificuldade = max(1.0, self.dificuldade_atual)
        velocidade = base_speed * dificuldade

        spawn_rate = lane_dados.get('spawn_rate', 2.5)
        spawn_intervalo = max(0.3, spawn_rate / dificuldade)

        min_gap = lane_dados.get('min_gap', 160)
        min_gap = max(32, min_gap / max(1.0, dificuldade * 0.9))

        largura = lane_dados.get('entity_width', config.TAMANHO_CARRO_LARGURA)
        spawn_jitter = lane_dados.get('spawn_jitter')
        if spawn_jitter is None:
            spawn_jitter = max(0.1, spawn_intervalo * 0.25)

        lane_dados['velocidade'] = velocidade

        return {
            'velocidade': velocidade,
            'spawn_intervalo': spawn_intervalo,
            'min_gap': min_gap,
            'entity_width': largura,
            'spawn_jitter': spawn_jitter
        }
        
    def deve_gerar_area_descanso(self):
        """
        Verifica se deve gerar uma área de descanso
        
        Returns:
            bool: True se deve gerar área de descanso
        """
        if self.contador_desafios == 0:
            return False
        
        # Gera área de descanso a cada X desafios
        return self.contador_desafios % self.ultimo_intervalo == 0
    
    def gerar_area_descanso(self, y_pos):
        """
        Gera uma área de descanso
        
        Args:
            y_pos: Posição Y para gerar a área
            
        Returns:
            SafeZone: Área de descanso gerada
        """
        safe_zone = SafeZone(y_pos, config.ALTURA_AREA_DESCANSO)
        self.safe_zones.append(safe_zone)
        
        # Criar chunk para a área de descanso
        chunk = Chunk(
            y_inicio=y_pos,
            tipo='safe_zone',
            dados={
                'altura': config.ALTURA_AREA_DESCANSO,
                'safe_zone': safe_zone
            }
        )
        self.chunks.append(chunk)
        
        # Atualizar próxima posição
        self.proximo_y = y_pos + config.ALTURA_AREA_DESCANSO
        
        # Variar o intervalo (5 ou 6 desafios)
        self.ultimo_intervalo = config.INTERVALO_DESAFIOS_PARA_DESCANSO + \
                                random.randint(0, config.VARIACAO_INTERVALO_DESAFIOS)
        
        return safe_zone
    
    def gerar_grupo_faixas(self, y_pos, num_faixas=None):
        """
        Gera um grupo de faixas de carros (1 desafio)
        
        Args:
            y_pos: Posição Y inicial
            num_faixas: Número de faixas (2-3 se None)
            
        Returns:
            Chunk: Chunk com dados das faixas
        """
        if num_faixas is None:
            num_faixas = random.randint(2, 3)
        
        altura_faixa = 32  # 1 célula (32px) - alinhado ao grid moderno  # Altura de cada faixa
        faixas = []
        
        for i in range(num_faixas):
            y_faixa = y_pos + (i * altura_faixa)
            lane_config = self._obter_lane_config('road')

            if lane_config:
                velocidade_base = lane_config.get('speed', 3.0)
                direcao = lane_config.get('dir', random.choice([1, -1]))
                spawn_rate = lane_config.get('spawn_rate', 2.5)
                min_gap = lane_config.get('min_gap', config.TAMANHO_CARRO_LARGURA * 2)
                entidade = lane_config.get('entity', 'car')
                largura_entidade = lane_config.get('width', config.TAMANHO_CARRO_LARGURA)
                spawn_jitter = lane_config.get('spawn_jitter')
            else:
                velocidade_base = random.uniform(2.0, 4.5)
                direcao = random.choice([1, -1])
                spawn_rate = 2.5
                min_gap = config.TAMANHO_CARRO_LARGURA * 2
                entidade = 'car'
                largura_entidade = config.TAMANHO_CARRO_LARGURA
                spawn_jitter = None

            faixa = {
                'y': y_faixa,
                'base_speed': velocidade_base,
                'direcao': direcao,
                'cor': random.choice(config.CORES_CARROS),
                'spawn_rate': spawn_rate,
                'min_gap': min_gap,
                'entity': entidade,
                'entity_width': largura_entidade,
                'spawn_jitter': spawn_jitter,
                'tipo': 'road'
            }
            parametros = self.obter_parametros_lane(faixa)
            faixa['velocidade'] = parametros['velocidade']

            faixas.append(faixa)
        
        altura_total = num_faixas * altura_faixa
        
        chunk = Chunk(
            y_inicio=y_pos,
            tipo='estrada',
            dados={
                'altura': altura_total,
                'faixas': faixas,
                'num_faixas': num_faixas
            }
        )
        
        self.chunks.append(chunk)
        self.proximo_y = y_pos + altura_total
        self.contador_desafios += 1
        
        return chunk
    
    def gerar_grupo_rio(self, y_pos, num_faixas=None, garantir_tronco_centro=False):
        """
        Gera um grupo de faixas de rio com plataformas
        
        Args:
            y_pos: Posição Y inicial
            num_faixas: Número de faixas (2-3 se None)
            
        Returns:
            Chunk: Chunk com dados do rio
        """
        if num_faixas is None:
            num_faixas = random.randint(2, 3)
        
        altura_faixa = 32  # 1 célula (32px) - alinhado ao grid moderno
        plataformas = []
        faixas_rio = []
        
        for i in range(num_faixas):
            y_faixa = y_pos + (i * altura_faixa)
            lane_config = self._obter_lane_config('river')

            if lane_config:
                velocidade_base = lane_config.get('speed', 2.0)
                direcao = lane_config.get('dir', random.choice([1, -1]))
                spawn_rate = lane_config.get('spawn_rate', 3.0)
                min_gap = lane_config.get('min_gap', 192)
                largura_padrao = lane_config.get('width', 4 * config.TAMANHO_CELL)
                spawn_jitter = lane_config.get('spawn_jitter')
                gerar_plataformas = False
            else:
                velocidade_base = random.uniform(1.5, 3.5)
                direcao = random.choice([1, -1])
                spawn_rate = 3.0
                min_gap = 6 * config.TAMANHO_CELL
                largura_padrao = random.choice([
                    3 * config.TAMANHO_CELL,
                    4 * config.TAMANHO_CELL,
                    6 * config.TAMANHO_CELL
                ])
                spawn_jitter = None
                gerar_plataformas = True

            faixa_rio = {
                'y': y_faixa,
                'base_speed': velocidade_base,
                'direcao': direcao,
                'spawn_rate': spawn_rate,
                'min_gap': min_gap,
                'entity': 'tronco',
                'entity_width': largura_padrao,
                'spawn_jitter': spawn_jitter,
                'tipo': 'river'
            }

            parametros = self.obter_parametros_lane(faixa_rio)
            faixa_rio['velocidade'] = parametros['velocidade']

            faixas_rio.append(faixa_rio)

            if not gerar_plataformas:
                continue

            # PRIMEIRA FAIXA: sempre garantir tronco no centro (onde jogador está)
            if i == 0 and garantir_tronco_centro:
                tipo_plataforma = 'tronco_garantido'
            else:
                # Gerar plataformas para esta faixa - APENAS TRONCOS (simples e claro)
                tipo_plataforma = 'tronco'  # Sempre troncos - sem complicação

            velocidade = faixa_rio['velocidade']

            if tipo_plataforma == 'tronco_garantido':
                # GARANTIR tronco grande e acessível no centro da tela (onde jogador está)
                num_troncos = random.randint(6, 8)  # Ainda mais troncos

                # Calcular posição do centro da tela ALINHADA AO GRID
                centro_cell = config.GRID_LARGURA // 2
                centro_tela = centro_cell * config.TAMANHO_CELL + config.TAMANHO_CELL // 2

                # GARANTIR pelo menos UM tronco grande no centro (múltiplo de TAMANHO_CELL)
                largura_central = 6 * config.TAMANHO_CELL  # 192px = 6 células
                tronco_central = Tronco(centro_tela, y_faixa, largura_central, velocidade, direcao)
                plataformas.append(tronco_central)

                # Gerar outros troncos ao redor (ALINHADOS AO GRID)
                posicoes_base = []
                espacamento_cells = config.GRID_LARGURA // (num_troncos + 1)
                for j in range(num_troncos - 1):  # -1 pois já criamos o central
                    x_cell = int((j + 1) * espacamento_cells) + random.randint(-1, 1)
                    x_cell = max(0, min(x_cell, config.GRID_LARGURA - 1))
                    pos_base = x_cell * config.TAMANHO_CELL + config.TAMANHO_CELL // 2

                    # Evitar sobreposição com o tronco central
                    if abs(pos_base - centro_tela) > 180:  # Distância segura (3 células)
                        posicoes_base.append(pos_base)

                for x_base in posicoes_base:
                    # Larguras sempre múltiplos de TAMANHO_CELL (3, 4 ou 6 células)
                    largura = random.choice([
                        3 * config.TAMANHO_CELL,  # 96px
                        4 * config.TAMANHO_CELL,  # 128px
                        6 * config.TAMANHO_CELL   # 192px
                    ])
                    tronco = Tronco(x_base, y_faixa, largura, velocidade, direcao)
                    plataformas.append(tronco)

            elif tipo_plataforma == 'tronco':
                # MAIS troncos (5-7) e sempre GRANDES
                num_troncos = random.randint(5, 7)

                # Distribuir uniformemente pela tela ALINHADO AO GRID
                posicoes_base = []
                espacamento_cells = config.GRID_LARGURA // (num_troncos + 1)
                for j in range(num_troncos):
                    # Posição alinhada ao grid com variação mínima
                    x_cell = int((j + 1) * espacamento_cells) + random.randint(-1, 1)
                    x_cell = max(0, min(x_cell, config.GRID_LARGURA - 1))
                    pos_base = x_cell * config.TAMANHO_CELL + config.TAMANHO_CELL // 2
                    posicoes_base.append(pos_base)

                # Ordenar para evitar sobreposição
                posicoes_base.sort()

                for j, x_base in enumerate(posicoes_base):
                    # SEMPRE troncos grandes - larguras múltiplas de TAMANHO_CELL (32px)
                    largura_opcoes = [
                        3 * config.TAMANHO_CELL,  # 96px
                        4 * config.TAMANHO_CELL,  # 128px
                        4 * config.TAMANHO_CELL,  # 128px (mais comum)
                        6 * config.TAMANHO_CELL,  # 192px
                        6 * config.TAMANHO_CELL   # 192px (mais comum)
                    ]
                    largura = random.choice(largura_opcoes)

                    # Ajustar posição se necessário para não sair da tela
                    if x_base + largura // 2 > config.LARGURA_TELA:
                        x_base = config.LARGURA_TELA - largura // 2
                        x_base = (x_base // config.TAMANHO_CELL) * config.TAMANHO_CELL + config.TAMANHO_CELL // 2
                    if x_base - largura // 2 < 0:
                        x_base = largura // 2
                        x_base = (x_base // config.TAMANHO_CELL) * config.TAMANHO_CELL + config.TAMANHO_CELL // 2

                    tronco = Tronco(x_base, y_faixa, largura, velocidade, direcao)
                    plataformas.append(tronco)
            
            # Tipo 'misto' removido - apenas troncos agora
            
            # Lilypads removidos - apenas troncos para simplicidade
        
        altura_total = num_faixas * altura_faixa
        
        chunk = Chunk(
            y_inicio=y_pos,
            tipo='rio',
            dados={
                'altura': altura_total,
                'faixas': faixas_rio,
                'plataformas': plataformas,
                'num_faixas': num_faixas
            }
        )
        
        self.chunks.append(chunk)
        self.proximo_y = y_pos + altura_total
        self.contador_desafios += 1
        
        return chunk
    
    def gerar_proximo_chunk(self):
        """
        Gera o próximo chunk (área de descanso, rio ou grupo de faixas)
        Gera para baixo (Y aumenta) - usado na inicialização
        
        Returns:
            Chunk ou SafeZone: Elemento gerado
        """
        # Verificar se deve gerar área de descanso
        if self.deve_gerar_area_descanso():
            return self.gerar_area_descanso(self.proximo_y)
        else:
            # Decidir entre estrada ou rio (50/50 para mais variedade)
            if random.random() < 0.5:
                return self.gerar_grupo_faixas(self.proximo_y)
            else:
                return self.gerar_grupo_rio(self.proximo_y)
    
    def gerar_proximo_chunk_invertido(self, y_pos):
        """
        Gera chunk acima (Y diminui) - usado durante o jogo
        
        Args:
            y_pos: Posição Y onde termina o chunk anterior
            
        Returns:
            Chunk: Chunk gerado
        """
        # Verificar se deve gerar área de descanso
        if self.deve_gerar_area_descanso():
            # Calcular posição acima
            altura = config.ALTURA_AREA_DESCANSO
            y_inicio = y_pos - altura
            safe_zone = SafeZone(y_inicio, altura)
            self.safe_zones.append(safe_zone)
            
            chunk = Chunk(
                y_inicio=y_inicio,
                tipo='safe_zone',
                dados={
                    'altura': altura,
                    'safe_zone': safe_zone
                }
            )
            self.chunks.append(chunk)
            
            # Variar o intervalo
            self.ultimo_intervalo = config.INTERVALO_DESAFIOS_PARA_DESCANSO + \
                                    random.randint(0, config.VARIACAO_INTERVALO_DESAFIOS)
            
            # Safe zone não muda o ultimo_tipo - mantém o anterior para continuar a sequência
            # (ex: se último foi estrada, após safe zone pode ir para rio)
            
            return chunk
        else:
            # Decidir entre estrada ou rio
            # SEMPRE adicionar grama entre estrada e rio
            precisa_grama = False
            if self.ultimo_tipo == 'estrada':
                # Último foi estrada, próximo deve ser rio OU grama
                proximo_tipo = 'rio'
                precisa_grama = True
            elif self.ultimo_tipo == 'rio':
                # Último foi rio, próximo deve ser estrada OU grama
                proximo_tipo = 'estrada'
                precisa_grama = True
            else:
                # Primeiro chunk ou grama, pode ser qualquer coisa
                if random.random() < 0.5:
                    proximo_tipo = 'estrada'
                else:
                    proximo_tipo = 'rio'
            
            # Se precisa grama, gerar primeiro
            if precisa_grama:
                altura_grama = config.ALTURA_AREA_DESCANSO
                y_grama = y_pos - altura_grama
                safe_zone = SafeZone(y_grama, altura_grama)
                self.safe_zones.append(safe_zone)
                
                chunk_grama = Chunk(
                    y_inicio=y_grama,
                    tipo='safe_zone',
                    dados={
                        'altura': altura_grama,
                        'safe_zone': safe_zone
                    }
                )
                self.chunks.append(chunk_grama)
                y_pos = y_grama  # Atualizar posição para gerar próximo chunk acima
            
            # Gerar estrada ou rio
            if proximo_tipo == 'estrada':
                # Estrada
                num_faixas = random.randint(2, 3)
                altura = num_faixas * 60
                y_inicio = y_pos - altura
                
                faixas = []
                for i in range(num_faixas):
                    y_faixa = y_inicio + (i * 60)
                    lane_config = self._obter_lane_config('road')

                    if lane_config:
                        velocidade_base = lane_config.get('speed', 3.0)
                        direcao = lane_config.get('dir', random.choice([1, -1]))
                        spawn_rate = lane_config.get('spawn_rate', 2.5)
                        min_gap = lane_config.get('min_gap', config.TAMANHO_CARRO_LARGURA * 2)
                        entidade = lane_config.get('entity', 'car')
                        largura_entidade = lane_config.get('width', config.TAMANHO_CARRO_LARGURA)
                        spawn_jitter = lane_config.get('spawn_jitter')
                    else:
                        velocidade_base = random.uniform(2.0, 4.5)
                        direcao = random.choice([1, -1])
                        spawn_rate = 2.5
                        min_gap = config.TAMANHO_CARRO_LARGURA * 2
                        entidade = 'car'
                        largura_entidade = config.TAMANHO_CARRO_LARGURA
                        spawn_jitter = None

                    faixa = {
                        'y': y_faixa,
                        'base_speed': velocidade_base,
                        'direcao': direcao,
                        'cor': random.choice(config.CORES_CARROS),
                        'spawn_rate': spawn_rate,
                        'min_gap': min_gap,
                        'entity': entidade,
                        'entity_width': largura_entidade,
                        'spawn_jitter': spawn_jitter,
                        'tipo': 'road'
                    }

                    parametros = self.obter_parametros_lane(faixa)
                    faixa['velocidade'] = parametros['velocidade']

                    faixas.append(faixa)
                
                chunk = Chunk(
                    y_inicio=y_inicio,
                    tipo='estrada',
                    dados={
                        'altura': altura,
                        'faixas': faixas,
                        'num_faixas': num_faixas
                    }
                )
                self.chunks.append(chunk)
                self.contador_desafios += 1
                self.ultimo_tipo = 'estrada'
                return chunk
            else:
                # Rio
                num_faixas = random.randint(2, 3)
                altura = num_faixas * 60
                y_inicio = y_pos - altura
                
                plataformas = []
                faixas_rio = []
                
                for i in range(num_faixas):
                    y_faixa = y_inicio + (i * 60)
                    lane_config = self._obter_lane_config('river')

                    if lane_config:
                        velocidade_base = lane_config.get('speed', 2.0)
                        direcao = lane_config.get('dir', random.choice([1, -1]))
                        spawn_rate = lane_config.get('spawn_rate', 3.0)
                        min_gap = lane_config.get('min_gap', 192)
                        largura_padrao = lane_config.get('width', 4 * config.TAMANHO_CELL)
                        spawn_jitter = lane_config.get('spawn_jitter')
                        gerar_plataformas = False
                    else:
                        velocidade_base = random.uniform(1.5, 3.5)
                        direcao = random.choice([1, -1])
                        spawn_rate = 3.0
                        min_gap = 6 * config.TAMANHO_CELL
                        largura_padrao = random.choice([
                            3 * config.TAMANHO_CELL,
                            4 * config.TAMANHO_CELL,
                            6 * config.TAMANHO_CELL
                        ])
                        spawn_jitter = None
                        gerar_plataformas = True

                    faixa_rio = {
                        'y': y_faixa,
                        'base_speed': velocidade_base,
                        'direcao': direcao,
                        'spawn_rate': spawn_rate,
                        'min_gap': min_gap,
                        'entity': 'tronco',
                        'entity_width': largura_padrao,
                        'spawn_jitter': spawn_jitter,
                        'tipo': 'river'
                    }

                    parametros = self.obter_parametros_lane(faixa_rio)
                    faixa_rio['velocidade'] = parametros['velocidade']

                    faixas_rio.append(faixa_rio)

                    if not gerar_plataformas:
                        continue

                    # Gerar plataformas - APENAS TRONCOS (sistema simplificado)
                    # MAIS troncos (5-7) e sempre GRANDES
                    num_troncos = random.randint(5, 7)

                    # Distribuir uniformemente pela tela (menos gaps)
                    posicoes_base = []
                    espacamento_base = config.LARGURA_TELA / (num_troncos + 1)
                    for j in range(num_troncos):
                        # Posição mais uniforme (menos variação)
                        pos_base = (j + 1) * espacamento_base + random.randint(-20, 20)
                        # Alinhar ao grid
                        pos_base = (pos_base // config.TAMANHO_CELL) * config.TAMANHO_CELL + config.TAMANHO_CELL // 2
                        posicoes_base.append(pos_base)

                    # Ordenar para evitar sobreposição
                    posicoes_base.sort()

                    velocidade = faixa_rio['velocidade']

                    for j, x_base in enumerate(posicoes_base):
                        # SEMPRE troncos grandes (múltiplos de TAMANHO_CELL)
                        largura_opcoes = [
                            3 * config.TAMANHO_CELL,  # 96px
                            4 * config.TAMANHO_CELL,  # 128px
                            4 * config.TAMANHO_CELL,  # 128px (mais comum)
                            6 * config.TAMANHO_CELL,  # 192px
                            6 * config.TAMANHO_CELL   # 192px (mais comum)
                        ]
                        largura = random.choice(largura_opcoes)

                        # Ajustar posição se necessário para não sair da tela
                        if x_base + largura // 2 > config.LARGURA_TELA:
                            x_base = config.LARGURA_TELA - largura // 2
                            x_base = (x_base // config.TAMANHO_CELL) * config.TAMANHO_CELL + config.TAMANHO_CELL // 2
                        if x_base - largura // 2 < 0:
                            x_base = largura // 2
                            x_base = (x_base // config.TAMANHO_CELL) * config.TAMANHO_CELL + config.TAMANHO_CELL // 2

                        tronco = Tronco(x_base, y_faixa, largura, velocidade, direcao)
                        plataformas.append(tronco)
                
                chunk = Chunk(
                    y_inicio=y_inicio,
                    tipo='rio',
                    dados={
                        'altura': altura,
                        'faixas': faixas_rio,
                        'plataformas': plataformas,
                        'num_faixas': num_faixas
                    }
                )
                self.chunks.append(chunk)
                self.contador_desafios += 1
                self.ultimo_tipo = 'rio'
                return chunk
    
    def atualizar(self, camera_offset):
        """
        Atualiza o gerador (remove chunks antigos, gera novos)

        Args:
            camera_offset: Offset atual da câmera
        """
        # Atualizar distância percorrida (quanto mais alto, maior a distância)
        self.distancia_percorrida = max(0, -camera_offset)

        # Remover chunks que saíram da tela (atrás da câmera, abaixo do jogador)
        # Usar margem maior para cleanup mais agressivo
        margem_cleanup = 400
        chunks_para_remover = []
        chunks_para_manter = []

        for c in self.chunks:
            if c.y_inicio < camera_offset + config.ALTURA_TELA + margem_cleanup:
                chunks_para_manter.append(c)
            else:
                chunks_para_remover.append(c)

        # Reciclar chunks removidos no pool (otimização de memória)
        for chunk in chunks_para_remover:
            if len(self.chunk_pool) < self.max_pool_size:
                # Limpar dados do chunk antes de adicionar ao pool
                chunk.dados.clear()
                self.chunk_pool.append(chunk)

        self.chunks = chunks_para_manter

        # Remover safe zones antigas com mesma margem
        self.safe_zones = [sz for sz in self.safe_zones
                          if sz.y_pos < camera_offset + config.ALTURA_TELA + margem_cleanup]
        
        # Gerar novos chunks à frente se necessário
        # O jogador vai "subir" (Y diminui), então geramos chunks com Y menor
        limite_geracao = camera_offset - config.DISTANCIA_GERACAO_CHUNK
        
        chunks_gerados = 0
        while self.proximo_y > limite_geracao and chunks_gerados < 50:
            # Gerar chunk acima (Y menor)
            chunk = self.gerar_proximo_chunk_invertido(self.proximo_y)
            if chunk:
                self.proximo_y = chunk.y_inicio
                chunks_gerados += 1
            else:
                break  # Evitar loop infinito
        
        # Atualizar dificuldade baseado na distância percorrida
        # Quanto mais o jogador sobe (Y diminui), maior a dificuldade
        progresso = max(0, config.ALTURA_TELA - camera_offset)
        self.distancia_percorrida = progresso

        # Dificuldade com limite máximo (evita velocidades impossíveis)
        dificuldade_base = 1.0 + (progresso / 2000) * 0.3
        # Limitar dificuldade máxima a 2.5x (configurável em config.py)
        dificuldade_max = getattr(config, 'DIFICULDADE_MAXIMA', 2.5)
        self.dificuldade_atual = min(dificuldade_base, dificuldade_max)
    
    def obter_faixas_visiveis(self, camera_offset):
        """
        Retorna as faixas visíveis na tela
        
        Args:
            camera_offset: Offset da câmera
            
        Returns:
            list: Lista de faixas visíveis
        """
        faixas_visiveis = []
        
        y_min = camera_offset - 100
        y_max = camera_offset + config.ALTURA_TELA + 100
        
        for chunk in self.chunks:
            if chunk.tipo == 'estrada':
                # Verificar se chunk está visível
                if chunk.y_inicio <= y_max and chunk.y_fim >= y_min:
                    faixas_visiveis.extend(chunk.dados.get('faixas', []))

        return faixas_visiveis

    def obter_faixas_rio_visiveis(self, camera_offset):
        """Retorna as faixas de rio visíveis na tela."""
        faixas_visiveis = []

        y_min = camera_offset - 100
        y_max = camera_offset + config.ALTURA_TELA + 100

        for chunk in self.chunks:
            if chunk.tipo == 'rio':
                if chunk.y_inicio <= y_max and chunk.y_fim >= y_min:
                    faixas_visiveis.extend(chunk.dados.get('faixas', []))

        return faixas_visiveis
    
    def obter_safe_zones_visiveis(self, camera_offset):
        """
        Retorna as safe zones visíveis
        
        Args:
            camera_offset: Offset da câmera
            
        Returns:
            list: Lista de SafeZones visíveis
        """
        y_min = camera_offset
        y_max = camera_offset + config.ALTURA_TELA
        
        visiveis = []
        for sz in self.safe_zones:
            if sz.y_pos <= y_max and sz.y_pos + sz.altura >= y_min:
                visiveis.append(sz)
        
        return visiveis
    
    def obter_plataformas_visiveis(self, camera_offset):
        """
        Retorna as plataformas do rio visíveis
        
        Args:
            camera_offset: Offset da câmera
            
        Returns:
            list: Lista de plataformas (apenas Tronco)
        """
        y_min = camera_offset - 100
        y_max = camera_offset + config.ALTURA_TELA + 100
        
        plataformas = []
        for chunk in self.chunks:
            if chunk.tipo == 'rio':
                # Verificar se chunk está visível
                if chunk.y_inicio <= y_max and chunk.y_fim >= y_min:
                    plataformas.extend(chunk.dados.get('plataformas', []))
        
        return plataformas
    
    def obter_chunks_visiveis(self, camera_offset):
        """
        Retorna todos os chunks visíveis
        
        Args:
            camera_offset: Offset da câmera
            
        Returns:
            list: Lista de chunks visíveis
        """
        y_min = camera_offset - 100
        y_max = camera_offset + config.ALTURA_TELA + 100
        
        visiveis = []
        for chunk in self.chunks:
            if chunk.y_inicio <= y_max and chunk.y_fim >= y_min:
                visiveis.append(chunk)
        
        return visiveis
    
    def resetar(self):
        """Reseta o gerador para estado inicial"""
        self.chunks = []
        self.safe_zones = []
        self.proximo_y = 0
        self.contador_desafios = 0
        self.distancia_percorrida = 0
        self.dificuldade_atual = 1.0
        self.ultimo_intervalo = config.INTERVALO_DESAFIOS_PARA_DESCANSO
        self.ultimo_tipo = None
        self.road_lane_index = 0
        self.river_lane_index = 0
    
    def inicializar_mundo_inicial(self):
        """Gera os chunks iniciais do mundo"""
        # Começar do final da tela, alinhado ao grid
        # Jogador spawna em y = ALTURA_TELA - 80, que é aproximadamente grid_y = 11 ou 12
        # Safe zone inicial deve estar abaixo do jogador
        
        # Calcular posição da safe zone inicial alinhada ao grid
        # Queremos que cubra da parte inferior até onde o jogador está
        altura_grama_inicial = config.TAMANHO_CELL * 6  # 6 células = 192px (múltiplo de 32)
        y_grama_inicial = config.ALTURA_TELA - altura_grama_inicial
        
        safe_zone_inicial = SafeZone(y_grama_inicial, altura_grama_inicial)
        self.safe_zones.append(safe_zone_inicial)
        
        self.proximo_y = y_grama_inicial
        
        chunk_grama_inicial = Chunk(
            y_inicio=y_grama_inicial,
            tipo='safe_zone',
            dados={
                'altura': altura_grama_inicial,
                'safe_zone': safe_zone_inicial
            }
        )
        self.chunks.append(chunk_grama_inicial)
        self.proximo_y = y_grama_inicial
        
        # Gerar chunks para cima (Y diminui) para preencher a tela e além
        for i in range(20):  # Mais chunks iniciais para preencher tela maior
            chunk = self.gerar_proximo_chunk_invertido(self.proximo_y)
            if chunk:
                self.proximo_y = chunk.y_inicio
    
    def __repr__(self):
        return f"ProceduralGenerator(chunks={len(self.chunks)}, desafios={self.contador_desafios})"

