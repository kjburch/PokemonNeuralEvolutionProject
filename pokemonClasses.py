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

    # allows the creation of a pokemon move object
    def __init__(self, Name, Type, Category, PP, Power, Accuracy, Status, Effect) -> object:
        self.name = Name
        self.type = Type
        self.category = Category
        self.maxPP = PP
        self.power = Power
        self.accuracy = Accuracy
        self.status = Status
        self.effect = Effect


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


class Battle:
    team1 = []
    team2 = []
    team1ActivePokemon = 0
    team2ActivePokemon = 0

    def __init__(self, t1, t2):
        self.team1 = t1
        self.team2 = t2

    def attack(self, move):
        # Physical
        # Special
        # Status
        return True

    # Options 0 through 8 represent all possible choices the NN can make
    def turn(self, choice):
        # Current Pokemon uses a move and tries to attack
        if choice < 4:
            # Ensures current pokemon is not fainted and chosen move has PP
            if self.team1[self.team1ActivePokemon].moves[choice].maxPP > 0 and self.team1[
                    self.team1ActivePokemon].hp > 0:
                self.attack(self.team1[self.team1ActivePokemon].moves[choice])
                return True
            else:
                return False
        # Switch to a different pokemon on the team if it has health
        elif 5 <= choice < 10:
            if self.team1[choice-5].hp > 0 and self.team1ActivePokemon is not (choice-5):
                self.team1ActivePokemon = choice-4
                return True
            else:
                return False
        else:
            return False
