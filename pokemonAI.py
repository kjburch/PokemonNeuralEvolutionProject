# It kinda works
# good luck

import math
import random
from pokemonData import *

# Global Variables
from pokemonClasses import *
from pokemonFunctions import *

pokemonGeneration = 1

# Main------------------------------------------------------------------------------------------------------------------
pokemonOU = getPokemonByTier("OU")
mvlist = getAllMoves(pokemonOU)

print(pokemonOU[0])
print()
print(pokemonOU[10])
print()
print(pokemonOU[7])
moves = []

for mv in mvlist:
    if mv.id == 28:
        moves.append(mv)
    elif mv.id == 14:
        moves.append(mv)
    elif mv.id == 1:
        moves.append(mv)
    elif mv.id == 111:
        moves.append(mv)

# ev order: hp, attack, defense, sp attack, sp defense, speed
# EVs are not currently set correctly however the damage calculator does work as intended for gen 1
pikachu = pokemonOU[0]
pikachu.moves = moves

fren = Pokemon("Fren", 10, [7, 6, 6, 7, 0], moves, [PokemonType.Electric], 1, Id=None,
               Weight=None)

squirtle = Pokemon("Squirtle", 15, [6, 7, 6, 6, 0], moves, [PokemonType.Water], 1, Id=None,
                   Weight=None)
torchic = Pokemon("Torchic", 15, [7, 6, 6, 7, 0], moves, [PokemonType.Electric], 1, Id=None,
                  Weight=None)

battle = Battle([pikachu, fren, pikachu, pikachu, fren, pikachu],
                [squirtle, torchic, squirtle, squirtle, torchic, squirtle])

# Options are 0 Through 9
# 0, 1, 2, 3 are the moves of the current active pokemon
# 4, 5, 6, 7, 8, 9 switches the current pokemon to one of the party members
res = battle.turn(0, True)
res = battle.turn(1, True)
res = battle.turn(2, True)
res = battle.turn(3, True)
res = battle.turn(4, True)
res = battle.turn(5, True)
res = battle.turn(6, True)
res = battle.turn(7, True)
res = battle.turn(8, True)
res = battle.turn(9, True)

# TODO TODO TODO TODO TODO
# TODO TODO TODO TODO TODO
# fix EV in calc damage
# program status effects
# program accuracy/evasion
#
# Program Neural Net :(
