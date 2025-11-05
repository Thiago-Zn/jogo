"""
Classe de Tartaruga (plataforma que mergulha e emerge)
"""

import pygame
import config


class Tartaruga(pygame.sprite.Sprite):
    """Classe que representa uma tartaruga que mergulha periodicamente"""

    def __init__(self, x, y, velocidade, direcao=1, ciclo_mergulho=180):
        """
        Inicializa uma tartaruga
        
        Args:
            x: Posição X inicial
            y: Posição Y (faixa do rio)
            velocidade: Velocidade de movimento
            direcao: Direção (1 = direita, -1 = esquerda)
            ciclo_mergulho: Frames para completar ciclo (emersa -> submersa -> emersa)
        """
        super().__init__()
        
        self.largura = 40
        self.altura = 35
        self.velocidade = velocidade
        self.direcao = direcao
        
        # Sistema de mergulho
        self.ciclo_mergulho = ciclo_mergulho
        self.frame_atual = 0
        self.emersa = True
        self.alpha = 255  # Transparência para efeito de mergulho
        
        # Criar surface
        self.image = pygame.Surface((self.largura, self.altura), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        
        # Desenhar a tartaruga
        self.desenhar()
    
    def desenhar(self):
        """Desenha a tartaruga"""
        self.image.fill((0, 0, 0, 0))  # Transparente
        
        # Cores da tartaruga
        cor_casco = (34, 139, 34)
        cor_casco_escuro = (0, 100, 0)
        cor_corpo = (107, 142, 35)
        
        if self.emersa:
            # Sombra
            pygame.draw.ellipse(
                self.image,
                (20, 40, 60, 80),
                (5, self.altura - 8, self.largura - 10, 10)
            )
            
            # Corpo (cabeça e patas)
            # Cabeça
            pygame.draw.circle(
                self.image,
                cor_corpo,
                (self.largura // 2, 12),
                6
            )
            
            # Olhos
            pygame.draw.circle(
                self.image,
                (0, 0, 0),
                (self.largura // 2 - 2, 10),
                2
            )
            pygame.draw.circle(
                self.image,
                (0, 0, 0),
                (self.largura // 2 + 2, 10),
                2
            )
            
            # Casco (oval)
            pygame.draw.ellipse(
                self.image,
                cor_casco_escuro,
                (8, 15, self.largura - 16, 18)
            )
            pygame.draw.ellipse(
                self.image,
                cor_casco,
                (10, 16, self.largura - 20, 16)
            )
            
            # Padrão do casco (hexágonos)
            for i in range(2):
                for j in range(2):
                    x = 15 + i * 10
                    y = 20 + j * 8
                    pygame.draw.circle(
                        self.image,
                        cor_casco_escuro,
                        (x, y),
                        4,
                        1
                    )
            
            # Patas (simplificadas)
            # Pata esquerda frente
            pygame.draw.circle(self.image, cor_corpo, (10, 20), 4)
            # Pata direita frente
            pygame.draw.circle(self.image, cor_corpo, (self.largura - 10, 20), 4)
            # Pata esquerda trás
            pygame.draw.circle(self.image, cor_corpo, (12, 28), 4)
            # Pata direita trás
            pygame.draw.circle(self.image, cor_corpo, (self.largura - 12, 28), 4)
        else:
            # Tartaruga submersa (apenas bolhas)
            for i in range(3):
                x = 10 + i * 10
                y = 15 + (i % 2) * 5
                pygame.draw.circle(
                    self.image,
                    (150, 200, 255, 100),
                    (x, y),
                    3,
                    1
                )
        
        # Aplicar transparência se estiver submergindo
        if not self.emersa:
            self.image.set_alpha(self.alpha)
        else:
            self.image.set_alpha(255)
    
    def update(self):
        """Atualiza a posição e estado da tartaruga"""
        # Movimento horizontal
        self.rect.centerx += int(self.velocidade * self.direcao)
        
        # Reposiciona quando sai da tela
        if self.direcao == 1 and self.rect.left > config.LARGURA_TELA:
            self.rect.right = -self.largura
        elif self.direcao == -1 and self.rect.right < 0:
            self.rect.left = config.LARGURA_TELA + self.largura
        
        # Atualizar ciclo de mergulho
        self.frame_atual = (self.frame_atual + 1) % self.ciclo_mergulho
        
        # Metade do ciclo emersa, metade submersa
        meio_ciclo = self.ciclo_mergulho // 2
        
        if self.frame_atual < meio_ciclo:
            # Emersa
            if not self.emersa:
                self.emersa = True
                self.desenhar()
            self.alpha = 255
        else:
            # Submersa
            if self.emersa:
                self.emersa = False
                self.desenhar()
            # Fade out/in suave
            if self.frame_atual < meio_ciclo + 20:
                # Submergindo
                self.alpha = max(0, 255 - (self.frame_atual - meio_ciclo) * 12)
            elif self.frame_atual > self.ciclo_mergulho - 20:
                # Emergindo
                self.alpha = min(255, (self.frame_atual - (self.ciclo_mergulho - 20)) * 12)
            else:
                self.alpha = 0
    
    def jogador_pode_subir(self, jogador):
        """
        Verifica se jogador pode subir na tartaruga (apenas se emersa)
        
        Args:
            jogador: Objeto Jogador
            
        Returns:
            bool: True se há colisão e tartaruga está emersa
        """
        return self.emersa and self.rect.colliderect(jogador.rect)
    
    def mover_jogador(self, jogador):
        """
        Move o jogador junto com a tartaruga
        
        Args:
            jogador: Objeto Jogador
        """
        if self.emersa:
            jogador.rect.centerx += int(self.velocidade * self.direcao)
            
            # Limitar para não sair da tela
            jogador.rect.left = max(0, jogador.rect.left)
            jogador.rect.right = min(config.LARGURA_TELA, jogador.rect.right)
    
    def esta_emersa(self):
        """Retorna se a tartaruga está emersa"""
        return self.emersa
    
    def __repr__(self):
        estado = "emersa" if self.emersa else "submersa"
        return f"Tartaruga(x={self.rect.centerx}, y={self.rect.centery}, {estado})"

