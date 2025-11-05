"""
Tela de menu do jogo - Versão com Mouse
"""

import pygame
import config
from entities.jogador import Jogador
from ui.button import Button


class Menu:
    """Classe responsável pela tela de menu com botões clicáveis"""
    
    def __init__(self, screen, font_grande, font_media, font_pequena):
        self.screen = screen
        self.font_grande = font_grande
        self.font_media = font_media
        self.font_pequena = font_pequena
        
        # Criar sapo de exemplo
        self.sapo_demo = Jogador(config.LARGURA_TELA // 2, 180)
        
        # Criar botões
        centro_x = config.LARGURA_TELA // 2
        self.botoes = []
        
        # Botão Jogar
        self.btn_jogar = Button(
            centro_x, 320,
            200, 50,
            "JOGAR"
        )
        self.botoes.append(self.btn_jogar)
        
        # Botão Configurações
        self.btn_config = Button(
            centro_x, 390,
            200, 50,
            "CONFIGURACOES"
        )
        self.botoes.append(self.btn_config)
        
        # Botão Sair
        self.btn_sair = Button(
            centro_x, 460,
            200, 50,
            "SAIR"
        )
        self.botoes.append(self.btn_sair)
        
        # Estado
        self.acao = None
        
        # Animação de fundo
        self.frame = 0
    
    def processar_eventos(self, eventos):
        """
        Processa eventos do menu
        
        Args:
            eventos: Lista de eventos do pygame
            
        Returns:
            str: Ação a realizar ('jogar', 'config', 'sair', None)
        """
        self.acao = None
        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()
        
        # Atualizar botões
        if self.btn_jogar.atualizar(mouse_pos, mouse_pressed):
            self.acao = 'jogar'
        
        if self.btn_config.atualizar(mouse_pos, mouse_pressed):
            self.acao = 'config'
        
        if self.btn_sair.atualizar(mouse_pos, mouse_pressed):
            self.acao = 'sair'
        
        # Processar eventos de teclado (compatibilidade)
        for evento in eventos:
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    self.acao = 'jogar'
                elif evento.key == pygame.K_ESCAPE:
                    self.acao = 'sair'
        
        return self.acao
    
    def desenhar(self, melhor_pontuacao=0):
        """Desenha o menu inicial com design moderno"""
        self.frame += 1
        
        # Fundo com gradiente animado
        for y in range(config.ALTURA_TELA):
            intensidade = int(255 - y * 0.3)
            offset = int(10 * (1 + 0.5 * (self.frame % 60) / 60))
            cor = (0, min(162, intensidade + offset), min(232, intensidade + offset))
            pygame.draw.line(self.screen, cor, (0, y), (config.LARGURA_TELA, y))
        
        # Nuvens decorativas animadas
        for i in range(5):
            x = ((i * 200) + (self.frame // 2)) % (config.LARGURA_TELA + 100)
            pygame.draw.ellipse(self.screen, (220, 240, 255), (x, 50 + i*20, 100, 40))
            pygame.draw.ellipse(self.screen, (230, 245, 255), (x + 30, 45 + i*20, 70, 35))
        
        # Sombra do título
        titulo_sombra = self.font_grande.render("ATRAVESSAR A RUA", True, (0, 0, 0))
        titulo_sombra_rect = titulo_sombra.get_rect(center=(config.LARGURA_TELA // 2 + 3, 103))
        self.screen.blit(titulo_sombra, titulo_sombra_rect)
        
        # Título principal
        titulo = self.font_grande.render("ATRAVESSAR A RUA", True, config.AMARELO)
        titulo_rect = titulo.get_rect(center=(config.LARGURA_TELA // 2, 100))
        self.screen.blit(titulo, titulo_rect)
        
        # Efeito de brilho no título
        titulo_brilho = self.font_grande.render("ATRAVESSAR A RUA", True, (255, 255, 200))
        titulo_brilho_rect = titulo_brilho.get_rect(center=(config.LARGURA_TELA // 2, 99))
        try:
            self.screen.blit(titulo_brilho, titulo_brilho_rect, special_flags=pygame.BLEND_ALPHA_SD2)
        except:
            self.screen.blit(titulo_brilho, titulo_brilho_rect)
        
        # Subtítulo
        subtitulo = self.font_pequena.render("v3.0 - Jogo Infinito com Sistema de Rio", True, config.BRANCO)
        subtitulo_rect = subtitulo.get_rect(center=(config.LARGURA_TELA // 2, 140))
        self.screen.blit(subtitulo, subtitulo_rect)
        
        # Desenha sapo de exemplo
        self.screen.blit(self.sapo_demo.image, self.sapo_demo.rect)
        
        # Melhor pontuação
        if melhor_pontuacao > 0:
            melhor_bg = pygame.Surface((280, 40))
            melhor_bg.fill((0, 0, 0))
            melhor_bg.set_alpha(150)
            melhor_bg_rect = melhor_bg.get_rect(center=(config.LARGURA_TELA // 2, 240))
            self.screen.blit(melhor_bg, melhor_bg_rect)
            
            melhor = self.font_pequena.render(
                f"Melhor Pontuacao: {melhor_pontuacao}", True, config.AMARELO
            )
            melhor_rect = melhor.get_rect(center=(config.LARGURA_TELA // 2, 240))
            self.screen.blit(melhor, melhor_rect)
        
        # Desenhar botões
        for botao in self.botoes:
            botao.desenhar(self.screen)
        
        # Instruções de mouse
        instrucao_mouse = self.font_pequena.render(
            "Use o MOUSE ou TECLADO (Espaco/ESC)", True, config.CINZA
        )
        instrucao_rect = instrucao_mouse.get_rect(center=(config.LARGURA_TELA // 2, 540))
        self.screen.blit(instrucao_mouse, instrucao_rect)
        
        # Círculos decorativos animados
        tamanho_circulo = 30 + int(5 * abs((self.frame % 120) - 60) / 60)
        pygame.draw.circle(self.screen, (255, 255, 255, 100), (100, 150), tamanho_circulo, 2)
        pygame.draw.circle(self.screen, (255, 255, 255, 100), (700, 450), tamanho_circulo, 2)
    
    def obter_acao(self):
        """Retorna a última ação do menu"""
        return self.acao
