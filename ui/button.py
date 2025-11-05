"""
Sistema de Botões Clicáveis
"""

import pygame
import config
from core.assets import load_font


class Button:
    """Classe que representa um botão clicável"""

    def __init__(self, x, y, largura, altura, texto, callback=None):
        """
        Inicializa um botão
        
        Args:
            x: Posição X (centro)
            y: Posição Y (centro)
            largura: Largura do botão
            altura: Altura do botão
            texto: Texto do botão
            callback: Função a chamar quando clicado
        """
        self.x = x
        self.y = y
        self.largura = largura
        self.altura = altura
        self.texto = texto
        self.callback = callback
        
        # Estados
        self.estado = 'normal'  # normal, hover, pressed
        self.habilitado = True
        
        # Cores
        self.cor_normal = config.VERDE
        self.cor_hover = config.VERDE_ESCURO
        self.cor_pressed = (20, 100, 40)
        self.cor_desabilitado = config.CINZA
        self.cor_texto = config.BRANCO
        
        # Criar rect
        self.rect = pygame.Rect(
            x - largura // 2,
            y - altura // 2,
            largura,
            altura
        )
        
        # Fonte
        self.fonte, _ = load_font(None, 36)
        
        # Animação
        self.escala = 1.0
        self.target_escala = 1.0
    
    def atualizar(self, mouse_pos, mouse_pressed):
        """
        Atualiza o estado do botão
        
        Args:
            mouse_pos: Posição do mouse (x, y)
            mouse_pressed: Tupla de botões do mouse pressionados
            
        Returns:
            bool: True se foi clicado
        """
        if not self.habilitado:
            self.estado = 'normal'
            return False
        
        # Verificar se mouse está sobre o botão
        if self.rect.collidepoint(mouse_pos):
            # Mouse sobre o botão
            if mouse_pressed[0]:  # Botão esquerdo pressionado
                self.estado = 'pressed'
                self.target_escala = 0.95
            else:
                # Mouse sobre mas não pressionado
                if self.estado == 'pressed':
                    # Foi clicado!
                    self.estado = 'hover'
                    self.target_escala = 1.05
                    if self.callback:
                        self.callback()
                    return True
                else:
                    self.estado = 'hover'
                    self.target_escala = 1.05
        else:
            self.estado = 'normal'
            self.target_escala = 1.0
        
        # Animação suave de escala
        if abs(self.escala - self.target_escala) > 0.01:
            self.escala += (self.target_escala - self.escala) * 0.2
        
        return False
    
    def desenhar(self, surface):
        """
        Desenha o botão
        
        Args:
            surface: Surface onde desenhar
        """
        # Calcular rect com escala
        largura_escalada = int(self.largura * self.escala)
        altura_escalada = int(self.altura * self.escala)
        
        rect_escalado = pygame.Rect(
            self.x - largura_escalada // 2,
            self.y - altura_escalada // 2,
            largura_escalada,
            altura_escalada
        )
        
        # Escolher cor baseado no estado
        if not self.habilitado:
            cor = self.cor_desabilitado
        elif self.estado == 'pressed':
            cor = self.cor_pressed
        elif self.estado == 'hover':
            cor = self.cor_hover
        else:
            cor = self.cor_normal
        
        # Desenhar sombra
        sombra_rect = rect_escalado.copy()
        sombra_rect.x += 4
        sombra_rect.y += 4
        pygame.draw.rect(surface, (0, 0, 0, 100), sombra_rect, border_radius=10)
        
        # Desenhar botão principal
        pygame.draw.rect(surface, cor, rect_escalado, border_radius=10)
        
        # Desenhar borda
        borda_cor = config.BRANCO if self.estado == 'hover' else config.VERDE_ESCURO
        pygame.draw.rect(surface, borda_cor, rect_escalado, 3, border_radius=10)
        
        # Desenhar texto
        texto_surface = self.fonte.render(self.texto, True, self.cor_texto)
        texto_rect = texto_surface.get_rect(center=(self.x, self.y))
        surface.blit(texto_surface, texto_rect)
    
    def definir_callback(self, callback):
        """Define a função de callback"""
        self.callback = callback
    
    def habilitar(self):
        """Habilita o botão"""
        self.habilitado = True
    
    def desabilitar(self):
        """Desabilita o botão"""
        self.habilitado = False
    
    def __repr__(self):
        return f"Button('{self.texto}', estado={self.estado})"


class ToggleButton(Button):
    """Botão de alternância (on/off)"""
    
    def __init__(self, x, y, largura, altura, texto, valor_inicial=False, callback=None):
        """
        Inicializa um botão de alternância
        
        Args:
            x, y: Posição
            largura, altura: Dimensões
            texto: Texto base
            valor_inicial: Estado inicial (True/False)
            callback: Função chamada com o novo valor
        """
        super().__init__(x, y, largura, altura, texto, callback)
        self.valor = valor_inicial
        self.atualizar_texto()
    
    def atualizar_texto(self):
        """Atualiza o texto do botão baseado no valor"""
        estado_texto = "ON" if self.valor else "OFF"
        self.texto = f"{self.texto.split(':')[0]}: {estado_texto}"
    
    def atualizar(self, mouse_pos, mouse_pressed):
        """Atualiza e alterna o valor quando clicado"""
        clicado = super().atualizar(mouse_pos, mouse_pressed)
        
        if clicado:
            self.valor = not self.valor
            self.atualizar_texto()
            if self.callback:
                self.callback(self.valor)
        
        return clicado
    
    def obter_valor(self):
        """Retorna o valor atual"""
        return self.valor
    
    def definir_valor(self, valor):
        """Define o valor"""
        self.valor = valor
        self.atualizar_texto()

