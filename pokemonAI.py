import neat
from pokemonData import *
import pickle
# Global Variables
from pokemonClasses import *
import copy
import os
os.environ["PATH"] += os.pathsep + 'E:/Program Files/Graphviz/bin'

pokemonGeneration = 1

# Main------------------------------------------------------------------------------------------------------------------
pokemonOU = getPokemonByTier("OU")
moveList = getAllMoves(pokemonOU)
# burn = PokemonMove(Name="burn", Type=PokemonType.Fire, Category=MoveCategory.Status, PP=100, Power=None, Accuracy=100,
#                    UserStatus=[0, 0, 0, 0], EnemyStatus=[0, 0, 0, 0], Effect=PokemonStatusEffect.Burn, EffectChance=100,
#                    SpecialEffect=SpecialMoveEffect.Error, UserHealthChange=0, TurnDelay=0, Id=-1)
# freeze = PokemonMove(Name="freeze", Type=PokemonType.Ice, Category=MoveCategory.Status, PP=1, Power=None,
#                      Accuracy=100,
#                      UserStatus=[0, 0, 0, 0], EnemyStatus=[0, 0, 0, 0], Effect=PokemonStatusEffect.Freeze,
#                      EffectChance=50,
#                      SpecialEffect=SpecialMoveEffect.Error, UserHealthChange=0, TurnDelay=0, Id=-1)
flinch = PokemonMove(Name="flinch", Type=PokemonType.Normal, Category=MoveCategory.Physical, PP=10, Power=10,
                     Accuracy=100,
                     UserStatus=[0, 0, 0, 0], EnemyStatus=[0, 0, 0, 0], Effect=PokemonStatusEffect.Flinch,
                     EffectChance=100,
                     SpecialEffect=SpecialMoveEffect.Error, UserHealthChange=0, TurnDelay=0, Id=-1)

# big 4: tauros, snorlax, chansey, exeggutor. these are in most actually good gen1 OU teams
# other variations exist but tauros is 100% in every team if you're really trying to win
big4 = getPokemonByName(pokemonOU, ["tauros", "snorlax", "chansey", "exeggutor"])
tauros = big4[0]
snorlax = big4[1]
chansey = big4[2]
exeggutor = big4[3]
others = getPokemonByName(pokemonOU, ["alakazam", "starmie", "rhydon", "zapdos", "lapras"])
alakazam = others[0]
starmie = others[1]
rhydon = others[2]
zapdos = others[3]
lapras = others[4]

# combos with big 4 taken from https://www.smogon.com/forums/threads/an-introduction-to-teambuilding-in-rby-ou.3667061/:
# rhydon, starmie
# alakazam, starmie
# alakazam, zapdos
# alakazam, lapras

tauros.moves = getMovesByName(moveList, ["earthquake", "body-slam", "hyper-beam", "blizzard"])
# can replace earthquake with hyper beam or self destruct for snorlax
snorlax.moves = getMovesByName(moveList, ["reflect", "body-slam", "earthquake", "rest"])
chansey.moves = getMovesByName(moveList, ["thunder-wave", "ice-beam", "thunderbolt", "soft-boiled"])
exeggutor.moves = getMovesByName(moveList, ["sleep-powder", "psychic", "explosion", "stun-spore"])
alakazam.moves = getMovesByName(moveList, ["recover", "thunder-wave", "psychic", "seismic-toss"])
starmie.moves = getMovesByName(moveList, ["recover", "thunder-wave", "surf", "thunderbolt"])
# this page says rhydon with substitute but its not implemented for now
rhydon.moves = getMovesByName(moveList, ["rock-slide", "body-slam", "earthquake", "hyper-beam"])
zapdos.moves = getMovesByName(moveList, ["thunderbolt", "drill-peck", "thunder-wave", "agility"])
lapras.moves = getMovesByName(moveList, ["blizzard", "thunderbolt", "hyper-beam", "sing"])

team1 = big4
team2 = copy.deepcopy(team1)
team1.append(alakazam)
team1.append(starmie)
team2.append(rhydon)
team2.append(copy.deepcopy(starmie))


def getTeam():
    if random.randint(0, 1) == 1:
        return copy.deepcopy(team1)
    return copy.deepcopy(team2)


