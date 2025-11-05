"""Classe do jogador (sapo)."""

import pygame

import config
from core.assets import load_image

JOGADOR_IMAGE_PATH = "images/jogador.png"


class Jogador(pygame.sprite.Sprite):
    """Classe que representa o personagem controlado pelo jogador."""

    def __init__(self, x, y):
        super().__init__()

        # Posição inicial (em coordenadas do mundo) - snap ao grid apenas uma vez na inicialização
        self.pos_inicial_x, self.pos_inicial_y = self._snap_ao_grid(x, y)

        # Posição atual em coordenadas do MUNDO (pixels livres, sem grid restritivo)
        self.x = float(self.pos_inicial_x)
        self.y = float(self.pos_inicial_y)

        # Animação e efeitos visuais
        self.angulo = 0
        self.tempo_animacao = 0.0  # Para animação contínua

        # Estado de movimento (para permitir input durante movimento)
        self.movendo = False
        self.frame_animacao = 0  # Contador de frames para animação de pulo
        self.velocidade = config.VELOCIDADE_JOGADOR  # Pixels por frame

        self.image, self._usando_substituto = load_image(
            JOGADOR_IMAGE_PATH,
            size=(config.TAMANHO_JOGADOR, config.TAMANHO_JOGADOR),
            fallback_draw=self._desenhar_no_surface,
        )
        self.rect = self.image.get_rect()

        # Atualizar rect imediatamente
        self.rect.centerx = int(self.x)
        self.rect.centery = int(self.y)

    def desenhar(self):
        """Redesenha o sprite apenas quando usamos o fallback gerado."""
        if self._usando_substituto:
            self._desenhar_no_surface(self.image)

    def _desenhar_no_surface(self, surface):
        """Desenha o sapo com pixel art profissional - AJUSTADO PARA 32x32."""
        surface.fill((0, 0, 0, 0))  # Transparente

        # CORES PROFISSIONAIS
        verde_base = (76, 153, 0)  # Verde vibrante
        verde_claro = (102, 204, 0)  # Highlight
        verde_escuro = (51, 102, 0)  # Shadow
        verde_medio = (64, 128, 0)  # Meio-tom

        # === CORPO PRINCIPAL (32x32) ===
        pygame.draw.ellipse(surface, verde_escuro, (4, 10, 24, 18))
        pygame.draw.ellipse(surface, verde_base, (3, 9, 26, 20))
        pygame.draw.ellipse(surface, verde_claro, (5, 11, 22, 12))
        pygame.draw.ellipse(surface, verde_medio, (6, 12, 20, 10))

        # === PERNAS TRASEIRAS ===
        pygame.draw.ellipse(surface, verde_escuro, (1, 20, 10, 10))
        pygame.draw.ellipse(surface, verde_escuro, (21, 20, 10, 10))
        pygame.draw.ellipse(surface, verde_base, (2, 19, 10, 10))
        pygame.draw.ellipse(surface, verde_base, (20, 19, 10, 10))
        pygame.draw.ellipse(surface, verde_claro, (3, 21, 6, 6))
        pygame.draw.ellipse(surface, verde_claro, (22, 21, 6, 6))

        # === PERNAS DIANTEIRAS ===
        pygame.draw.ellipse(surface, verde_base, (4, 12, 8, 6))
        pygame.draw.ellipse(surface, verde_base, (20, 12, 8, 6))
        pygame.draw.ellipse(surface, verde_escuro, (5, 13, 6, 4))
        pygame.draw.ellipse(surface, verde_escuro, (21, 13, 6, 4))

        # === OLHOS PROFISSIONAIS (ajustados para 32x32) ===
        pygame.draw.circle(surface, (255, 255, 255), (12, 12), 6)
        pygame.draw.circle(surface, (255, 255, 255), (20, 12), 6)
        pygame.draw.circle(surface, (0, 0, 0), (12, 12), 6, 1)
        pygame.draw.circle(surface, (0, 0, 0), (20, 12), 6, 1)
        pygame.draw.circle(surface, (0, 0, 0), (12, 12), 4)
        pygame.draw.circle(surface, (0, 0, 0), (20, 12), 4)
        pygame.draw.circle(surface, (255, 255, 255), (11, 11), 2)
        pygame.draw.circle(surface, (255, 255, 255), (19, 11), 2)

        # === BOCA ===
        pygame.draw.arc(surface, (0, 0, 0), (10, 18, 12, 6), 0, 3.14, 1)

        # === MANCHAS/PELE ===
        pygame.draw.circle(surface, verde_escuro, (9, 16), 1)
        pygame.draw.circle(surface, verde_escuro, (23, 16), 1)
        pygame.draw.circle(surface, verde_escuro, (16, 19), 2)

    def _snap_ao_grid(self, x, y):
        """Snap posição ao grid - usado APENAS para inicialização e reset"""
        grid_x = int(x / config.TAMANHO_CELL)
        grid_y = int(y / config.TAMANHO_CELL)
        # Retorna centro da célula
        snapped_x = grid_x * config.TAMANHO_CELL + config.TAMANHO_CELL // 2
        snapped_y = grid_y * config.TAMANHO_CELL + config.TAMANHO_CELL // 2
        return snapped_x, snapped_y
    
    def obter_grid_pos(self):
        """Retorna posição atual convertida para grid - usado apenas para lógica auxiliar"""
        grid_x = int(self.x / config.TAMANHO_CELL)
        grid_y = int(self.y / config.TAMANHO_CELL)
        return grid_x, grid_y
    
    def mover(self, dx, dy):
        """
        Move o jogador diretamente em pixels - MOVIMENTO LIVRE E FLUIDO
        dx, dy: -1, 0, ou 1 (direção do movimento)

        Sistema moderno: Movimento direto em pixels sem restrições de grid
        """
        # Removido bloqueio de input durante animação para jogabilidade mais fluida
        
        # Calcular deslocamento em pixels
        deslocamento_x = dx * self.velocidade
        deslocamento_y = dy * self.velocidade
        
        # Nova posição
        nova_x = self.x + deslocamento_x
        nova_y = self.y + deslocamento_y
        
        # Verificar limites APENAS horizontais (mundo infinito vertical)
        min_x = self.rect.width // 2
        max_x = config.LARGURA_TELA - self.rect.width // 2
        
        # Aplicar movimento horizontal se estiver dentro dos limites
        if min_x <= nova_x <= max_x:
            self.x = nova_x
        
        # Movimento vertical: SEMPRE permitido (mundo infinito)
        self.y = nova_y
        
        # Atualizar rect imediatamente
        self.rect.centerx = int(self.x)
        self.rect.centery = int(self.y)
        
        # Iniciar animação de pulo sutil
        self.movendo = True
        self.frame_animacao = 0
        self.tempo_animacao += 0.1  # Para animação contínua (opcional)
    
    def atualizar(self, delta_time=1/60):
        """
        Atualiza animação de pulo sutil durante movimento
        Sistema: Movimento já é direto em pixels, apenas adiciona efeito visual de pulo

        Args:
            delta_time: Tempo desde o último frame (em segundos)
        """
        if self.movendo:
            # Efeito de pulo sutil (arco parabólico) - baseado em tempo
            self.frame_animacao += 1
            if self.frame_animacao < 4:
                # Arco parabólico pequeno
                progresso = self.frame_animacao / 4.0
                offset_y = int(4 * (1 - abs(progresso - 0.5) * 2))  # Pico no meio
                self.rect.centery = int(self.y) - offset_y
            else:
                # Voltar à posição normal
                self.rect.centerx = int(self.x)
                self.rect.centery = int(self.y)
                self.movendo = False
                self.frame_animacao = 0

        # Atualizar animação contínua
        self.tempo_animacao += delta_time

    def resetar_posicao(self):
        """Retorna o jogador à posição inicial (snap ao grid apenas no reset)"""
        self.x, self.y = self._snap_ao_grid(self.pos_inicial_x, self.pos_inicial_y)
        self.rect.centerx = int(self.x)
        self.rect.centery = int(self.y)
        self.angulo = 0
        self.movendo = False
        self.tempo_animacao = 0.0
        self.frame_animacao = 0
        self.desenhar()

    def chegou_ao_topo(self):
        """Verifica se o jogador chegou ao topo (venceu)"""
        return self.rect.centery <= 80

