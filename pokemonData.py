from pokemonClasses import *
from pokemonEnums import *
import csv


def getPokemonByTier(tier):
    with open("data/gen1.csv") as file:
        pokemonRaw = []
        pokemonList = []
        reader = csv.reader(file, delimiter=";")
        tierCol = 3
        for row in reader:
            if row[tierCol] == tier:
                row[0] = row[0].lower()
                pokemonRaw.append(row)

    # get pokemon ID
    pokemonIdDict = {}
    firstRow = True
    with open("data/pokemon.csv") as file:
        reader = csv.reader(file, delimiter=",")
        for row in reader:
            # gen 1 filter
            if firstRow:
                firstRow = False
                continue
            pokeID = int(row[0])
            if pokeID <= 151:
                pokemonIdDict[row[1]] = pokeID
            else:
                break

    nameCol = 0
    hpCol = 4
    statCol = 5
    moves = []
    typeCol = 1
    level = 100

    for pokemon in pokemonRaw:
        name = pokemon[nameCol]
        hp = pokemon[hpCol]
        ev = pokemon[statCol:statCol+5]
        typeList = pokemon[typeCol].lower().replace("[", "").replace("]", "").replace("'", "").split(", ")
        pokemonList.append(Pokemon(name, hp, ev, moves, typeList, level, pokemonIdDict[name]))

    # for pokemon in pokemonList:
    #     print(pokemon)
    #     print("----------------")
    return pokemonList


# returns tuple (possible Pokemon Moves IDs for given pokemon, all gen 1 pokemon moves)
def getAllMoves(pokemonList):
    movesRaw = []
    moveList = []
    bannedMoves = [104, 107, 90, 12, 32, 19, 91]
    # 2d array, row index + 1 is pokemon ID with list having all possible move IDs
    possiblePokemonMoves = [[]]
    for x in range(0, 151):
        possiblePokemonMoves.append([])

    pokeIdSet = set()
    moveIdSet = set()
    for pkm in pokemonList:
        pokeIdSet.add(pkm.getId())

    first = True
    with open("data/pokemon_moves.csv") as file:
        reader = csv.reader(file, delimiter=",")
        for row in reader:
            if first:
                first = False
                continue
            # gen 1 filter
            if int(row[0]) <= 151:
                pokemonId = int(row[0])
                moveId = int(row[2])
                if pokemonId in pokeIdSet and moveId <= 165 and moveId not in bannedMoves:
                    possiblePokemonMoves[pokemonId-1].append(moveId)
                    moveIdSet.add(moveId)
            else:
                break

    counter = 1
    print("Move ids:")
    for id in moveIdSet:
        print(id)
    print("Move id set length:", len(moveIdSet))

    with open("data/moves.csv") as file:
        reader = csv.reader(file, delimiter=",")
        for row in reader:
            # gen 1 filter
            if row[2] == str(1) and int(row[0]) in moveIdSet:
                movesRaw.append(row)

    idCol = 0
    nameCol = 1
    typeCol = 3
    categoryCol = 9
    ppCol = 5
    powerCol = 4
    accCol = 6
    effectCol = 10
    effectChanceCol = 11

    for mv in movesRaw:
        name = mv[nameCol]
        type = int(mv[typeCol])
        category = int(mv[categoryCol])
        pp = int(mv[ppCol])
        power = getInt(mv[powerCol], mv, powerCol)
        acc = getInt(mv[accCol], mv, accCol)
        effect = int(mv[effectCol])
        status = [0, 0, 0, 0]  # getStatus(effect)
        effectChance = getInt(mv[effectChanceCol], mv, effectChanceCol)
        id = mv[idCol]
        moveList.append(PokemonMove(name, type, category, pp, power, acc, status, effect, effectChance, id))

    return (possiblePokemonMoves, moveList)


def getInt(strparam, mv, col):
    if strparam == "":
        return None
    else:
        return int(mv[col])


def getUniqueEffectList(moveList):
    effectSet = set()
    for mv in moveList:
        effectSet.add(mv.getEffect())

    for e in effectSet:
        print(e)
    return effectSet


