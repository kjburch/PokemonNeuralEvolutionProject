from pokemonEnums import *
from pokemonFunctions import *
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
        return ("Name:"+str(self.name)+"\nType: "+str(self.type)+"\nCategory: "+str(
            self.category)+"\nPP: "+str(self.maxPP)+"\nPower: "+str(self.power)+"\nAccuracy: "+str(self.accuracy)
                +"\nUser Status: "+str(self.userStatus)+"\nEnemy Status: "+str(self.enemyStatus)+"\nEffect: "+str(
                    self.effect)+"\nEffect Chance: "+str(self.effectChance)
                +"\nSpecial Effect: "+str(self.specialEffect)+"\nUser Health Change: "+str(
                    self.userHealthChange)+"\nTurn Delay: "+str(self.turnDelay)
                +"\nID: "+str(self.id))


# Pokemon Class, meant to represent a single pokemon, not a single pokemon species
class Pokemon:
    name = ""
    hp = 0
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

    # allows the creation of a pokemon object
    def __init__(self, Name, HP, EV, Moves, Type, Level, Id, Weight) -> object:
        self.name = Name
        self.hp = HP
        self.ev = EV
        self.moves = Moves
        self.type = Type
        self.level = Level
        self.statusModifier = [0, 0, 0, 0, 0]
        self.statusEffects = []
        self.id = Id
        self.weight = Weight

    # Prints the Pokemon and all of its Attributes
    def __str__(self):
        return ("Name:"+str(self.name)+"\nHP:"+str(self.hp)+"\nEV:"+str(self.ev)+"\nMoves:"+str(
            self.moves)+"\nType:"+str(self.type)+"\nLevel:"+
                str(self.level)+"\nStatus Modifier:"+str(self.statusModifier)+"\nStatus Effects:"+str(
                    self.statusEffects)+"\nID:"+str(self.id)+"\nWeight:"+str(self.weight))

    def getId(self):
        return self.id


class Battle:
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

    # Processes a valid attack
    def attack(self, move):
        # Not fully implemented yet
        # Physical Moves
        print(move.category)
        if move.category == MoveCategory.Physical:
            damage = calcDamage(
                self.currentTeam[self.currentTeamActivePokemon], self.otherTeam[self.otherTeamActivePokemon], move,
                True)[0]
            print("  The attack did", damage, "points of damage")
            self.otherTeam[self.otherTeamActivePokemon].hp -= damage
        # Special Moves
        elif move.category == MoveCategory.Special:
            damage = calcDamage(
                self.currentTeam[self.currentTeamActivePokemon], self.otherTeam[self.otherTeamActivePokemon], move,
                True)[0]
            print("  The attack did", damage, "points of damage")
            self.otherTeam[self.otherTeamActivePokemon].hp -= damage
        # Status Moves
        elif move.category == MoveCategory.Status:
            if move.specialEffect == 0:
                for i in range(0, 5):
                    self.currentTeam[self.currentTeamActivePokemon].statusModifier[i] += move.userStatus[i]
                    self.otherTeam[self.otherTeamActivePokemon].statusModifier[i] += move.enemyStatus[i]
                    if move.effectChance is None and move.effect != 1:
                        self.otherTeam[self.otherTeamActivePokemon].statusEffects.append(move.effect)
                    else:
                        rnum = random.randint(0, 100)
                        if rnum <= move.effectChance:
                            self.otherTeam[self.otherTeamActivePokemon].statusEffects.append(move.effect)
            else:
                self.specialMove(self, move)

        if self.otherTeam[self.otherTeamActivePokemon].hp <= 0:
            print(" ", self.otherTeam[self.otherTeamActivePokemon].name, "has fainted!")
        if self.currentTeam[self.currentTeamActivePokemon].hp <= 0:
            print(" ", self.currentTeam[self.currentTeamActivePokemon].name, "has fainted!")

        return True

    # Process a special move
    def specialMove(self, move):
        print("Special move effects not yet implemented")

    # Process a single turn of battle using the current active team and a valid move/swap choice
    # Choices 0 through 9 represent all possible choices the NN can make
    # Out results in a verbose output of the turn
    def turn(self, choice, out):
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
                    if out:
                        print(" ", str(self.currentTeam[self.currentTeamActivePokemon].name), "used the move",
                              str(self.currentTeam[self.currentTeamActivePokemon].moves[choice].name), "on opponent's",
                              str(self.otherTeam[self.otherTeamActivePokemon].name))
                    # attacks the opponent using the desired move
                    self.attack(self.currentTeam[self.currentTeamActivePokemon].moves[choice])
                    # swap active team after a successful move execution
                    self.swapTeam()
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
                if len(self.currentTeam) > (choice-4) and self.currentTeam[
                    choice-4].hp > 0 and self.currentTeamActivePokemon is not (choice-4):
                    # Verbose output for when the swap is successful
                    if out:
                        print(" ", str(self.currentTeam[self.currentTeamActivePokemon].name), "was swapped out\n ",
                              str(self.currentTeam[choice-4].name), "was swapped in")
                    self.currentTeamActivePokemon = choice-4
                    # Swaps team when choice is successfully executed
                    self.swapTeam()
                    return True
                else:
                    # Verbose output for when swap does not work properly
                    if out:
                        # If the pokemon being swapped to does nto exist
                        if len(self.currentTeam) <= (choice-4):
                            print(" ", "Could not swap", str(self.currentTeam[self.currentTeamActivePokemon].name),
                                  "with Pokemon", (choice-4), "because that Pokemon is NULL")
                        else:
                            print(" ", "Could not swap", str(self.currentTeam[self.currentTeamActivePokemon].name),
                                  "with",
                                  str(self.currentTeam[choice-4].name), "because: ")
                            # If the pokemon being swapped to has no HP
                            if self.currentTeam[choice-4].hp <= 0:
                                print(" ", str(self.currentTeam[choice-4].name), "has zero HP remaining")
                                # If the pokemon being swapped to is already the active pokemon
                            if self.currentTeamActivePokemon == choice-4:
                                print(" ", str(self.currentTeam[choice-4].name), "is the active pokemon already")
                    return False
            # If the choice is not one of the 10 valid battle commands, nothing happens
            else:
                if out:
                    print(" ", choice, "is not a valid Pokemon Battle command")
                return False
        # returns the battle winner
        else:
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
