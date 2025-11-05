#!/usr/bin/env python3
"""
🐸 ATRAVESSAR A RUA v2.0 - Um jogo inspirado em Frogger 🐸
Versão melhorada usando Pygame-CE - Biblioteca moderna e compatível

Objetivo: Atravesse a rua cheia de carros sem ser atingido!
Controles: Setas do teclado (↑ ↓ ← →) ou WASD
"""

import pygame
import random
import sys
import time

import config
from entities import Jogador, Carro, SafeZone, Tronco
from game import GameState, CollisionSystem, Camera, ProceduralGenerator, RiverPhysics
from ui import Menu, HUD, GameOverScreen


class JogoAtraversarRua:
    """Classe principal que gerencia todo o jogo"""

    def __init__(self, seed=config.DEFAULT_SEED):
        # Configuração da tela (pygame já foi inicializado em main())
        try:
            self.tela_cheia = False
            self.screen = pygame.display.set_mode((config.LARGURA_TELA, config.ALTURA_TELA))
            pygame.display.set_caption(config.TITULO)
            self.clock = pygame.time.Clock()
            self.delta_time = 0.0  # Delta time para física frame-independent
        except Exception as e:
            raise RuntimeError(f"Falha ao criar janela do jogo: {e}")
        
        # Garantir que fontes estão inicializadas
        if not pygame.font.get_init():
            pygame.font.init()
        
        # Fontes
        try:
            self.font_grande = pygame.font.Font(None, 72)
            self.font_media = pygame.font.Font(None, 48)
            self.font_pequena = pygame.font.Font(None, 32)
        except Exception as e:
            raise RuntimeError(f"Falha ao criar fontes: {e}")
        
        # Sistema de aleatoriedade
        if isinstance(seed, random.Random):
            self.rng = seed
        elif seed is None:
            self.rng = random.Random()
        else:
            self.rng = random.Random(seed)

        # Estado do jogo
        self.estado = GameState.MENU
        self.pontuacao = 0
        self.nivel = 1
        self.vidas = config.VIDAS_INICIAIS
        self.tempo_inicio = 0
        self.melhor_pontuacao = 0
        self.melhor_nivel = 1

        # Controle de progressão/dificuldade
        self.marcos_tempo_dificuldade = 0
        self.tempo_total_partida = 0.0

        # Sprites
        self.jogador = None
        self.carros_group = pygame.sprite.Group()

        # Cache de grid visual (otimização de renderização)
        self.grid_cache = None
        self.criar_cache_grid()
        
        # UI
        self.menu = Menu(self.screen, self.font_grande, self.font_media, self.font_pequena)
        self.hud = HUD(self.screen, self.font_pequena)
        self.game_over_screen = GameOverScreen(self.screen, self.font_grande, self.font_media, self.font_pequena)
        
        # Sistema de colisão
        self.collision_system = CollisionSystem()
        
        # Sistema de câmera e geração procedimental
        self.camera = Camera()
        self.procedural_generator = ProceduralGenerator(rng=self.rng)
        self.river_physics = RiverPhysics()

        # Controle de área de descanso
        self.jogador_em_safe_zone = False
        self.tempo_em_safe_zone = 0.0  # Tempo acumulado em safe zone

        # Sistema de invulnerabilidade
        self.invulneravel = False
        self.tempo_invulnerabilidade = 0.0
        self.duracao_invulnerabilidade = 2.0  # 2 segundos de invulnerabilidade
        
        # Grupos de sprites para rio
        self.plataformas_group = pygame.sprite.Group()

        # Gerenciamento dos spawners por faixa
        self.lane_spawners = {}

        # Não inicializar jogo ainda (será inicializado quando começar a jogar)

    def alternar_tela_cheia(self):
        """Alterna entre modo janela e tela cheia"""
        self.tela_cheia = not self.tela_cheia
        
        try:
            if self.tela_cheia:
                # Tela cheia - manter resolução do jogo mas em fullscreen
                self.screen = pygame.display.set_mode(
                    (config.LARGURA_TELA, config.ALTURA_TELA),
                    pygame.FULLSCREEN | pygame.SCALED  # SCALED mantém proporção
                )
                print("[INFO] Modo tela cheia ativado (scaled)")
            else:
                # Modo janela
                self.screen = pygame.display.set_mode(
                    (config.LARGURA_TELA, config.ALTURA_TELA)
                )
                print("[INFO] Modo janela ativado")
            
            # Recriar UI com nova tela (mantém mesmas dimensões)
            self.menu = Menu(self.screen, self.font_grande, self.font_media, self.font_pequena)
            self.hud = HUD(self.screen, self.font_pequena)
            self.game_over_screen = GameOverScreen(self.screen, self.font_grande, self.font_media, self.font_pequena)

            # Recriar cache de grid
            self.criar_cache_grid()
        except Exception as e:
            print(f"[ERRO] Falha ao alternar tela cheia: {e}")
            # Reverter para modo janela em caso de erro
            self.tela_cheia = False
            self.screen = pygame.display.set_mode(
                (config.LARGURA_TELA, config.ALTURA_TELA)
            )
    
    def iniciar_novo_jogo(self):
        """Inicia um novo jogo do zero"""
        # Resetar pontuação e estado
        self.pontuacao = 0
        self.nivel = 1
        self.vidas = config.VIDAS_INICIAIS
        self.marcos_tempo_dificuldade = 0
        self.tempo_total_partida = 0.0

        # Inicializar jogo
        self.inicializar_jogo()

        # Mudar estado e iniciar tempo
        self.estado = GameState.PLAYING
        self.tempo_inicio = time.time()

    def inicializar_jogo(self):
        """Inicializa ou reinicia o jogo (sem resetar pontuação)"""
        # Limpar sprites
        self.carros_group.empty()
        self.plataformas_group.empty()
        self.lane_spawners.clear()

        # Resetar sistemas
        self.camera.resetar()
        self.procedural_generator.resetar()
        self.river_physics.resetar()

        # Ajustar dificuldade atual antes de gerar o mundo
        self.procedural_generator.atualizar_dificuldade(self.nivel, self.marcos_tempo_dificuldade)

        # Inicializar mundo procedimental
        self.procedural_generator.inicializar_mundo_inicial()

        # Criar jogador alinhado ao centro horizontal e na parte inferior
        # Posição Y alinhada ao grid: 4 células do fundo (grid perfeito)
        grid_y_inicial = config.GRID_ALTURA - 4
        y_inicial_jogador = grid_y_inicial * config.TAMANHO_CELL + config.TAMANHO_CELL // 2
        x_inicial_jogador = (config.GRID_LARGURA // 2) * config.TAMANHO_CELL + config.TAMANHO_CELL // 2
        self.jogador = Jogador(x_inicial_jogador, y_inicial_jogador)

        # Atualizar câmera imediatamente após criar jogador
        self.camera.update(self.jogador)

        # Não criar carros estáticos mais - serão gerados proceduralmente

    def _criar_carro_para_faixa(self, faixa, x_pos=None):
        """Cria um carro alinhado a uma faixa configurada."""
        if x_pos is None:
            if faixa['direcao'] == 1:
                x_pos = -config.TAMANHO_CARRO_LARGURA
            else:
                x_pos = config.LARGURA_TELA + config.TAMANHO_CARRO_LARGURA

        carro = Carro(
            x_pos,
            faixa['y'],
            faixa['velocidade'],
            faixa.get('cor', config.VERMELHO),
            faixa['direcao']
        )
        carro.lane_id = faixa.get('id')
        carro.base_velocidade = faixa.get('velocidade_base', faixa['velocidade'])
        carro.spawn_intervalo_base = faixa.get('spawn_interval_base')
        self.carros_group.add(carro)
        return carro

    def _spawn_carros_iniciais(self, faixa, carros_lane):
        quantidade = max(0, faixa.get('spawn_inicial', config.CARROS_POR_FAIXA_INICIAL))
        if quantidade <= 0:
            return

        espacamento = config.LARGURA_TELA // (quantidade + 1)
        for i in range(quantidade):
            x_pos = (i + 1) * espacamento + self.rng.randint(-config.TAMANHO_CELL, config.TAMANHO_CELL)
            x_pos = max(config.TAMANHO_CELL // 2, min(x_pos, config.LARGURA_TELA - config.TAMANHO_CELL // 2))
            if faixa['direcao'] == -1:
                x_pos = config.LARGURA_TELA - x_pos
            x_pos = (x_pos // config.TAMANHO_CELL) * config.TAMANHO_CELL + config.TAMANHO_CELL // 2
            carro = self._criar_carro_para_faixa(faixa, x_pos=x_pos)
            carros_lane.append(carro)

    def atualizar_carros_procedurais(self):
        """Atualiza carros baseados nas faixas geradas proceduralmente"""
        faixas_visiveis = self.procedural_generator.obter_faixas_visiveis(self.camera.offset_y)
        tempo_atual = self.tempo_total_partida
        lanes_ativos = set(self.procedural_generator.lanes.keys())

        # Limpar spawners/carros de faixas removidas
        for lane_id in list(self.lane_spawners.keys()):
            if lane_id not in lanes_ativos:
                del self.lane_spawners[lane_id]

        for carro in list(self.carros_group):
            lane_id = getattr(carro, 'lane_id', None)
            if lane_id is not None and lane_id not in lanes_ativos:
                carro.kill()

        carros_por_lane = {}
        for carro in self.carros_group:
            lane_id = getattr(carro, 'lane_id', None)
            if lane_id is None:
                continue
            carros_por_lane.setdefault(lane_id, []).append(carro)

        for faixa in faixas_visiveis:
            lane_id = faixa.get('id')
            if lane_id is None:
                continue

            spawner = self.lane_spawners.get(lane_id)
            intervalo_faixa = faixa.get('spawn_interval', 1.5)

            if not spawner:
                proximo_spawn = tempo_atual + self.rng.uniform(0.1, max(0.2, intervalo_faixa))
                spawner = {
                    'intervalo': intervalo_faixa,
                    'proximo_spawn': proximo_spawn,
                }
                self.lane_spawners[lane_id] = spawner
                carros_lane = carros_por_lane.setdefault(lane_id, [])
                self._spawn_carros_iniciais(faixa, carros_lane)
            else:
                spawner['intervalo'] = intervalo_faixa
                spawner['proximo_spawn'] = min(spawner['proximo_spawn'], tempo_atual + spawner['intervalo'])
                carros_lane = carros_por_lane.setdefault(lane_id, [])

            limite_carros = faixa.get('max_carros', config.CARROS_POR_FAIXA_MAX)
            if len(carros_lane) < limite_carros and tempo_atual >= spawner['proximo_spawn']:
                carro = self._criar_carro_para_faixa(faixa)
                carros_lane.append(carro)
                spawner['proximo_spawn'] = tempo_atual + spawner['intervalo']

        # Remover carros que saíram da área visível
        y_min, y_max = self.camera.obter_area_visivel()
        for carro in list(self.carros_group):
            if carro.rect.centery < y_min - 120 or carro.rect.centery > y_max + 120:
                carro.kill()

    def _aplicar_dificuldade(self):
        """Aplica os multiplicadores atuais de dificuldade aos spawners e entidades."""
        ratio_vel = self.procedural_generator.atualizar_dificuldade(
            self.nivel,
            self.marcos_tempo_dificuldade
        )

        tempo_atual = self.tempo_total_partida

        # Atualizar intervalos dos spawners existentes
        for lane_id in list(self.lane_spawners.keys()):
            faixa = self.procedural_generator.obter_faixa_por_id(lane_id)
            if not faixa:
                del self.lane_spawners[lane_id]
                continue

            intervalo = faixa.get('spawn_interval', self.lane_spawners[lane_id]['intervalo'])
            self.lane_spawners[lane_id]['intervalo'] = intervalo
            self.lane_spawners[lane_id]['proximo_spawn'] = min(
                self.lane_spawners[lane_id]['proximo_spawn'],
                tempo_atual + intervalo
            )

        # Atualizar carros existentes
        for carro in self.carros_group:
            lane_id = getattr(carro, 'lane_id', None)
            if lane_id is None:
                continue
            faixa = self.procedural_generator.obter_faixa_por_id(lane_id)
            if not faixa:
                continue
            carro.base_velocidade = faixa.get('velocidade_base', carro.velocidade)
            carro.velocidade = faixa.get('velocidade', carro.velocidade)

        # Atualizar plataformas (troncos) existentes
        for chunk in self.procedural_generator.chunks:
            if chunk.tipo != 'rio':
                continue
            for plataforma in chunk.dados.get('plataformas', []):
                base = getattr(plataforma, 'base_velocidade', None)
                if base is None and ratio_vel:
                    plataforma.base_velocidade = plataforma.velocidade / ratio_vel
                if hasattr(plataforma, 'base_velocidade'):
                    plataforma.velocidade = plataforma.base_velocidade * self.procedural_generator.dificuldade_atual

    def _atualizar_progressao_dificuldade(self):
        """Atualiza nível e marcos temporais e aplica dificuldade quando necessário."""
        dificuldade_alterada = False

        distancia = self.procedural_generator.distancia_percorrida
        nivel_por_distancia = config.calcular_nivel_por_distancia(distancia)
        if nivel_por_distancia > self.nivel:
            self.nivel = nivel_por_distancia
            self.melhor_nivel = max(self.melhor_nivel, self.nivel)
            dificuldade_alterada = True

        max_marcos = getattr(config, 'MAX_MARCOS_TEMPO', 0)
        while self.tempo_total_partida >= (self.marcos_tempo_dificuldade + 1) * config.DIFICULDADE_INTERVALO_TEMPO:
            if max_marcos and self.marcos_tempo_dificuldade >= max_marcos:
                break
            self.marcos_tempo_dificuldade += 1
            dificuldade_alterada = True

        if dificuldade_alterada:
            self._aplicar_dificuldade()
    
    def verificar_safe_zone(self):
        """Verifica se o jogador está em uma área de descanso"""
        if self.jogador is None:
            return

        safe_zones = self.procedural_generator.obter_safe_zones_visiveis(self.camera.offset_y)

        estava_em_safe_zone = self.jogador_em_safe_zone
        self.jogador_em_safe_zone = False

        for sz in safe_zones:
            if sz.colidir_com_jogador(self.jogador):
                self.jogador_em_safe_zone = True
                break

        # Sistema de safe zone - recuperar vida se ficar tempo suficiente
        if self.jogador_em_safe_zone:
            self.tempo_em_safe_zone += self.delta_time
            # A cada 5 segundos em safe zone, recupera 1 vida (máximo de VIDAS_MAXIMAS)
            if self.tempo_em_safe_zone >= 5.0 and self.vidas < config.VIDAS_MAXIMAS:
                self.vidas += 1
                self.tempo_em_safe_zone = 0.0
        else:
            self.tempo_em_safe_zone = 0.0

        # Feedback visual
        if self.jogador_em_safe_zone and not estava_em_safe_zone:
            # Entrou em safe zone - poderia adicionar som/efeito visual
            pass
        elif not self.jogador_em_safe_zone and estava_em_safe_zone:
            # Saiu de safe zone
            pass

    def processar_eventos(self):
        """Processa eventos do pygame"""
        eventos = pygame.event.get()
        
        for evento in eventos:
            if evento.type == pygame.QUIT:
                return False
            
            if evento.type == pygame.KEYDOWN:
                # F11 para alternar tela cheia
                if evento.key == pygame.K_F11:
                    self.alternar_tela_cheia()
                
                if evento.key == pygame.K_ESCAPE:
                    if self.estado == GameState.MENU:
                        return False
                    else:
                        self.estado = GameState.MENU
                
                if evento.key == pygame.K_SPACE:
                    if self.estado == GameState.MENU:
                        self.iniciar_novo_jogo()
                    elif self.estado == GameState.GAME_OVER:
                        self.iniciar_novo_jogo()
        
        # Processar menu se estiver no menu
        if self.estado == GameState.MENU:
            acao = self.menu.processar_eventos(eventos)
            if acao == 'jogar':
                self.iniciar_novo_jogo()
            elif acao == 'sair':
                return False
            elif acao == 'config':
                # TODO: Implementar menu de configurações
                pass
        
        # Processar game over
        elif self.estado == GameState.GAME_OVER:
            acao = self.game_over_screen.processar_eventos(eventos)
            if acao == 'jogar':
                self.iniciar_novo_jogo()
            elif acao == 'menu':
                self.estado = GameState.MENU
        
        # Processar movimento discreto (grid-based) durante o jogo
        if self.estado == GameState.PLAYING and self.jogador is not None:
            for evento in eventos:
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_UP or evento.key == pygame.K_w:
                        self.jogador.mover(0, -1)
                    elif evento.key == pygame.K_DOWN or evento.key == pygame.K_s:
                        self.jogador.mover(0, 1)
                    elif evento.key == pygame.K_LEFT or evento.key == pygame.K_a:
                        self.jogador.mover(-1, 0)
                    elif evento.key == pygame.K_RIGHT or evento.key == pygame.K_d:
                        self.jogador.mover(1, 0)
        
        return True

    def atualizar_plataformas_procedurais(self):
        """Atualiza plataformas baseadas nos chunks de rio"""
        # Obter plataformas visíveis
        plataformas_visiveis = self.procedural_generator.obter_plataformas_visiveis(self.camera.offset_y)
        
        # Sincronizar grupo de sprites
        self.plataformas_group.empty()
        for plataforma in plataformas_visiveis:
            self.plataformas_group.add(plataforma)

    def atualizar(self):
        """Atualiza a lógica do jogo"""
        if self.estado == GameState.PLAYING:
            self.tempo_total_partida += self.delta_time

            # Atualizar jogador (animação) com delta time
            if self.jogador:
                self.jogador.atualizar(self.delta_time)

            # Atualizar câmera com delta time
            self.camera.update(self.jogador, self.delta_time)
            
            # Atualizar geração procedimental (CRÍTICO para mundo infinito)
            self.procedural_generator.atualizar(self.camera.offset_y)

            # Ajustar dificuldade de acordo com progresso e tempo
            self._atualizar_progressao_dificuldade()

            # Atualizar pontuação baseada em progresso (distância percorrida)
            distancia = int(self.procedural_generator.distancia_percorrida / 10)
            if distancia > self.pontuacao:
                self.pontuacao = distancia
            
            # Atualizar carros baseados nas faixas geradas
            self.atualizar_carros_procedurais()
            
            # Atualizar plataformas baseadas nos chunks de rio
            self.atualizar_plataformas_procedurais()
            
            # Atualizar carros existentes com delta time
            for carro in self.carros_group:
                carro.atualizar(self.delta_time)

            # Atualizar plataformas existentes com delta time
            for plataforma in self.plataformas_group:
                plataforma.atualizar(self.delta_time)
            
            # Verificar física do rio - TODOS os chunks de rio, não apenas visíveis
            chunks_rio = [c for c in self.procedural_generator.chunks if c.tipo == 'rio']
            status_rio = self.river_physics.atualizar(self.jogador, chunks_rio, self.delta_time)
            
            # Atualizar sistema de invulnerabilidade
            if self.invulneravel:
                self.tempo_invulnerabilidade += self.delta_time
                if self.tempo_invulnerabilidade >= self.duracao_invulnerabilidade:
                    self.invulneravel = False
                    self.tempo_invulnerabilidade = 0.0

            # Verificar se jogador está afogando (apenas se não estiver invulnerável)
            if status_rio['afogando'] and not self.invulneravel:
                self.vidas -= 1
                self.jogador.resetar_posicao()

                # Ativar invulnerabilidade
                self.invulneravel = True
                self.tempo_invulnerabilidade = 0.0

                if self.vidas <= 0:
                    self.estado = GameState.GAME_OVER
                    if self.pontuacao > self.melhor_pontuacao:
                        self.melhor_pontuacao = self.pontuacao
            
            # Verificar se jogador está em área de descanso
            self.verificar_safe_zone()
            
            # Verificar colisões
            self.verificar_colisoes()
            
            # Verificar vitória desabilitada - modo infinito ativo

    def verificar_colisoes(self):
        """Verifica colisões entre jogador e carros"""
        if self.jogador is None or self.invulneravel:
            return

        colisoes = self.collision_system.check_collision_pygame(
            self.jogador, self.carros_group
        )

        if colisoes:
            self.vidas -= 1
            self.jogador.resetar_posicao()

            # Ativar invulnerabilidade
            self.invulneravel = True
            self.tempo_invulnerabilidade = 0.0

            if self.vidas <= 0:
                self.estado = GameState.GAME_OVER
                if self.pontuacao > self.melhor_pontuacao:
                    self.melhor_pontuacao = self.pontuacao

    def verificar_vitoria(self):
        """Verifica se o jogador chegou ao topo"""
        if self.jogador is None:
            return
            
        if self.jogador.chegou_ao_topo():
            # Pontuação baseada no tempo
            tempo_decorrido = time.time() - self.tempo_inicio
            bonus_tempo = max(0, int(config.BONUS_TEMPO_MAX - tempo_decorrido * 10))
            self.pontuacao += config.PONTOS_BASE + bonus_tempo + (self.nivel * config.BONUS_NIVEL)

            # Próximo nível
            self.nivel += 1
            self.vidas = min(self.vidas + 1, config.VIDAS_MAXIMAS)
            self.inicializar_jogo()
            self.tempo_inicio = time.time()

    def criar_cache_grid(self):
        """Cria cache do grid visual para otimização de renderização"""
        # Grid muito discreto (cinza claro e bem transparente)
        cor_grid = (150, 150, 150, 40)  # Cinza claro com alpha baixo

        # Criar surface com alpha para transparência
        self.grid_cache = pygame.Surface((config.LARGURA_TELA, config.ALTURA_TELA), pygame.SRCALPHA)

        # Desenhar linhas verticais do grid (bem discretas)
        for x in range(0, config.LARGURA_TELA + 1, config.TAMANHO_CELL):
            pygame.draw.line(self.grid_cache, cor_grid, (x, 0), (x, config.ALTURA_TELA), 1)

    def desenhar_grid_visual(self):
        """Desenha o grid visual usando cache - OTIMIZADO"""
        # Usar cache de linhas verticais
        if self.grid_cache:
            self.screen.blit(self.grid_cache, (0, 0))

        # Desenhar apenas linhas horizontais dinamicamente (variam com câmera)
        cor_grid = (150, 150, 150, 40)
        y_min, y_max = self.camera.obter_area_visivel()

        for i in range(-5, 25):  # Linhas horizontais
            y_mundo = int(y_min) + (i * config.TAMANHO_CELL)
            y_tela = self.camera.aplicar_offset(y_mundo)
            if 0 <= y_tela <= config.ALTURA_TELA:
                pygame.draw.line(self.screen, cor_grid, (0, y_tela), (config.LARGURA_TELA, y_tela), 1)
    
    def desenhar_fundo(self):
        """Desenha o cenário do jogo com geração procedimental"""
        # Fundo base (céu)
        self.screen.fill(config.AZUL)
        
        # Obter área visível da câmera
        y_min, y_max = self.camera.obter_area_visivel()
        
        # Obter chunks visíveis
        chunks = self.procedural_generator.obter_chunks_visiveis(self.camera.offset_y)
        
        # Ordenar chunks por Y (do mais baixo para o mais alto)
        chunks_ordenados = sorted(chunks, key=lambda c: c.y_inicio)
        
        # Desenhar chunks na ordem (safe zones primeiro para não serem cobertas)
        for chunk in chunks_ordenados:
            y_tela_inicio = self.camera.aplicar_offset(chunk.y_inicio)
            y_tela_fim = self.camera.aplicar_offset(chunk.y_fim)
            
            if chunk.tipo == 'safe_zone':
                # Safe zone já tem seu próprio método de renderização
                safe_zone = chunk.dados.get('safe_zone')
                if safe_zone:
                    safe_zone.renderizar(self.screen, self.camera.offset_y)
            
            elif chunk.tipo == 'estrada':
                # Desenhar faixas de estrada
                faixas = chunk.dados.get('faixas', [])
                for faixa in faixas:
                    y_tela = self.camera.aplicar_offset(faixa['y'])

                    # Desenhar asfalto da faixa - ALINHADO AO GRID 32px
                    altura_faixa = config.TAMANHO_CELL  # 1 célula (32px)
                    pygame.draw.rect(
                        self.screen,
                        config.ASFALTO,
                        (0, y_tela - altura_faixa // 2, config.LARGURA_TELA, altura_faixa)
                    )
                    
                    # Linhas amarelas - ALINHADAS AO GRID
                    espacamento_linhas = config.TAMANHO_CELL * 2  # A cada 2 células (64px)
                    largura_linha = config.TAMANHO_CELL // 2  # Meia célula (16px)
                    for x in range(0, config.LARGURA_TELA, espacamento_linhas):
                        pygame.draw.rect(
                            self.screen,
                            config.AMARELO,
                            (x + config.TAMANHO_CELL // 4, y_tela - 2, largura_linha, 4)
                        )
            
            elif chunk.tipo == 'rio':
                # Desenhar água - ALINHADO AO GRID
                altura_chunk = chunk.dados.get('altura', 96)  # 3 células (96px) - múltiplo de 32
                
                # Água base (azul)
                pygame.draw.rect(
                    self.screen,
                    (50, 100, 200),
                    (0, y_tela_inicio, config.LARGURA_TELA, altura_chunk)
                )
                
                # Água simples sem linhas horríveis - apenas cor sólida
                # Sem efeitos desnecessários

    def desenhar(self):
        """Renderiza a tela"""
        if self.estado == GameState.MENU:
            self.menu.desenhar(self.melhor_pontuacao, self.melhor_nivel)
        elif self.estado == GameState.PLAYING:
            self.desenhar_fundo()
            
            # Desenhar grid visual (sutil)
            self.desenhar_grid_visual()
            
            # Desenhar sprites com offset da câmera
            # Plataformas
            for plataforma in self.plataformas_group:
                y_tela = self.camera.aplicar_offset(plataforma.rect.centery)
                rect_tela = plataforma.rect.copy()
                rect_tela.centery = y_tela
                self.screen.blit(plataforma.image, rect_tela)

            # Carros
            for carro in self.carros_group:
                y_tela = self.camera.aplicar_offset(carro.rect.centery)
                rect_tela = carro.rect.copy()
                rect_tela.centery = y_tela
                self.screen.blit(carro.image, rect_tela)

            # Jogador (com efeito visual de invulnerabilidade)
            if self.jogador is not None:
                y_tela = self.camera.aplicar_offset(self.jogador.rect.centery)
                rect_tela = self.jogador.rect.copy()
                rect_tela.centery = y_tela

                # Efeito de piscar durante invulnerabilidade
                if not self.invulneravel or int(self.tempo_invulnerabilidade * 10) % 2 == 0:
                    self.screen.blit(self.jogador.image, rect_tela)

            # Desenha HUD (sempre no topo)
            tempo_decorrido = time.time() - self.tempo_inicio if self.tempo_inicio > 0 else 0
            self.hud.desenhar(self.pontuacao, self.nivel, self.vidas, tempo_decorrido)
            
        elif self.estado == GameState.GAME_OVER:
            self.desenhar_fundo()
            
            # Desenhar sprites com offset da câmera
            # Plataformas
            for plataforma in self.plataformas_group:
                y_tela = self.camera.aplicar_offset(plataforma.rect.centery)
                rect_tela = plataforma.rect.copy()
                rect_tela.centery = y_tela
                self.screen.blit(plataforma.image, rect_tela)
            
            # Carros
            for carro in self.carros_group:
                y_tela = self.camera.aplicar_offset(carro.rect.centery)
                rect_tela = carro.rect.copy()
                rect_tela.centery = y_tela
                self.screen.blit(carro.image, rect_tela)
            
            # Jogador
            if self.jogador is not None:
                y_tela = self.camera.aplicar_offset(self.jogador.rect.centery)
                rect_tela = self.jogador.rect.copy()
                rect_tela.centery = y_tela
                self.screen.blit(self.jogador.image, rect_tela)
            
            # HUD
            tempo_decorrido = time.time() - self.tempo_inicio if self.tempo_inicio > 0 else 0
            self.hud.desenhar(self.pontuacao, self.nivel, self.vidas, tempo_decorrido)
            # Desenha tela de game over
            self.game_over_screen.desenhar(self.pontuacao, self.nivel, self.melhor_nivel)

        pygame.display.flip()

    def executar(self):
        """Loop principal do jogo"""
        rodando = True

        while rodando:
            # Processar eventos
            rodando = self.processar_eventos()

            # Atualizar lógica
            self.atualizar()

            # Desenhar
            self.desenhar()

            # Controlar FPS e calcular delta time
            self.delta_time = self.clock.tick(config.FPS) / 1000.0  # Converter ms para segundos

        pygame.quit()
        sys.exit()


def main():
    """Função principal"""
    try:
        print("=" * 50)
        print("ATRAVESSAR A RUA v2.0 - Frogger Style")
        print("=" * 50)
        print("\nControles:")
        print("  Setas ou WASD : Mover o sapo")
        print("  ESPACO        : Iniciar/Reiniciar")
        print("  ESC           : Menu/Sair")
        print("\nObjetivo:")
        print("  Atravesse a rua sem ser atingido pelos carros!")
        print("  Chegue ao topo para avancar de nivel!")
        print("\nIniciando jogo...\n")
        
        # Verificar se pygame está disponível
        try:
            pygame.init()
            # Inicializar módulo de fontes explicitamente
            pygame.font.init()
            print("[OK] Pygame inicializado")
        except Exception as e:
            print(f"[ERRO] Falha ao inicializar Pygame: {e}")
            print("\nInstale o Pygame-CE:")
            print("  python -m pip install pygame-ce")
            input("\nPressione ENTER para sair...")
            return
        
        # Criar e executar o jogo
        jogo = JogoAtraversarRua()
        print("[OK] Jogo criado com sucesso")
        print("[OK] Abrindo janela do jogo...\n")
        jogo.executar()
        
    except KeyboardInterrupt:
        print("\n\nJogo interrompido pelo usuario.")
    except Exception as e:
        print(f"\n[ERRO CRITICO] Erro ao executar o jogo: {e}")
        print("\nDetalhes do erro:")
        import traceback
        traceback.print_exc()
        print("\n" + "=" * 50)
        print("SOLUCAO:")
        print("  1. Verifique se Pygame-CE esta instalado:")
        print("     python -m pip install pygame-ce")
        print("  2. Verifique se todos os arquivos estao presentes")
        print("  3. Tente executar: python atravessar_rua.py")
        print("=" * 50)
        input("\nPressione ENTER para sair...")


if __name__ == "__main__":
    main()
