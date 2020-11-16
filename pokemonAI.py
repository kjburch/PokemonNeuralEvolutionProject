# It kinda works
# good luck

import math
import random

# Global Variables
from pokemonClasses import *
from pokemonFunctions import *

pokemonGeneration = 1


# Main------------------------------------------------------------------------------------------------------------------

electric = PokemonMove("Electric", PokemonType.Electric, MoveCategory.Special, PP=10, Power=90, Accuracy=90, Status=None, Effect=None, Id=None, EffectChance=0)
plant = PokemonMove("Plant", PokemonType.Electric, MoveCategory.Special, PP=0, Power=90, Accuracy=90, Status=None, Effect=None, Id=None, EffectChance=0)
water = PokemonMove("Water", PokemonType.Electric, MoveCategory.Special, PP=10, Power=90, Accuracy=90, Status=None, Effect=None, Id=None, EffectChance=0)
fire = PokemonMove("Fire", PokemonType.Electric, MoveCategory.Special, PP=10, Power=90, Accuracy=90, Status=None, Effect=None, Id=None, EffectChance=0)

# ev order: hp, attack, defense, sp attack, sp defense, speed
# EVs are not currently set correctly however the damage calculator does work as intended for gen 1
pikachu = Pokemon("Pikachu", 15, [7, 6, 6, 7], [electric, plant, water], [PokemonType.Electric], 1, Id= None)
fren = Pokemon("Fren", 10, [7, 6, 6, 7], [electric, plant, water, fire], [PokemonType.Electric], 1, Id= None)

squirtle = Pokemon("Squirtle", 15, [6, 7, 6, 6], [electric, plant, water, fire], [PokemonType.Water], 1, Id=None)
torchic = Pokemon("Torchic", 15, [7, 6, 6, 7], [electric, plant, water, fire], [PokemonType.Electric], 1, Id= None)

battle = Battle([pikachu, fren, pikachu], [squirtle, torchic, squirtle])

# Options are 0 Through 9
# 0, 1, 2, 3 are the moves of the current active pokemon
# 4, 5, 6, 7, 8, 9 switches the current pokemon to one of the party members
res = battle.turn(2, True)
res = battle.turn(10, True)
res = battle.turn(2, True)
res = battle.turn(1, True)
res = battle.turn(5, True)
res = battle.turn(1, True)
res = battle.turn(2, True)
res = battle.turn(3, True)