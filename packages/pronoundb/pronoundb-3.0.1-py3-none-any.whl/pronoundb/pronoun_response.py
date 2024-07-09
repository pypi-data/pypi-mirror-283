from dataclasses import dataclass
from typing import Optional


@dataclass
class PronounResponse:
    decoration: Optional[str]
    sets: dict[str, list[str]]

    def __init__(self, data):
        self.decoration = data['decoration']
        self.sets = data['sets']
