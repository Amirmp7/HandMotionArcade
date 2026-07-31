"""
Physics engine for the Hand-Controlled Ball Game.

Responsible for:
- Ball movement
- Wall collisions
- Paddle collision
- Coin collision
- Bomb collision (جدید)
- Ball acceleration
"""

from __future__ import annotations

from typing import Sequence

from config import GameConfig
from objects import Ball, Coin, Paddle, Bomb


class PhysicsEngine:
    def __init__(self, config: GameConfig):
        self.config = config

    # ======================================================

    def update_ball(self, ball: Ball, dt: float) -> None:
        ball.update(dt)

    # ======================================================

    def handle_wall_collision(self, ball: Ball) -> None:
        if ball.rect.left <= 0:
            ball.rect.left = 0
            ball.bounce_x()
        elif ball.rect.right >= self.config.display.width:
            ball.rect.right = self.config.display.width
            ball.bounce_x()

        if ball.rect.top <= 0:
            ball.rect.top = 0
            ball.bounce_ceiling()

    # ======================================================

    def handle_paddle_collision(self, ball: Ball, paddle: Paddle) -> bool:
        if not ball.rect.colliderect(paddle.rect):
            return False

        ball.rect.bottom = paddle.rect.top
        ball.bounce_paddle()

        hit_ratio = (ball.rect.centerx - paddle.rect.centerx) / (paddle.rect.width / 2)
        hit_ratio = max(-1.0, min(1.0, hit_ratio))
        ball.velocity.x += hit_ratio * self.config.physics.paddle_hit_angle

        max_x = self.config.ball.maximum_speed * 0.75
        ball.velocity.x = max(-max_x, min(ball.velocity.x, max_x))

        ball.accelerate()
        return True

    # ======================================================

    def handle_coin_collision(self, ball: Ball, coins: Sequence[Coin]) -> int:
        collected = 0
        for coin in coins:
            if not ball.rect.colliderect(coin.rect):
                continue
            coin.respawn()
            collected += 1
        return collected

    # ======================================================

    def handle_bomb_collision(self, ball: Ball, bombs: Sequence[Bomb]) -> int:
        """
        Check collision with bombs.
        Returns the number of bombs hit (each gives -penalty score).
        """
        hit_count = 0
        for bomb in bombs:
            if not ball.rect.colliderect(bomb.rect):
                continue
            bomb.respawn()
            hit_count += 1
        return hit_count

    # ======================================================

    def ball_out_of_bounds(self, ball: Ball) -> bool:
        return ball.rect.bottom >= self.config.display.height

    # ======================================================

    def clamp_ball_speed(self, ball: Ball) -> None:
        speed = ball.velocity.length()
        if speed > self.config.ball.maximum_speed:
            ball.velocity.scale_to_length(self.config.ball.maximum_speed)