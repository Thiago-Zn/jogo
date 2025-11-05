"""Classe dos carros (obstáculos)."""

import pygame

import config
from core.assets import load_image

CARRO_IMAGE_PATH = "images/carro.png"


class Carro(pygame.sprite.Sprite):
    """Classe que representa um carro obstáculo."""

    def __init__(self, x, y, velocidade, cor, direcao=1):
        super().__init__()

        self.velocidade = velocidade
        self.cor = cor
        self.direcao = direcao  # 1 = direita, -1 = esquerda

        self.image, self._usando_substituto = load_image(
            CARRO_IMAGE_PATH,
            size=(config.TAMANHO_CARRO_LARGURA, config.TAMANHO_CARRO_ALTURA),
            fallback_draw=self._desenhar_no_surface,
        )
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y

    def desenhar(self):
        """Redesenha o carro apenas quando usamos o substituto procedimental."""
        if self._usando_substituto:
            self._desenhar_no_surface(self.image)

    def _desenhar_no_surface(self, surface):
        """Desenha carro com pixel art profissional - AJUSTADO PARA 64x32."""
        surface.fill((0, 0, 0, 0))  # Transparente

        # CORES PROFISSIONAIS
        cor_escura = tuple(max(0, c - 40) for c in self.cor)  # Cor escura (sombra)
        cor_clara = tuple(min(255, c + 50) for c in self.cor)  # Cor clara (highlight)
        cor_meio = tuple(min(255, c + 20) for c in self.cor)  # Cor média

        # === SOMBRA REALISTA ===
        sombra_y = config.TAMANHO_CARRO_ALTURA - 3
        pygame.draw.ellipse(surface, (10, 10, 10), (2, sombra_y, 60, 4))

        # === ESTRUTURA DO CARRO (64x32) ===
        # Base/carreceria inferior
        base_y = config.TAMANHO_CARRO_ALTURA - 8
        pygame.draw.rect(surface, cor_escura, (1, base_y, 62, 6))
        # Corpo principal
        pygame.draw.rect(surface, self.cor, (2, 4, 60, 22), border_radius=3)
        # Highlight no teto (brilho do sol)
        pygame.draw.rect(surface, cor_clara, (4, 6, 56, 12), border_radius=2)
        # Gradiente lateral
        pygame.draw.rect(surface, cor_meio, (3, 7, 58, 10), border_radius=1)

        # === JANELAS PROFISSIONAIS ===
        cor_janela = (80, 140, 180)  # Azul janela
        cor_janela_escura = (50, 100, 140)  # Sombra janela
        cor_reflexo = (180, 200, 220)  # Reflexo

        if self.direcao == 1:  # Indo para direita
            # Janela traseira
            pygame.draw.rect(surface, cor_janela_escura, (48, 8, 12, 8), border_radius=1)
            pygame.draw.rect(surface, cor_janela, (50, 10, 8, 6), border_radius=1)
            # Reflexo na janela
            pygame.draw.line(surface, cor_reflexo, (52, 10), (56, 10), 1)
            # Janela dianteira
            pygame.draw.rect(surface, cor_janela_escura, (58, 8, 4, 8), border_radius=1)
        else:  # Indo para esquerda
            # Janela traseira
            pygame.draw.rect(surface, cor_janela_escura, (4, 8, 12, 8), border_radius=1)
            pygame.draw.rect(surface, cor_janela, (6, 10, 8, 6), border_radius=1)
            # Reflexo na janela
            pygame.draw.line(surface, cor_reflexo, (8, 10), (12, 10), 1)
            # Janela dianteira
            pygame.draw.rect(surface, cor_janela_escura, (0, 8, 4, 8), border_radius=1)

        # === RODAS PROFISSIONAIS ===
        roda_y = config.TAMANHO_CARRO_ALTURA - 4
        pygame.draw.circle(surface, (20, 20, 20), (12, roda_y), 4)  # Pneu escuro
        pygame.draw.circle(surface, (40, 40, 40), (12, roda_y), 3)  # Aro
        pygame.draw.circle(surface, (60, 60, 60), (12, roda_y), 2)  # Centro

        pygame.draw.circle(surface, (20, 20, 20), (52, roda_y), 4)  # Pneu escuro
        pygame.draw.circle(surface, (40, 40, 40), (52, roda_y), 3)  # Aro
        pygame.draw.circle(surface, (60, 60, 60), (52, roda_y), 2)  # Centro

        # === FARÓIS REALISTAS ===
        cor_farol_base = (255, 255, 200)
        cor_farol_brilho = (255, 255, 100)

        if self.direcao == 1:  # Direita
            pygame.draw.circle(surface, cor_farol_base, (60, 10), 3)
            pygame.draw.circle(surface, cor_farol_brilho, (60, 10), 2)
            pygame.draw.circle(surface, cor_farol_base, (60, 20), 3)
            pygame.draw.circle(surface, cor_farol_brilho, (60, 20), 2)
        else:  # Esquerda
            pygame.draw.circle(surface, cor_farol_base, (4, 10), 3)
            pygame.draw.circle(surface, cor_farol_brilho, (4, 10), 2)
            pygame.draw.circle(surface, cor_farol_base, (4, 20), 3)
            pygame.draw.circle(surface, cor_farol_brilho, (4, 20), 2)

        # === DETALHES ===
        pygame.draw.line(surface, cor_escura, (32, 8), (32, 22), 1)
        pygame.draw.line(surface, (200, 200, 200), (4, 12), (60, 12), 1)

    def update(self):
        """Atualiza a posição do carro (método compatível com sprite.Group.update())"""
        self.atualizar(1/60)

    def atualizar(self, delta_time=1/60):
        """
        Atualiza a posição do carro com delta time para física frame-independent

        Args:
            delta_time: Tempo desde o último frame (em segundos)
        """
        # Movimento baseado em velocidade em pixels por segundo
        self.rect.centerx += int(self.velocidade * self.direcao * 60 * delta_time)

        # Reposiciona quando sai da tela
        if self.direcao == 1 and self.rect.left > config.LARGURA_TELA:
            self.rect.right = -config.TAMANHO_CARRO_LARGURA
        elif self.direcao == -1 and self.rect.right < 0:
            self.rect.left = config.LARGURA_TELA + config.TAMANHO_CARRO_LARGURA

