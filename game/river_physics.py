"""
Sistema de Física do Rio
"""

import pygame
import config


class RiverPhysics:
    """Gerencia a física do jogador no rio (apenas troncos, água)"""

    def __init__(self):
        """Inicializa o sistema de física do rio"""
        self.jogador_em_plataforma = False
        self.plataforma_atual = None
        self.jogador_na_agua = False
    
    def verificar_colisao_plataformas(self, jogador, plataformas):
        """
        Verifica se o jogador está em uma plataforma (apenas troncos)
        
        Args:
            jogador: Objeto Jogador
            plataformas: Lista de plataformas (apenas Troncos)
            
        Returns:
            tuple: (esta_em_plataforma, plataforma) ou (False, None)
        """
        # Usar rect do jogador - colisão precisa
        jogador_rect = jogador.rect.copy()
        
        for plataforma in plataformas:
            # Verificar colisão PRECISA
            if jogador_rect.colliderect(plataforma.rect):
                # Verificar se está realmente sobre a plataforma (centro dentro)
                if plataforma.rect.left <= jogador_rect.centerx <= plataforma.rect.right:
                    # Troncos sempre disponíveis - sem complicação
                    return (True, plataforma)
        
        return (False, None)
    
    def verificar_afogamento(self, jogador, y_rio_inicio, y_rio_fim, plataformas):
        """
        Verifica se o jogador está na água sem plataforma
        
        Args:
            jogador: Objeto Jogador
            y_rio_inicio: Y inicial da área de rio
            y_rio_fim: Y final da área de rio
            plataformas: Lista de plataformas
            
        Returns:
            bool: True se jogador está afogando
        """
        # Verificar se jogador está na área do rio
        jogador_y = jogador.rect.centery
        
        if y_rio_inicio <= jogador_y <= y_rio_fim:
            # Está na área do rio, verificar se está em plataforma
            esta_em_plataforma, _ = self.verificar_colisao_plataformas(jogador, plataformas)
            
            if not esta_em_plataforma:
                self.jogador_na_agua = True
                return True
        
        self.jogador_na_agua = False
        return False
    
    def aplicar_movimento_plataforma(self, jogador, plataformas, delta_time=1/60):
        """
        Move o jogador junto com a plataforma se estiver em cima de uma

        Args:
            jogador: Objeto Jogador
            plataformas: Lista de plataformas
            delta_time: Tempo desde o último frame (em segundos)
        """
        esta_em_plataforma, plataforma = self.verificar_colisao_plataformas(jogador, plataformas)

        if esta_em_plataforma and plataforma:
            self.jogador_em_plataforma = True
            self.plataforma_atual = plataforma

            # Mover jogador com o tronco - MOVIMENTO FLUIDO E SINCRONIZADO
            if hasattr(plataforma, 'velocidade'):
                # Mover posição X do jogador junto com o tronco (movimento livre em pixels)
                # Movimento baseado em velocidade em pixels por segundo
                movimento = plataforma.velocidade * plataforma.direcao * 60 * delta_time
                jogador.x += movimento

                # Atualizar rect visual
                jogador.rect.centerx = int(jogador.x)

                # Limitar dentro da tela (movimento livre mas com limites)
                min_x = jogador.rect.width // 2
                max_x = config.LARGURA_TELA - jogador.rect.width // 2
                if jogador.x < min_x:
                    jogador.x = float(min_x)
                    jogador.rect.centerx = int(jogador.x)
                elif jogador.x > max_x:
                    jogador.x = float(max_x)
                    jogador.rect.centerx = int(jogador.x)
        else:
            # Jogador saiu da plataforma - não precisa fazer nada especial
            pass
        self.jogador_em_plataforma = esta_em_plataforma and plataforma is not None
        if not self.jogador_em_plataforma:
            self.plataforma_atual = None
    
    def atualizar(self, jogador, chunks_rio, delta_time=1/60):
        """
        Atualiza a física do rio para o jogador

        Args:
            jogador: Objeto Jogador
            chunks_rio: Lista de TODOS os chunks de rio (não apenas visíveis)
            delta_time: Tempo desde o último frame (em segundos)

        Returns:
            dict: Status da física {
                'afogando': bool,
                'em_plataforma': bool,
                'plataforma': objeto ou None
            }
        """
        # Coletar todas as plataformas dos chunks de rio
        plataformas = []
        areas_rio = []

        for chunk in chunks_rio:
            if chunk.tipo == 'rio':
                # Adicionar plataformas do chunk
                plataformas.extend(chunk.dados.get('plataformas', []))
                areas_rio.append((chunk.y_inicio, chunk.y_fim))

        # Aplicar movimento de plataforma com delta time
        if plataformas:
            self.aplicar_movimento_plataforma(jogador, plataformas, delta_time)

        # Verificar afogamento
        afogando = False
        for y_inicio, y_fim in areas_rio:
            if self.verificar_afogamento(jogador, y_inicio, y_fim, plataformas):
                afogando = True
                break

        return {
            'afogando': afogando,
            'em_plataforma': self.jogador_em_plataforma,
            'plataforma': self.plataforma_atual
        }
    
    def resetar(self):
        """Reseta o estado da física do rio"""
        self.jogador_em_plataforma = False
        self.plataforma_atual = None
        self.jogador_na_agua = False
    
    def __repr__(self):
        return f"RiverPhysics(plataforma={self.jogador_em_plataforma}, agua={self.jogador_na_agua})"

