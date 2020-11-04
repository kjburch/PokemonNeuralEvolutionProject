from pokemonClasses import *
from pokemonEnums import *
import csv


def getAllMoves():
    movesRaw = []
    moveList = []
    with open("data/moves.csv") as file:
        reader = csv.reader(file, delimiter=",")
        for row in reader:
            if row[2] == str(1):
                movesRaw.append(row)

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
        status = getStatus(effect)
        effectChance = getInt(mv[effectChanceCol], mv, effectChanceCol)
        moveList.append(PokemonMove(name, type, category, pp, power, acc, status, effect, effectChance))

    return moveList


def getStatus(effectNum):
    return [0, 0, 0, 0]


def getInt(strparam, mv, col):
    if strparam == "":
        return None
    else:
        return int(mv[col])



