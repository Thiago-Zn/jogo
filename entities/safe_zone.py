"""
Classe de Área de Descanso (Safe Zone)
"""

import pygame
import config


class SafeZone:
    """Classe que representa uma área de descanso segura"""

    def __init__(self, y_pos, altura=None):
        """
        Inicializa uma área de descanso
        
        Args:
            y_pos: Posição Y no mundo (coordenada vertical)
            altura: Altura da zona (padrão: ALTURA_AREA_DESCANSO)
        """
        self.y_pos = y_pos
        self.altura = altura if altura else config.ALTURA_AREA_DESCANSO
        self.largura = config.LARGURA_TELA
        self.ativa = True
        
        # Cores para renderização - MAIS CLARAS E VISÍVEIS
        self.cor_principal = (100, 200, 100)  # Verde mais claro e vibrante
        self.cor_detalhe = (80, 180, 80)  # Verde médio
        self.cor_borda = (60, 160, 60)  # Verde escuro para borda
        
        # Para animações futuras
        self.tempo_animacao = 0
        
    def esta_dentro(self, y):
        """
        Verifica se uma coordenada Y está dentro da zona
        
        Args:
            y: Coordenada Y a verificar
            
        Returns:
            bool: True se está dentro da zona
        """
        return self.y_pos <= y <= self.y_pos + self.altura
    
    def colidir_com_jogador(self, jogador):
        """
        Verifica colisão com o jogador
        
        Args:
            jogador: Objeto Jogador
            
        Returns:
            bool: True se jogador está dentro da área de descanso
        """
        jogador_y = jogador.rect.centery
        return self.esta_dentro(jogador_y)
    
    def renderizar(self, surface, camera, interpolation=1.0):
        """
        Desenha a área de descanso na tela

        Args:
            surface: Surface do pygame onde desenhar
            camera: Instância da câmera para transformar coordenadas
            interpolation: Fator de interpolação entre atualizações de física
        """
        _, y_tela = camera.world_to_screen((0, self.y_pos), interpolation)

        # Não renderizar se estiver fora da tela
        if y_tela + self.altura < 0 or y_tela > camera.viewport_rect.height:
            return

        # Desenhar fundo principal da área de descanso - MAIS VISÍVEL
        pygame.draw.rect(
            surface,
            self.cor_principal,
            (0, y_tela, self.largura, self.altura)
        )
        
        # BORDA VISÍVEL para destacar safe zone
        pygame.draw.rect(
            surface,
            self.cor_borda,
            (0, y_tela, self.largura, self.altura),
            3  # Borda grossa
        )
        
        # Linha central para indicar área segura
        pygame.draw.line(
            surface,
            self.cor_detalhe,
            (0, y_tela + self.altura // 2),
            (self.largura, y_tela + self.altura // 2),
            2
        )
        
        # Adicionar textura de grama (pequenos detalhes)
        self._desenhar_textura_grama(surface, y_tela)

        # Adicionar bordas sutis para indicar zona segura
        self._desenhar_bordas(surface, y_tela)
    
    def _desenhar_textura_grama(self, surface, y_tela):
        """
        Desenha textura de grama na área de descanso
        
        Args:
            surface: Surface do pygame
            y_tela: Posição Y na tela
        """
        # Desenhar pequenos detalhes de grama em padrão
        import random
        random.seed(int(self.y_pos))  # Seed baseado na posição para consistência
        
        for i in range(0, self.largura, 20):
            for j in range(0, int(self.altura), 15):
                # Pequenas linhas de grama
                if random.random() > 0.3:
                    x = i + random.randint(-5, 5)
                    y = y_tela + j + random.randint(-3, 3)
                    altura_linha = random.randint(3, 6)
                    
                    pygame.draw.line(
                        surface,
                        self.cor_detalhe,
                        (x, y),
                        (x, y + altura_linha),
                        1
                    )
    
    def _desenhar_bordas(self, surface, y_tela):
        """
        Desenha bordas sutis na área de descanso
        
        Args:
            surface: Surface do pygame
            y_tela: Posição Y na tela
        """
        # Borda superior (mais escura)
        pygame.draw.line(
            surface,
            config.VERDE_ESCURO,
            (0, y_tela),
            (self.largura, y_tela),
            2
        )
        
        # Borda inferior (mais escura)
        pygame.draw.line(
            surface,
            config.VERDE_ESCURO,
            (0, y_tela + self.altura),
            (self.largura, y_tela + self.altura),
            2
        )
    
    def update(self, delta_time=0):
        """
        Atualiza a área de descanso (para animações futuras)
        
        Args:
            delta_time: Tempo desde último frame
        """
        self.tempo_animacao += delta_time
    
    def desativar(self):
        """Desativa a área de descanso"""
        self.ativa = False
    
    def __repr__(self):
        return f"SafeZone(y={self.y_pos}, altura={self.altura}, ativa={self.ativa})"

