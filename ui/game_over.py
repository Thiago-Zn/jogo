"""
Tela de Game Over - Versão com Botões
"""

import pygame
import config
from ui.button import Button


class GameOverScreen:
    """Classe responsável pela tela de game over com botões clicáveis"""
    
    def __init__(self, screen, font_grande, font_media, font_pequena):
        self.screen = screen
        self.font_grande = font_grande
        self.font_media = font_media
        self.font_pequena = font_pequena
        
        # Criar botões usando a API correta (mesma do menu)
        centro_x = config.LARGURA_TELA // 2
        
        # Botão Jogar Novamente
        self.btn_jogar = Button(
            centro_x, 480,
            250, 50,
            "JOGAR NOVAMENTE"
        )
        self.btn_jogar.cor_normal = config.VERDE_ESCURO
        self.btn_jogar.cor_hover = config.VERDE
        
        # Botão Menu
        self.btn_menu = Button(
            centro_x, 545,
            200, 45,
            "MENU PRINCIPAL"
        )
        self.btn_menu.cor_normal = config.CINZA_ESCURO
        self.btn_menu.cor_hover = config.CINZA
        
        self.botoes = [self.btn_jogar, self.btn_menu]
        self.acao = None
    
    def processar_eventos(self, eventos):
        """
        Processa eventos da tela de game over
        
        Args:
            eventos: Lista de eventos do pygame
            
        Returns:
            str: Ação ('jogar', 'menu', None)
        """
        self.acao = None
        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()
        
        # Atualizar botões
        if self.btn_jogar.atualizar(mouse_pos, mouse_pressed):
            self.acao = 'jogar'
        
        if self.btn_menu.atualizar(mouse_pos, mouse_pressed):
            self.acao = 'menu'
        
        # Processar eventos de teclado (compatibilidade)
        for evento in eventos:
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    self.acao = 'jogar'
                elif evento.key == pygame.K_ESCAPE:
                    self.acao = 'menu'
        
        return self.acao
        
    def desenhar(self, pontuacao, nivel, melhor_nivel):
        """
        Desenha a tela de game over com design moderno

        Args:
            pontuacao: Pontuação final
            nivel: Nível alcançado
            melhor_nivel: Maior nível alcançado na sessão
        """
        # Fundo semi-transparente
        overlay = pygame.Surface((config.LARGURA_TELA, config.ALTURA_TELA))
        overlay.set_alpha(230)
        overlay.fill(config.PRETO)
        self.screen.blit(overlay, (0, 0))
        
        # Borda decorativa
        pygame.draw.rect(self.screen, config.VERMELHO, (30, 60, config.LARGURA_TELA - 60, 500), 5)
        pygame.draw.rect(self.screen, config.AMARELO, (35, 65, config.LARGURA_TELA - 70, 490), 3)
        
        # Sombra do texto Game Over
        texto_go_sombra = self.font_grande.render("GAME OVER!", True, (0, 0, 0))
        texto_go_sombra_rect = texto_go_sombra.get_rect(center=(config.LARGURA_TELA // 2 + 3, 403))
        self.screen.blit(texto_go_sombra, texto_go_sombra_rect)
        
        # Texto Game Over principal
        texto_go = self.font_grande.render("GAME OVER!", True, config.VERMELHO)
        texto_go_rect = texto_go.get_rect(center=(config.LARGURA_TELA // 2, 400))
        self.screen.blit(texto_go, texto_go_rect)
        
        # Placa de estatísticas
        placa = pygame.Surface((400, 180))
        placa.fill((20, 20, 40))
        placa.set_alpha(220)
        placa_rect = placa.get_rect(center=(config.LARGURA_TELA // 2, 260))
        self.screen.blit(placa, placa_rect)
        pygame.draw.rect(self.screen, config.AMARELO, placa_rect, 3, border_radius=10)
        
        # Pontuação final
        texto_pontos_label = self.font_pequena.render("Pontuação:", True, config.BRANCO)
        texto_pontos_label_rect = texto_pontos_label.get_rect(center=(config.LARGURA_TELA // 2, 220))
        self.screen.blit(texto_pontos_label, texto_pontos_label_rect)
        
        texto_pontos = self.font_grande.render(f"{pontuacao}", True, config.VERDE)
        texto_pontos_rect = texto_pontos.get_rect(center=(config.LARGURA_TELA // 2, 260))
        self.screen.blit(texto_pontos, texto_pontos_rect)
        
        # Nível alcançado
        texto_nivel = self.font_media.render(f"Nivel Alcancado: Nivel {nivel}", True, config.AMARELO)
        texto_nivel_rect = texto_nivel.get_rect(center=(config.LARGURA_TELA // 2, 310))
        self.screen.blit(texto_nivel, texto_nivel_rect)

        if melhor_nivel and melhor_nivel > 1:
            texto_melhor = self.font_pequena.render(
                f"Maior Nivel na Sessao: {melhor_nivel}", True, config.BRANCO
            )
            texto_melhor_rect = texto_melhor.get_rect(center=(config.LARGURA_TELA // 2, 340))
            self.screen.blit(texto_melhor, texto_melhor_rect)
        
        # Desenhar botões
        self.btn_jogar.desenhar(self.screen)
        self.btn_menu.desenhar(self.screen)
        
        # Instruções de teclado (pequenas)
        texto_teclado = self.font_pequena.render(
            "Ou use: ESPACO=Jogar | ESC=Menu", True, config.CINZA
        )
        texto_teclado_rect = texto_teclado.get_rect(center=(config.LARGURA_TELA // 2, 120))
        self.screen.blit(texto_teclado, texto_teclado_rect)
