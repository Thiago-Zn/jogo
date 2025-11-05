"""
Classe de Tronco (plataforma flutuante no rio)
"""

import pygame
import config


class Tronco(pygame.sprite.Sprite):
    """Classe que representa um tronco flutuante no rio"""

    def __init__(self, x, y, largura, velocidade, direcao=1):
        """
        Inicializa um tronco
        
        Args:
            x: Posição X inicial
            y: Posição Y (faixa do rio)
            largura: Largura do tronco (múltiplo de 32px)
            velocidade: Velocidade de movimento
            direcao: Direção (1 = direita, -1 = esquerda)
        """
        super().__init__()
        
        self.largura = largura  # Já é múltiplo de 32 (96, 128, 160, 192)
        self.altura = 32  # 1 célula (32px) - alinhado ao grid
        self.velocidade = velocidade
        self.direcao = direcao
        
        # Criar surface
        self.image = pygame.Surface((self.largura, self.altura), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        
        # Desenhar o tronco
        self.desenhar()
    
    def desenhar(self):
        """Desenha tronco com pixel art profissional - AJUSTADO PARA 32px ALTURA"""
        self.image.fill((0, 0, 0, 0))  # Transparente
        
        # CORES PROFISSIONAIS DE MADEIRA
        marrom_base = (101, 67, 33)      # Marrom escuro (casca)
        marrom_claro = (139, 90, 43)     # Marrom médio (centro)
        marrom_escuro = (69, 39, 19)     # Marrom muito escuro (sombra)
        marrom_highlight = (160, 110, 60) # Marrom claro (brilho)
        
        # === SOMBRA NA ÁGUA ===
        # Sombra suave e realista
        sombra_cores = [
            (40, 20, 10),  # Mais escura
            (50, 30, 15),  # Média
        ]
        for i in range(2):
            pygame.draw.ellipse(
                self.image,
                sombra_cores[i],
                (2 + i, self.altura - 2 + i, self.largura - 4 - i*2, 4 - i),
            )
        
        # === CORPO PRINCIPAL (32px altura) ===
        # Base escura
        pygame.draw.rect(self.image, marrom_escuro, (0, 4, self.largura, self.altura - 8))
        # Corpo principal
        pygame.draw.rect(self.image, marrom_base, (1, 6, self.largura - 2, self.altura - 12))
        # Highlight superior (brilho do sol)
        pygame.draw.ellipse(self.image, marrom_highlight, (2, 8, self.largura - 4, 10))
        # Meio-tom
        pygame.draw.rect(self.image, marrom_claro, (2, 9, self.largura - 4, 8))
        
        # === ANÉIS DE CRESCIMENTO (TEXTURA DE MADEIRA) ===
        # Anéis bem desenhados para textura real
        num_aneis = max(2, self.largura // 32)
        for i in range(num_aneis):
            x = (i + 1) * (self.largura // (num_aneis + 1))
            # Anel escuro
            pygame.draw.line(self.image, marrom_escuro, (x, 10), (x, 20), 1)
            # Anel claro ao lado
            if x + 1 < self.largura - 1:
                pygame.draw.line(self.image, marrom_highlight, (x + 1, 11), (x + 1, 19), 1)
        
        # === EXTREMIDADES ARREDONDADAS ===
        # Círculos nas pontas para forma cilíndrica (ajustados para 32px)
        pygame.draw.circle(self.image, marrom_escuro, (1, self.altura // 2), 4)
        pygame.draw.circle(self.image, marrom_escuro, (self.largura - 1, self.altura // 2), 4)
        pygame.draw.circle(self.image, marrom_base, (1, self.altura // 2), 3)
        pygame.draw.circle(self.image, marrom_base, (self.largura - 1, self.altura // 2), 3)
        # Highlight nas extremidades
        pygame.draw.circle(self.image, marrom_highlight, (2, self.altura // 2 - 1), 2)
        pygame.draw.circle(self.image, marrom_highlight, (self.largura - 2, self.altura // 2 - 1), 2)
        
        # === RACHADURAS E DETALHES ===
        # Pequenas rachaduras para realismo
        if self.largura > 64:
            for i in range(2):
                x_rach = 8 + i * (self.largura // 3)
                pygame.draw.line(self.image, marrom_escuro, (x_rach, 11), (x_rach, 19), 1)
        
        # === BORDAS ===
        # Borda superior e inferior para profundidade
        pygame.draw.line(self.image, marrom_escuro, (1, 10), (self.largura - 1, 10), 1)
        pygame.draw.line(self.image, marrom_escuro, (1, 20), (self.largura - 1, 20), 1)
    
    def update(self):
        """Atualiza a posição do tronco (método compatível com sprite.Group.update())"""
        self.atualizar(1/60)

    def atualizar(self, delta_time=1/60):
        """
        Atualiza a posição do tronco com delta time para física frame-independent

        Args:
            delta_time: Tempo desde o último frame (em segundos)
        """
        # Movimento baseado em velocidade em pixels por segundo
        self.rect.centerx += int(self.velocidade * self.direcao * 60 * delta_time)

        # Reposiciona quando sai da tela
        if self.direcao == 1 and self.rect.left > config.LARGURA_TELA:
            self.rect.right = -self.largura
        elif self.direcao == -1 and self.rect.right < 0:
            self.rect.left = config.LARGURA_TELA + self.largura
