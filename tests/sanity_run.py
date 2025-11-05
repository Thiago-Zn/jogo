"""Sanity test for initializing and running the game loop without rendering."""

import os

# Configure pygame for headless environments before importing it
os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")
os.environ.setdefault("USE_LANE_CONFIG", "1")

import pygame

import config
from atravessar_rua import JogoAtraversarRua


def test_sanity_run_headless():
    pygame.init()
    pygame.font.init()

    try:
        jogo = JogoAtraversarRua()
        jogo.iniciar_novo_jogo()

        fixed_dt = 1.0 / config.FPS
        total_time = 3.0
        steps = int(total_time / fixed_dt)

        for _ in range(steps):
            pygame.event.pump()
            jogo.delta_time = fixed_dt
            jogo.atualizar()
    finally:
        pygame.quit()
