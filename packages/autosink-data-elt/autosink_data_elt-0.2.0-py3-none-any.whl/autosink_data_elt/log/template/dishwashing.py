# 내장
from typing import List, Deque
from dataclasses import dataclass, field, asdict
from collections import deque

# 프로젝트
from autosink_data_elt.log.template.interaction import *


@dataclass
class DishwashingDataV1:
    version: int
    user_id: str
    dishwashing_id: str
    dishwashing_start: str
    interactions: List[InteractionV1] = field(default_factory=list)

    def to_dict(self):
        data_dict = asdict(self)
        data_dict['interactions'] = [interaction.to_dict() for interaction in self.interactions]
        return data_dict

    def __post_init__(self):
        if self.interactions and isinstance(self.interactions[0], dict):
            self.interactions = [InteractionV1(**interaction) for interaction in self.interactions]


@dataclass
class DishwashingDataV2:
    version: int
    user_id: str
    dishwashing_id: str
    dishwashing_start: str
    interactions: Deque[InteractionV2] = field(default_factory=lambda: deque(maxlen=10))

    def to_dict(self):
        data_dict = asdict(self)
        data_dict['interactions'] = [interaction.to_dict() for interaction in self.interactions]
        return data_dict

    def __post_init__(self):
        if self.interactions and isinstance(self.interactions[0], dict):
            self.interactions = [InteractionV2(**interaction) for interaction in self.interactions]
