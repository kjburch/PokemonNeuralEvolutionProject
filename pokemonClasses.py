import time

import numpy as np
import copy
from pokemonEnums import *
from pokemonFunctions import *
import random
import cv2 as cv


# Pokemon move class, meant to represent 1 pokemon move and all its effects / attributes
class PokemonMove:
    name = ""
    type = PokemonType.Error
    category = MoveCategory.Error
    maxPP = 0
    power = 0
    accuracy = 0
    # plus/ minus Attack, Defense, Special, Speed, Evasion/Accuracy
    # for a move that causes changes in the poke stat
    userStatus = [0, 0, 0, 0, 0]
    enemyStatus = [0, 0, 0, 0, 0]
    effect = PokemonStatusEffect.Error
    effectChance = 0
    specialEffect = 0
    userHealthChange = 0
    turnDelay = 0
    id = 0

    # allows the creation of a pokemon move object
    def __init__(self, Name, Type, Category, PP, Power, Accuracy, UserStatus, EnemyStatus, Effect, EffectChance,
                 SpecialEffect, UserHealthChange, TurnDelay, Id) -> object:
        self.name = Name
        self.type = Type
        self.category = Category
        self.maxPP = PP
        self.power = Power
        self.accuracy = Accuracy
        self.userStatus = UserStatus
        self.enemyStatus = EnemyStatus
        self.effect = Effect
        self.effectChance = EffectChance
        self.specialEffect = SpecialEffect
        self.userHealthChange = UserHealthChange
        self.turnDelay = TurnDelay
        self.id = Id

    def getEffect(self):
        return self.effect

    def __str__(self):
        return ("Name:" + str(self.name) + "\nType: " + str(self.type) + "\nCategory: " + str(
            self.category) + "\nPP: " + str(self.maxPP) + "\nPower: " + str(self.power) + "\nAccuracy: " + str(
            self.accuracy)
                + "\nUser Status: " + str(self.userStatus) + "\nEnemy Status: " + str(
                    self.enemyStatus) + "\nEffect: " + str(
                    self.effect) + "\nEffect Chance: " + str(self.effectChance)
                + "\nSpecial Effect: " + str(self.specialEffect) + "\nUser Health Change: " + str(
                    self.userHealthChange) + "\nTurn Delay: " + str(self.turnDelay)
                + "\nID: " + str(self.id))


# Pokemon Class, meant to represent a single pokemon, not a single pokemon species
class Pokemon:
    name = ""
    hp = 0
    maxHp = 0
    # ev order: attack, defense, special, speed
    ev = []
    moves = []
    type = []
    level = 0
    # plus/ minus attack, defense, special, speed, accuracy
    statusModifier = [0, 0, 0, 0, 0]
    statusEffects = []
    id = 0
    weight = 0
    firstEffectRound = []
    lastMoveHitBy = None

    # allows the creation of a pokemon object
    def __init__(self, Name, HP, EV, Moves, Type, Level, Id, Weight) -> object:
        self.name = Name
        self.maxHp = HP
        self.hp = HP
        self.maxHp = HP
        self.ev = EV
        self.moves = Moves
        self.type = Type
        self.level = Level
        self.statusModifier = [0, 0, 0, 0, 0]
        self.statusEffects = []
        self.id = Id
        self.weight = Weight
        self.firstEffectRound = []
        lastMoveHitBy = None

    # Prints the Pokemon and all of its Attributes
    def __str__(self):
        return ("Name:" + str(self.name) + "\nHP:" + str(self.hp) + "\nEV:" + str(self.ev) + "\nMoves:" + str(
            self.moves) + "\nType:" + str(self.type) + "\nLevel:" +
                str(self.level) + "\nStatus Modifier:" + str(self.statusModifier) + "\nStatus Effects:" + str(
                    self.statusEffects) + "\nID:" + str(self.id) + "\nWeight:" + str(self.weight))

    def getId(self):
        return self.id


