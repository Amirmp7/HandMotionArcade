"""
Special effects system.

Contains particle system for:
- Spark effects (paddle hit)
- Coin collection burst
- Ball trail
- Bomb explosion
"""

from __future__ import annotations

import random
import math
from dataclasses import dataclass, field
from typing import List, Optional

import pygame

from config import GameConfig


@dataclass
class Particle:
    x: float
    y: float
    vx: float
    vy: float
    size: float
    color: tuple[int, int, int]
    lifetime: float
    max_lifetime: float
    gravity: float = 0.0
    friction: float = 0.98
    shrink_speed: float = 0.0
    
    def update(self, dt: float) -> None:
        self.x += self.vx * dt
        self.y += self.vy * dt
        self.vx *= self.friction
        self.vy *= self.friction
        self.vy += self.gravity * dt
        self.lifetime -= dt
        if self.shrink_speed > 0:
            self.size -= self.shrink_speed * dt
            if self.size < 0.5:
                self.size = 0.5
    
    @property
    def is_alive(self) -> bool:
        return self.lifetime > 0 and self.size > 0.5
    
    @property
    def alpha(self) -> int:
        if self.max_lifetime <= 0:
            return 255
        ratio = max(0.0, self.lifetime / self.max_lifetime)
        return int(255 * ratio)
    
    def draw(self, screen: pygame.Surface, offset_x: int = 0, offset_y: int = 0) -> None:
        if not self.is_alive:
            return
        
        pos_x = int(self.x + offset_x)
        pos_y = int(self.y + offset_y)
        size = int(max(1, self.size))
        
        if self.alpha < 255:
            surf = pygame.Surface((size * 2, size * 2), pygame.SRCALPHA)
            color_with_alpha = (*self.color, self.alpha)
            pygame.draw.circle(surf, color_with_alpha, (size, size), size)
            screen.blit(surf, (pos_x - size, pos_y - size))
        else:
            pygame.draw.circle(screen, self.color, (pos_x, pos_y), size)


@dataclass
class ParticleSystem:
    config: GameConfig
    particles: List[Particle] = field(default_factory=list)
    max_particles: int = 500
    
    def __post_init__(self) -> None:
        self.max_particles = self.config.particles.max_particles
    
    def update(self, dt: float) -> None:
        for particle in self.particles[:]:
            particle.update(dt)
            if not particle.is_alive:
                self.particles.remove(particle)
    
    def draw(self, screen: pygame.Surface, offset_x: int = 0, offset_y: int = 0) -> None:
        for particle in self.particles:
            particle.draw(screen, offset_x, offset_y)
    
    def add_particle(self, particle: Particle) -> None:
        if len(self.particles) >= self.max_particles:
            self.particles.pop(0)
        self.particles.append(particle)
    
    # ==========================================================
    # Spark (paddle hit)
    # ==========================================================
    
    def add_spark_burst(
        self,
        x: float,
        y: float,
        count: int = 20,
        speed: float = 200.0,
        colors: Optional[List[tuple[int, int, int]]] = None,
        lifetime: float = 0.6,
    ) -> None:
        if colors is None:
            colors = [
                (255, 200, 200),
                (200, 220, 255),
                (255, 255, 255),
                (180, 200, 255),
            ]
        
        for _ in range(count):
            angle = random.uniform(0, 2 * math.pi)
            speed_abs = random.uniform(speed * 0.3, speed * 1.2)
            vx = math.cos(angle) * speed_abs
            vy = math.sin(angle) * speed_abs * random.uniform(0.5, 1.0)
            
            size = random.uniform(2.0, 5.0)
            color = random.choice(colors)
            life = random.uniform(lifetime * 0.5, lifetime * 1.2)
            
            particle = Particle(
                x=x, y=y,
                vx=vx, vy=vy,
                size=size,
                color=color,
                lifetime=life,
                max_lifetime=life,
                gravity=50.0,
                friction=0.96,
                shrink_speed=1.5,
            )
            self.add_particle(particle)
    
    # ==========================================================
    # Coin burst
    # ==========================================================
    
    def add_coin_burst(
        self,
        x: float,
        y: float,
        count: int = 30,
        speed: float = 150.0,
        lifetime: float = 1.0,
    ) -> None:
        colors = [
            (255, 215, 0),
            (255, 200, 50),
            (255, 180, 0),
            (255, 255, 150),
            (255, 230, 100),
        ]
        
        for _ in range(count):
            angle = random.uniform(0, 2 * math.pi)
            speed_abs = random.uniform(speed * 0.2, speed * 1.5)
            vx = math.cos(angle) * speed_abs
            vy = math.sin(angle) * speed_abs
            
            size = random.uniform(2.0, 6.0)
            color = random.choice(colors)
            life = random.uniform(lifetime * 0.6, lifetime * 1.4)
            
            particle = Particle(
                x=x, y=y,
                vx=vx, vy=vy,
                size=size,
                color=color,
                lifetime=life,
                max_lifetime=life,
                gravity=80.0,
                friction=0.97,
                shrink_speed=1.0,
            )
            self.add_particle(particle)
    
    # ==========================================================
    # Ball trail
    # ==========================================================
    
    def add_trail_particle(
        self,
        x: float,
        y: float,
        color: tuple[int, int, int],
        size: float = 8.0,
        lifetime: float = 0.3,
    ) -> None:
        vx = random.uniform(-10, 10)
        vy = random.uniform(-10, 10)
        
        particle = Particle(
            x=x, y=y,
            vx=vx, vy=vy,
            size=size * random.uniform(0.3, 0.8),
            color=color,
            lifetime=lifetime,
            max_lifetime=lifetime,
            gravity=0.0,
            friction=0.99,
            shrink_speed=5.0,
        )
        self.add_particle(particle)
    
    # ==========================================================
    # Bomb explosion (جدید)
    # ==========================================================
    
    def add_bomb_explosion(
        self,
        x: float,
        y: float,
        count: int = 40,
        speed: float = 300.0,
        lifetime: float = 0.8,
    ) -> None:
        colors = [
            (255, 50, 0),
            (255, 100, 0),
            (255, 150, 0),
            (255, 200, 50),
            (200, 50, 0),
            (255, 80, 80),
        ]
        
        for _ in range(count):
            angle = random.uniform(0, 2 * math.pi)
            speed_abs = random.uniform(speed * 0.2, speed * 1.6)
            vx = math.cos(angle) * speed_abs
            vy = math.sin(angle) * speed_abs
            
            size = random.uniform(3.0, 8.0)
            color = random.choice(colors)
            life = random.uniform(lifetime * 0.5, lifetime * 1.3)
            
            particle = Particle(
                x=x, y=y,
                vx=vx, vy=vy,
                size=size,
                color=color,
                lifetime=life,
                max_lifetime=life,
                gravity=120.0,
                friction=0.95,
                shrink_speed=2.0,
            )
            self.add_particle(particle)