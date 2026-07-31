"""
Game objects module.

Contains the core game entities:
- Paddle
- Ball
- Coin
- Bomb
"""

from __future__ import annotations

from dataclasses import dataclass, field
import random

import pygame

from config import GameConfig


# ==========================================================
# Paddle
# ==========================================================

@dataclass
class Paddle:
    config: GameConfig
    rect: pygame.Rect = field(default=None, init=False)
    
    def __post_init__(self) -> None:
        self.rect = pygame.Rect(
            self.config.display.width // 2 - self.config.player.paddle_width // 2,
            self.config.display.height - self.config.player.bottom_margin,
            self.config.player.paddle_width,
            self.config.player.paddle_height,
        )

    @property
    def center(self) -> int:
        return self.rect.centerx

    def move_to(self, x: int) -> None:
        self.rect.centerx = x
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > self.config.display.width:
            self.rect.right = self.config.display.width

    def draw(self, screen: pygame.Surface) -> None:
        pygame.draw.rect(
            screen,
            self.config.player.paddle_color,
            self.rect,
            border_radius=self.config.player.paddle_radius,
        )


# ==========================================================
# Ball
# ==========================================================

@dataclass
class Ball:
    config: GameConfig
    rect: pygame.Rect = field(default=None, init=False)
    velocity: pygame.Vector2 = field(default=None, init=False)
    
    def __post_init__(self) -> None:
        self.rect = pygame.Rect(
            0,
            0,
            self.config.ball.size,
            self.config.ball.size,
        )
        self.velocity = pygame.Vector2()
        self.velocity.y = -self.config.ball.initial_speed

    def reset(self) -> None:
        self.rect.center = (
            self.config.display.width // 2,
            self.config.display.height // 2,
        )
        direction = random.choice([-1, 1])
        self.velocity.x = direction * self.config.ball.initial_speed
        self.velocity.y = -self.config.ball.initial_speed

    def update(self, dt: float) -> None:
        self.rect.x += int(self.velocity.x * dt)
        self.rect.y += int(self.velocity.y * dt)

    def bounce_x(self) -> None:
        self.velocity.x *= -1

    def bounce_paddle(self) -> None:
        self.velocity.y = -abs(self.velocity.y)

    def bounce_ceiling(self) -> None:
        self.velocity.y = abs(self.velocity.y)

    def accelerate(self) -> None:
        speed = self.velocity.length()
        if speed >= self.config.ball.maximum_speed:
            return
        if speed <= 0:
            return
        speed += self.config.ball.speed_increment
        self.velocity.scale_to_length(speed)

    @property
    def position(self) -> pygame.Vector2:
        return pygame.Vector2(self.rect.center)

    def draw(self, screen: pygame.Surface) -> None:
        shape = getattr(self.config, 'ball_shape', 'circle')
        if shape == 'square':
            pygame.draw.rect(screen, self.config.ball.ball_color, self.rect)
        elif shape == 'triangle':
            points = [
                (self.rect.centerx, self.rect.top),
                (self.rect.left, self.rect.bottom),
                (self.rect.right, self.rect.bottom),
            ]
            pygame.draw.polygon(screen, self.config.ball.ball_color, points)
        else: 
            pygame.draw.ellipse(screen, self.config.ball.ball_color, self.rect)


# ==========================================================
# Coin
# ==========================================================

@dataclass
class Coin:
    config: GameConfig
    rect: pygame.Rect = field(default=None, init=False)
    
    def __post_init__(self) -> None:
        self.rect = pygame.Rect(
            0,
            0,
            self.config.coin.size,
            self.config.coin.size,
        )
        self.respawn()

    def respawn(self) -> None:
        padding = self.config.coin.spawn_padding
        top_margin = 80
        bottom_margin = 180
        
        self.rect.x = random.randint(
            padding,
            self.config.display.width - self.config.coin.size - padding,
        )
        self.rect.y = random.randint(
            top_margin,
            self.config.display.height - bottom_margin - self.config.coin.size,
        )

    def draw(self, screen: pygame.Surface) -> None:
        pygame.draw.ellipse(
            screen,
            self.config.coin.coin_color,
            self.rect,
        )


# ==========================================================
# Bomb 
# ==========================================================

@dataclass
class Bomb:
    config: GameConfig
    rect: pygame.Rect = field(default=None, init=False)
    
    def __post_init__(self) -> None:
        self.rect = pygame.Rect(
            0,
            0,
            self.config.bomb.size,
            self.config.bomb.size,
        )
        self.respawn()

    def respawn(self) -> None:
        padding = self.config.bomb.spawn_padding
        top_margin = 80
        bottom_margin = 180
        
        self.rect.x = random.randint(
            padding,
            self.config.display.width - self.config.bomb.size - padding,
        )
        self.rect.y = random.randint(
            top_margin,
            self.config.display.height - bottom_margin - self.config.bomb.size,
        )

    def draw(self, screen: pygame.Surface) -> None:
        pygame.draw.ellipse(
            screen,
            self.config.colors.bomb_color,
            self.rect,
        )
        pygame.draw.line(
            screen,
            (180, 180, 180),
            (self.rect.centerx, self.rect.top),
            (self.rect.centerx + 8, self.rect.top - 10),
            2,
        )
        pygame.draw.circle(
            screen,
            (255, 200, 50),
            (self.rect.centerx + 8, self.rect.top - 12),
            4,
        )