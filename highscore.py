"""
High score management system.

Handles loading and saving high scores to a JSON file.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import List


@dataclass
class HighScoreEntry:
    """A single entry in the high score list."""
    name: str
    score: int
    level: str


@dataclass(slots=True)
class HighScoreManager:
    """Manages high scores with file I/O."""
    
    file_path: Path
    max_entries: int = 5
    _entries: List[HighScoreEntry] = field(default_factory=list)
    
    def __post_init__(self) -> None:
        self.load()
    
    def load(self) -> None:
        """Load high scores from JSON file."""
        if not self.file_path.exists():
            self._entries = []
            return
        
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self._entries = [
                    HighScoreEntry(**entry) for entry in data
                ]
        except (json.JSONDecodeError, KeyError, TypeError):
            self._entries = []
    
    def save(self) -> None:
        """Save high scores to JSON file."""
        self.file_path.parent.mkdir(parents=True, exist_ok=True)
        
        data = [
            {"name": e.name, "score": e.score, "level": e.level}
            for e in self._entries
        ]
        with open(self.file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    def add_score(self, name: str, score: int, level: str) -> bool:
        """Add a new score if it's high enough."""
        new_entry = HighScoreEntry(name=name, score=score, level=level)
        self._entries.append(new_entry)
        self._entries.sort(key=lambda e: e.score, reverse=True)
        if len(self._entries) > self.max_entries:
            self._entries = self._entries[:self.max_entries]
        self.save()
        return True
    
    def get_entries(self) -> List[HighScoreEntry]:
        """Return the list of high scores."""
        return self._entries.copy()
    
    def is_high_score(self, score: int) -> bool:
        """Check if a score is high enough to be in the top list."""
        if len(self._entries) < self.max_entries:
            return True
        return score > self._entries[-1].score