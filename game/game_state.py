"""
Gerenciador de estados do jogo
"""

from enum import Enum


class GameState(Enum):
    """Estados possíveis do jogo"""
    MENU = "menu"
    PLAYING = "jogando"
    GAME_OVER = "game_over"
    VICTORY = "vitoria"

