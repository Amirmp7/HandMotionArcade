"""
Settings management system.

Handles player preferences like colors, sound, ball/paddle styles, and background.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
import json
import pygame

from config import BACKGROUND_THEMES


@dataclass(slots=True)
class Settings:
    """Player settings."""
    ball_color: tuple[int, int, int] = (255, 80, 80)
    paddle_color: tuple[int, int, int] = (240, 240, 240)
    
    # "circle", "square", "triangle"
    ball_shape: str = "circle"
    sound_enabled: bool = True
    default_level: str = "medium"
    last_player_name: str = ""
    background_theme: str = "deep_blue"
    
    def to_dict(self) -> dict:
        return {
            "ball_color": self.ball_color,
            "paddle_color": self.paddle_color,
            "ball_shape": self.ball_shape,
            "sound_enabled": self.sound_enabled,
            "default_level": self.default_level,
            "last_player_name": self.last_player_name,
            "background_theme": self.background_theme,
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> Settings:
        return cls(
            ball_color=tuple(data.get("ball_color", (255, 80, 80))),
            paddle_color=tuple(data.get("paddle_color", (240, 240, 240))),
            ball_shape=data.get("ball_shape", "circle"),
            sound_enabled=data.get("sound_enabled", True),
            default_level=data.get("default_level", "medium"),
            last_player_name=data.get("last_player_name", ""),
            background_theme=data.get("background_theme", "deep_blue"),
        )


class SettingsManager:
    """Loads and saves settings to a JSON file."""
    
    def __init__(self, file_path: Path) -> None:
        self.file_path = file_path
        self.settings = self.load()
    
    def load(self) -> Settings:
        if not self.file_path.exists():
            return Settings()
        
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return Settings.from_dict(data)
        except:
            return Settings()
    
    def save(self) -> None:
        self.file_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.file_path, 'w', encoding='utf-8') as f:
            json.dump(self.settings.to_dict(), f, indent=2)
    
    def set(self, **kwargs) -> None:
        for key, value in kwargs.items():
            if hasattr(self.settings, key):
                setattr(self.settings, key, value)
        self.save()
    
    def get_background_colors(self) -> tuple[tuple[int, int, int], tuple[int, int, int]]:
        """Return the top and bottom background colors for the current theme."""
        theme = self.settings.background_theme
        if theme in BACKGROUND_THEMES:
            return BACKGROUND_THEMES[theme]
        return BACKGROUND_THEMES["deep_blue"]