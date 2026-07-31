"""
Audio management module.

Handles loading and playing sound effects for the game.
If a sound file is missing, the game continues without crashing.
"""

from __future__ import annotations

from pathlib import Path

import pygame

from config import GameConfig

from config import resource_path 


class AudioManager:
    """Simple sound effect manager."""

    def __init__(self, config: GameConfig) -> None:
        self.config = config

        try:
            pygame.mixer.init()
        except pygame.error:
            self.enabled = False
            return

        self.enabled = True

        self.bounce = self._load_sound("bounce.wav")
        self.coin = self._load_sound("coin.wav")
        self.game_over = self._load_sound("game_over.wav")
        self.bomb = self._load_sound("bomb.wav")

    def _load_sound(self, filename: str) -> pygame.mixer.Sound | None:
        """Load a sound file safely."""
        path = self.config.paths.sounds / filename  

        if not path.exists():
            return None

        try:
            sound = pygame.mixer.Sound(str(path))
            sound.set_volume(self.config.audio.effects_volume)
            return sound
        except pygame.error:
            return None

    def play_bounce(self) -> None:
        if self.enabled and self.bounce:
            self.bounce.play()

    def play_coin(self) -> None:
        if self.enabled and self.coin:
            self.coin.play()

    def play_game_over(self) -> None:
        if self.enabled and self.game_over:
            self.game_over.play()

    def stop_all(self) -> None:
        if self.enabled:
            pygame.mixer.stop()
            
    def play_bomb(self) -> None:                   
        if self.enabled and self.bomb:
            self.bomb.play()