from pokemonFunctions import *
from pokeDisplay import *
import random


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
                 SpecialEffect, UserHealthChange, TurnDelay, Id):
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
    # plus/ minus attack, defense, special, speed, accuracy, evasion
    statusModifier = [0, 0, 0, 0, 0, 0]
    statusEffects = []
    id = 0
    weight = 0
    firstEffectRound = []
    lastMoveHitBy = None

    # allows the creation of a pokemon object
    def __init__(self, Name, HP, EV, Moves, Type, Level, Id, Weight):
        self.name = Name
        self.maxHp = HP
        self.hp = HP
        self.maxHp = HP
        self.ev = EV
        self.moves = Moves
        self.type = Type
        self.level = Level
        self.statusModifier = [0, 0, 0, 0, 0, 0]
        self.statusEffects = []
        self.id = Id
        self.weight = Weight
        self.firstEffectRound = []
        self.lastMoveHitBy = PokemonMove(Name="default", Type=PokemonType.Error, Category=MoveCategory.Error, PP=9,
                                         Power=None, Accuracy=0,
                                         UserStatus=[0, 0, 0, 0], EnemyStatus=[0, 0, 0, 0],
                                         Effect=PokemonStatusEffect.Error, EffectChance=None,
                                         SpecialEffect=SpecialMoveEffect.Error, UserHealthChange=0, TurnDelay=0, Id=-1)

    # Prints the Pokemon and all of its Attributes
    def __str__(self):
        return ("Name:" + str(self.name) + "\nHP:" + str(self.hp) + "\nEV:" + str(self.ev) + "\nMoves:" + str(
            self.moves) + "\nType:" + str(self.type) + "\nLevel:" +
                str(self.level) + "\nStatus Modifier:" + str(self.statusModifier) + "\nStatus Effects:" + str(
                    self.statusEffects) + "\nID:" + str(self.id) + "\nWeight:" + str(self.weight))

    def getId(self):
        return self.id


