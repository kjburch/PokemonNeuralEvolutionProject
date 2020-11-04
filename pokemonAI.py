# It kinda works
# good luck

import math
import random


# Global Variables
from pokemonClasses import *
from pokemonFunctions import *

pokemonGeneration = 1


# Main------------------------------------------------------------------------------------------------------------------

thundershock = PokemonMove("thundershock", PokemonType.Electric, MoveCategory.Special, 30, 40, 100, [],
                           PokemonStatusEffect.Error)

# ev order: hp, attack, defense, sp attack, sp defense, speed
# EVs are not currently set correctly however the damage calculator does work as intended for gen 1
pikachu = Pokemon("pikachu", 35, [35, 55, 30, 10, 7], "static", [thundershock], [PokemonType.Electric], 1)

squirtle = Pokemon("squirtle", 35, [44, 48, 65, 6, 43], "torrent", [], [PokemonType.Water], 1)


d = calcDamage(pikachu, squirtle, thundershock, 1, Weather.none, 0, 0)

print(d[1])
