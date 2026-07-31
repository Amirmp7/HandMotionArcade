"""
Main game module - with mouse interaction and proper game over handling.
"""

from __future__ import annotations

import sys
import traceback

import pygame

from audio import AudioManager
from config import GameConfig, LEVELS, BACKGROUND_THEMES
from detector import HandDetector
from effects import ParticleSystem
from objects import Ball, Coin, Paddle, Bomb
from physics import PhysicsEngine
from renderer import Renderer
from state import GameState, StateManager
from highscore import HighScoreManager
from settings import SettingsManager


class Game:
    def __init__(self, config: GameConfig) -> None:
        self.config = config

        pygame.init()
        self.screen = pygame.display.set_mode(
            (config.display.width, config.display.height),
            pygame.DOUBLEBUF,
        )
        pygame.display.set_caption(config.display.title)
        self.clock = pygame.time.Clock()

        self.renderer = Renderer(self.screen, config)
        self.physics = PhysicsEngine(config)
        self.detector = HandDetector(config)
        self.audio = AudioManager(config)
        self.particles = ParticleSystem(config)

        self.highscore_manager = HighScoreManager(config.paths.highscore_file)
        self.settings_manager = SettingsManager(config.paths.settings_file)

        self.apply_settings()

        self.player_name = self.settings_manager.settings.last_player_name
        self.current_level = self.settings_manager.settings.default_level
        self.score = 0
        self.running = True
        self.hand_detected = False

        self.paddle = None
        self.ball = None
        self.coins = []
        self.bombs = []
        self.create_objects_for_level(self.current_level)

        self.state_manager = StateManager()
        self.state_manager.change(GameState.NAME_ENTRY)

        self.menu_buttons = {}
        self.options_buttons = {}
        self.level_buttons = {}
        self.game_over_buttons = {}

    # ============================================================
    #  Object creation
    # ============================================================

    def create_objects_for_level(self, level_name: str) -> None:
        level = LEVELS.get(level_name)
        if not level:
            level = LEVELS["medium"]
            level_name = "medium"

        self.current_level = level_name
        self.config.ball.initial_speed = level.ball_initial_speed
        self.config.ball.maximum_speed = level.ball_max_speed
        self.config.ball.speed_increment = level.speed_increment
        self.config.coin.count = level.coin_count
        self.config.bomb.count = level.bomb_count
        self.config.bomb.penalty = level.bomb_penalty
        self.config.player.paddle_width = level.paddle_width
        self.config.player.paddle_height = level.paddle_height

        self.paddle = Paddle(self.config)
        self.ball = Ball(self.config)
        self.coins = [Coin(self.config) for _ in range(self.config.coin.count)]
        self.bombs = [Bomb(self.config) for _ in range(self.config.bomb.count)]

    # ============================================================
    #  Apply settings
    # ============================================================

    def apply_settings(self) -> None:
        settings = self.settings_manager.settings
        self.config.ball.ball_color = settings.ball_color
        self.config.player.paddle_color = settings.paddle_color
        setattr(self.config, 'ball_shape', settings.ball_shape)
        self.audio.enabled = settings.sound_enabled
        top, bottom = self.settings_manager.get_background_colors()
        self.config.colors.background_top = top
        self.config.colors.background_bottom = bottom
        self.renderer.update_background()

    def apply_level(self, level_name: str) -> None:
        self.create_objects_for_level(level_name)

    # ============================================================
    #  Core loop
    # ============================================================

    def run(self) -> None:
        try:
            while self.running:
                dt = self.clock.tick(self.config.display.target_fps) / 1000.0
                self._handle_events()
                self._update(dt)
                self._render()
        except Exception:
            traceback.print_exc()
            raise
        finally:
            self._cleanup()

    # ============================================================
    #  Event handling (with mouse support)
    # ============================================================

    def _handle_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                return

            # --- Mouse clicks ---
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = event.pos

                if self.state_manager.is_menu():
                    for key, rect in self.menu_buttons.items():
                        if rect.collidepoint(pos):
                            if key == 'start':
                                self.state_manager.change(GameState.LEVEL_SELECT)
                            elif key == 'options':
                                self.state_manager.change(GameState.SETTINGS)
                            elif key == 'quit':
                                self.running = False

                elif self.state_manager.is_state(GameState.LEVEL_SELECT):
                    for key, rect in self.level_buttons.items():
                        if rect.collidepoint(pos):
                            if key == 'back':
                                self.state_manager.change(GameState.MENU)
                            elif key in ['easy', 'medium', 'hard']:
                                self.apply_level(key)
                                self._reset_round()
                                self.state_manager.change(GameState.PLAYING)

                elif self.state_manager.is_state(GameState.SETTINGS):
                    for key, rect in self.options_buttons.items():
                        if rect.collidepoint(pos):
                            if key == 'back':
                                self.state_manager.change(GameState.MENU)
                            elif key == 'ball_color_prev':
                                self._cycle_ball_color(backward=True)
                            elif key == 'ball_color_next':
                                self._cycle_ball_color(backward=False)
                            elif key == 'paddle_color_prev':
                                self._cycle_paddle_color(backward=True)
                            elif key == 'paddle_color_next':
                                self._cycle_paddle_color(backward=False)
                            elif key == 'shape_prev':
                                self._cycle_ball_shape(backward=True)
                            elif key == 'shape_next':
                                self._cycle_ball_shape(backward=False)
                            elif key in ('sound_prev', 'sound_next'):
                                self._toggle_sound()
                            elif key == 'bg_prev':
                                self._cycle_background(backward=True)
                            elif key == 'bg_next':
                                self._cycle_background(backward=False)

                elif self.state_manager.is_game_over():
                    for key, rect in self.game_over_buttons.items():
                        if rect.collidepoint(pos):
                            if key == 'menu':
                                self._reset_game()
                                self.state_manager.change(GameState.MENU)
                                print("🏠 Returning to menu")

            # --- Keyboard ---
            if event.type == pygame.KEYDOWN:
                if self.state_manager.is_state(GameState.NAME_ENTRY):
                    if event.key == pygame.K_RETURN and self.player_name.strip():
                        self.settings_manager.set(last_player_name=self.player_name)
                        self.state_manager.change(GameState.MENU)
                    elif event.key == pygame.K_BACKSPACE:
                        self.player_name = self.player_name[:-1]
                    elif len(self.player_name) < 20:
                        self.player_name += event.unicode

                elif self.state_manager.is_playing():
                    if event.key == pygame.K_p:
                        self._toggle_pause()

                elif self.state_manager.is_state(GameState.PAUSED):
                    if event.key == pygame.K_p:
                        self._toggle_pause()

    # ============================================================
    #  Update
    # ============================================================

    def _update(self, dt: float) -> None:
        if not self.state_manager.is_playing():
            return

        # Ensure objects exist
        if self.ball is None or self.paddle is None:
            return

        self.particles.update(dt)
        self._update_hand()

        self.physics.update_ball(self.ball, dt)
        self.physics.handle_wall_collision(self.ball)

        if self.physics.handle_paddle_collision(self.ball, self.paddle):
            self.audio.play_bounce()
            self.particles.add_spark_burst(
                self.ball.rect.centerx,
                self.ball.rect.bottom,
                count=25,
                speed=250.0,
            )

        collected = self.physics.handle_coin_collision(self.ball, self.coins)
        if collected:
            self.score += collected
            self.audio.play_coin()
            self.particles.add_coin_burst(
                self.ball.rect.centerx,
                self.ball.rect.centery,
                count=35,
                speed=180.0,
            )

        bomb_hits = self.physics.handle_bomb_collision(self.ball, self.bombs)
        if bomb_hits:
            penalty = bomb_hits * self.config.bomb.penalty
            self.score -= penalty
            self.audio.play_bomb()
            self.particles.add_bomb_explosion(
                self.ball.rect.centerx,
                self.ball.rect.centery,
                count=40,
                speed=300.0,
            )

        if self.physics.ball_out_of_bounds(self.ball):
            self._game_over()

    # ============================================================
    #  Render
    # ============================================================

    def _render(self) -> None:
        current = self.state_manager.current

        if current == GameState.NAME_ENTRY:
            self.renderer.draw_name_entry(self.player_name)
        elif current == GameState.MENU:
            self.menu_buttons = self.renderer.draw_main_menu(self.highscore_manager)
            # Show camera error if camera is not opened
            if not self.detector.is_opened():
                error_msg = self.detector.get_error_message()
                if error_msg:
                    self.renderer.draw_camera_error(error_msg)
        elif current == GameState.LEVEL_SELECT:
            self.level_buttons = self.renderer.draw_level_select()
        elif current == GameState.SETTINGS:
            self.options_buttons = self.renderer.draw_options_menu(
                self.settings_manager.settings
            )
        elif current in (GameState.PLAYING, GameState.PAUSED):
            self.renderer.render(
                ball=self.ball,
                paddle=self.paddle,
                coins=self.coins,
                bombs=self.bombs,
                score=self.score,
                fps=self.clock.get_fps(),
                hand_detected=self.hand_detected,
                highscore_manager=self.highscore_manager,
            )
            self.particles.draw(self.screen)
            if current == GameState.PAUSED:
                self.renderer.draw_pause_overlay()
        elif current == GameState.GAME_OVER:
            self.renderer.draw_background()
            self.particles.draw(self.screen)
            self.game_over_buttons = self.renderer.draw_game_over(self.score)

        pygame.display.flip()

    # ============================================================
    #  Private helpers
    # ============================================================

    def _update_hand(self) -> None:
        if not self.detector.is_opened():
            return

        frame = self.detector.read_frame()
        if frame is None:
            self.hand_detected = False
            return

        hand_x = self.detector.get_hand_position(frame)
        if hand_x is not None:
            self.hand_detected = True
            screen_x = int(hand_x * self.config.display.width)
            self.paddle.move_to(screen_x)

            self.particles.add_trail_particle(
                self.ball.rect.centerx,
                self.ball.rect.centery,
                self.config.ball.ball_color,
                size=self.config.ball.size * 0.3,
                lifetime=0.3,
            )
        else:
            self.hand_detected = False

    def _toggle_pause(self) -> None:
        if self.state_manager.is_playing():
            self.state_manager.change(GameState.PAUSED)
        elif self.state_manager.is_state(GameState.PAUSED):
            self.state_manager.change(GameState.PLAYING)

    def _game_over(self) -> None:
        self.state_manager.change(GameState.GAME_OVER)
        self.audio.play_game_over()

        if self.score > 0:
            self.highscore_manager.add_score(
                self.player_name,
                self.score,
                self.current_level.capitalize()
            )

    def _reset_round(self) -> None:
        if self.ball is not None:
            self.ball.reset()
        for coin in self.coins:
            coin.respawn()
        for bomb in self.bombs:
            bomb.respawn()

    def _reset_game(self) -> None:
        self.score = 0
        self._reset_round()

    def _cleanup(self) -> None:
        self.detector.release()
        self.audio.stop_all()
        pygame.quit()

    # ============================================================
    #  Settings manipulation
    # ============================================================

    def _cycle_ball_color(self, backward=False) -> None:
        colors = [
            (255, 80, 80), (80, 200, 255), (80, 255, 80),
            (255, 200, 80), (200, 80, 255), (255, 255, 255)
        ]
        current = self.settings_manager.settings.ball_color
        try:
            idx = colors.index(current)
        except ValueError:
            idx = 0
        if backward:
            idx = (idx - 1) % len(colors)
        else:
            idx = (idx + 1) % len(colors)
        new_color = colors[idx]
        self.settings_manager.set(ball_color=new_color)
        self.apply_settings()

    def _cycle_paddle_color(self, backward=False) -> None:
        colors = [(240, 240, 240), (100, 200, 255), (255, 200, 80), (255, 100, 100), (200, 255, 100)]
        current = self.settings_manager.settings.paddle_color
        try:
            idx = colors.index(current)
        except ValueError:
            idx = 0
        if backward:
            idx = (idx - 1) % len(colors)
        else:
            idx = (idx + 1) % len(colors)
        new_color = colors[idx]
        self.settings_manager.set(paddle_color=new_color)
        self.apply_settings()

    def _cycle_ball_shape(self, backward=False) -> None:
        shapes = ["circle", "square", "triangle"]
        current = self.settings_manager.settings.ball_shape
        idx = shapes.index(current) if current in shapes else 0
        if backward:
            idx = (idx - 1) % len(shapes)
        else:
            idx = (idx + 1) % len(shapes)
        new_shape = shapes[idx]
        self.settings_manager.set(ball_shape=new_shape)
        self.apply_settings()

    def _toggle_sound(self) -> None:
        new_state = not self.settings_manager.settings.sound_enabled
        self.settings_manager.set(sound_enabled=new_state)
        self.apply_settings()

    def _cycle_background(self, backward=False) -> None:
        themes = list(BACKGROUND_THEMES.keys())
        current = self.settings_manager.settings.background_theme
        idx = themes.index(current) if current in themes else 0
        if backward:
            idx = (idx - 1) % len(themes)
        else:
            idx = (idx + 1) % len(themes)
        new_theme = themes[idx]
        self.settings_manager.set(background_theme=new_theme)
        self.apply_settings()

    # ============================================================
    #  Factory
    # ============================================================

    @classmethod
    def create(cls, config: GameConfig | None = None) -> Game:
        if config is None:
            config = GameConfig()
        return cls(config)


if __name__ == "__main__":
    game = Game.create()
    game.run()