"""
Heads-up Display (HUD) do jogo
"""

import pygame
import config


class HUD:
    """Classe responsável pelo HUD durante o jogo"""
    
    def __init__(self, screen, font_pequena):
        self.screen = screen
        self.font_pequena = font_pequena
        
    def desenhar(self, pontuacao, nivel, vidas, tempo_decorrido):
        """
        Desenha o HUD na tela
        
        Args:
            pontuacao: Pontuação atual
            nivel: Nível atual
            vidas: Número de vidas
            tempo_decorrido: Tempo decorrido em segundos
        """
        # Pontuação
        texto_pontos = self.font_pequena.render(f"Pontos: {pontuacao}", True, config.BRANCO)
        self.screen.blit(texto_pontos, (10, 10))
        
        # Nível
        texto_nivel = self.font_pequena.render(f"Nível: {nivel}", True, config.BRANCO)
        texto_nivel_rect = texto_nivel.get_rect()
        texto_nivel_rect.topright = (config.LARGURA_TELA - 10, 10)
        self.screen.blit(texto_nivel, texto_nivel_rect)
        
        # Vidas
        texto_vidas = self.font_pequena.render("Vidas:", True, config.BRANCO)
        texto_vidas_rect = texto_vidas.get_rect()
        texto_vidas_rect.centerx = config.LARGURA_TELA // 2
        texto_vidas_rect.y = 10
        self.screen.blit(texto_vidas, texto_vidas_rect)
        
        for i in range(vidas):
            pygame.draw.circle(
                self.screen, config.VERMELHO,
                (config.LARGURA_TELA // 2 + 60 + i * 30, 25),
                10
            )
        
        # Timer
        texto_tempo = self.font_pequena.render(
            f"Tempo: {tempo_decorrido:.1f}s", True, config.BRANCO
        )
        self.screen.blit(texto_tempo, (10, config.ALTURA_TELA - 30))

