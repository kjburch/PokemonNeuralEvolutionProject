import math
import random
from pokemonEnums import *

pokemonGeneration = 1


# Calculates and returns Attack Damage
def calcDamage(attackingPokemon, defendingPokemon, move, targets, weather, badge, other):
    # Level modifier calc
    if pokemonGeneration != 1:
        l = 1
    # gen 1 crit based on pokemon speed
    # does not currently take into account special cases
    else:
        P = attackingPokemon.ev[5] / 512
        rTemp = random.randint(0, 100)
        if rTemp / 100 < P:
            l = attackingPokemon.level * 2
        else:
            l = attackingPokemon.level

    # Doubles or Triples battle target modifier
    if targets > 1:
        t = 0.75
    else:
        t = 1

    # Weather Calculation Modifiers
    if weather == Weather.Sun:
        if move.type == PokemonType.Fire:
            w = 1.5
        if move.type == PokemonType.Water:
            w = 0.5
    elif weather == Weather.Rain:
        if move.type == PokemonType.Fire:
            w = 0.5
        if move.type == PokemonType.Water:
            w = 1.5
    else:
        w = 1

    # Badge Multiplier, Gen 2 only
    # Not yet implemented
    if pokemonGeneration != 2:
        b = 1
    else:
        # will be implemented at some point
        b = 1

    # Critical Hit Chance
    # Refers to crit hit table
    # not fully implemented
    if pokemonGeneration != 1:
        r2 = random.randint(0, 1000)
        # After gen 5
        if pokemonGeneration > 5:
            if r2 / 1000 < 6.25:
                c = 1.5
            else:
                c = 1
        # Gen 2 through 5
        else:
            if r2 / 1000 < 6.25:
                c = 2
            else:
                c = 1
    # Does not exist in Gen 1
    else:
        c = 1

    # Random Num Generator
    r = random.randint(85, 100) / 100

    # Other Calculation
    # Not yet implemented
    o = 1

    # Stab calculation
    if move.type in attackingPokemon.type:
        s = 1.5

    # Type Effectiveness
    ty = 1
    for i in defendingPokemon.type:
        ty = ty * typeEffectivenessGen1[move.type][i]

    # Burn modifier Calculation
    if PokemonStatusEffect.Burn in attackingPokemon.statusEffects and move.category == MoveCategory.Physical:
        bu = 0.5
    else:
        bu = 1

    # Modifier Calculation
    modifier = t * w * b * c * r * s * ty * bu * o

    # Attack and Defense calc variable
    # attack or defense stat multiplied by the stat modifier
    # If the attack is physical
    if move.category == MoveCategory.Physical:
        A = attackingPokemon.ev[1] * statModifier[attackingPokemon.statusModifier[0]]
        D = defendingPokemon.ev[2] * statModifier[defendingPokemon.statusModifier[1]]
    # If the attack is special
    else:
        # Generation 1 combines special attack and special defense into 1 stat called special
        if pokemonGeneration == 1:
            A = attackingPokemon.ev[3] * statModifier[attackingPokemon.statusModifier[2]]
            D = defendingPokemon.ev[3] * statModifier[defendingPokemon.statusModifier[2]]
        else:
            A = attackingPokemon.ev[3] * statModifier[attackingPokemon.statusModifier[2]]
            D = defendingPokemon.ev[4] * statModifier[defendingPokemon.statusModifier[3]]

    # Calculates the base dam without modifiers
    base = math.floor(math.floor(math.floor(2 * l / 5+2) * move.power * A / D) / 50)+2

    # actually calculates the damage
    damage = math.floor(base * modifier)

    textOut = "Printing Damage Calculation Variables:\n\nTargets: "+str(t)+", Weather: "+str(w)+", Badge: "+str(
        b)+", Critical: "+str(c)+", Random: "+str(r)+", Stab: "+str(s)+", Type: "+str(ty)+", Burn: "+str(
        bu)+", Other: "+str(o)+"\nAttacking Pokemon Level: "+str(l)+", Move Power: "+str(
        move.power)+", Attacking Pokemon Attack Stat: "+str(A)+", Defending Pokemon Defense Stat: "+str(
        D)+"\n\nBase Damage: "+str(base)+"\nDamage Modifier: "+str(modifier)+"\n\nActual damage: "+str(damage)

    return damage, textOut
