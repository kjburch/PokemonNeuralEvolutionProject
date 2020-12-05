import math
import random
import copy
from pokemonEnums import *


# Calculates and returns Attack Damage
def calcDamage(attackingPokemon, defendingPokemon, move, randBool, critBool=True):
    # Tracks the fitness score of an attack
    fitnessOut = 0

    # Level
    criticalHit = False
    attackerLevel = attackingPokemon.level

    # Critical Hit Probability
    if critBool:
        P = math.floor((attackingPokemon.ev[3] / 512) * 1000)
        if random.randint(0, 1000) < P:
            attackerLevel = attackerLevel * 2
            criticalHit = True
            # print("Next attack is critical")

    # Attack and defense stat
    if move.category == MoveCategory.Physical or move.name == "hyper-beam":
        A = calcStatRBYFromDV("", attackingPokemon.ev[0], 100)
        D = calcStatRBYFromDV("", defendingPokemon.ev[1], 100)
        if not criticalHit:
            A = A * statModifier[attackingPokemon.statusModifier[0]]
            D = D * statModifier[defendingPokemon.statusModifier[1]]
            if PokemonStatusEffect.Reflect in defendingPokemon.statusEffects and \
                    move.name != "Confusion":
                D *= 2
    else:
        A = calcStatRBYFromDV("", attackingPokemon.ev[2], 100)
        D = calcStatRBYFromDV("", defendingPokemon.ev[2], 100)
        if not criticalHit:
            A = A * statModifier[attackingPokemon.statusModifier[2]]
            D = D * statModifier[defendingPokemon.statusModifier[2]]

    # Random Calculation
    if randBool:
        randNum = random.randint(85, 100) / 100
    else:
        randNum = 0.925

    # Stab Move
    if move.type in attackingPokemon.type:
        stab = 1.5
        # add to fitness for using stab moves
        fitnessOut += 1
    else:
        stab = 1

    # Type Effectiveness
    typeModifier = 1
    for t1 in attackingPokemon.type:
        for t2 in defendingPokemon.type:
            typeModifier = typeModifier * typeEffectiveness[t1][t2]
    # Increase fitness for using super effective attacks / punish for using not effective attacks
    if typeModifier > 1:
        fitnessOut += 1
    if typeModifier < 1:
        fitnessOut -= 1

    # Burn Modifier
    burn = False
    if PokemonStatusEffect.Burn in attackingPokemon.statusEffects:
        A = int(A / 2)
        burn = True

    # Modifier Calculation
    modifier = randNum * stab * typeModifier
    # Calculates the base dam without modifiers
    base = math.floor(math.floor(math.floor(2 * attackerLevel / 5+2) * move.power * A / D) / 50)+2

    # actually calculates the damage
    damage = math.floor(base * modifier)

    textOut = "Printing Damage Calculation Variables:\n\nRandom: "+str(randNum)+", Stab: "+str(
        stab)+", Random Removed: "+str(randBool)+", Critical Hit: "+str(
        criticalHit)+", Type: "+str(typeModifier)+", Burn: "+str(burn)+"\nAttacking Pokemon Level: "+str(
        attackingPokemon.level)+", Move Power: "+str(
        move.power)+", Attacking Pokemon Attack Stat: "+str(
        A)+", Defending Pokemon Defense Stat: "+str(
        D)+"\n\nBase Damage: "+str(base)+"\nDamage Modifier: "+str(modifier)+"\n\nActual damage: "+str(
        damage)

    return damage, textOut, fitnessOut


def calcTypeAdvantage(p1, p2):
    typeModifier = 1
    for t1 in p1.type:
        for t2 in p2.type:
            typeModifier = typeModifier * typeEffectiveness[t1][t2]
    return typeModifier


def calcStatRBYFromDV(stat, base, level):
    if stat == 'hp':
        return math.floor((((base+15) * 2+63) * level) / 100)+level+10
    else:
        return math.floor((((base+15) * 2+63) * level) / 100)+5


def getMovesById(moves, ids):
    mvlist = []
    for id in ids:
        for mv in moves:
            if mv.id == id:
                mvlist.append(copy.copy(mv))
    return mvlist


def getMovesByName(moves, names):
    mvlist = []
    for name in names:
        for mv in moves:
            if mv.name == name:
                mvlist.append(copy.deepcopy(mv))
    return mvlist


def getPokemonById(pokemon, ids):
    plist = []
    for id in ids:
        for pk in pokemon:
            if pk.id == id:
                plist.append(copy.copy(pk))
    return plist


def getPokemonByName(pokemon, names):
    plist = []
    for name in names:
        for pk in pokemon:
            if pk.name == name:
                plist.append(copy.copy(pk))
    return plist


def printPokemonMoves(pokemon):
    for mv in pokemon.moves:
        print(mv)
        print("------------------")


def printPokemonStats(pokemons):
    for pokemon in pokemons:
        print(pokemon.name+" stats:")
        print("HP: "+str(pokemon.hp))
        print("Attack: "+str(pokemon.ev[0]))
        print("Defense: "+str(pokemon.ev[1]))
        print("Special: "+str(pokemon.ev[2]))
        print("Speed: "+str(pokemon.ev[3]))
        print("---------------------------")
