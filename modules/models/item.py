from enum import Enum

class EffectType(Enum):
    StrengthModifier = 0
    InteligenceModifier = 1
    CharismaModifier = 2

class Effect:
    def __init__(self, effect: EffectType, modifier: int):
        self.effect = effect
        self.modifier = modifier


class Item:
    def __init__(self, name, effect: Effect):

        self.name = name
        self.effect = effect