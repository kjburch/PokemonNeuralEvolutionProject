from pokemonEnums import *
from pokemonFunctions import *


# Pokemon move class, meant to represent 1 pokemon move and all its effects / attributes
class PokemonMove:
    name = ""
    type = PokemonType.Error
    category = MoveCategory.Error
    maxPP = 0
    power = 0
    accuracy = 0
    # plus/ minus Attack, Defense, Special, Speed
    # for a move that causes changes in the poke stat
    status = [0, 0, 0, 0]
    effect = PokemonStatusEffect.Error
    effectChance = 0
    id = 0

    # allows the creation of a pokemon move object
    def __init__(self, Name, Type, Category, PP, Power, Accuracy, Status, Effect, EffectChance, Id) -> object:
        self.name = Name
        self.type = Type
        self.category = Category
        self.maxPP = PP
        self.power = Power
        self.accuracy = Accuracy
        self.status = Status
        self.effect = Effect
        self.effectChance = EffectChance
        self.id = Id

    def getEffect(self):
        return self.effect

    def __str__(self):
        return ("Name:"+str(self.name)+"\nType:"+str(self.type)+"\nCategory:"+str(
            self.category)+"\nPP:"+str(self.maxPP)+"\nPower:"+str(self.power)+"\nAccuracy:"+str(self.accuracy)
                +"\nStatus:"+str(self.status)+"\nEffect:"+str(self.effect)+"\nEffect Chance:"+str(self.effectChance)
                +"\nID:"+str(self.id))


# Pokemon Class, meant to represent a single pokemon, not a single pokemon species
class Pokemon:
    name = ""
    hp = 0
    # ev order: attack, defense, special attack, special defense, speed
    ev = []
    moves = []
    type = []
    level = 0
    # plus/ minus attack, defense, special, speed
    statusModifier = [0, 0, 0, 0]
    statusEffects = []
    id = 0

    # allows the creation of a pokemon object
    def __init__(self, Name, HP, EV, Moves, Type, Level, Id) -> object:
        self.name = Name
        self.hp = HP
        self.ev = EV
        self.moves = Moves
        self.type = Type
        self.level = Level
        self.statusModifier = [0, 0, 0, 0]
        self.statusEffects = []
        self.id = Id

    # Prints the Pokemon and all of its Attributes
    def __str__(self):
        return ("Name:"+str(self.name)+"\nHP:"+str(self.hp)+"\nEV:"+str(self.ev)+"\nMoves:"+str(
            self.moves)+"\nType:"+str(self.type)+"\nLevel:"+
                str(self.level)+"\nStatus Effects:"+str(self.statusEffects)+"\nID:"+str(self.id))

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

    def attack(self, move):
        # Not fully implemented yet
        # Physical
        if move.category == MoveCategory.Physical:
            damage = calcDamage(
                self.currentTeam[self.currentTeamActivePokemon], self.otherTeam[self.otherTeamActivePokemon], move,
                True)[0]
            print("  The attack did", damage, "points of damage")
            self.otherTeam[self.otherTeamActivePokemon].hp -= damage
        # Special
        elif move.category == MoveCategory.Special:
            damage = calcDamage(
                self.currentTeam[self.currentTeamActivePokemon], self.otherTeam[self.otherTeamActivePokemon], move,
                True)[0]
            print("  The attack did", damage, "points of damage")
            self.otherTeam[self.otherTeamActivePokemon].hp -= damage
        # Status
        elif move.category == MoveCategory.Status:
            print("  Not implemented")

        if self.otherTeam[self.otherTeamActivePokemon].hp <= 0:
            print(" ", self.otherTeam[self.otherTeamActivePokemon].name, "has fainted!")
        if self.currentTeam[self.currentTeamActivePokemon].hp <= 0:
            print(" ", self.currentTeam[self.currentTeamActivePokemon].name, "has fainted!")

        return True

    # Options 0 through 8 represent all possible choices the NN can make
    # Out results in a verbose output of the turn
    def turn(self, choice, out):
        win = self.winner()
        if win == -1:
            if out:
                print("\nTurn Number", self.turnNum, ":")
            # Current Pokemon uses a move and tries to attack
            if choice < 4:
                # Ensures current pokemon is not fainted and chosen move has PP
                if len(self.currentTeam[self.currentTeamActivePokemon].moves) > choice and \
                        self.currentTeam[self.currentTeamActivePokemon].moves[choice].maxPP > 0 and self.currentTeam[
                        self.currentTeamActivePokemon].hp > 0:
                    if out:
                        print(" ", str(self.currentTeam[self.currentTeamActivePokemon].name), "used the move",
                              str(self.currentTeam[self.currentTeamActivePokemon].moves[choice].name), "on opponent's",
                              str(self.otherTeam[self.otherTeamActivePokemon].name))
                    self.attack(self.currentTeam[self.currentTeamActivePokemon].moves[choice])
                    self.swapTeam()
                    return True
                else:
                    if out:
                        if len(self.currentTeam[self.currentTeamActivePokemon].moves) <= choice:
                            print(" ", str(self.currentTeam[self.currentTeamActivePokemon].name),
                                  "could not use move", choice, "because that Move is NULL")
                        else:
                            print(" ", str(self.currentTeam[self.currentTeamActivePokemon].name),
                                  "could not use the move",
                                  str(self.currentTeam[self.currentTeamActivePokemon].moves[choice].name), "because:")
                            if self.currentTeam[self.currentTeamActivePokemon].moves[choice].maxPP <= 0:
                                print(" ", str(self.currentTeam[self.currentTeamActivePokemon].moves[choice].name),
                                      "has no PP remaining.")
                            if self.currentTeam[self.currentTeamActivePokemon].hp <= 0:
                                print(" ", str(self.currentTeam[self.currentTeamActivePokemon].name),
                                      "has no health remaining.")
                    return False
            # Switch to a different pokemon on the team if it has health
            elif 4 <= choice <= 9:
                if len(self.currentTeam) > (choice-4) and self.currentTeam[
                        choice-4].hp > 0 and self.currentTeamActivePokemon is not (choice-4):
                    if out:
                        print(" ", str(self.currentTeam[self.currentTeamActivePokemon].name), "was swapped out\n ",
                              str(self.currentTeam[choice-4].name), "was swapped in")
                    self.currentTeamActivePokemon = choice-4
                    self.swapTeam()
                    return True
                else:
                    if out:
                        if len(self.currentTeam) <= (choice-4):
                            print(" ", "Could not swap", str(self.currentTeam[self.currentTeamActivePokemon].name),
                                  "with Pokemon", (choice-4), "because that Pokemon is NULL")
                        else:
                            print(" ", "Could not swap", str(self.currentTeam[self.currentTeamActivePokemon].name),
                                  "with",
                                  str(self.currentTeam[choice-4].name), "because: ")
                            if self.currentTeam[choice-4].hp <= 0:
                                print(" ", str(self.currentTeam[choice-4].name), "has zero HP remaining")
                            if self.currentTeamActivePokemon == choice-4:
                                print(" ", str(self.currentTeam[choice-4].name), "is the active pokemon already")
                    return False
            else:
                if out:
                    print(" ", choice, "is not a valid Pokemon Battle command")
                return False
        else:
            print("The battle is over!!!\n  Team", win, "is victorious")
            return win

    # Returns winner if one exists
    def winner(self):
        one = True
        two = True
        for p in self.currentTeam:
            if p.hp > 0:
                one = False
        for p in self.otherTeam:
            if p.hp > 0:
                two = False
        if one:
            return 1
        elif two:
            return 2
        else:
            return -1