class Battle:
    # Keeps track of turn
    turnNum = 0
    # Team 1
    Team1 = []
    Team1ActivePokemon = 0
    # Team 2
    Team2 = []
    Team2ActivePokemon = 0
    # Current Team
    currentTeam = []
    currentTeamActivePokemon = 0
    # Other team
    otherTeam = []
    otherTeamActivePokemon = 0

    def __init__(self, t1, t2):
        self.Team1, self.currentTeam = t1, t1
        self.Team2, self.otherTeam = t2, t2

    # Swaps the current team with the other team
    def swapTeam(self):
        # Stores team data temporarily
        tempTeam = self.currentTeam
        tempActive = self.currentTeamActivePokemon
        # Switches current team and with non-active team
        self.currentTeam = self.otherTeam
        self.currentTeamActivePokemon = self.otherTeamActivePokemon
        self.otherTeam = tempTeam
        self.otherTeamActivePokemon = tempActive

    # Processes a valid attack
    def attack(self, move, out=False):
        # Not fully implemented yet
        # Physical Moves
        # simulate status effects that occur before turn
        skipTurn = self.simulateStatusEffect(self.currentTeam[self.currentTeamActivePokemon], True)
        if skipTurn:
            # print(self.currentTeam[
            #           self.currentTeamActivePokemon].name + " cannot attack this round due to a status effect")
            return True

        # Uses the moves PP
        move.maxPP -= 1

        # Check to see if the move hits (Accuracy and Evasion)
        if move.accuracy is not None:
            hitChance = move.accuracy * statModifier[self.currentTeam[self.currentTeamActivePokemon].statusModifier[4]] / \
                        statModifier[self.otherTeam[self.otherTeamActivePokemon].statusModifier[5]] * 100
            if random.randint(0, 10000) > hitChance:
                print("The attack missed its target!")
                return True

        if move.category == MoveCategory.Physical:
            damage = calcDamage(
                self.currentTeam[self.currentTeamActivePokemon], self.otherTeam[self.otherTeamActivePokemon], move,
                True)[0]
            print("  The attack did", damage, "points of damage")
            self.otherTeam[self.otherTeamActivePokemon].hp -= damage
            self.otherTeam[self.otherTeamActivePokemon].lastMoveHitBy = move
            self.rollStatusEffect(self.otherTeam[self.otherTeamActivePokemon], move)
            if move.userHealthChange != 0:
                self.currentTeam[self.currentTeamActivePokemon].hp = 0
                self.swapTeam()
                displaySwap()
        # Special Moves
        elif move.category == MoveCategory.Special:
            damage = calcDamage(
                self.currentTeam[self.currentTeamActivePokemon], self.otherTeam[self.otherTeamActivePokemon], move,
                True)[0]
            print("  The attack did", damage, "points of damage")
            self.otherTeam[self.otherTeamActivePokemon].hp -= damage
            self.otherTeam[self.otherTeamActivePokemon].lastMoveHitBy = move
            self.rollStatusEffect(self.otherTeam[self.otherTeamActivePokemon], move)
        # Status Moves
        elif move.category == MoveCategory.Status:
            if move.specialEffect == 0:
                if move.effect not in self.otherTeam[self.otherTeamActivePokemon].statusEffects:
                    self.rollStatusEffect(self.otherTeam[self.otherTeamActivePokemon], move)
                else:
                    print(move.name + " fails as " + self.otherTeam[self.otherTeamActivePokemon].name + " is already" +
                          " affected by the status effect.")
            else:
                self.specialMove(move, self.currentTeam[self.currentTeamActivePokemon],
                                 self.otherTeam[self.otherTeamActivePokemon])

        # simulate status effects that occur after turn (poison)
        self.simulateStatusEffect(self.currentTeam[self.currentTeamActivePokemon], False)

        if self.otherTeam[self.otherTeamActivePokemon].hp <= 0:
            print(" ", self.otherTeam[self.otherTeamActivePokemon].name, "has fainted!")
        if self.currentTeam[self.currentTeamActivePokemon].hp <= 0:
            print(" ", self.currentTeam[self.currentTeamActivePokemon].name, "has fainted!")

        return True

    # Process a special move
    def specialMove(self, move, user, enemy):
        if move.specialEffect == SpecialMoveEffect.HealHalfMaxHP:
            heal = math.floor(user.maxHp / 2)
            if user.hp + heal > user.maxHp:
                user.hp = user.maxHp
                print(user.name + " has healed to full health!")
            else:
                user.hp += heal
                print(user.name + " has healed for " + str(heal) + " health!")
        elif move.specialEffect == SpecialMoveEffect.Rest:
            user.health = user.maxHp
            user.statusEffects.append(PokemonStatusEffect.Sleep)
            user.firstEffectRound.append(2)
            print(user.name + " has healed to full health!")
        else:
            raise Exception("Move " + move.name + " not yet implemented")

    def rollStatusEffect(self, pokemon, move):
        if move.effect != PokemonStatusEffect.Error:
            if move.type == PokemonType.Fire and PokemonType.Fire in pokemon.type:
                return
            elif move.effect == PokemonStatusEffect.Freeze and PokemonType.Ice in pokemon.type:
                return
            elif (move.effect == PokemonStatusEffect.Poison or move.effect == PokemonStatusEffect.BadlyPoisoned) and \
                    PokemonType.Poison in pokemon.type:
                return
            elif move.name == "body-slam" and PokemonType.Normal in pokemon.type:
                return
            elif move.effect in nonVolatileStatusEffects:
                for effect in pokemon.statusEffects:
                    if effect in nonVolatileStatusEffects:
                        print("The move fails as the pokemon is already affected by a non-volatile status effect")
                        return
            if move.effectChance is None:
                pokemon.statusEffects.append(move.effect)
                pokemon.firstEffectRound.append(0)
                print("Effect " + str(move.effect) + " has been applied to " + pokemon.name)
            else:
                rnum = random.randint(0, 100)
                print("rnum: " + str(rnum) + ", chance=" + str(move.effectChance))
                if rnum <= move.effectChance:
                    pokemon.statusEffects.append(move.effect)
                    pokemon.firstEffectRound.append(0)
                    print("Effect" + str(move.effect) + " has been applied to " + pokemon.name)

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
                    print(pokemon.name + " thaws out!")
                    return False
                print(pokemon.name + " is frozen solid!")
                return True
            elif effect == PokemonStatusEffect.Paralysis and before:
                # speed reduced 75%
                if firstRound == 0:
                    pokemon.ev[3] *= 0.25
                    print(pokemon.name + "'s speed is reduced to " + str(pokemon.ev[3]) + " because of paralysis.")
                    pokemon.firstEffectRound[i] += 1
                rand = random.randint(0, 100)
                if rand <= 25:
                    print(pokemon.name + " is paralyzed and unable to move!")
                    return True
                return False
            elif effect == PokemonStatusEffect.Poison and not before:
                decrease = math.floor(pokemon.maxHp / 16.0)
                if decrease < 1:
                    decrease = 1
                pokemon.hp -= decrease
                print(pokemon.name + " loses " + str(decrease) + " health to poison.")
                return False
            elif effect == PokemonStatusEffect.BadlyPoisoned and not before:
                decrease = math.floor(pokemon.maxHp / 16.0 + pokemon.maxHp * firstRound / 16.0)
                if decrease < 1:
                    decrease = 1
                pokemon.hp -= decrease
                print(pokemon.name + "loses" + str(decrease) + "health to bad poison.")
                pokemon.firstEffectRound[i] += 1
                return False
            elif effect == PokemonStatusEffect.Sleep and before:
                # intial round when rolling
                if firstRound == 0:
                    pokemon.firstEffectRound[i] = random.randint(1, 7)
                    print(pokemon.name + " is fast asleep")
                    return True
                # last round when 1
                elif firstRound == 1:
                    del pokemon.firstEffectRound[i]
                    del pokemon.statusEffects[i]
                    print(pokemon.name + " awakens!")
                    return False
                else:
                    pokemon.firstEffectRound[i] -= 1
                    print(pokemon.name + " is fast asleep")
                    return True
            elif effect == PokemonStatusEffect.Confusion and before:
                if firstRound == 0:
                    pokemon.firstEffectRound[i] = random.randint(2, 5)
                    print("Confusion on " + pokemon.name + " for " + str(pokemon.firstEffectRound[i]) + " rounds")
                elif firstRound == 1:
                    del pokemon.firstEffectRound[i]
                    del pokemon.statusEffects[i]
                    print(pokemon.name + " has snapped out of confusion!")
                    return False
                else:
                    r = random.randint(1, 2)
                    if r == 1:
                        c = PokemonMove(Name="Confusion", Type=PokemonType.Confusion, Category=MoveCategory.Physical,
                                        PP=100, Power=40,
                                        Accuracy=100, UserStatus=[0, 0, 0, 0], EnemyStatus=[0, 0, 0, 0],
                                        Effect=PokemonStatusEffect.Error, EffectChance=None,
                                        SpecialEffect=None, UserHealthChange=None, TurnDelay=None, Id=999)
                        dmg = calcDamage(pokemon, pokemon, c, False, False)[0]
                        pokemon.hp -= dmg
                        print(pokemon.name + " hurt itself in confusion for " + str(dmg) + " damage!")
                        pokemon.firstEffectRound[i] -= 1
                        return True
                    pokemon.firstEffectRound[i] -= 1
                    return False
            elif effect == PokemonStatusEffect.Burn:
                decrease = math.floor(pokemon.maxHp / 16.0)
                if before and pokemon.hp - decrease <= 0:
                    pokemon.hp -= decrease
                    print(pokemon.name + " loses " + str(decrease) + " health to burn.")
                    print("It is applied before the pokemon's turn when it is lethal.")
                    self.swapTeam()
                    displaySwap()
                    return True
                elif not before:
                    if decrease < 1:
                        decrease = 1
                    pokemon.hp -= decrease
                    print(pokemon.name + " loses " + str(decrease) + " health to burn.")
                    return False
            elif effect == PokemonStatusEffect.Bound and before:
                placeholder = True
                # not yet implemented

    def round(self, choiceTeam1, choiceTeam2, out=False, display=False):
        win = self.winner()

        if self.turnNum == 0:
            self.turnNum += 1
            displayNextRound(self.turnNum)

        if win == -1:
            self.currentTeam = self.Team1
            self.currentTeamActivePokemon = self.Team1ActivePokemon
            self.otherTeam = self.Team2
            self.otherTeamActivePokemon = self.Team2ActivePokemon

            # If a pokemon is currently fainted and must be swapped before the round can continue
            if self.currentTeam[self.currentTeamActivePokemon].hp <= 0:
                self.turn(choiceTeam1, out, display)
                self.Team1 = self.currentTeam
                self.Team1ActivePokemon = self.currentTeamActivePokemon
                return True

            if self.otherTeam[self.otherTeamActivePokemon].hp <= 0:
                self.swapTeam()
                self.turn(choiceTeam2, out, display)
                self.swapTeam()
                self.Team2 = self.otherTeam
                self.Team2ActivePokemon = self.otherTeamActivePokemon
                return True

            # Determines turn order and allows each team to take their turn
            team1Speed = calcStatRBYFromDV("speed", self.Team1[self.Team1ActivePokemon].ev[3],
                                           self.Team1[self.Team1ActivePokemon].level) * statModifier[
                             self.Team1[self.Team1ActivePokemon].statusModifier[3]]
            team2Speed = calcStatRBYFromDV("speed", self.Team2[
                self.Team2ActivePokemon].ev[3], self.Team2[self.Team2ActivePokemon].level) * statModifier[
                             self.Team2[self.Team2ActivePokemon].statusModifier[3]]

            # Ensures that the swap happens before the attack
            if choiceTeam1 >= 4:
                team1Speed = 9999
            if choiceTeam2 >= 4:
                team2Speed = 9999

            if team1Speed > team2Speed:
                # Team 1 goes first
                if self.turn(choiceTeam1, out, display):
                    self.swapTeam()
                    displaySwap()
                    self.turn(choiceTeam2, out, display)
                else:
                    return False
                self.swapTeam()

            elif team1Speed < team2Speed:
                # team 2 goes first
                self.swapTeam()
                if self.turn(choiceTeam2, out, display):
                    self.swapTeam()
                    displaySwap()
                    self.turn(choiceTeam1, out, display)
                else:
                    return False
            else:
                # team that goes first is random
                if random.randint(0, 1) == 1:
                    # Team 1 is first
                    if self.turn(choiceTeam1, out, display):
                        self.swapTeam()
                        displaySwap()
                        self.turn(choiceTeam2, out, display)
                    else:
                        return False
                    self.swapTeam()
                else:
                    # Team two is first
                    self.swapTeam()
                    if self.turn(choiceTeam2, out, display):
                        self.swapTeam()
                        displaySwap()
                        self.turn(choiceTeam1, out, display)
                    else:
                        return False

            self.Team1 = self.currentTeam
            self.Team1ActivePokemon = self.currentTeamActivePokemon
            self.Team2 = self.otherTeam
            self.Team2ActivePokemon = self.otherTeamActivePokemon

            self.turnNum += 1
            displayNextRound(self.turnNum)
            return True
        else:
            if display:
                displayWinner(win)
            if out:
                print("The battle is over! Team", win, "is victorious!")
            return win

    # Process a single turn of battle using the current active team and a valid move/swap choice
    # Choices 0 through 9 represent all possible choices the NN can make
    # Out results in a verbose output of the turn
    def turn(self, choice, out=False, display=False):
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
                    showBattle(self.currentTeam, self.currentTeamActivePokemon, self.otherTeam,
                               self.otherTeamActivePokemon, choice)
                if out:
                    print(" ", str(self.currentTeam[self.currentTeamActivePokemon].name), "used the move",
                          str(self.currentTeam[self.currentTeamActivePokemon].moves[choice].name), "on opponent's",
                          str(self.otherTeam[self.otherTeamActivePokemon].name))
                # attacks the opponent using the desired move
                self.attack(self.currentTeam[self.currentTeamActivePokemon].moves[choice])
                if display:
                    showBattle(self.currentTeam, self.currentTeamActivePokemon, self.otherTeam,
                               self.otherTeamActivePokemon, choice)
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
                    showBattle(self.currentTeam, self.currentTeamActivePokemon, self.otherTeam,
                               self.otherTeamActivePokemon, choice)
                if out:
                    print(" ", str(self.currentTeam[self.currentTeamActivePokemon].name), "was swapped out\n ",
                          str(self.currentTeam[choice - 4].name), "was swapped in")
                self.currentTeamActivePokemon = choice - 4
                return True
            else:
                # Verbose output for when swap does not work properly
                if out:
                    # If the pokemon being swapped to does not exist
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
            raise Exception(" ", choice, "is not a valid Pokemon Battle command")
            return False

    # Returns winner if one exists
    def winner(self):
        # If either team has no remaining usable pokemon, returns the winning team
        Team1AllFainted = True
        Team2AllFainted = True
        for p in self.Team1:
            if p.hp > 0:
                Team1AllFainted = False
        for p in self.Team2:
            if p.hp > 0:
                Team2AllFainted = False
        # Current team is out of usable pokemon
        # Other team wins
        if Team2AllFainted:
            return 1
        # Other team is out of usable pokemon
        # Current team wins
        elif Team1AllFainted:
            return 2
        # There is no winner at the moment
        else:
            return -1
