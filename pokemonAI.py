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
pikachu = Pokemon("pikachu", 35, [7, 6, 6, 7],  [thundershock], [PokemonType.Electric], 1)

squirtle = Pokemon("squirtle", 35, [6, 7, 6, 6],  [], [PokemonType.Water], 1)


d = calcDamage(pikachu, squirtle, thundershock, True)

print(d[1])