def getStatusArrayFromEffect(e):
    userAttack, userDefense, userSpecialAttack, userSpecialDefense, userSpeed, userEvasion = 0
    enemyAttack, enemyDefense, enemySpecialAttack, enemySpecialDefense, enemySpeed, enemyAccuracy = 0
    turnDelay = 0  # some moves activate after 1+ turns
    userHealthChange = 0

    statusEffectVerbose = PokemonStatusEffect.Error
    chance = False
    specialEffectsInt = 0

    if e == 2:
        # puts target to sleep
        statusEffectVerbose = PokemonStatusEffect.Sleep
    elif e == 3:
        # has effectChance to poison target
        statusEffectVerbose = PokemonStatusEffect.Poison
        chance = True
    elif e == 4:
        # drains half the damage to heal (absorb/mega drain)
        specialEffectsInt = SpecialMoveEffect.Absorb
    elif e == 5:
        # has effectChance to burn target
        statusEffectVerbose = PokemonStatusEffect.Burn
        chance = True
    elif e == 6:
        # has effectChance to freeze target
        statusEffectVerbose = PokemonStatusEffect.Freeze
        chance = True
    elif e == 7:
        # has effectChance to paralyze target
        statusEffectVerbose = PokemonStatusEffect.Paralysis
        chance = True
    elif e == 8:
        # (SELF) user faints
        specialEffectsInt = SpecialMoveEffect.Faint
        userHealthChange = -1
    elif e == 9:
        # basically dream eater
        # only works if target asleep
        # drains half the damage to heal like absorb
        specialEffectsInt = SpecialMoveEffect.DreamEater
    elif e == 10:
        # uses the target's last used move, basically "Mirror move"
        # Assist moves, time-delayed moves, “meta” moves that operate on other moves/Pokémon/abilities,
        # and some other special moves cannot be copied and are ignored;
        specialEffectsInt = SpecialMoveEffect.MirrorMove
    elif e == 11:
        # raise user attack by one stage
        userAttack = 1
    elif e == 12:
        # raise user defense by one stage
        userDefense = 1
    elif e == 17:
        # raise user evasion by one stage
        userEvasion = 1
    elif e == 18:
        # move never misses
        specialEffectsInt = SpecialMoveEffect.NeverMiss
    elif e == 19:
        # lower target attack by one stage
        enemyAttack = -1
    elif e == 20:
        # lower target defense by one stage
        enemyDefense = -1
    elif e == 24:
        # lower target accuracy by one stage
        enemyAccuracy = -1
    elif e == 26:
        # reset stat stages of both active pokemon to 0
        # remove stat  reductions due to burns, paralysis
        # move = Haze
        specialEffectsInt = SpecialMoveEffect.Haze
    elif e == 27:
        # wait for 2 turns, hit back for twice damage it took
        # move = Bide
        specialEffectsInt = SpecialMoveEffect.Bide
        turnDelay = 2
    elif e == 28:
        # hits every turn for 2-3 turns, then confuses the user.
        # move = Trash and Petal Dance (lol)
        specialEffectsInt = SpecialMoveEffect.ThrashOrPetalDance
    elif e == 29:
        # roar or whirlwind
        # no effect in battle
        # delete this goddamn move
        specialEffectsInt = SpecialMoveEffect.NoEffect
    elif e == 30:
        # hits 2-5 times in a turn
        # fury attack, pin missile, many more
        specialEffectsInt = SpecialMoveEffect.MultiHit
    elif e == 31:
        # move = Conversion
        # changes user's current type to target's type
        # delete this shit
        specialEffectsInt = SpecialMoveEffect.Conversion
    elif e == 32:
        # has effectChance to make the target flinch
        chance = True
        statusEffectVerbose = SpecialMoveEffect.Flinch
    elif e == 33:
        # heals user by half its max hp
        # recover, soft boiled
        specialEffectsInt = SpecialMoveEffect.HealHalfMaxHP
        userHealthChange = 0.50
    elif e == 34:
        # badly poisons target
        statusEffectVerbose = PokemonStatusEffect.BadlyPoisoned
    elif e == 36:
        # Reduces damage from special attacks by 50% for five turns.
        # doubles the user's special while active
        specialEffectsInt = SpecialMoveEffect.DoubleSpecialDefense
    elif e == 38:
        # User sleeps for two turns, completely healing itself.
        userHealthChange = 1.0
    elif e == 40:
        # razor wind move
        # does nothing on turn selected
        # user cannot switch pokemon until next turn when razor wind executes
        specialEffectsInt = SpecialMoveEffect.RazorWind
        turnDelay = 1
    elif e == 42:
        # dragon rage - does 40 damage exactly
        specialEffectsInt = SpecialMoveEffect.DragonRage
    elif e == 43:
        # inflicts damage for 2-5 turns AND target cannot attack
        # a few moves use this, all of them use the same chance for # turns
        # look up wrap or clamp in gen1 for turn chance
        specialEffectsInt = SpecialMoveEffect.MultiHitNoAttack
    elif e == 45:
        # hits twice in one turn
        # like double kick or something
        # cant double damage if including critcal hits
        specialEffectsInt = SpecialMoveEffect.HitTwice
    elif e == 47:
        # Protects the user's stats from being changed by enemy moves until it switches out
        # move = Mist
        specialEffectsInt = SpecialMoveEffect.ProtectStats
    elif e == 49:
        # receive 1/4 of damage as recoil
        # should change userHealthChange but need damage
        specialEffectsInt = SpecialMoveEffect.Recoil
    elif e == 50:
        # confuses target
        statusEffectVerbose = PokemonStatusEffect.Confusion
    elif e == 51:
        # raise user attack by two stages
        userAttack = 2
    elif e == 52:
        # raise user defense by two stages
        userDefense = 2
    elif e == 53:
        # raise speed by two stages
        userSpeed = 2
    elif e == 54:
        # raise user sp attack by two stages
        userSpecialAttack = 2
    elif e == 55:
        # raise special atk by two stages
        userSpecialAttack = 2
    elif e == 66:
        # reduces damage from physical attacks by half
        # move = reflect, physical version of light screen
        # double defense stat
        specialEffectsInt = SpecialMoveEffect.DoubleDefense
    elif e == 67:
        # poisons target 100% chance
        statusEffectVerbose = PokemonStatusEffect.Poison
    elif e == 68:
        # paralyzes target 100% chance
        statusEffectVerbose = PokemonStatusEffect.Paralysis
    elif e == 69:
        # has effectChance to lower enemy attack by one stage
        chance = True
        enemyAttack = -1
    elif e == 70:
        # has effectChance to lower enemy defense by one stage
        chance = True
        enemyDefense = -1
    elif e == 71:
        # has effectChance to lower enemy speed by one stage
        chance = True
        enemySpeed = -1
    elif e == 72:
        # has effectChance to lower enemy sp attack by one stage
        chance = True
        enemySpecialAttack = -1
    elif e == 73:
        # has effectChance to lower enemy sp defense by one stage
        chance = True
        enemySpecialDefense = -1
    elif e == 74:
        # has effectChance to lower target accuracy by one stage
        chance = True
        enemyAccuracy = -1
    elif e == 76:
        # user charges one turn before attacking
        # has effectChance to make target flinch
        chance = True
        turnDelay = 1
        specialEffectsInt = SpecialMoveEffect.Flinch
    elif e == 77:
        # has effectChance to confuse the target
        chance = True
        statusEffectVerbose = PokemonStatusEffect.Confusion
    elif e == 80:
        # substitute, probably not worth implementing
        # as its complex in gen1
        specialEffectsInt = SpecialMoveEffect.Substitute
    elif e == 81:
        # user foregoes next turn to recharge
        # hyper beam
        specialEffectsInt = SpecialMoveEffect.Recharge
    elif e == 82:
        # if user is hit after using this move, attack rises by one stage
        # rage
        specialEffectsInt = SpecialMoveEffect.Rage

    specialEffectsInt += 1
    statusEffectVerbose = 200
    userHealthChange += 3400

    # return [attack,defense,special,speed]


pokemon = getPokemonByTier("OU")
possibleMoves, mvlist = getAllMoves(pokemon)

# for mv in mvlist:
#     print(mv)
#     print("----------")
# print(len(mvlist))
effects = getUniqueEffectList(mvlist)
print("Unique effects: ", len(effects))
# getAllPokemon()
