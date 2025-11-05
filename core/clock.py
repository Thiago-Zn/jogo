"""Utilities for driving fixed-step simulation loops."""

from __future__ import annotations

import time
from typing import Callable, Optional

PHYSICS_HZ = 120
_MAX_FRAME_TIME = 0.25  # seconds


class FixedStepClock:
    """Accumulates frame time and executes a fixed-step callback."""

    def __init__(self, physics_hz: int = PHYSICS_HZ) -> None:
        if physics_hz <= 0:
            raise ValueError("physics_hz must be positive")
        self.physics_hz = physics_hz
        self.dt = 1.0 / float(physics_hz)
        self._accumulator = 0.0
        self._last_time = time.perf_counter()

    def reset(self) -> None:
        """Resets the accumulator so the next step starts fresh."""
        self._accumulator = 0.0
        self._last_time = time.perf_counter()

    def step(
        self,
        update_fn: Callable[[float], None],
        render_fn: Optional[Callable[[float], None]] = None,
    ) -> float:
        """Advance the simulation, running ``update_fn`` at a fixed time step.

        Args:
            update_fn: Callback executed once per fixed step. Receives ``dt``.
            render_fn: Optional callback executed once per outer frame with the
                interpolation factor between the last completed update and the
                next one. Receives ``alpha`` in ``[0, 1)``.

        Returns:
            The interpolation factor that was supplied to ``render_fn`` (or the
            current accumulator ratio if ``render_fn`` is not provided).
        """
        now = time.perf_counter()
        frame_time = now - self._last_time
        self._last_time = now

        if frame_time > _MAX_FRAME_TIME:
            frame_time = _MAX_FRAME_TIME

        self._accumulator += frame_time

        while self._accumulator >= self.dt:
            update_fn(self.dt)
            self._accumulator -= self.dt

        alpha = self._accumulator / self.dt if self.dt else 0.0

        if render_fn is not None:
            render_fn(alpha)

        return alpha
