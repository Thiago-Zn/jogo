"""
Módulo de lógica do jogo
"""

from .game_state import GameState
from .collision import CollisionSystem
from .camera import Camera
from .procedural_generator import ProceduralGenerator
from .river_physics import RiverPhysics

__all__ = ['GameState', 'CollisionSystem', 'Camera', 'ProceduralGenerator', 'RiverPhysics']

