"""Componentes do HUD do jogo."""

from __future__ import annotations

import pygame

import config


class HUD:
    """Classe responsável por desenhar o HUD durante o jogo."""

    def __init__(self, screen: pygame.Surface, font_pequena: pygame.font.Font,
                 font_media: pygame.font.Font | None = None) -> None:
        self.screen = screen
        self.font_pequena = font_pequena
        self.font_media = font_media or pygame.font.Font(None, max(48, font_pequena.get_height() * 2))
        self.outline_color = config.PRETO
        self.outline_width = 2

    # ------------------------------------------------------------------
    # Helpers
    def _render_text(self, texto: str, cor: tuple[int, int, int],
                     fonte: pygame.font.Font, outline: int | None = None) -> pygame.Surface:
        """Renderiza texto com contorno para facilitar a leitura."""

        outline = self.outline_width if outline is None else outline
        texto_surf = fonte.render(texto, True, cor)

        if outline <= 0:
            return texto_surf

        largura = texto_surf.get_width() + outline * 2
        altura = texto_surf.get_height() + outline * 2
        surface = pygame.Surface((largura, altura), pygame.SRCALPHA)

        contorno = fonte.render(texto, True, self.outline_color)
        for dx in (-outline, 0, outline):
            for dy in (-outline, 0, outline):
                if dx == 0 and dy == 0:
                    continue
                surface.blit(contorno, (dx + outline, dy + outline))

        surface.blit(texto_surf, (outline, outline))
        return surface

    def _draw_heart(self, pos_x: int, pos_y: int, tamanho: int,
                    cor_preenchimento: tuple[int, int, int]) -> None:
        """Desenha um ícone de coração preenchido na posição indicada."""

        tamanho = max(12, tamanho)
        raio = max(3, tamanho // 3)
        heart = pygame.Surface((tamanho, tamanho), pygame.SRCALPHA)

        centro = tamanho // 2
        topo = raio
        base = tamanho - 2

        pygame.draw.circle(heart, cor_preenchimento, (raio, topo), raio)
        pygame.draw.circle(heart, cor_preenchimento, (tamanho - raio, topo), raio)
        pygame.draw.polygon(heart, cor_preenchimento, [(0, topo), (tamanho, topo), (centro, base)])

        pygame.draw.circle(heart, self.outline_color, (raio, topo), raio, 2)
        pygame.draw.circle(heart, self.outline_color, (tamanho - raio, topo), raio, 2)
        pygame.draw.polygon(heart, self.outline_color, [(0, topo), (tamanho, topo), (centro, base)], 2)

        self.screen.blit(heart, (pos_x, pos_y))

    def _draw_lives(self, vidas: int, centro_x: int, topo_y: int) -> None:
        """Desenha os ícones de vida alinhados ao centro da tela."""

        max_vidas = max(vidas, getattr(config, "VIDAS_MAXIMAS", vidas))
        tamanho_icone = self.font_pequena.get_height() + 8
        espacamento = tamanho_icone + 6
        largura_total = max_vidas * espacamento - 6
        inicio_x = centro_x - largura_total // 2

        for indice in range(max_vidas):
            pos_x = inicio_x + indice * espacamento
            cor = config.VERMELHO if indice < vidas else config.CINZA
            self._draw_heart(pos_x, topo_y, tamanho_icone, cor)

    # ------------------------------------------------------------------
    # API pública
    def desenhar(self, pontuacao: int, nivel: int, vidas: int, tempo_decorrido: float,
                 *, melhor_pontuacao: int = 0, seed: int | str | None = None,
                 dificuldade: float = 1.0, distancia: float = 0.0,
                 camera_offset: float = 0.0, pausado: bool = False,
                 fps: float = 0.0, safe_zone: bool = False,
                 invulneravel: bool = False, estado_texto: str | None = None) -> None:
        """Desenha o HUD com informações de jogo e status."""

        largura_tela = self.screen.get_width()
        altura_tela = self.screen.get_height()
        margem = 16

        # Bloco superior esquerdo
        bloco_esquerdo = [
            f"Pontos: {pontuacao}",
            f"Melhor: {melhor_pontuacao}",
            f"Tempo: {tempo_decorrido:.1f}s",
            f"Distância: {int(distancia / max(1, config.TAMANHO_CELL))} células",
        ]

        y_esquerda = margem
        for linha in bloco_esquerdo:
            texto = self._render_text(linha, config.BRANCO, self.font_pequena)
            self.screen.blit(texto, (margem, y_esquerda))
            y_esquerda += texto.get_height() + 4

        # Bloco superior direito
        bloco_direito = [f"Nível: {nivel}"]
        if seed is not None:
            bloco_direito.append(f"Seed: {seed}")
        bloco_direito.extend([
            f"Dificuldade: {dificuldade:.2f}x",
            f"FPS: {fps:.0f}",
        ])

        y_direita = margem
        for linha in bloco_direito:
            texto = self._render_text(linha, config.BRANCO, self.font_pequena)
            rect = texto.get_rect(topright=(largura_tela - margem, y_direita))
            self.screen.blit(texto, rect)
            y_direita += texto.get_height() + 4

        # Vidas no topo central
        label_vidas = self._render_text("Vidas", config.BRANCO, self.font_pequena)
        label_rect = label_vidas.get_rect(midtop=(largura_tela // 2, margem))
        self.screen.blit(label_vidas, label_rect)
        self._draw_lives(vidas, largura_tela // 2, label_rect.bottom + 4)

        # Informações de status na parte inferior esquerda
        status_partes: list[str] = []
        if pausado:
            status_partes.append("Pausado")
        elif estado_texto:
            status_partes.append(estado_texto.capitalize())

        if safe_zone:
            status_partes.append("Área segura")
        if invulneravel:
            status_partes.append("Invulnerável")

        status_texto = "Status: " + (" | ".join(status_partes) if status_partes else "Explorando")
        if pausado:
            cor_status = config.AMARELO
        elif invulneravel:
            cor_status = config.LARANJA
        elif safe_zone:
            cor_status = config.VERDE
        else:
            cor_status = config.BRANCO
        status_surface = self._render_text(status_texto, cor_status, self.font_pequena)
        status_pos = (margem, altura_tela - status_surface.get_height() - margem)
        self.screen.blit(status_surface, status_pos)

        # Dados complementares no canto inferior direito
        camera_texto = self._render_text(
            f"Camera Y: {int(camera_offset)}", config.BRANCO, self.font_pequena
        )
        camera_rect = camera_texto.get_rect(
            bottomright=(largura_tela - margem, altura_tela - margem)
        )
        self.screen.blit(camera_texto, camera_rect)

        # Banner de pausa
        if pausado:
            largura_banner = largura_tela - margem * 2
            altura_banner = self.font_media.get_height() + 24
            banner_surface = pygame.Surface((largura_banner, altura_banner), pygame.SRCALPHA)
            banner_surface.fill((0, 0, 0, 180))

            banner_rect = banner_surface.get_rect(center=(largura_tela // 2, altura_tela // 2))
            self.screen.blit(banner_surface, banner_rect.topleft)

            titulo = self._render_text("JOGO PAUSADO", config.AMARELO, self.font_media, outline=3)
            titulo_rect = titulo.get_rect(center=(banner_rect.centerx, banner_rect.centery - 5))
            self.screen.blit(titulo, titulo_rect)

            subtitulo = self._render_text(
                "Pressione P para continuar ou R para reiniciar",
                config.BRANCO,
                self.font_pequena,
            )
            subtitulo_rect = subtitulo.get_rect(center=(banner_rect.centerx, banner_rect.centery + 28))
            self.screen.blit(subtitulo, subtitulo_rect)
