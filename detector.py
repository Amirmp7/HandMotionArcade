"""
Hand detection module using MediaPipe.

Detects the user's hand and returns a smoothed horizontal position.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

import cv2
import mediapipe as mp
import numpy as np

from config import GameConfig


@dataclass
class HandDetector:
    """
    Detects the user's hand and converts its horizontal position
    into a normalized value in [0, 1] with exponential smoothing.
    """

    config: GameConfig

    cap: Optional[cv2.VideoCapture] = field(default=None, init=False)
    mp_hands: Optional[mp.solutions.hands] = field(default=None, init=False)
    hands: Optional[mp.solutions.hands.Hands] = field(default=None, init=False)
    drawer: Optional[mp.solutions.drawing_utils] = field(default=None, init=False)
    _smoothed_x: Optional[float] = field(default=None, init=False)
    _error_message: str = field(default="", init=False)

    def __post_init__(self) -> None:
        # Try to open camera
        try:
            self.cap = cv2.VideoCapture(
                self.config.hand.camera_index,
                cv2.CAP_DSHOW,
            )
            if not self.cap.isOpened():
                self._error_message = (
                    "Camera not found.\n"
                    "Please follow these steps:\n"
                    "1. Go to Settings > Privacy > Camera and enable access.\n"
                    "2. Close any other app using the camera.\n"
                    "3. Restart your computer if needed."
                )
                print(self._error_message)
                self.cap = None
                return

            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.config.hand.camera_width)
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.config.hand.camera_height)
            print("Camera opened successfully.")

        except Exception as e:
            self._error_message = f"Error opening camera: {e}"
            print(self._error_message)
            self.cap = None

        # Initialize MediaPipe
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            model_complexity=1,
            min_detection_confidence=self.config.hand.detection_confidence,
            min_tracking_confidence=self.config.hand.tracking_confidence,
        )
        self.drawer = mp.solutions.drawing_utils
        self._smoothed_x = None

    def read_frame(self) -> np.ndarray | None:
        if self.cap is None or not self.cap.isOpened():
            return None
        success, frame = self.cap.read()
        if not success:
            return None
        return cv2.flip(frame, 1)

    def get_hand_position(self, frame: np.ndarray) -> float | None:
        if frame is None or self.hands is None:
            return None

        try:
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            rgb.flags.writeable = False
            result = self.hands.process(rgb)

            if not result.multi_hand_landmarks:
                return None

            landmarks = result.multi_hand_landmarks[0]

            if self.config.debug.show_hand_landmarks:
                self.drawer.draw_landmarks(
                    frame,
                    landmarks,
                    self.mp_hands.HAND_CONNECTIONS,
                )

            control_point = landmarks.landmark[self.mp_hands.HandLandmark.WRIST]
            x = max(0.0, min(1.0, control_point.x))

            alpha = self.config.hand.smoothing_factor
            if self._smoothed_x is None:
                self._smoothed_x = x
            else:
                self._smoothed_x = alpha * x + (1.0 - alpha) * self._smoothed_x

            return max(0.0, min(1.0, self._smoothed_x))

        except Exception as e:
            print(f"Hand detection error: {e}")
            return None

    def is_opened(self) -> bool:
        return self.cap is not None and self.cap.isOpened()

    def get_error_message(self) -> str:
        """Return error message for displaying in-game."""
        return self._error_message

    def release(self) -> None:
        if self.cap is not None:
            self.cap.release()
            print("Camera released.")
        if self.hands is not None:
            self.hands.close()
        cv2.destroyAllWindows()

    def __enter__(self) -> HandDetector:
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.release()