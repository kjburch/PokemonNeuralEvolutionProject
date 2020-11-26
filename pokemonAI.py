
from pokemonData import *

# Global Variables
from pokemonClasses import *
from pokemonFunctions import *

pokemonGeneration = 1

# Main------------------------------------------------------------------------------------------------------------------
pokemonOU = getPokemonByTier("OU")
moveList = getAllMoves(pokemonOU)


moves = []

for mv in moveList:
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

for p in pokemonOU:
    p.moves = moves

team1 = []
for i in range(0, 6):
    team1.append(pokemonOU[i])
team2 = []
for i in range(6, 12):
    team2.append(pokemonOU[i])

battle = Battle(team1, team2)

# Options are 0 Through 9
# 0, 1, 2, 3 are the moves of the current active pokemon
# 4, 5, 6, 7, 8, 9 switches the current pokemon to one of the party members

while battle.winner() == -1:
    rand = random.randint(0,9)
    res = battle.turn(rand, False, True)
res = battle.turn(rand, False, True)
res = battle.turn(rand, False, True)
res = battle.turn(rand, False, True)
res = battle.turn(rand, False, True)
res = battle.turn(rand, False, True)
res = battle.turn(rand, False, True)





print(res)

# TODO TODO TODO TODO TODO
# TODO TODO TODO TODO TODO
# fix EV in calc damage
# program status effects
# program accuracy/evasion
#
# Program Neural Net :(