class Battle:
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

    # Keeps track of turn
    turnNum = 0
    # Current Team
    currentTeam = []
    currentTeamActivePokemon = 0
    # Other team
    otherTeam = []
    otherTeamActivePokemon = 0

    def __init__(self, t1, t2):
        self.currentTeam = t1
        self.otherTeam = t2

    def showBattle(self, choice):
        clone = self.template.copy()
        # Other Team
        cv.putText(clone, str(self.otherTeam[self.otherTeamActivePokemon].name).upper(),
                   self.topNamePosition, cv.FONT_HERSHEY_SIMPLEX, color=(0, 0, 0), fontScale=1.5,
                   thickness=4)
        cv.putText(clone, str(self.otherTeam[self.otherTeamActivePokemon].level).upper(),
                   self.topLvlPosition, cv.FONT_HERSHEY_SIMPLEX, color=(0, 0, 0), fontScale=1,
                   thickness=4)
        # Current Team
        cv.putText(clone, str(self.currentTeam[self.currentTeamActivePokemon].name).upper(),
                   self.botNamePosition, cv.FONT_HERSHEY_SIMPLEX, color=(0, 0, 0), fontScale=1.5,
                   thickness=4)
        cv.putText(clone, str(self.currentTeam[self.currentTeamActivePokemon].level).upper(),
                   self.botLvlPosition, cv.FONT_HERSHEY_SIMPLEX, color=(0, 0, 0), fontScale=1,
                   thickness=4)
        # Health Bars
        if self.otherTeam[self.otherTeamActivePokemon].hp != self.otherTeam[self.otherTeamActivePokemon].maxHp:
            if self.otherTeam[self.otherTeamActivePokemon].hp > 0:
                cv.rectangle(clone, (399, 104), (int(160 + (399 - 160) * (
                        self.otherTeam[self.otherTeamActivePokemon].hp / self.otherTeam[
                    self.otherTeamActivePokemon].maxHp)), 95), color=(255, 255, 255), thickness=-1)
            else:
                cv.rectangle(clone, (399, 104), (160, 95), color=(255, 255, 255), thickness=-1)
        if self.currentTeam[self.currentTeamActivePokemon].hp != self.currentTeam[self.currentTeamActivePokemon].maxHp:
            if self.currentTeam[self.currentTeamActivePokemon].hp > 0:
                cv.rectangle(clone, (719, 355), (int(480 + (719 - 480) * (
                        self.currentTeam[self.currentTeamActivePokemon].hp / self.currentTeam[
                    self.currentTeamActivePokemon].maxHp)), 364), color=(255, 255, 255), thickness=-1)
            else:
                cv.rectangle(clone, (719, 375), (480, 384), color=(255, 255, 255), thickness=-1)

        # Poke Balls
        for i in range(0, len(self.otherTeam)):
            if self.otherTeam[i].hp <= 0:
                cv.drawMarker(clone, (77 + 45 * i, 167), (0, 0, 0), markerType=cv.MARKER_TILTED_CROSS, markerSize=25,
                              thickness=6)
        for i in range(0, len(self.currentTeam)):
            if self.currentTeam[i].hp <= 0:
                cv.drawMarker(clone, (502 + 45 * i, 467), (0, 0, 0), markerType=cv.MARKER_TILTED_CROSS, markerSize=25,
                              thickness=6)

        # Add Pokemon
        pokeTop = cv.resize(
            cv.imread("Images/Red and Blue Front/" + str(self.otherTeam[self.otherTeamActivePokemon].id) + ".PNG"),
            (int(56 * 4.6), int(56 * 4.6)), interpolation=cv.INTER_NEAREST)
        x_offset = 470
        y_offset = 0
        clone[y_offset:y_offset + pokeTop.shape[0], x_offset:x_offset + pokeTop.shape[1]] = pokeTop
        pokeBot = cv.resize(
            cv.imread("Images/Back Sprites/" + str(self.currentTeam[self.currentTeamActivePokemon].id) + ".PNG"),
            (56 * 5, 56 * 5), interpolation=cv.INTER_NEAREST)
        x_offset = 38
        y_offset = 205
        clone[y_offset:y_offset + pokeBot.shape[0], x_offset:x_offset + pokeBot.shape[1]] = pokeBot

        # add health Numbers
        if self.currentTeam[self.currentTeamActivePokemon].hp <= 0:
            cv.putText(clone, "0 / " + str(
                self.currentTeam[self.currentTeamActivePokemon].maxHp), self.botHealthNum,
                       cv.FONT_HERSHEY_SIMPLEX, color=(0, 0, 0), fontScale=1.5, thickness=6)
        else:
            cv.putText(clone, str(self.currentTeam[self.currentTeamActivePokemon].hp) + " / " + str(
                self.currentTeam[self.currentTeamActivePokemon].maxHp), self.botHealthNum,
                       cv.FONT_HERSHEY_SIMPLEX, color=(0, 0, 0), fontScale=1.5, thickness=6)
        # Choice and text
        if choice < 4:
            cv.drawContours(clone, [np.array([(360, 560), (360, 590), (380, 575)])], 0, (0, 0, 0), -1)
            s = str(self.currentTeam[self.currentTeamActivePokemon].name).upper() + "\nused the move\n" + str(
                self.currentTeam[self.currentTeamActivePokemon].moves[choice].name).upper() + "\non opponent's\n" + str(
                self.otherTeam[self.otherTeamActivePokemon].name).upper()
        else:
            w = 250
            cv.drawContours(clone, [np.array([(360 + w, 560), (360 + w, 590), (380 + w, 575)])], 0, (0, 0, 0), -1)
            clone2 = clone.copy()
            s = str(self.currentTeam[self.currentTeamActivePokemon].name).upper() + "\nwas swapped out\n"
            y0, dy = self.textLocation[1], 30
            for i, line in enumerate(s.split('\n')):
                y = y0 + i * dy
                cv.putText(clone2, line, (self.textLocation[0], y), cv.FONT_HERSHEY_SIMPLEX, color=(0, 0, 0),
                           fontScale=1,
                           thickness=2)
            cv.imshow("display", clone2)
            cv.waitKey(0)
            pokeBot = cv.resize(
                cv.imread("Images/Back Sprites/" + str(self.currentTeam[choice - 4].id) + ".PNG"),
                (56 * 5, 56 * 5), interpolation=cv.INTER_NEAREST)
            x_offset = 38
            y_offset = 205
            clone[y_offset:y_offset + pokeBot.shape[0], x_offset:x_offset + pokeBot.shape[1]] = pokeBot
            s = str(self.currentTeam[choice - 4].name).upper() + "\nwas swapped in"

        y0, dy = self.textLocation[1], 30
        for i, line in enumerate(s.split('\n')):
            y = y0 + i * dy
            cv.putText(clone, line, (self.textLocation[0], y), cv.FONT_HERSHEY_SIMPLEX, color=(0, 0, 0), fontScale=1,
                       thickness=2)

        cv.imshow("display", clone)
        cv.waitKey(0)

    # Swaps the current team with the other team
    def swapTeam(self):
        # Increments turn count
        self.turnNum += 1
        # Stores team data temporarily
        tempTeam = self.currentTeam
        tempActive = self.currentTeamActivePokemon
        # Switches current team and with non-active team
        self.currentTeam = self.otherTeam
        self.currentTeamActivePokemon = self.otherTeamActivePokemon
        self.otherTeam = tempTeam
        self.otherTeamActivePokemon = tempActive

    def displaySwap(self):
        clone = self.template.copy()
        cv.putText(clone, "NOW VIEWING THE OTHER TEAM", (80, 290), fontScale=2.5, thickness=4,
                   fontFace=cv.FONT_HERSHEY_PLAIN, color=(0, 55, 0))
        cv.imshow("display", clone)
        cv.waitKey(0)

    # Processes a valid attack
    def attack(self, move):
        # Not fully implemented yet
        # Physical Moves
        print(move.category)
        b = self.simulateStatusEffect(self.currentTeam[self.currentTeamActivePokemon], True)
        if b:
            print(self.currentTeam[
                      self.currentTeamActivePokemon].name + "cannot attack this round due to a status effect")
            return True
        if move.category == MoveCategory.Physical:
            damage = calcDamage(
                self.currentTeam[self.currentTeamActivePokemon], self.otherTeam[self.otherTeamActivePokemon], move,
                True)[0]
            print("  The attack did", damage, "points of damage")
            self.otherTeam[self.otherTeamActivePokemon].hp -= damage
            self.otherTeam[self.otherTeamActivePokemon].lastMoveHitBy = move
            self.rollStatusEffect(self.otherTeam[self.otherTeamActivePokemon], move)
        # Special Moves
        elif move.category == MoveCategory.Special:
            damage = calcDamage(
                self.currentTeam[self.currentTeamActivePokemon], self.otherTeam[self.otherTeamActivePokemon], move,
                True)[0]
            print("  The attack did", damage, "points of damage")
            self.otherTeam[self.otherTeamActivePokemon].hp -= damage
            self.otherTeamActivePokemon.lastMoveHitBy = move
            self.rollStatusEffect(self.otherTeam[self.otherTeamActivePokemon], move)
        # Status Moves
        elif move.category == MoveCategory.Status:
            if move.specialEffect == 0:
                for i in range(0, 5):
                    self.currentTeam[self.currentTeamActivePokemon].statusModifier[i] += move.userStatus[i]
                    self.otherTeam[self.otherTeamActivePokemon].statusModifier[i] += move.enemyStatus[i]
                    self.rollStatusEffect(self.otherTeam[self.otherTeamActivePokemon], move)
            else:
                self.specialMove(self, move)

        self.simulateStatusEffect(self.currentTeam[self.currentTeamActivePokemon], False)
        if self.otherTeam[self.otherTeamActivePokemon].hp <= 0:
            print(" ", self.otherTeam[self.otherTeamActivePokemon].name, "has fainted!")
        if self.currentTeam[self.currentTeamActivePokemon].hp <= 0:
            print(" ", self.currentTeam[self.currentTeamActivePokemon].name, "has fainted!")

        self.simulateStatusEffect(self.currentTeam[self.currentTeamActivePokemon], True)
        return True

    # Process a special move
    def specialMove(self, move):
        print("Special move effects not yet implemented")

    def rollStatusEffect(self, pokemon, move):
        if move.effect != 1:
            if move.type == PokemonType.Fire and pokemon.type == PokemonType.Fire:
                return
            elif move.effect == PokemonStatusEffect.Freeze and pokemon.type == PokemonType.Ice:
                return
            elif (
                    move.effect == PokemonStatusEffect.Poison or move.effect == PokemonStatusEffect.BadlyPoisoned) and pokemon.type == PokemonType.Poison:
                return
            if move.effectChance is None:
                pokemon.statusEffects.append(move.effect)
                pokemon.firstEffectRound.append(0)
            else:
                rnum = random.randint(0, 100)
                if rnum <= move.effectChance:
                    pokemon.statusEffects.append(move.effect)
                    pokemon.firstEffectRound.append(0)

    # simulate status effect (burn, freeze, etc)
    # returns true if move skipped (frozen, paralyzed, etc), false otherwise
    # firstEffectRound
    def simulateStatusEffect(self, pokemon, before):
        for i in range(0, len(pokemon.statusEffects)):
            effect = pokemon.statusEffects[i]
            firstRound = pokemon.firstEffectRound[i]
            if effect == PokemonStatusEffect.Freeze and before:
                # frozen until hit by fire type move other than fire spin or opponent uses Haze
                if pokemon.lastMoveHitBy.type == PokemonType.Fire:
                    del pokemon.statusEffects[i]
                    del pokemon.firstEffectRound[i]
                    return False
                return True
            elif effect == PokemonStatusEffect.Paralysis and before:
                rand = random.randint(0, 100)
                if rand <= 25:
                    del pokemon.statusEffects[i]
                    del pokemon.firstEffectRound[i]
                    pokemon.ev[3] *= 4
                    print("The paralysis for" + pokemon.name + "has ended.")
                    continue
                # speed reduced 75%
                if firstRound == 0:
                    pokemon.ev[3] *= 0.25
                    pokemon.firstEffectRound[i] += 1
                rand = random.randint(0, 100)
                if rand <= 25:
                    print(pokemon.name + "is paralyzed and unable to move!")
                    return True
                return False
            elif effect == PokemonStatusEffect.Poison and not before:
                decrease = pokemon.maxHp / 16.0
                if decrease < 1:
                    decrease = 1
                pokemon.hp -= decrease
                print(pokemon.name + "loses" + decrease + "health to poison.")
                return False
            elif effect == PokemonStatusEffect.BadlyPoisoned and not before:
                decrease = pokemon.maxHp / 16.0 + pokemon.maxHp * firstRound / 16.0
                if decrease < 1:
                    decrease = 1
                pokemon.hp -= decrease
                print(pokemon.name + "loses" + decrease + "health to bad poison.")
                pokemon.firstEffectRound[i] += 1
                return False
            elif effect == PokemonStatusEffect.Sleep and before:
                # intial round when rolling
                if firstRound == 0:
                    pokemon.firstEffectRound[i] = random.randint(1, 7)
                    print(pokemon.name + "is fast asleep")
                    return True
                # last round when 1
                elif firstRound == 1:
                    del pokemon.firstEffectRound[i]
                    del pokemon.statusEffects[i]
                    print(pokemon.name + "awakens!")
                    return False
                else:
                    pokemon.firstEffectRound[i] -= 1
                    print(pokemon.name + "is fast asleep")
                    return True
            elif effect == PokemonStatusEffect.Bound and before:
                placeholder = True
            elif effect == PokemonStatusEffect.Confusion:
                if firstRound == 0:
                    pokemon.firstEffectRound[i] = random.randint(2, 5)
                elif firstRound == 1:
                    del pokemon.firstEffectRound[i]
                    del pokemon.statusEffects[i]
                    print(pokemon.name + "has snapped out of confusion!")
                    return False
                else:
                    r = random.randint(1, 2)
                    if r == 1:
                        c = PokemonMove(Name="Confusion", Type=PokemonType.Confusion, Category=MoveCategory.Physical,
                                        PP=100, Power=40,
                                        Accuracy=100, UserStatus=[0, 0, 0, 0], EnemyStatus=[0, 0, 0, 0],
                                        Effect=PokemonStatusEffect.Error, EffectChance=None,
                                        SpecialEffect=None, UserHealthChange=None, TurnDelay=None, Id=999)
                        pokemon.hp -= calcDamage(pokemon, pokemon, c, False, False)
                        print(pokemon.name + "hurt itself in confusion!")
                    pokemon.firstEffectRound[i] -= 1
                    return False

    # Process a single turn of battle using the current active team and a valid move/swap choice
    # Choices 0 through 9 represent all possible choices the NN can make
    # Out results in a verbose output of the turn
    def turn(self, choice, out=False, display=False):
        # Checks to see if any team has no usable pokemon remaining
        win = self.winner()
        # Only runs if both teams have remaining usable pokemon
        if win == -1:
            if out:
                print("\nTurn Number", self.turnNum, ":")
            # Current Pokemon uses a move and tries to attack
            # choice represents which of the pokemon's four moves is used
            if choice < 4:
                # Ensures current pokemon is not fainted and chosen move has PP
                if len(self.currentTeam[self.currentTeamActivePokemon].moves) > choice and \
                        self.currentTeam[self.currentTeamActivePokemon].moves[choice].maxPP > 0 and self.currentTeam[
                    self.currentTeamActivePokemon].hp > 0:
                    # verbose output for successful move execution
                    if display:
                        self.showBattle(choice)
                    if out:
                        print(" ", str(self.currentTeam[self.currentTeamActivePokemon].name), "used the move",
                              str(self.currentTeam[self.currentTeamActivePokemon].moves[choice].name), "on opponent's",
                              str(self.otherTeam[self.otherTeamActivePokemon].name))
                    # attacks the opponent using the desired move
                    self.attack(self.currentTeam[self.currentTeamActivePokemon].moves[choice])
                    if display:
                        self.showBattle(choice)
                    # swap active team after a successful move execution
                    self.swapTeam()
                    if display:
                        self.displaySwap()
                    return True
                # Move execution was unsuccessful
                else:
                    # Verbose output for unsuccessful move execution
                    if out:
                        # When the desired move does not exist
                        if len(self.currentTeam[self.currentTeamActivePokemon].moves) <= choice:
                            print(" ", str(self.currentTeam[self.currentTeamActivePokemon].name),
                                  "could not use move", choice, "because that Move is NULL")
                        else:
                            print(" ", str(self.currentTeam[self.currentTeamActivePokemon].name),
                                  "could not use the move",
                                  str(self.currentTeam[self.currentTeamActivePokemon].moves[choice].name), "because:")
                            # when the desired move has no remaining PP
                            if self.currentTeam[self.currentTeamActivePokemon].moves[choice].maxPP <= 0:
                                print(" ", str(self.currentTeam[self.currentTeamActivePokemon].moves[choice].name),
                                      "has no PP remaining.")
                                # when the active pokemon has no health remaining
                            if self.currentTeam[self.currentTeamActivePokemon].hp <= 0:
                                print(" ", str(self.currentTeam[self.currentTeamActivePokemon].name),
                                      "has no health remaining.")
                    return False
            # Switch to a different pokemon on the team, returns true if swap was successful, returns false if swap
            # was not successful
            # choice represents which of the pokemon 1-6 is going to be swapped to
            elif 4 <= choice <= 9:
                if len(self.currentTeam) > (choice - 4) and self.currentTeam[
                    choice - 4].hp > 0 and self.currentTeamActivePokemon is not (choice - 4):
                    # Verbose output for when the swap is successful
                    if display:
                        self.showBattle(choice)
                    if out:
                        print(" ", str(self.currentTeam[self.currentTeamActivePokemon].name), "was swapped out\n ",
                              str(self.currentTeam[choice - 4].name), "was swapped in")
                    self.currentTeamActivePokemon = choice - 4
                    # Swaps team when choice is successfully executed
                    self.swapTeam()
                    if display:
                        self.displaySwap()
                    return True
                else:
                    # Verbose output for when swap does not work properly
                    if out:
                        # If the pokemon being swapped to does nto exist
                        if len(self.currentTeam) <= (choice - 4):
                            print(" ", "Could not swap", str(self.currentTeam[self.currentTeamActivePokemon].name),
                                  "with Pokemon", (choice - 4), "because that Pokemon is NULL")
                        else:
                            print(" ", "Could not swap", str(self.currentTeam[self.currentTeamActivePokemon].name),
                                  "with",
                                  str(self.currentTeam[choice - 4].name), "because: ")
                            # If the pokemon being swapped to has no HP
                            if self.currentTeam[choice - 4].hp <= 0:
                                print(" ", str(self.currentTeam[choice - 4].name), "has zero HP remaining")
                                # If the pokemon being swapped to is already the active pokemon
                            if self.currentTeamActivePokemon == choice - 4:
                                print(" ", str(self.currentTeam[choice - 4].name), "is the active pokemon already")
                    return False
            # If the choice is not one of the 10 valid battle commands, nothing happens
            else:
                if out:
                    print(" ", choice, "is not a valid Pokemon Battle command")
                return False
        # returns the battle winner
        else:
            if display:
                clone = self.template.copy()
                cv.putText(clone, "The battle is over!!! Team" + str(win) + " is victorious", (0, 290), fontScale=2.5,
                           thickness=4,
                           fontFace=cv.FONT_HERSHEY_PLAIN, color=(0, 0, 255))
                cv.imshow("display", clone)
                time.sleep(1)
                cv.waitKey(0)
            if out:
                print("The battle is over!!!\n  Team", win, "is victorious")
            return win

    # Returns winner if one exists
    def winner(self):
        # If either team has no remaining usable pokemon, returns the winning team
        currentTeamAllFainted = True
        otherTeamAllFainted = True
        for p in self.currentTeam:
            if p.hp > 0:
                currentTeamAllFainted = False
        for p in self.otherTeam:
            if p.hp > 0:
                otherTeamAllFainted = False
        # Current team is out of usable pokemon
        # Other team wins
        if currentTeamAllFainted:
            return 1
        # Other team is out of usable pokemon
        # Current team wins
        elif otherTeamAllFainted:
            return 2
        # There is no winner at the moment
        else:
            return -1
