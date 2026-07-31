"""
Global configuration system.

All adjustable parameters of the game are centralized here.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

import numpy as np
import os
import sys

def resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller"""
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

# ==========================================================
# Project Paths
# ==========================================================

BASE_DIR = Path(__file__).parent

ASSETS_DIR = BASE_DIR / "assets"
SOUNDS_DIR = ASSETS_DIR / "sounds"
IMAGES_DIR = ASSETS_DIR / "images"
FONTS_DIR = ASSETS_DIR / "fonts"
DATA_DIR = BASE_DIR / "data"
HIGHSCORE_FILE = DATA_DIR / "highscore.json"
SETTINGS_FILE = DATA_DIR / "settings.json"


# ==========================================================
# Path Configuration
# ==========================================================

@dataclass(slots=True)
class PathConfig:
    assets: Path = ASSETS_DIR
    sounds: Path = SOUNDS_DIR
    images: Path = IMAGES_DIR
    fonts: Path = FONTS_DIR
    data: Path = DATA_DIR
    highscore_file: Path = HIGHSCORE_FILE
    settings_file: Path = SETTINGS_FILE


# ==========================================================
# Display Configuration
# ==========================================================

@dataclass(slots=True)
class DisplayConfig:
    width: int = 1280
    height: int = 720
    target_fps: int = 60
    show_fps: bool = False
    title: str = "Hand Motion Arcade"
    fullscreen: bool = False
    vsync: bool = True


# ==========================================================
# Color Themes
# ==========================================================
BACKGROUND_THEMES = {
    "deep_blue": ((35, 40, 80), (10, 12, 25)),
    "sunset": ((80, 40, 60), (30, 10, 40)),
    "forest": ((30, 60, 40), (10, 25, 20)),
    "midnight": ((20, 20, 40), (5, 5, 15)),
    "ocean": ((20, 60, 80), (5, 20, 40)),
    "lava": ((80, 30, 20), (40, 10, 5)),
}


@dataclass(slots=True)
class ColorConfig:
    background_top: tuple[int, int, int] = (35, 40, 80)
    background_bottom: tuple[int, int, int] = (10, 12, 25)
    
    white: tuple[int, int, int] = (240, 240, 240)
    red: tuple[int, int, int] = (255, 90, 90)
    gold: tuple[int, int, int] = (255, 215, 0)
    green: tuple[int, int, int] = (70, 230, 120)
    gray: tuple[int, int, int] = (160, 160, 160)
    hud_text: tuple[int, int, int] = (230, 230, 230)
    success: tuple[int, int, int] = (70, 230, 120)
    error: tuple[int, int, int] = (255, 80, 80)
    black: tuple[int, int, int] = (0, 0, 0)
    shadow: tuple[int, int, int] = (30, 30, 30)
    coin_shadow: tuple[int, int, int] = (180, 140, 20)
    secondary_text: tuple[int, int, int] = (180, 180, 180)
    panel: tuple[int, int, int] = (32, 36, 52)
    border: tuple[int, int, int] = (85, 92, 110)
    warning: tuple[int, int, int] = (255, 180, 0)
    bomb_color: tuple[int, int, int] = (200, 20, 20)  
    bomb_shadow: tuple[int, int, int] = (100, 10, 10)


# ==========================================================
# Player Configuration
# ==========================================================

@dataclass(slots=True)
class PlayerConfig:
    paddle_width: int = 150
    paddle_height: int = 18
    paddle_radius: int = 10
    bottom_margin: int = 50
    paddle_color: tuple[int, int, int] = (240, 240, 240)


# ==========================================================
# Ball Configuration
# ==========================================================

@dataclass(slots=True)
class BallConfig:
    size: int = 30
    initial_speed: float = 420.0
    speed_increment: float = 25.0
    maximum_speed: float = 1100.0
    radius: int = 15
    ball_color: tuple[int, int, int] = (255, 80, 80)


# ==========================================================
# Coin Configuration
# ==========================================================

@dataclass(slots=True)
class CoinConfig:
    size: int = 24
    count: int = 5
    spawn_padding: int = 30
    coin_color: tuple[int, int, int] = (255, 215, 0)


# ==========================================================
# Bomb Configuration (جدید)
# ==========================================================

@dataclass(slots=True)
class BombConfig:
    size: int = 28
    count: int = 3                
    spawn_padding: int = 30
    bomb_color: tuple[int, int, int] = (200, 20, 20)
    penalty: int = 5                


