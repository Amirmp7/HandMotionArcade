"""
Game state management system.

Controls the current state of the game and provides safe state transitions.
"""

from __future__ import annotations

from enum import Enum, auto
from dataclasses import dataclass
from typing import Set


# ==========================================================
# Custom Exception
# ==========================================================

class InvalidStateTransitionError(Exception):
    """Raised when an invalid state transition is attempted."""
    pass


# ==========================================================
# Game States
# ==========================================================

class GameState(Enum):
    """All possible game states."""
    BOOT = auto()
    NAME_ENTRY = auto()    
    MENU = auto()
    LEVEL_SELECT = auto() 
    PLAYING = auto()
    PAUSED = auto()
    GAME_OVER = auto()
    SETTINGS = auto()       
    EXIT = auto()


# ==========================================================
# State Transition Rules (immutable mapping)
# ==========================================================

_ALLOWED_TRANSITIONS: dict[GameState, Set[GameState]] = {
    GameState.BOOT: {GameState.NAME_ENTRY, GameState.EXIT},
    GameState.NAME_ENTRY: {GameState.MENU, GameState.EXIT},
    GameState.MENU: {GameState.LEVEL_SELECT, GameState.SETTINGS, GameState.EXIT},
    GameState.LEVEL_SELECT: {GameState.PLAYING, GameState.MENU, GameState.EXIT},
    GameState.PLAYING: {GameState.PAUSED, GameState.GAME_OVER, GameState.EXIT},
    GameState.PAUSED: {GameState.PLAYING, GameState.MENU, GameState.EXIT},
    GameState.GAME_OVER: {GameState.MENU, GameState.EXIT},
    GameState.SETTINGS: {GameState.MENU, GameState.EXIT},
    GameState.EXIT: set(),
}


# ==========================================================
# State Manager
# ==========================================================

@dataclass(slots=True)
class StateManager:
    """Manages the current game state and validates transitions."""

    current: GameState = GameState.BOOT

    def change(self, new_state: GameState, raise_on_invalid: bool = False) -> bool:
        """
        Attempt to change the game state.

        Args:
            new_state: The desired new state.
            raise_on_invalid: If True, raises InvalidStateTransitionError on failure.

        Returns:
            True if transition succeeded, False otherwise.
        """
        allowed = _ALLOWED_TRANSITIONS.get(self.current, set())
        if new_state not in allowed:
            if raise_on_invalid:
                raise InvalidStateTransitionError(
                    f"Cannot transition from {self.current.name} to {new_state.name}"
                )
            return False

        self.current = new_state
        return True

    def is_state(self, state: GameState) -> bool:
        """Check if the current state matches the given state."""
        return self.current == state

    def is_playing(self) -> bool:
        return self.current == GameState.PLAYING

    def is_game_over(self) -> bool:
        return self.current == GameState.GAME_OVER

    def is_menu(self) -> bool:
        return self.current == GameState.MENU

    def is_state(self, state: GameState) -> bool:
        return self.current == state

    def is_exit_state(self) -> bool:
        return self.current == GameState.EXIT

    def reset(self) -> None:
        """Reset the state manager to BOOT state."""
        self.current = GameState.BOOT