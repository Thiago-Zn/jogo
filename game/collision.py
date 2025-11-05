"""
Sistema de detecção de colisão
"""

import pygame
import config


class CollisionSystem:
    """Sistema de detecção e tratamento de colisões"""
    
    @staticmethod
    def check_collision(jogador, carros):
        """
        Verifica colisões entre jogador e carros
        
        Args:
            jogador: Sprite do jogador
            carros: Grupo ou lista de sprites de carros
            
        Returns:
            Lista de carros que colidiram com o jogador
        """
        colisoes = []
        
        # Verifica colisão usando bounding box com margem
        for carro in carros:
            distancia_x = abs(jogador.rect.centerx - carro.rect.centerx)
            distancia_y = abs(jogador.rect.centery - carro.rect.centery)
            
            # Colisão com margem de erro (80% do tamanho)
            threshold_x = (config.TAMANHO_JOGADOR + config.TAMANHO_CARRO_LARGURA) * 0.4
            threshold_y = (config.TAMANHO_JOGADOR + config.TAMANHO_CARRO_ALTURA) * 0.4
            
            if distancia_x < threshold_x and distancia_y < threshold_y:
                colisoes.append(carro)
        
        return colisoes
    
    @staticmethod
    def check_collision_pygame(jogador, carros_group):
        """
        Verifica colisões usando pygame.sprite.collide_rect_ratio
        
        Args:
            jogador: Sprite do jogador
            carros_group: pygame.sprite.Group de carros
            
        Returns:
            Lista de carros que colidiram
        """
        return pygame.sprite.spritecollide(
            jogador, carros_group, False,
            pygame.sprite.collide_rect_ratio(0.8)
        )

