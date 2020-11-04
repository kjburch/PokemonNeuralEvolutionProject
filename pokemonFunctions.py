import math
import random
from pokemonEnums import *


# Calculates and returns Attack Damage
def calcDamage(attackingPokemon, defendingPokemon, move, randBool):
    # Level
    criticalHit = False
    attackerLevel = attackingPokemon.level

    # Critical Hit Probability
    P = math.floor((attackingPokemon.ev[3] / 512) * 1000)
    if random.randint(0, 1000) < P:
        attackerLevel = attackerLevel * 2
        criticalHit = True

    # Might not be right ;)
    # Attack and defense stat
    if move.category == MoveCategory.Physical:
        attackerAttackStat = attackingPokemon.ev[0]
        D = defendingPokemon.ev[1]
    else:
        attackerAttackStat = attackingPokemon.ev[2]
        D = defendingPokemon.ev[2]

    # Random Calculation
    if randBool:
        randNum = random.randint(85, 100) / 100
    else:
        randNum = 0.925

    # Stab Move
    if move.type in attackingPokemon.type:
        stab = 1.5
    else:
        stab = 1

    # Type Effectiveness
    typeModifier = 1
    for t1 in attackingPokemon.type:
        for t2 in defendingPokemon.type:
            typeModifier = typeModifier * typeEffectiveness[t1][t2]

    # Burn Modifier
    burn = False
    if PokemonStatusEffect.Burn in attackingPokemon.statusEffects:
        attackerAttackStat = int(attackerAttackStat / 2)
        burn = True

    # Modifier Calculation
    modifier = randNum * stab * typeModifier
    # Calculates the base dam without modifiers
    base = math.floor(math.floor(math.floor(2 * attackerLevel / 5+2) * move.power * attackerAttackStat / D) / 50)+2

    # actually calculates the damage
    damage = math.floor(base * modifier)

    textOut = "Printing Damage Calculation Variables:\n\nRandom: "+str(randNum)+", Stab: "+str(
        stab)+", Random Removed: "+str(randBool)+", Critical Hit: "+str(
        criticalHit)+", Type: "+str(typeModifier)+", Burn: "+str(burn)+"\nAttacking Pokemon Level: "+str(
        attackingPokemon.level)+", Move Power: "+str(
        move.power)+", Attacking Pokemon Attack Stat: "+str(
        attackerAttackStat)+", Defending Pokemon Defense Stat: "+str(
        D)+"\n\nBase Damage: "+str(base)+"\nDamage Modifier: "+str(modifier)+"\n\nActual damage: "+str(damage)

    return damage, textOut
