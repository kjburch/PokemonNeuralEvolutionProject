from pokemonEnums import *


# Pokemon move class, meant to represent 1 pokemon move and all its effects / attributes
class PokemonMove:
    name = ""
    type = PokemonType.Error
    category = MoveCategory.Error
    maxPP = 0
    power = 0
    accuracy = 0
    # plus/ minus Attack, Defense, Special, Speed
    # for a move that causes changes in the poke stat
    status = [0, 0, 0, 0]
    effect = PokemonStatusEffect.Error
    effectChance = 0

    # allows the creation of a pokemon move object
    def __init__(self, Name, Type, Category, PP, Power, Accuracy, Status, Effect, EffectChance) -> object:
        self.name = Name
        self.type = Type
        self.category = Category
        self.maxPP = PP
        self.power = Power
        self.accuracy = Accuracy
        self.status = Status
        self.effect = Effect
        self.effectChance = EffectChance

    def __str__(self):
        return ("Name:" + str(self.name) + "\nType:" + str(self.type) + "\nCategory:" + str(
            self.category) + "\nPP:" + str(self.maxPP) + "\nPower:" + str(self.power) + "\nAccuracy:" + str(self.accuracy)
            + "\nStatus:" + str(self.status) + "\nEffect:" + str(self.effect) + "\nEffect Chance:" + str(self.effectChance))


# Pokemon Class, meant to represent a single pokemon, not a single pokemon species
class Pokemon:
    name = ""
    hp = 0
    # ev order: attack, defense, special, speed
    ev = []
    moves = []
    type = []
    level = 0
    # plus/ minus attack, defense, special, speed
    statusModifier = [0, 0, 0, 0]
    statusEffects = []

    # allows the creation of a pokemon object
    def __init__(self, Name, HP, EV, Moves, Type, Level) -> object:
        self.name = Name
        self.hp = HP
        self.ev = EV
        self.moves = Moves
        self.type = Type
        self.level = Level
        self.statusModifier = [0, 0, 0, 0]
        self.statusEffects = []

    # Prints the Pokemon and all of its Attributes
    def display(self):
        print("Name:", self.name, "\nHP:", self.hp, "\nEV:", self.ev, "\nAbility:", self.ability, "\nMoves:",
              self.moves, "\nType:", self.type, "\nLevel:", self.level, "Status Effects:", self.statusEffects)
