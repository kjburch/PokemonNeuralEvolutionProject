import cv2 as cv
import numpy as np
from os import path

from pokemonEnums import PokemonStatusEffect

template = cv.resize(cv.imread("Images/pokemonTemplate.png"), (160 * 5, 144 * 5), interpolation=cv.INTER_NEAREST)

topPokemonPosition = (500, 0)

topNamePosition = (50, 40)
topLvlPosition = (200, 72)

botPokemonPosition = (0, 180)

botNamePosition = (400, 295)
botLvlPosition = (600, 331)
botHealthBar = (600, 350)
botHealthNum = (480, 430)

textLocation = (30, 550)


def showBattle(currentTeam, currentTeamActivePokemon, otherTeam, otherTeamActivePokemon, choice):
    clone = template.copy()

    # Other Team Pokemon Name and Level
    cv.putText(clone, str(otherTeam[otherTeamActivePokemon].name).upper(),
               topNamePosition, cv.FONT_HERSHEY_SIMPLEX, color=(0, 0, 0), fontScale=1.5,
               thickness=4)
    cv.putText(clone, str(otherTeam[otherTeamActivePokemon].level).upper(),
               topLvlPosition, cv.FONT_HERSHEY_SIMPLEX, color=(0, 0, 0), fontScale=1,
               thickness=4)
    # Current Team Pokemon Name and Level
    cv.putText(clone, str(currentTeam[currentTeamActivePokemon].name).upper(),
               botNamePosition, cv.FONT_HERSHEY_SIMPLEX, color=(0, 0, 0), fontScale=1.5,
               thickness=4)
    cv.putText(clone, str(currentTeam[currentTeamActivePokemon].level).upper(),
               botLvlPosition, cv.FONT_HERSHEY_SIMPLEX, color=(0, 0, 0), fontScale=1,
               thickness=4)
    # Health Bars
    if otherTeam[otherTeamActivePokemon].hp != otherTeam[otherTeamActivePokemon].maxHp:
        if otherTeam[otherTeamActivePokemon].hp > 0:
            cv.rectangle(clone, (399, 104), (int(160 + (399 - 160) * (
                    otherTeam[otherTeamActivePokemon].hp / otherTeam[
                otherTeamActivePokemon].maxHp)), 95), color=(255, 255, 255), thickness=-1)
        else:
            cv.rectangle(clone, (399, 104), (160, 95), color=(255, 255, 255), thickness=-1)
    if currentTeam[currentTeamActivePokemon].hp != currentTeam[currentTeamActivePokemon].maxHp:
        if currentTeam[currentTeamActivePokemon].hp > 0:
            cv.rectangle(clone, (719, 355), (int(480 + (719 - 480) * (
                    currentTeam[currentTeamActivePokemon].hp / currentTeam[
                currentTeamActivePokemon].maxHp)), 364), color=(255, 255, 255), thickness=-1)
        else:
            cv.rectangle(clone, (719, 375), (480, 384), color=(255, 255, 255), thickness=-1)

    # Status conditions
    effectOther = np.empty(shape=(0, 0, 0))
    effectCurrent = np.empty(shape=(0, 0, 0))
    for sc in otherTeam[otherTeamActivePokemon].statusEffects:
        p = "Images/Status Conditions/" + str(int(sc)) + ".png"
        if path.isfile(p):
            effectOther = cv.resize(cv.imread(p), (18 * 5, 7 * 5), interpolation=cv.INTER_NEAREST)
    for sc in currentTeam[currentTeamActivePokemon].statusEffects:
        p = "Images/Status Conditions/" + str(int(sc)) + ".png"
        if path.isfile(p):
            effectCurrent = cv.resize(cv.imread(p), (18 * 5, 7 * 5), interpolation=cv.INTER_NEAREST)

    if effectOther.shape == (35, 90, 3):
        x_offset = 70
        y_offset = 46
        clone[y_offset:y_offset + effectOther.shape[0], x_offset:x_offset + effectOther.shape[1]] = effectOther
    if effectCurrent.shape == (35, 90, 3):
        x_offset = 470
        y_offset = 305
        clone[y_offset:y_offset + effectCurrent.shape[0], x_offset:x_offset + effectCurrent.shape[1]] = effectCurrent

    # Display Poke Balls
    for i in range(0, len(otherTeam)):
        if otherTeam[i].hp <= 0:
            cv.drawMarker(clone, (82 + 40 * i, 167), (0, 0, 0), markerType=cv.MARKER_TILTED_CROSS, markerSize=25,
                          thickness=6)

    for i in range(0, len(currentTeam)):
        if currentTeam[i].hp <= 0:
            cv.drawMarker(clone, (522 + 40 * i, 467), (0, 0, 0), markerType=cv.MARKER_TILTED_CROSS, markerSize=25,
                          thickness=6)

    # Add Pokemon Images
    pokeTop = cv.resize(
        cv.imread("Images/Red and Blue Front/" + str(otherTeam[otherTeamActivePokemon].id) + ".PNG"),
        (int(56 * 4.6), int(56 * 4.6)), interpolation=cv.INTER_NEAREST)
    x_offset = 470
    y_offset = 0
    clone[y_offset:y_offset + pokeTop.shape[0], x_offset:x_offset + pokeTop.shape[1]] = pokeTop
    pokeBot = cv.resize(
        cv.imread("Images/Back Sprites/" + str(currentTeam[currentTeamActivePokemon].id) + ".PNG"),
        (56 * 5, 56 * 5), interpolation=cv.INTER_NEAREST)
    x_offset = 38
    y_offset = 205
    clone[y_offset:y_offset + pokeBot.shape[0], x_offset:x_offset + pokeBot.shape[1]] = pokeBot

    # Add health Numbers
    if currentTeam[currentTeamActivePokemon].hp <= 0:
        cv.putText(clone, "0 / " + str(
            currentTeam[currentTeamActivePokemon].maxHp), botHealthNum,
                   cv.FONT_HERSHEY_SIMPLEX, color=(0, 0, 0), fontScale=1.5, thickness=6)
    else:
        cv.putText(clone, str(currentTeam[currentTeamActivePokemon].hp) + " / " + str(
            currentTeam[currentTeamActivePokemon].maxHp), botHealthNum,
                   cv.FONT_HERSHEY_SIMPLEX, color=(0, 0, 0), fontScale=1.5, thickness=6)

    # Choice and text
    if choice < 4:
        cv.drawContours(clone, [np.array([(360, 560), (360, 590), (380, 575)])], 0, (0, 0, 0), -1)
        s = str(currentTeam[currentTeamActivePokemon].name).upper() + "\nused the move\n" + str(
            currentTeam[currentTeamActivePokemon].moves[choice].name).upper() + "\non opponent's\n" + str(
            otherTeam[otherTeamActivePokemon].name).upper()
    else:
        w = 250
        cv.drawContours(clone, [np.array([(360 + w, 560), (360 + w, 590), (380 + w, 575)])], 0, (0, 0, 0), -1)
        clone2 = clone.copy()
        s = str(currentTeam[currentTeamActivePokemon].name).upper() + "\nwas swapped out\n"
        y0, dy = textLocation[1], 30
        for i, line in enumerate(s.split('\n')):
            y = y0 + i * dy
            cv.putText(clone2, line, (textLocation[0], y), cv.FONT_HERSHEY_SIMPLEX, color=(0, 0, 0),
                       fontScale=1,
                       thickness=2)
        cv.imshow("display", clone2)
        cv.waitKey(0)
        pokeBot = cv.resize(
            cv.imread("Images/Back Sprites/" + str(currentTeam[choice - 4].id) + ".PNG"),
            (56 * 5, 56 * 5), interpolation=cv.INTER_NEAREST)
        x_offset = 38
        y_offset = 205
        clone[y_offset:y_offset + pokeBot.shape[0], x_offset:x_offset + pokeBot.shape[1]] = pokeBot
        s = str(currentTeam[choice - 4].name).upper() + "\nwas swapped in"

    y0, dy = textLocation[1], 30
    for i, line in enumerate(s.split('\n')):
        y = y0 + i * dy
        cv.putText(clone, line, (textLocation[0], y), cv.FONT_HERSHEY_SIMPLEX, color=(0, 0, 0), fontScale=1,
                   thickness=2)

    cv.imshow("display", clone)
    cv.waitKey(0)


def displayWinner(win):
    clone = template.copy()
    cv.rectangle(clone, (180, 300), (625, 190), color=(0, 0, 0), thickness=-1)
    cv.putText(clone, "The Battle Is Over!!!", (190, 230), fontScale=2.5,
               thickness=4,
               fontFace=cv.FONT_HERSHEY_PLAIN, color=(0, 0, 255))
    cv.putText(clone, "Team " + str(win) + " Is Victorious", (190, 290), fontScale=2.5,
               thickness=4,
               fontFace=cv.FONT_HERSHEY_PLAIN, color=(0, 0, 255))
    cv.imshow("display", clone)
    cv.waitKey(0)


def displaySwap():
    clone = template.copy()
    cv.putText(clone, "NOW VIEWING THE OTHER TEAM", (80, 290), fontScale=2.5, thickness=4,
               fontFace=cv.FONT_HERSHEY_PLAIN, color=(0, 55, 0))
    cv.imshow("display", clone)
    cv.waitKey(0)
