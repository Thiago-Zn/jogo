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

    def __init__(self):
        # Configuração da tela (pygame já foi inicializado em main())
        try:
            self.tela_cheia = False
            self.screen = pygame.display.set_mode((config.LARGURA_TELA, config.ALTURA_TELA))
            pygame.display.set_caption(config.TITULO)
            self.clock = pygame.time.Clock()
            self.fixed_dt = 1.0 / config.FPS
            self.accumulator = 0.0
            self.frame_delta = 0.0
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
        
        # Estado do jogo
        self.estado = GameState.MENU
        self.pontuacao = 0
        self.nivel = 1
        self.vidas = config.VIDAS_INICIAIS
        self.tempo_inicio = 0
        self.melhor_pontuacao = 0
        
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
        deadzone_altura = config.TAMANHO_CELL * 6
        deadzone_topo = config.ALTURA_TELA - deadzone_altura - config.TAMANHO_CELL
        deadzone = pygame.Rect(0, max(0, deadzone_topo), config.LARGURA_TELA, deadzone_altura)
        mundo_altura = 10_000_000
        limites_mundo = pygame.Rect(0, 0, config.LARGURA_TELA, mundo_altura)
        self.camera = Camera(
            (config.LARGURA_TELA, config.ALTURA_TELA),
            world_bounds=limites_mundo,
            deadzone=deadzone,
        )
        self.procedural_generator = ProceduralGenerator()
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
        
        # Criar jogador alinhado ao centro horizontal e na parte inferior
        # Posição Y alinhada ao grid: 4 células do fundo (grid perfeito)
        grid_y_inicial = config.GRID_ALTURA - 4
        y_inicial_jogador = grid_y_inicial * config.TAMANHO_CELL + config.TAMANHO_CELL // 2
        x_inicial_jogador = (config.GRID_LARGURA // 2) * config.TAMANHO_CELL + config.TAMANHO_CELL // 2
        self.jogador = Jogador(x_inicial_jogador, y_inicial_jogador)

        # Resetar sistemas
        self.procedural_generator.resetar()
        self.river_physics.resetar()

        # Inicializar mundo procedimental
        self.procedural_generator.inicializar_mundo_inicial()

        posicao_tela_jogador = config.ALTURA_TELA - (config.TAMANHO_CELL * 5)
        camera_topo = max(0, y_inicial_jogador - posicao_tela_jogador)
        self.camera.move_to((0, camera_topo))
        self.accumulator = 0.0

        # Não criar carros estáticos mais - serão gerados proceduralmente

    def verificar_safe_zone(self, delta_time):
        """Verifica se o jogador está em uma área de descanso"""
        if self.jogador is None:
            return

        view = self.camera.get_view_rect()
        safe_zones = self.procedural_generator.obter_safe_zones_visiveis(view)

        estava_em_safe_zone = self.jogador_em_safe_zone
        self.jogador_em_safe_zone = False

        for sz in safe_zones:
            if sz.colidir_com_jogador(self.jogador):
                self.jogador_em_safe_zone = True
                break

        # Sistema de safe zone - recuperar vida se ficar tempo suficiente
        if self.jogador_em_safe_zone:
            self.tempo_em_safe_zone += delta_time
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
        view = self.camera.get_view_rect()
        plataformas_visiveis = self.procedural_generator.obter_plataformas_visiveis(view)

        # Sincronizar grupo de sprites
        self.plataformas_group.empty()
        for plataforma in plataformas_visiveis:
            self.plataformas_group.add(plataforma)

    def atualizar_carros_procedurais(self):
        """Atualiza carros baseados nas faixas geradas proceduralmente"""
        view = self.camera.get_view_rect()
        faixas_visiveis = self.procedural_generator.obter_faixas_visiveis(view)

        for faixa in faixas_visiveis:
            faixa_y = faixa['y']

            tem_carro = False
            for carro in self.carros_group:
                if abs(carro.rect.centery - faixa_y) < 30:
                    tem_carro = True
                    break

            if not tem_carro:
                carros_por_faixa = random.randint(2, 4)
                for i in range(carros_por_faixa):
                    espacamento_cells = config.LARGURA_TELA // (carros_por_faixa + 1) // config.TAMANHO_CELL
                    x_cell = int((i + 1) * espacamento_cells) + random.randint(-1, 1)
                    x_cell = max(0, min(x_cell, config.GRID_LARGURA - 1))
                    x_inicial = x_cell * config.TAMANHO_CELL + config.TAMANHO_CELL // 2

                    if faixa['direcao'] == -1:
                        x_cell_invertido = config.GRID_LARGURA - 1 - x_cell
                        x_inicial = x_cell_invertido * config.TAMANHO_CELL + config.TAMANHO_CELL // 2

                    carro = Carro(
                        x_inicial,
                        faixa_y,
                        faixa['velocidade'],
                        faixa['cor'],
                        faixa['direcao']
                    )
                    self.carros_group.add(carro)

        y_min = view.top
        y_max = view.bottom
        for carro in list(self.carros_group):
            if carro.rect.centery < y_min - 100 or carro.rect.centery > y_max + 100:
                carro.kill()

    def fixed_update(self, delta_time):
        """Atualiza a lógica do jogo usando passo de física fixo."""
        if self.estado != GameState.PLAYING:
            return

        if self.jogador:
            self.jogador.atualizar(delta_time)

        self.camera.follow(self.jogador.rect if self.jogador else None)

        view = self.camera.get_view_rect()
        self.procedural_generator.atualizar(view)

        distancia = int(self.procedural_generator.distancia_percorrida / 10)
        if distancia > self.pontuacao:
            self.pontuacao = distancia

        self.atualizar_carros_procedurais()
        self.atualizar_plataformas_procedurais()

        for carro in self.carros_group:
            carro.atualizar(delta_time)

        for plataforma in self.plataformas_group:
            plataforma.atualizar(delta_time)

        chunks_rio = [c for c in self.procedural_generator.chunks if c.tipo == 'rio']
        status_rio = self.river_physics.atualizar(self.jogador, chunks_rio, delta_time)

        if self.invulneravel:
            self.tempo_invulnerabilidade += delta_time
            if self.tempo_invulnerabilidade >= self.duracao_invulnerabilidade:
                self.invulneravel = False
                self.tempo_invulnerabilidade = 0.0

        if status_rio['afogando'] and not self.invulneravel:
            self.vidas -= 1
            self.jogador.resetar_posicao()

            self.invulneravel = True
            self.tempo_invulnerabilidade = 0.0

            if self.vidas <= 0:
                self.estado = GameState.GAME_OVER
                if self.pontuacao > self.melhor_pontuacao:
                    self.melhor_pontuacao = self.pontuacao

        self.verificar_safe_zone(delta_time)
        self.verificar_colisoes()

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

    def desenhar_grid_visual(self, interpolation):
        """Desenha o grid visual usando cache - OTIMIZADO"""
        if self.grid_cache:
            self.screen.blit(self.grid_cache, (0, 0))

        cor_grid = (150, 150, 150, 40)
        view = self.camera.get_view_rect(interpolation)
        primeira_linha = (view.top // config.TAMANHO_CELL) * config.TAMANHO_CELL
        ultima_linha = view.bottom + config.TAMANHO_CELL * 2

        y = primeira_linha - config.TAMANHO_CELL * 5
        while y <= ultima_linha:
            _, y_tela = self.camera.world_to_screen((0, y), interpolation)
            if 0 <= y_tela <= config.ALTURA_TELA:
                pygame.draw.line(self.screen, cor_grid, (0, y_tela), (config.LARGURA_TELA, y_tela), 1)
            y += config.TAMANHO_CELL

    def desenhar_fundo(self, interpolation):
        """Desenha o cenário do jogo com geração procedimental"""
        self.screen.fill(config.AZUL)

        view = self.camera.get_view_rect()
        chunks = self.procedural_generator.obter_chunks_visiveis(view)
        chunks_ordenados = sorted(chunks, key=lambda c: c.y_inicio)

        for chunk in chunks_ordenados:
            y_tela_inicio = self.camera.world_to_screen((0, chunk.y_inicio), interpolation)[1]
            y_tela_fim = self.camera.world_to_screen((0, chunk.y_fim), interpolation)[1]

            if chunk.tipo == 'safe_zone':
                safe_zone = chunk.dados.get('safe_zone')
                if safe_zone:
                    safe_zone.renderizar(self.screen, self.camera, interpolation)

            elif chunk.tipo == 'estrada':
                faixas = chunk.dados.get('faixas', [])
                for faixa in faixas:
                    y_tela = self.camera.world_to_screen((0, faixa['y']), interpolation)[1]

                    altura_faixa = config.TAMANHO_CELL
                    pygame.draw.rect(
                        self.screen,
                        config.ASFALTO,
                        (0, y_tela - altura_faixa // 2, config.LARGURA_TELA, altura_faixa)
                    )

                    espacamento_linhas = config.TAMANHO_CELL * 2
                    largura_linha = config.TAMANHO_CELL // 2
                    for x in range(0, config.LARGURA_TELA, espacamento_linhas):
                        pygame.draw.rect(
                            self.screen,
                            config.AMARELO,
                            (x + config.TAMANHO_CELL // 4, y_tela - 2, largura_linha, 4)
                        )

            elif chunk.tipo == 'rio':
                altura_chunk = chunk.dados.get('altura', 96)

                pygame.draw.rect(
                    self.screen,
                    (50, 100, 200),
                    (0, y_tela_inicio, config.LARGURA_TELA, altura_chunk)
                )

    def desenhar(self, interpolation):
        """Renderiza a tela"""
        if self.estado == GameState.MENU:
            self.menu.desenhar(self.melhor_pontuacao)
        elif self.estado == GameState.PLAYING:
            self.desenhar_fundo(interpolation)
            self.desenhar_grid_visual(interpolation)
            self._desenhar_sprites(interpolation)

            tempo_decorrido = time.time() - self.tempo_inicio if self.tempo_inicio > 0 else 0
            self.hud.desenhar(self.pontuacao, self.nivel, self.vidas, tempo_decorrido)

        elif self.estado == GameState.GAME_OVER:
            self.desenhar_fundo(interpolation)
            self._desenhar_sprites(interpolation, incluir_jogador=True)

            tempo_decorrido = time.time() - self.tempo_inicio if self.tempo_inicio > 0 else 0
            self.hud.desenhar(self.pontuacao, self.nivel, self.vidas, tempo_decorrido)
            self.game_over_screen.desenhar(self.pontuacao, self.nivel)

        pygame.display.flip()

    def _desenhar_sprites(self, interpolation, incluir_jogador=False):
        """Desenha plataformas, carros e opcionalmente o jogador."""
        for plataforma in self.plataformas_group:
            centro_tela = self.camera.world_to_screen(plataforma.rect.center, interpolation)
            rect_tela = plataforma.rect.copy()
            rect_tela.center = centro_tela
            self.screen.blit(plataforma.image, rect_tela)

        for carro in self.carros_group:
            centro_tela = self.camera.world_to_screen(carro.rect.center, interpolation)
            rect_tela = carro.rect.copy()
            rect_tela.center = centro_tela
            self.screen.blit(carro.image, rect_tela)

        if self.jogador is not None:
            centro_jogador = self.camera.world_to_screen(self.jogador.rect.center, interpolation)
            rect_jogador = self.jogador.rect.copy()
            rect_jogador.center = centro_jogador

            if incluir_jogador or not self.invulneravel or int(self.tempo_invulnerabilidade * 10) % 2 == 0:
                self.screen.blit(self.jogador.image, rect_jogador)

    def executar(self):
        """Loop principal do jogo"""
        rodando = True

        while rodando:
            # Processar eventos
            rodando = self.processar_eventos()
            if not rodando:
                break

            frame_time = self.clock.tick(config.FPS) / 1000.0
            frame_time = min(frame_time, 0.25)
            self.frame_delta = frame_time
            self.accumulator = min(self.accumulator + frame_time, self.fixed_dt * 5)

            while self.accumulator >= self.fixed_dt:
                self.fixed_update(self.fixed_dt)
                self.accumulator -= self.fixed_dt

            interpolation = self.accumulator / self.fixed_dt if self.fixed_dt > 0 else 0.0
            self.desenhar(interpolation)

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
