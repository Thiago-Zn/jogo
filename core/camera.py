"""Camera system with dead-zone tracking and interpolation support."""

from __future__ import annotations

import math
from typing import Optional, Sequence, Tuple

import pygame
from pygame.math import Vector2


class Camera:
    """2D camera with dead-zone tracking and interpolation aware transforms."""

    def __init__(
        self,
        viewport_size: Sequence[float],
        *,
        world_bounds: Optional[pygame.Rect | Tuple[int, int, int, int]] = None,
        deadzone: Optional[pygame.Rect | Tuple[float, float, float, float]] = None,
    ) -> None:
        width, height = int(viewport_size[0]), int(viewport_size[1])
        if width <= 0 or height <= 0:
            raise ValueError("viewport_size must be positive")

        self.viewport_rect = pygame.Rect(0, 0, width, height)
        self._viewport_size = Vector2(width, height)

        self._position = Vector2(0, 0)
        self._previous_position = Vector2(0, 0)

        self._bounds_min = Vector2(-math.inf, -math.inf)
        self._bounds_max = Vector2(math.inf, math.inf)
        self.world_bounds: Optional[pygame.Rect] = None
        if world_bounds is not None:
            self.set_world_bounds(world_bounds)

        self.deadzone = pygame.Rect(0, 0, 0, 0)
        self.set_deadzone(deadzone)

    @property
    def position(self) -> Vector2:
        """Current camera position (top-left) in world space."""

        return self._position

    @property
    def previous_position(self) -> Vector2:
        """Previous camera position used for interpolation."""

        return self._previous_position

    @property
    def viewport_size(self) -> Tuple[int, int]:
        """Return the viewport size as an integer tuple."""

        return self.viewport_rect.width, self.viewport_rect.height

    def set_world_bounds(self, bounds: Optional[pygame.Rect | Tuple[int, int, int, int]]) -> None:
        """Update the world bounds used for clamping the camera."""

        if bounds is None:
            self.world_bounds = None
            self._bounds_min.xy = (-math.inf, -math.inf)
            self._bounds_max.xy = (math.inf, math.inf)
        else:
            rect = pygame.Rect(bounds)
            self.world_bounds = rect
            self._bounds_min.xy = (rect.left, rect.top)
            self._bounds_max.xy = (rect.right, rect.bottom)

        self._clamp_to_world()
        self._previous_position.xy = self._position

    def set_deadzone(self, deadzone: Optional[pygame.Rect | Tuple[float, float, float, float]]) -> None:
        """Configure the dead-zone rectangle relative to the viewport."""

        if deadzone is None:
            width = int(self.viewport_rect.width * 0.4)
            height = int(self.viewport_rect.height * 0.4)
            left = (self.viewport_rect.width - width) // 2
            top = (self.viewport_rect.height - height) // 2
            rect = pygame.Rect(left, top, width, height)
        else:
            rect = pygame.Rect(deadzone)

        rect.width = max(1, min(rect.width, self.viewport_rect.width))
        rect.height = max(1, min(rect.height, self.viewport_rect.height))
        rect.left = max(0, min(rect.left, self.viewport_rect.width - rect.width))
        rect.top = max(0, min(rect.top, self.viewport_rect.height - rect.height))
        self.deadzone = rect

    def move_to(self, position: Sequence[float]) -> None:
        """Snap the camera to a world position (top-left)."""

        self._position.xy = position
        self._clamp_to_world()
        self._previous_position.xy = self._position

    def follow(self, target: Optional[pygame.Rect]) -> None:
        """Adjust the camera to keep *target* within the configured dead-zone."""

        if target is None:
            return

        self._previous_position.xy = self._position

        target_center = Vector2(target.centerx, target.centery)
        relative = target_center - self._position

        dx = 0.0
        if relative.x < self.deadzone.left:
            dx = relative.x - self.deadzone.left
        elif relative.x > self.deadzone.right:
            dx = relative.x - self.deadzone.right

        dy = 0.0
        if relative.y < self.deadzone.top:
            dy = relative.y - self.deadzone.top
        elif relative.y > self.deadzone.bottom:
            dy = relative.y - self.deadzone.bottom

        if dx or dy:
            self._position.x += dx
            self._position.y += dy
            self._clamp_to_world()

    def get_offset(self, interpolation: float = 1.0) -> Vector2:
        """Return the interpolated camera position as a vector."""

        return self._interpolated_position(interpolation)

    def get_view_rect(self, interpolation: float = 1.0) -> pygame.Rect:
        """Return the interpolated viewport rectangle in world coordinates."""

        offset = self._interpolated_position(interpolation)
        return pygame.Rect(
            int(round(offset.x)),
            int(round(offset.y)),
            self.viewport_rect.width,
            self.viewport_rect.height,
        )

    def world_to_screen(
        self, position: Sequence[float], interpolation: float = 1.0
    ) -> Tuple[int, int]:
        """Convert a world position to screen coordinates."""

        offset = self._interpolated_position(interpolation)
        pos = Vector2(position) - offset
        return int(round(pos.x)), int(round(pos.y))

    def screen_to_world(
        self, position: Sequence[float], interpolation: float = 1.0
    ) -> Tuple[int, int]:
        """Convert screen coordinates to world space."""

        offset = self._interpolated_position(interpolation)
        pos = Vector2(position) + offset
        return int(round(pos.x)), int(round(pos.y))

    def _interpolated_position(self, interpolation: float) -> Vector2:
        """Compute the interpolated camera position between frames."""

        t = max(0.0, min(1.0, interpolation))
        if t == 1.0:
            return self._position.copy()
        if t == 0.0:
            return self._previous_position.copy()
        return self._previous_position.lerp(self._position, t)

    def _clamp_to_world(self) -> None:
        """Clamp the camera position to the configured world bounds."""

        min_x, min_y = self._bounds_min
        max_x, max_y = self._bounds_max

        if math.isfinite(min_x) or math.isfinite(max_x):
            max_allowed_x = max_x - self.viewport_rect.width
            if max_allowed_x < min_x:
                self._position.x = min_x
            else:
                self._position.x = max(min_x, min(self._position.x, max_allowed_x))

        if math.isfinite(min_y) or math.isfinite(max_y):
            max_allowed_y = max_y - self.viewport_rect.height
            if max_allowed_y < min_y:
                self._position.y = min_y
            else:
                self._position.y = max(min_y, min(self._position.y, max_allowed_y))

