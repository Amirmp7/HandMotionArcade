"""
Rendering module - clean and stable version without extra icons.
"""

from __future__ import annotations

import pygame

from config import GameConfig
from objects import Ball, Coin, Paddle, Bomb
from highscore import HighScoreManager

# Color names for display in Options
COLOR_NAMES = {
    (255, 80, 80): "Red",
    (80, 200, 255): "Blue",
    (80, 255, 80): "Green",
    (255, 200, 80): "Orange",
    (200, 80, 255): "Purple",
    (255, 255, 255): "White",
    (240, 240, 240): "White",
    (100, 200, 255): "Light Blue",
    (255, 200, 80): "Gold",
    (255, 100, 100): "Light Red",
    (200, 255, 100): "Light Green",
}


class Renderer:
    def __init__(self, screen: pygame.Surface, config: GameConfig) -> None:
        self.screen = screen
        self.config = config

        pygame.font.init()
        self.font = pygame.font.SysFont(
            config.ui.font_name,
            config.ui.font_size,
            bold=True,
        )
        self.small_font = pygame.font.SysFont(
            config.ui.font_name,
            config.ui.small_font_size,
        )

        self._line_spacing = 32
        self._background_surface = None
        self._rebuild_background()

    # ============================================================
    #  Background
    # ============================================================

    def _rebuild_background(self) -> None:
        top = self.config.colors.background_top
        bottom = self.config.colors.background_bottom
        width = self.config.display.width
        height = self.config.display.height
        surface = pygame.Surface((width, height))
        for y in range(height):
            t = y / height
            color = (
                int(top[0] * (1 - t) + bottom[0] * t),
                int(top[1] * (1 - t) + bottom[1] * t),
                int(top[2] * (1 - t) + bottom[2] * t),
            )
            pygame.draw.line(surface, color, (0, y), (width, y))
        self._background_surface = surface

    def update_background(self) -> None:
        self._rebuild_background()

    def draw_background(self) -> None:
        if self._background_surface is None:
            self._rebuild_background()
        self.screen.blit(self._background_surface, (0, 0))

    # ============================================================
    #  Text helper
    # ============================================================

    def _draw_text(
        self,
        text: str,
        font: pygame.font.Font,
        color: tuple[int, int, int],
        position: tuple[int, int],
        center: bool = False,
    ) -> None:
        surface = font.render(text, True, color)
        if center:
            rect = surface.get_rect(center=position)
            self.screen.blit(surface, rect)
        else:
            self.screen.blit(surface, position)

    # ============================================================
    #  Drawing game objects
    # ============================================================

    def draw_ball(self, ball: Ball) -> None:
        shadow = ball.rect.move(4, 4)
        pygame.draw.ellipse(self.screen, self.config.colors.shadow, shadow)
        ball.draw(self.screen)

    def draw_paddle(self, paddle: Paddle) -> None:
        shadow = paddle.rect.move(3, 3)
        pygame.draw.rect(
            self.screen,
            self.config.colors.shadow,
            shadow,
            border_radius=self.config.player.paddle_radius,
        )
        pygame.draw.rect(
            self.screen,
            self.config.player.paddle_color,
            paddle.rect,
            border_radius=self.config.player.paddle_radius,
        )

    def draw_coins(self, coins: list[Coin]) -> None:
        for coin in coins:
            shadow = coin.rect.move(2, 2)
            pygame.draw.ellipse(self.screen, self.config.colors.coin_shadow, shadow)
            pygame.draw.ellipse(self.screen, self.config.coin.coin_color, coin.rect)

    def draw_bombs(self, bombs: list[Bomb]) -> None:
        for bomb in bombs:
            shadow = bomb.rect.move(2, 2)
            pygame.draw.ellipse(self.screen, self.config.colors.bomb_shadow, shadow)
            bomb.draw(self.screen)

    def draw_hud(self, score: int, fps: float, hand_detected: bool) -> None:
        margin = self.config.ui.hud_padding
        y = margin
        self._draw_text(
            f"Score : {score}",
            self.font,
            self.config.colors.hud_text,
            (margin, y),
        )
        y += self._line_spacing
        if self.config.debug.show_fps:
            self._draw_text(
                f"FPS : {fps:.0f}",
                self.small_font,
                self.config.colors.secondary_text,
                (margin, y),
            )
            y += self._line_spacing
        status = "HAND DETECTED" if hand_detected else "NO HAND"
        color = self.config.colors.success if hand_detected else self.config.colors.error
        self._draw_text(status, self.small_font, color, (margin, y))

    # ============================================================
    #  High score board
    # ============================================================

    def _draw_highscore(self, highscore_manager: HighScoreManager, x_start: int = None, y_start: int = None) -> None:
        entries = highscore_manager.get_entries()
        if not entries:
            return
        if x_start is None:
            x_start = self.config.display.width // 2 - 150
        if y_start is None:
            y_start = 10

        panel_width = 300
        panel_height = 30 + len(entries) * 24
        panel = pygame.Surface((panel_width, panel_height), pygame.SRCALPHA)
        panel.fill((0, 0, 0, 160))
        self.screen.blit(panel, (x_start - 10, y_start - 5))

        self._draw_text(
            "High Scores",
            self.small_font,
            self.config.colors.gold,
            (x_start, y_start),
        )
        y = y_start + 28
        for entry in entries:
            self._draw_text(
                f"{entry.name[:10]}: {entry.score}  ({entry.level})",
                self.small_font,
                self.config.colors.hud_text,
                (x_start, y),
            )
            y += 22

    # ============================================================
    #  Camera error message
    # ============================================================

    def draw_camera_error(self, error_message: str) -> None:
        """Draw a camera error message on the screen."""
        width, height = self.config.display.width, self.config.display.height

        # Semi-transparent panel
        panel = pygame.Surface((width - 200, 200), pygame.SRCALPHA)
        panel.fill((0, 0, 0, 200))
        panel_rect = panel.get_rect(center=(width // 2, height // 2))
        self.screen.blit(panel, panel_rect)
        pygame.draw.rect(self.screen, (255, 80, 80), panel_rect, 3, border_radius=10)

        # Error title
        self._draw_text(
            "Camera Access Error",
            self.font,
            (255, 80, 80),
            (width // 2, height // 2 - 60),
            center=True,
        )

        # Error message lines
        lines = error_message.split('\n')
        y = height // 2 - 10
        for line in lines:
            self._draw_text(
                line.strip(),
                self.small_font,
                self.config.colors.hud_text,
                (width // 2, y),
                center=True,
            )
            y += 30

        # Additional guidance
        self._draw_text(
            "After enabling access, restart the game.",
            self.small_font,
            self.config.colors.secondary_text,
            (width // 2, height // 2 + 80),
            center=True,
        )

    # ============================================================
    #  Main Menu
    # ============================================================

    def draw_main_menu(self, highscore_manager: HighScoreManager) -> dict:
        self.draw_background()
        width, height = self.config.display.width, self.config.display.height

        self._draw_text(
            "Hand Motion Arcade",
            self.font,
            self.config.colors.hud_text,
            (width // 2, 150),
            center=True,
        )

        button_width = 220
        button_height = 55
        start_y = 280
        spacing = 70

        start_rect = pygame.Rect(width // 2 - button_width // 2, start_y, button_width, button_height)
        options_rect = pygame.Rect(width // 2 - button_width // 2, start_y + spacing, button_width, button_height)
        quit_rect = pygame.Rect(width // 2 - button_width // 2, start_y + 2 * spacing, button_width, button_height)

        for rect, label, color in [
            (start_rect, "Start Game", self.config.colors.success),
            (options_rect, "Options", self.config.colors.hud_text),
            (quit_rect, "Quit", self.config.colors.error),
        ]:
            pygame.draw.rect(self.screen, (40, 40, 60), rect, border_radius=8)
            pygame.draw.rect(self.screen, color, rect, 2, border_radius=8)
            self._draw_text(label, self.font, color, (rect.centerx, rect.centery), center=True)

        self._draw_highscore(highscore_manager, x_start=width // 2 - 150, y_start=height - 200)

        self._draw_text(
            "Control the paddle with your hand via webcam",
            self.small_font,
            self.config.colors.secondary_text,
            (width // 2, height - 30),
            center=True,
        )
        return {'start': start_rect, 'options': options_rect, 'quit': quit_rect}

    # ============================================================
    #  Level Select
    # ============================================================

    def draw_level_select(self) -> dict:
        self.draw_background()
        width, height = self.config.display.width, self.config.display.height

        self._draw_text(
            "Select Difficulty",
            self.font,
            self.config.colors.hud_text,
            (width // 2, 150),
            center=True,
        )

        btns = {}
        levels = [('easy', 'Easy', self.config.colors.success),
                  ('medium', 'Medium', self.config.colors.hud_text),
                  ('hard', 'Hard', self.config.colors.error)]
        y_start = 250
        spacing = 80
        btn_width = 220
        btn_height = 55

        for i, (key, label, color) in enumerate(levels):
            y = y_start + i * spacing
            rect = pygame.Rect(width // 2 - btn_width // 2, y, btn_width, btn_height)
            pygame.draw.rect(self.screen, (40, 40, 60), rect, border_radius=8)
            pygame.draw.rect(self.screen, color, rect, 2, border_radius=8)
            self._draw_text(label, self.font, color, (rect.centerx, rect.centery), center=True)
            btns[key] = rect

        back_rect = pygame.Rect(width // 2 - 80, height - 100, 160, 40)
        pygame.draw.rect(self.screen, (40, 40, 60), back_rect, border_radius=8)
        pygame.draw.rect(self.screen, (200, 200, 200), back_rect, 2, border_radius=8)
        self._draw_text("Back", self.small_font, (200, 200, 200), (back_rect.centerx, back_rect.centery), center=True)
        btns['back'] = back_rect

        return btns

    # ============================================================
    #  Options Menu
    # ============================================================

    def draw_options_menu(self, settings) -> dict:
        self.draw_background()
        width, height = self.config.display.width, self.config.display.height

        panel_width = 650
        panel_height = 480
        panel = pygame.Surface((panel_width, panel_height), pygame.SRCALPHA)
        panel.fill((20, 20, 40, 200))
        panel_rect = panel.get_rect(center=(width // 2, height // 2))
        self.screen.blit(panel, panel_rect)
        pygame.draw.rect(self.screen, (100, 100, 150), panel_rect, 2, border_radius=10)

        self._draw_text(
            "Settings",
            self.font,
            self.config.colors.hud_text,
            (width // 2, panel_rect.top + 40),
            center=True,
        )

        y_start = panel_rect.top + 100
        row_height = 55
        btn_size = 35

        def draw_row(label, current_value, x_center, y, prev_rect, next_rect, color_preview=None, shape_preview=None):
            self._draw_text(label, self.small_font, self.config.colors.hud_text, (x_center - 250, y), center=False)
            pygame.draw.rect(self.screen, (60, 60, 80), prev_rect, border_radius=6)
            pygame.draw.rect(self.screen, (150, 150, 200), prev_rect, 1, border_radius=6)
            self._draw_text("<", self.small_font, (200, 200, 200), (prev_rect.centerx, prev_rect.centery), center=True)

            if color_preview is not None:
                pygame.draw.circle(self.screen, color_preview, (x_center, y), 18)
                pygame.draw.circle(self.screen, (200, 200, 200), (x_center, y), 18, 2)
                color_name = COLOR_NAMES.get(color_preview, str(color_preview))
                self._draw_text(color_name, self.small_font, self.config.colors.hud_text, (x_center + 35, y), center=False)
            elif shape_preview is not None:
                shape_name = shape_preview.capitalize()
                self._draw_text(shape_name, self.small_font, self.config.colors.hud_text, (x_center, y), center=True)
            else:
                self._draw_text(str(current_value), self.small_font, self.config.colors.hud_text, (x_center, y), center=True)

            pygame.draw.rect(self.screen, (60, 60, 80), next_rect, border_radius=6)
            pygame.draw.rect(self.screen, (150, 150, 200), next_rect, 1, border_radius=6)
            self._draw_text(">", self.small_font, (200, 200, 200), (next_rect.centerx, next_rect.centery), center=True)

        btns = {}
        x_center = panel_rect.centerx

        y = y_start
        prev_rect = pygame.Rect(x_center - 160, y - btn_size//2, btn_size, btn_size)
        next_rect = pygame.Rect(x_center + 160 - btn_size, y - btn_size//2, btn_size, btn_size)
        draw_row("Ball Color", settings.ball_color, x_center, y, prev_rect, next_rect, color_preview=settings.ball_color)
        btns['ball_color_prev'] = prev_rect
        btns['ball_color_next'] = next_rect

        y += row_height
        prev_rect = pygame.Rect(x_center - 160, y - btn_size//2, btn_size, btn_size)
        next_rect = pygame.Rect(x_center + 160 - btn_size, y - btn_size//2, btn_size, btn_size)
        draw_row("Paddle Color", settings.paddle_color, x_center, y, prev_rect, next_rect, color_preview=settings.paddle_color)
        btns['paddle_color_prev'] = prev_rect
        btns['paddle_color_next'] = next_rect

        y += row_height
        prev_rect = pygame.Rect(x_center - 160, y - btn_size//2, btn_size, btn_size)
        next_rect = pygame.Rect(x_center + 160 - btn_size, y - btn_size//2, btn_size, btn_size)
        draw_row("Ball Shape", settings.ball_shape, x_center, y, prev_rect, next_rect, shape_preview=settings.ball_shape)
        btns['shape_prev'] = prev_rect
        btns['shape_next'] = next_rect

        y += row_height
        prev_rect = pygame.Rect(x_center - 160, y - btn_size//2, btn_size, btn_size)
        next_rect = pygame.Rect(x_center + 160 - btn_size, y - btn_size//2, btn_size, btn_size)
        sound_status = "ON" if settings.sound_enabled else "OFF"
        draw_row("Sound", sound_status, x_center, y, prev_rect, next_rect)
        btns['sound_prev'] = prev_rect
        btns['sound_next'] = next_rect

        y += row_height
        prev_rect = pygame.Rect(x_center - 160, y - btn_size//2, btn_size, btn_size)
        next_rect = pygame.Rect(x_center + 160 - btn_size, y - btn_size//2, btn_size, btn_size)
        theme_display = settings.background_theme.replace('_', ' ').title()
        draw_row("Background", theme_display, x_center, y, prev_rect, next_rect)
        btns['bg_prev'] = prev_rect
        btns['bg_next'] = next_rect

        back_rect = pygame.Rect(panel_rect.centerx - 70, panel_rect.bottom - 55, 140, 38)
        pygame.draw.rect(self.screen, (60, 60, 80), back_rect, border_radius=8)
        pygame.draw.rect(self.screen, (200, 200, 200), back_rect, 2, border_radius=8)
        self._draw_text("Back", self.small_font, (200, 200, 200), (back_rect.centerx, back_rect.centery), center=True)
        btns['back'] = back_rect

        return btns

    # ============================================================
    #  Game Over screen
    # ============================================================

    def draw_game_over(self, score: int) -> dict:
        width, height = self.config.display.width, self.config.display.height

        overlay = pygame.Surface((width, height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200))
        self.screen.blit(overlay, (0, 0))

        self._draw_text(
            "GAME OVER",
            self.font,
            self.config.colors.error,
            (width // 2, height // 2 - 80),
            center=True,
        )

        self._draw_text(
            f"Score: {score}",
            self.font,
            self.config.colors.hud_text,
            (width // 2, height // 2 - 20),
            center=True,
        )

        btn_width = 180
        btn_height = 50
        menu_rect = pygame.Rect(width // 2 - btn_width // 2, height // 2 + 50, btn_width, btn_height)

        pygame.draw.rect(self.screen, (40, 40, 60), menu_rect, border_radius=8)
        pygame.draw.rect(self.screen, self.config.colors.hud_text, menu_rect, 2, border_radius=8)
        self._draw_text(
            "Menu",
            self.small_font,
            self.config.colors.hud_text,
            (menu_rect.centerx, menu_rect.centery),
            center=True,
        )

        return {'menu': menu_rect}

    # ============================================================
    #  Name entry, pause, and other overlays
    # ============================================================

    def draw_name_entry(self, player_name: str) -> None:
        self.draw_background()
        width, height = self.config.display.width, self.config.display.height

        self._draw_text(
            "Enter Your Name",
            self.font,
            self.config.colors.hud_text,
            (width // 2, height // 2 - 80),
            center=True,
        )
        box_rect = pygame.Rect(width // 2 - 150, height // 2 - 30, 300, 60)
        pygame.draw.rect(self.screen, (50, 50, 70), box_rect, border_radius=8)
        pygame.draw.rect(self.screen, (100, 100, 130), box_rect, 2, border_radius=8)
        display_name = player_name + ("|" if pygame.time.get_ticks() % 1000 < 500 else "")
        self._draw_text(display_name, self.font, self.config.colors.hud_text, (width // 2, height // 2), center=True)
        self._draw_text(
            "Press ENTER to continue",
            self.small_font,
            self.config.colors.secondary_text,
            (width // 2, height // 2 + 80),
            center=True,
        )

    def draw_pause_overlay(self) -> None:
        width, height = self.config.display.width, self.config.display.height
        overlay = pygame.Surface((width, height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 128))
        self.screen.blit(overlay, (0, 0))
        self._draw_text("PAUSED", self.font, self.config.colors.hud_text, (width // 2, height // 2), center=True)
        self._draw_text(
            "Press P to Resume",
            self.small_font,
            self.config.colors.secondary_text,
            (width // 2, height // 2 + 50),
            center=True,
        )

    # ============================================================
    #  Main render method for gameplay
    # ============================================================

    def render(
        self,
        ball: Ball,
        paddle: Paddle,
        coins: list[Coin],
        bombs: list[Bomb],
        score: int,
        fps: float,
        hand_detected: bool,
        highscore_manager: HighScoreManager,
    ) -> None:
        self.draw_background()
        self.draw_coins(coins)
        self.draw_bombs(bombs)
        self.draw_ball(ball)
        self.draw_paddle(paddle)
        self.draw_hud(score, fps, hand_detected)
        self._draw_highscore(highscore_manager, x_start=self.config.display.width - 280, y_start=10)