"""
Sistema de Câmera e Scroll
"""

import pygame
import config


class Camera:
    """Classe que gerencia a câmera e o scroll do jogo"""

    def __init__(self):
        """Inicializa o sistema de câmera"""
        self.offset_y = 0  # Offset vertical da câmera
        self.velocidade_scroll = config.VELOCIDADE_SCROLL
        self.scroll_ativo = False

        # Limites de scroll
        self.limite_superior = 0
        self.limite_inferior = None  # Infinito

        # Para scroll suave com interpolação (frame-independent)
        self.target_offset = 0
        self.suavidade = 7.0  # Velocidade de interpolação ajustada para delta time
        
        # Posição do jogador (para acompanhamento)
        self.jogador_y = 0
        
    def update(self, jogador=None, delta_time=1/60):
        """
        Atualiza a posição da câmera com INTERPOLAÇÃO SUAVE frame-independent
        Segue a posição Y do jogador (movimento livre em pixels) para movimento fluido

        Args:
            jogador: Objeto do jogador
            delta_time: Tempo desde o último frame (em segundos)
        """
        if jogador and hasattr(jogador, 'y'):
            # Usar posição Y direta do jogador (movimento livre em pixels)
            posicao_tela_jogador = config.ALTURA_TELA - (config.TAMANHO_CELL * 5)  # 5 células do fundo (160px)

            # Calcular offset baseado na posição Y do jogador (coordenadas do mundo)
            y_mundo_jogador = jogador.y

            # Offset necessário para mostrar o jogador na posição desejada
            novo_target = y_mundo_jogador - posicao_tela_jogador

            # Atualizar target (sempre atualizar para movimento suave)
            self.target_offset = novo_target

        # INTERPOLAÇÃO SUAVE (LERP) frame-independent
        # Fórmula: pos = pos + (target - pos) * (velocidade * delta_time)
        diferenca = self.target_offset - self.offset_y

        # Se estiver muito perto, snap final
        if abs(diferenca) < 0.5:
            self.offset_y = self.target_offset
        else:
            # Interpolação suave com delta time
            self.offset_y += diferenca * self.suavidade * delta_time
        
        # Aplicar limites (não pode voltar para baixo)
        if self.limite_superior is not None:
            self.offset_y = max(self.limite_superior, self.offset_y)
        if self.limite_inferior is not None:
            self.offset_y = min(self.limite_inferior, self.offset_y)
    
    def aplicar_offset(self, y):
        """
        Converte coordenada do mundo para coordenada da tela
        
        Args:
            y: Coordenada Y no mundo
            
        Returns:
            int: Coordenada Y na tela
        """
        return int(y - self.offset_y)
    
    def obter_y_mundo(self, y_tela):
        """
        Converte coordenada da tela para coordenada do mundo
        
        Args:
            y_tela: Coordenada Y na tela
            
        Returns:
            int: Coordenada Y no mundo
        """
        return int(y_tela + self.offset_y)
    
    def esta_visivel(self, y_mundo, altura=0):
        """
        Verifica se uma posição está visível na tela
        
        Args:
            y_mundo: Coordenada Y no mundo
            altura: Altura do objeto (opcional)
            
        Returns:
            bool: True se está visível
        """
        y_tela = self.aplicar_offset(y_mundo)
        return -altura <= y_tela <= config.ALTURA_TELA
    
    def obter_area_visivel(self):
        """
        Retorna a área visível do mundo (coordenadas Y)

        Returns:
            tuple: (y_superior, y_inferior) em coordenadas do mundo
        """
        y_superior = self.obter_y_mundo(0)
        y_inferior = self.obter_y_mundo(config.ALTURA_TELA)
        return (y_superior, y_inferior)

    def get_world_view_rect(self, padding=0):
        """Retorna um retângulo do mundo correspondente à área visível da câmera."""
        altura_padding = padding * 2
        y_superior, y_inferior = self.obter_area_visivel()
        altura = (y_inferior - y_superior) + altura_padding
        y_inicio = y_superior - padding
        return pygame.Rect(-padding, y_inicio, config.LARGURA_TELA + padding * 2, altura)

    def rect_intersects_view(self, rect, padding=0):
        """Verifica se um retângulo do mundo cruza a área visível (com margem)."""
        return self.get_world_view_rect(padding).colliderect(rect)

    def world_to_screen(self, rect_or_pos):
        """Converte coordenadas do mundo para a tela, preservando tipos básicos."""
        if isinstance(rect_or_pos, pygame.Rect):
            novo = rect_or_pos.copy()
            novo.y -= int(self.offset_y)
            return novo

        if isinstance(rect_or_pos, (tuple, list)) and len(rect_or_pos) >= 2:
            x, y = rect_or_pos[:2]
            return (int(x), int(y - self.offset_y))

        raise TypeError("world_to_screen aceita pygame.Rect ou tuplas (x, y)")
    
    def resetar(self):
        """Reseta a câmera para posição inicial - AJUSTADO PARA GRID 32px"""
        # Calcular posição inicial baseada no grid moderno
        # Jogador começa 4 células do fundo (grid perfeito)
        grid_y_inicial = config.GRID_ALTURA - 4
        y_mundo_inicial = grid_y_inicial * config.TAMANHO_CELL + config.TAMANHO_CELL // 2
        
        # Posição do jogador na tela (proporcional à nova resolução)
        posicao_tela_jogador = config.ALTURA_TELA - (config.TAMANHO_CELL * 5)  # 5 células do fundo
        
        # Offset inicial para mostrar jogador na posição correta
        self.target_offset = y_mundo_inicial - posicao_tela_jogador
        self.offset_y = self.target_offset  # Snap inicial imediato
        self.scroll_ativo = False
        self.jogador_y = y_mundo_inicial
    
    def ativar_scroll(self):
        """Ativa o scroll automático"""
        self.scroll_ativo = True
    
    def desativar_scroll(self):
        """Desativa o scroll automático"""
        self.scroll_ativo = False
    
    def ajustar_velocidade_scroll(self, velocidade):
        """
        Ajusta a velocidade do scroll
        
        Args:
            velocidade: Nova velocidade
        """
        self.velocidade_scroll = velocidade
    
    def __repr__(self):
        return f"Camera(offset_y={self.offset_y:.1f}, target={self.target_offset:.1f})"