# ==========================================================
# Physics Configuration
# ==========================================================

@dataclass(slots=True)
class PhysicsConfig:
    gravity: float = 0.0
    paddle_hit_angle: float = 180.0
    enable_screen_shake: bool = False


# ==========================================================
# Hand Tracking Configuration
# ==========================================================

@dataclass(slots=True)
class HandConfig:
    camera_index: int = 0
    camera_width: int = 640
    camera_height: int = 480
    max_hands: int = 1
    detection_confidence: float = 0.75
    tracking_confidence: float = 0.75
    smoothing_factor: float = 0.25

    hsv_lower: np.ndarray = field(
        default_factory=lambda: np.array([0, 20, 70], dtype=np.uint8)
    )
    hsv_upper: np.ndarray = field(
        default_factory=lambda: np.array([20, 255, 255], dtype=np.uint8)
    )


# ==========================================================
# Audio Configuration
# ==========================================================

@dataclass(slots=True)
class AudioConfig:
    master_volume: float = 0.8
    music_volume: float = 0.5
    effects_volume: float = 1.0
    enabled: bool = True
    music_enabled: bool = True
    effects_enabled: bool = True


# ==========================================================
# Particle Configuration
# ==========================================================

@dataclass(slots=True)
class ParticleConfig:
    max_particles: int = 500
    lifetime: float = 1.2
    gravity: float = 300.0

# ==========================================================
# Level Configuration (with bomb_penalty)
# ==========================================================

@dataclass(slots=True)
class LevelConfig:
    name: str
    ball_initial_speed: float
    ball_max_speed: float
    speed_increment: float
    coin_count: int
    bomb_count: int
    bomb_penalty: int  
    paddle_width: int
    paddle_height: int

LEVELS = {
    "easy": LevelConfig(
        name="Easy",
        ball_initial_speed=300.0,
        ball_max_speed=700.0,
        speed_increment=15.0,
        coin_count=6,
        bomb_count=2,
        bomb_penalty=1,    
        paddle_width=180,
        paddle_height=18,
    ),
    "medium": LevelConfig(
        name="Medium",
        ball_initial_speed=420.0,
        ball_max_speed=1100.0,
        speed_increment=25.0,
        coin_count=5,
        bomb_count=3,
        bomb_penalty=1,        
        paddle_width=150,
        paddle_height=18,
    ),
    "hard": LevelConfig(
        name="Hard",
        ball_initial_speed=550.0,
        ball_max_speed=1400.0,
        speed_increment=35.0,
        coin_count=4,
        bomb_count=5,
        bomb_penalty=2,     
        paddle_width=120,
        paddle_height=18,
    ),
}


# ==========================================================
# UI Configuration
# ==========================================================

@dataclass(slots=True)
class UIConfig:
    font_name: str = "Segoe UI"
    title_font_size: int = 52
    font_size: int = 32
    small_font_size: int = 22
    hud_padding: int = 20
    border_radius: int = 10


# ==========================================================
# Debug Configuration
# ==========================================================

@dataclass(slots=True)
class DebugConfig:
    enabled: bool = False
    show_fps: bool = True
    show_hitboxes: bool = False
    show_hand_landmarks: bool = True
    show_velocity: bool = False
    show_collisions: bool = False


# ==========================================================
# Main Configuration Object
# ==========================================================

@dataclass(slots=True)
class GameConfig:
    paths: PathConfig = field(default_factory=PathConfig)
    display: DisplayConfig = field(default_factory=DisplayConfig)
    colors: ColorConfig = field(default_factory=ColorConfig)
    player: PlayerConfig = field(default_factory=PlayerConfig)
    ball: BallConfig = field(default_factory=BallConfig)
    coin: CoinConfig = field(default_factory=CoinConfig)
    bomb: BombConfig = field(default_factory=BombConfig)
    physics: PhysicsConfig = field(default_factory=PhysicsConfig)
    hand: HandConfig = field(default_factory=HandConfig)
    audio: AudioConfig = field(default_factory=AudioConfig)
    particles: ParticleConfig = field(default_factory=ParticleConfig)
    ui: UIConfig = field(default_factory=UIConfig)
    debug: DebugConfig = field(default_factory=DebugConfig)
    
    ball_shape: str = "circle"  