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
        self.plataforma_atual = None  # Plataforma em contato neste frame
        self.plataforma_anexada = None  # Plataforma mantida pelo coyote time
        self.jogador_na_agua = False
        self.coyote_timer = 0.0
        self.coyote_duration = 0.1  # 100 ms

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
    
    def _aplicar_movimento_plataforma(self, jogador, plataforma, delta_time=1/60):
        """Aplica movimento contínuo baseado na velocidade da plataforma."""
        if not plataforma:
            return

        deslocamento = getattr(plataforma, 'deslocamento_ultimo_passo', None)
        if deslocamento is None:
            # Fallback para plataformas antigas
            velocidade = getattr(plataforma, 'velocidade_horizontal', None)
            if velocidade is None:
                velocidade_base = getattr(plataforma, 'velocidade', 0.0)
                direcao = getattr(plataforma, 'direcao', 0)
                velocidade = velocidade_base * 60.0 * direcao
            deslocamento = velocidade * delta_time

        jogador.x += deslocamento

        # Limitar dentro da tela antes de sincronizar rects
        min_x = jogador.rect.width // 2
        max_x = config.LARGURA_TELA - jogador.rect.width // 2
        if jogador.x < min_x:
            jogador.x = float(min_x)
        elif jogador.x > max_x:
            jogador.x = float(max_x)

        jogador.rect.centerx = int(round(jogador.x))

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

        # Determinar contato com plataforma
        esta_em_plataforma, plataforma = self.verificar_colisao_plataformas(jogador, plataformas)
        self.jogador_em_plataforma = esta_em_plataforma and plataforma is not None
        self.plataforma_atual = plataforma if self.jogador_em_plataforma else None

        if self.jogador_em_plataforma:
            self.plataforma_anexada = plataforma
            self.coyote_timer = 0.0
        else:
            if self.plataforma_anexada is not None:
                self.coyote_timer += delta_time
                if self.coyote_timer >= self.coyote_duration:
                    self.plataforma_anexada = None
                    self.coyote_timer = 0.0
            else:
                self.coyote_timer = 0.0

        # Aplicar movimento baseado na plataforma atual em contato
        if self.plataforma_atual is not None:
            self._aplicar_movimento_plataforma(jogador, self.plataforma_atual, delta_time)

        # Verificar se jogador está em alguma área de rio
        jogador_y = jogador.rect.centery
        em_rio = any(y_inicio <= jogador_y <= y_fim for y_inicio, y_fim in areas_rio)

        if not em_rio:
            # Resetar estado se saiu da água
            self.plataforma_anexada = None
            self.coyote_timer = 0.0

        afogando = em_rio and self.plataforma_anexada is None
        self.jogador_na_agua = afogando

        coyote_restante = 0.0
        if self.plataforma_anexada is not None and not self.jogador_em_plataforma:
            coyote_restante = max(0.0, self.coyote_duration - self.coyote_timer)

        return {
            'afogando': afogando,
            'em_plataforma': self.jogador_em_plataforma,
            'plataforma': self.plataforma_atual,
            'anexado': self.plataforma_anexada is not None,
            'plataforma_anexada': self.plataforma_anexada,
            'coyote_restante': coyote_restante,
            'em_rio': em_rio
        }

    def resetar(self):
        """Reseta o estado da física do rio"""
        self.jogador_em_plataforma = False
        self.plataforma_atual = None
        self.plataforma_anexada = None
        self.jogador_na_agua = False
        self.coyote_timer = 0.0

    def __repr__(self):
        return f"RiverPhysics(plataforma={self.jogador_em_plataforma}, agua={self.jogador_na_agua})"

    def resetar_estado_jogador(self):
        """Limpa estados relacionados ao jogador (para respawns)."""
        self.jogador_em_plataforma = False
        self.plataforma_atual = None
        self.plataforma_anexada = None
        self.jogador_na_agua = False
        self.coyote_timer = 0.0

