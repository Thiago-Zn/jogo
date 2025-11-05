"""
Classe dos carros (obstáculos)
"""

import pygame
import config


class Carro(pygame.sprite.Sprite):
    """Classe que representa um carro obstáculo"""

    def __init__(self, x, y, velocidade, cor, direcao=1, largura=None):
        super().__init__()

        self.largura = largura or config.TAMANHO_CARRO_LARGURA
        self.altura = config.TAMANHO_CARRO_ALTURA
        # Criar surface para o sprite
        self.image = pygame.Surface((self.largura, self.altura), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y

        self.velocidade = velocidade
        self.cor = cor
        self.direcao = direcao  # 1 = direita, -1 = esquerda

        # Desenhar o carro
        self.desenhar()

    def desenhar(self):
        """Desenha carro com pixel art profissional - AJUSTADO PARA 64x32"""
        self.image.fill((0, 0, 0, 0))  # Transparente

        # CORES PROFISSIONAIS
        cor_escura = tuple(max(0, c - 40) for c in self.cor)  # Cor escura (sombra)
        cor_clara = tuple(min(255, c + 50) for c in self.cor)  # Cor clara (highlight)
        cor_meio = tuple(min(255, c + 20) for c in self.cor)  # Cor média

        # === SOMBRA REALISTA ===
        sombra_y = self.altura - 3
        pygame.draw.ellipse(self.image, (10, 10, 10), (2, sombra_y, self.largura - 4, 4))

        # === ESTRUTURA DO CARRO (64x32) ===
        # Base/carreceria inferior
        base_y = self.altura - 8
        pygame.draw.rect(self.image, cor_escura, (1, base_y, self.largura - 2, 6))
        # Corpo principal
        pygame.draw.rect(self.image, self.cor, (2, 4, self.largura - 4, self.altura - 10), border_radius=3)
        # Highlight no teto (brilho do sol)
        highlight_altura = max(10, self.altura // 3)
        pygame.draw.rect(self.image, cor_clara, (4, 6, self.largura - 8, highlight_altura), border_radius=2)
        # Gradiente lateral
        pygame.draw.rect(self.image, cor_meio, (3, 7, self.largura - 6, max(8, highlight_altura - 2)), border_radius=1)

        # === JANELAS PROFISSIONAIS ===
        cor_janela = (80, 140, 180)      # Azul janela
        cor_janela_escura = (50, 100, 140)  # Sombra janela
        cor_reflexo = (180, 200, 220)    # Reflexo

        janela_largura = max(10, self.largura // 6)
        janela_offset = max(4, self.largura // 12)
        janela_altura = max(6, self.altura // 4)

        if self.direcao == 1:  # Indo para direita
            # Janela traseira
            pygame.draw.rect(self.image, cor_janela_escura, (self.largura - janela_offset - janela_largura, 8, janela_largura, janela_altura), border_radius=1)
            pygame.draw.rect(self.image, cor_janela, (self.largura - janela_offset - janela_largura + 2, 10, janela_largura - 4, janela_altura - 2), border_radius=1)
            # Reflexo na janela
            pygame.draw.line(self.image, cor_reflexo, (self.largura - janela_offset - janela_largura + 4, 10), (self.largura - janela_offset - 4, 10), 1)
            # Janela dianteira
            pygame.draw.rect(self.image, cor_janela_escura, (self.largura - janela_offset // 2, 8, janela_offset // 2, janela_altura), border_radius=1)
        else:  # Indo para esquerda
            # Janela traseira
            pygame.draw.rect(self.image, cor_janela_escura, (janela_offset, 8, janela_largura, janela_altura), border_radius=1)
            pygame.draw.rect(self.image, cor_janela, (janela_offset + 2, 10, janela_largura - 4, janela_altura - 2), border_radius=1)
            # Reflexo na janela
            pygame.draw.line(self.image, cor_reflexo, (janela_offset + 4, 10), (janela_offset + janela_largura - 4, 10), 1)
            # Janela dianteira
            pygame.draw.rect(self.image, cor_janela_escura, (0, 8, janela_offset // 2, janela_altura), border_radius=1)

        # === RODAS PROFISSIONAIS ===
        # Rodas (ajustadas para 32px de altura)
        roda_y = self.altura - 4
        roda_offset = max(12, self.largura // 6)
        roda_frente = self.largura - roda_offset
        for pos in (roda_offset, roda_frente):
            pygame.draw.circle(self.image, (20, 20, 20), (pos, roda_y), 4)  # Pneu escuro
            pygame.draw.circle(self.image, (40, 40, 40), (pos, roda_y), 3)  # Aro
            pygame.draw.circle(self.image, (60, 60, 60), (pos, roda_y), 2)  # Centro

        # === FARÓIS REALISTAS ===
        cor_farol_base = (255, 255, 200)
        cor_farol_brilho = (255, 255, 100)

        farol_offset = max(4, self.largura // 18)

        if self.direcao == 1:  # Direita
            # Farol direito
            pygame.draw.circle(self.image, cor_farol_base, (self.largura - farol_offset, 10), 3)
            pygame.draw.circle(self.image, cor_farol_brilho, (self.largura - farol_offset, 10), 2)
            # Farol esquerdo
            pygame.draw.circle(self.image, cor_farol_base, (self.largura - farol_offset, 20), 3)
            pygame.draw.circle(self.image, cor_farol_brilho, (self.largura - farol_offset, 20), 2)
        else:  # Esquerda
            # Farol direito
            pygame.draw.circle(self.image, cor_farol_base, (farol_offset, 10), 3)
            pygame.draw.circle(self.image, cor_farol_brilho, (farol_offset, 10), 2)
            # Farol esquerdo
            pygame.draw.circle(self.image, cor_farol_base, (farol_offset, 20), 3)
            pygame.draw.circle(self.image, cor_farol_brilho, (farol_offset, 20), 2)

        # === DETALHES ===
        # Linha de separação (portas)
        pygame.draw.line(self.image, cor_escura, (self.largura // 2, 8), (self.largura // 2, self.altura - 10), 1)
        # Grades/chrome
        pygame.draw.line(self.image, (200, 200, 200), (4, 12), (self.largura - 4, 12), 1)

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

        largura_sprite = getattr(self, "largura", self.rect.width)
        # Reposiciona quando sai da tela
        if self.direcao == 1 and self.rect.left > config.LARGURA_TELA:
            self.rect.right = -largura_sprite
        elif self.direcao == -1 and self.rect.right < 0:
            self.rect.left = config.LARGURA_TELA + largura_sprite

