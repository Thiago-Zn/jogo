"""
Classe de Nenúfar (plataforma estática no rio)
"""

import pygame
import config


class Lilypad(pygame.sprite.Sprite):
    """Classe que representa um nenúfar (plataforma estática no rio)"""

    def __init__(self, x, y):
        """
        Inicializa um nenúfar
        
        Args:
            x: Posição X
            y: Posição Y (faixa do rio)
        """
        super().__init__()
        
        self.largura = 45
        self.altura = 40
        
        # Criar surface
        self.image = pygame.Surface((self.largura, self.altura), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        
        # Animação sutil (balanço)
        self.frame = 0
        self.offset_y = 0
        
        # Desenhar o nenúfar
        self.desenhar()
    
    def desenhar(self):
        """Desenha o nenúfar"""
        self.image.fill((0, 0, 0, 0))  # Transparente
        
        # Cores do nenúfar
        cor_folha = (60, 179, 113)
        cor_folha_escuro = (34, 139, 34)
        cor_flor = (255, 192, 203)
        cor_centro = (255, 255, 150)
        
        # Sombra na água
        pygame.draw.ellipse(
            self.image,
            (20, 40, 60, 80),
            (5, self.altura - 10, self.largura - 10, 12)
        )
        
        # Folha principal (círculo com corte)
        centro_x = self.largura // 2
        centro_y = self.altura // 2
        
        # Desenhar folha (círculo)
        pygame.draw.circle(
            self.image,
            cor_folha_escuro,
            (centro_x, centro_y),
            18
        )
        pygame.draw.circle(
            self.image,
            cor_folha,
            (centro_x, centro_y),
            16
        )
        
        # Corte em V na folha (característica de nenúfar)
        pontos_corte = [
            (centro_x, centro_y - 16),
            (centro_x - 5, centro_y - 5),
            (centro_x, centro_y),
            (centro_x + 5, centro_y - 5)
        ]
        pygame.draw.polygon(
            self.image,
            (50, 100, 200),  # Cor da água
            pontos_corte
        )
        
        # Veias da folha
        for angulo in range(0, 360, 45):
            import math
            rad = math.radians(angulo)
            x_fim = centro_x + int(12 * math.cos(rad))
            y_fim = centro_y + int(12 * math.sin(rad))
            pygame.draw.line(
                self.image,
                cor_folha_escuro,
                (centro_x, centro_y),
                (x_fim, y_fim),
                1
            )
        
        # Flor pequena no centro (opcional)
        if self.frame % 120 < 60:  # Flor aparece periodicamente
            # Pétalas
            for i in range(5):
                import math
                angulo = (360 / 5) * i
                rad = math.radians(angulo)
                x_petala = centro_x + int(6 * math.cos(rad))
                y_petala = centro_y + int(6 * math.sin(rad))
                pygame.draw.circle(
                    self.image,
                    cor_flor,
                    (x_petala, y_petala),
                    4
                )
            
            # Centro da flor
            pygame.draw.circle(
                self.image,
                cor_centro,
                (centro_x, centro_y),
                3
            )
    
    def update(self):
        """Atualiza a animação do nenúfar"""
        self.frame += 1
        
        # Balanço sutil (simulando movimento da água)
        import math
        self.offset_y = int(2 * math.sin(self.frame * 0.05))
        
        # Redesenhar se necessário (para animação da flor)
        if self.frame % 60 == 0:
            self.desenhar()
    
    def jogador_pode_subir(self, jogador):
        """
        Verifica se jogador pode subir no nenúfar
        
        Args:
            jogador: Objeto Jogador
            
        Returns:
            bool: True se há colisão
        """
        # Criar rect ajustado para colisão mais precisa (área menor)
        collision_rect = self.rect.inflate(-10, -10)
        return collision_rect.colliderect(jogador.rect)
    
    def __repr__(self):
        return f"Lilypad(x={self.rect.centerx}, y={self.rect.centery})"

