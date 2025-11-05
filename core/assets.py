"""Robust asset loading helpers used across the project."""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Callable, Optional, Tuple

import pygame

LOGGER = logging.getLogger(__name__)

_BASE_DIR = Path(__file__).resolve().parent.parent
_ASSETS_DIR = _BASE_DIR / "assets"

_FAILED_IMAGE_PATHS: set[str] = set()
_MISSING_IMAGE_PATHS: set[str] = set()
_FAILED_SOUND_PATHS: set[str] = set()
_MISSING_SOUND_PATHS: set[str] = set()
_FAILED_MUSIC_PATHS: set[str] = set()
_MISSING_MUSIC_PATHS: set[str] = set()
_FAILED_FONT_PATHS: set[str] = set()
_MISSING_FONT_PATHS: set[str] = set()


class SilentSound:
    """Sound-like object that performs no action."""

    def play(self, *_, **__):
        return None

    def stop(self):
        return None

    def fadeout(self, *_):
        return None

    def set_volume(self, *_):
        return None

    def get_length(self):
        return 0.0


FallbackDrawer = Callable[[pygame.Surface], None]


def _resolve_path(path: Optional[str]) -> Tuple[Optional[Path], bool]:
    """Return a candidate path and whether it exists."""
    if not path:
        return None, False

    candidate = Path(path)
    search_paths = []
    if candidate.is_absolute():
        search_paths.append(candidate)
    else:
        search_paths.extend(
            [
                _ASSETS_DIR / candidate,
                _BASE_DIR / candidate,
                Path.cwd() / candidate,
            ]
        )

    for candidate_path in search_paths:
        if candidate_path.exists():
            return candidate_path, True

    return (search_paths[0] if search_paths else candidate), False


def _create_placeholder_surface(size: Tuple[int, int]) -> pygame.Surface:
    surface = pygame.Surface(size, pygame.SRCALPHA)
    surface.fill((200, 50, 50, 180))
    pygame.draw.line(surface, (255, 255, 255), (0, 0), (size[0], size[1]), 3)
    pygame.draw.line(surface, (255, 255, 255), (0, size[1]), (size[0], 0), 3)
    return surface


def load_image(
    path: Optional[str],
    *,
    size: Optional[Tuple[int, int]] = None,
    fallback_draw: Optional[FallbackDrawer] = None,
    convert_alpha: bool = True,
) -> Tuple[pygame.Surface, bool]:
    """Load an image from disk or create a placeholder surface."""
    resolved_path, exists = _resolve_path(path)

    if path and exists:
        try:
            image = pygame.image.load(str(resolved_path))
            if convert_alpha and pygame.display.get_init():
                image = image.convert_alpha()
            elif not convert_alpha and pygame.display.get_init():
                image = image.convert()
            if size and image.get_size() != size:
                image = pygame.transform.smoothscale(image, size)
            return image, False
        except Exception as exc:  # noqa: BLE001 - we want to catch all pygame loading issues
            if path not in _FAILED_IMAGE_PATHS:
                LOGGER.warning("Falha ao carregar imagem '%s': %s. Usando substituto gerado.", path, exc)
                _FAILED_IMAGE_PATHS.add(path)
    elif path:
        if path not in _MISSING_IMAGE_PATHS:
            LOGGER.warning("Imagem '%s' não encontrada. Usando substituto gerado.", path)
            _MISSING_IMAGE_PATHS.add(path)

    final_size = size or (64, 64)
    surface = _create_placeholder_surface(final_size)
    if fallback_draw:
        try:
            surface.fill((0, 0, 0, 0))
            fallback_draw(surface)
        except Exception as exc:  # noqa: BLE001 - desenho não pode quebrar execução
            LOGGER.warning("Falha ao desenhar substituto para '%s': %s", path, exc)
    return surface, True


def load_sound(path: Optional[str]) -> Tuple[object, bool]:
    """Load a sound or return a silent placeholder."""
    if not pygame.mixer.get_init():
        try:
            pygame.mixer.init()  # type: ignore[no-untyped-call]
        except Exception as exc:  # noqa: BLE001 - mixer init may fail in headless envs
            if path not in _FAILED_SOUND_PATHS:
                LOGGER.warning(
                    "Mixer não pôde ser inicializado para som '%s': %s. Usando som silencioso.",
                    path,
                    exc,
                )
                _FAILED_SOUND_PATHS.add(path or "<mixer>")
            return SilentSound(), True

    resolved_path, exists = _resolve_path(path)
    if path and exists:
        try:
            return pygame.mixer.Sound(str(resolved_path)), False
        except Exception as exc:  # noqa: BLE001
            if path not in _FAILED_SOUND_PATHS:
                LOGGER.warning("Falha ao carregar som '%s': %s. Usando som silencioso.", path, exc)
                _FAILED_SOUND_PATHS.add(path)
            return SilentSound(), True
    elif path:
        if path not in _MISSING_SOUND_PATHS:
            LOGGER.warning("Som '%s' não encontrado. Usando som silencioso.", path)
            _MISSING_SOUND_PATHS.add(path)
    return SilentSound(), True


def load_font(path: Optional[str], size: int) -> Tuple[pygame.font.Font, bool]:
    """Load a font from disk or fall back to the default pygame font."""
    if not pygame.font.get_init():
        pygame.font.init()

    resolved_path, exists = _resolve_path(path)
    using_placeholder = False
    if path and exists:
        try:
            return pygame.font.Font(str(resolved_path), size), False
        except Exception as exc:  # noqa: BLE001
            if path not in _FAILED_FONT_PATHS:
                LOGGER.warning("Falha ao carregar fonte '%s': %s. Usando fonte padrão.", path, exc)
                _FAILED_FONT_PATHS.add(path)
            using_placeholder = True
    elif path:
        if path not in _MISSING_FONT_PATHS:
            LOGGER.warning("Fonte '%s' não encontrada. Usando fonte padrão.", path)
            _MISSING_FONT_PATHS.add(path)
        using_placeholder = True

    try:
        return pygame.font.Font(None, size), using_placeholder
    except Exception as exc:  # noqa: BLE001
        LOGGER.error("Falha ao carregar fonte padrão: %s. Tentando pygame.font.SysFont.", exc)
        default_name = pygame.font.get_default_font() or "arial"
        return pygame.font.SysFont(default_name, size), True


def load_music(path: Optional[str]) -> bool:
    """Load music into pygame.mixer.music, returning True on success."""
    if not path:
        LOGGER.warning("Nenhum caminho fornecido para música. Ignorando carregamento.")
        return False

    if not pygame.mixer.get_init():
        try:
            pygame.mixer.init()  # type: ignore[no-untyped-call]
        except Exception as exc:  # noqa: BLE001
            if path not in _FAILED_MUSIC_PATHS:
                LOGGER.warning("Mixer não pôde ser inicializado para música '%s': %s", path, exc)
                _FAILED_MUSIC_PATHS.add(path)
            return False

    resolved_path, exists = _resolve_path(path)
    if exists:
        try:
            pygame.mixer.music.load(str(resolved_path))
            return True
        except Exception as exc:  # noqa: BLE001
            if path not in _FAILED_MUSIC_PATHS:
                LOGGER.warning("Falha ao carregar música '%s': %s", path, exc)
                _FAILED_MUSIC_PATHS.add(path)
    else:
        if path not in _MISSING_MUSIC_PATHS:
            LOGGER.warning("Música '%s' não encontrada.", path)
            _MISSING_MUSIC_PATHS.add(path)
    return False
