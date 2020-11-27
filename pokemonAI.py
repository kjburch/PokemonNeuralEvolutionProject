from pokemonData import *

# Global Variables
from pokemonClasses import *
from pokemonFunctions import *

pokemonGeneration = 1

# Main------------------------------------------------------------------------------------------------------------------
pokemonOU = getPokemonByTier("OU")
moveList = getAllMoves(pokemonOU)
burn = PokemonMove(Name="burn", Type=PokemonType.Fire, Category=MoveCategory.Status, PP=100, Power=None, Accuracy=100,
                   UserStatus=[0, 0, 0, 0], EnemyStatus=[0, 0, 0, 0], Effect=PokemonStatusEffect.Burn, EffectChance=100,
                   SpecialEffect=SpecialMoveEffect.Error, UserHealthChange=0, TurnDelay=0, Id=-1)
freeze = PokemonMove(Name="freeze", Type=PokemonType.Ice, Category=MoveCategory.Status, PP=100, Power=None,
                     Accuracy=100,
                     UserStatus=[0, 0, 0, 0], EnemyStatus=[0, 0, 0, 0], Effect=PokemonStatusEffect.Freeze,
                     EffectChance=100,
                     SpecialEffect=SpecialMoveEffect.Error, UserHealthChange=0, TurnDelay=0, Id=-1)

# for move in moveList:
#     print(move)
# stun spore, poison powder, supersonic
ids = [78, 77, 48]
moves = getMovesById(moveList, ids)
moves.append(burn)
# for mv in moves:
#     print(mv)
#     print("----------")
# ev order: hp, attack, defense, sp attack, sp defense, speed
# EVs are not currently set correctly however the damage calculator does work as intended for gen 1

for i in range(0, 12):
    pokemonOU[i].moves = moves
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
    rand = random.randint(0, 3)
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
