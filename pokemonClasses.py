from pokemonEnums import *


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
    def __init__(self, Name, Type, Category, PP, Power, Accuracy, UserStatus, EnemyStatus, Effect, EffectChance, SpecialEffect, UserHealthChange, TurnDelay, Id) -> object:
        self.name = Name
        self.type = Type
        self.category = Category
        self.maxPP = PP
        self.power = Power
        self.accuracy = Accuracy
        self.userStatusstatus = UserStatus
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
            self.category) + "\nPP: " + str(self.maxPP) + "\nPower: " + str(self.power) + "\nAccuracy: " + str(self.accuracy)
            + "\nUser Status: " + str(self.userStatusstatus) + "\nEnemy Status: " + str(self.enemyStatus) + "\nEffect: " + str(self.effect) + "\nEffect Chance: " + str(self.effectChance)
            + "\nSpecial Effect: " + str(self.specialEffect) + "\nUser Health Change: " + str(self.userHealthChange) + "\nTurn Delay: " + str(self.turnDelay)
            + "\nID: " + str(self.id))


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
    weight = 0

    # allows the creation of a pokemon object
    def __init__(self, Name, HP, EV, Moves, Type, Level, Id, Weight) -> object:
        self.name = Name
        self.hp = HP
        self.ev = EV
        self.moves = Moves
        self.type = Type
        self.level = Level
        self.statusModifier = [0, 0, 0, 0]
        self.statusEffects = []
        self.id = Id
        self.weight = Weight

    # Prints the Pokemon and all of its Attributes
    def __str__(self):
        return ("Name:" + str(self.name) + "\nHP:" + str(self.hp) + "\nEV:" + str(self.ev) + "\nMoves:" + str(self.moves) + "\nType:" + str(self.type) + "\nLevel:" +
                str(self.level) + "\nStatus Effects:" + str(self.statusEffects) + "\nID:" + str(self.id) + "\nWeight:" + str(self.weight))

    def getId(self):
        return self.id

class Battle:
    # List of each team's pokemon
    team1 = []
    team2 = []
    # Each team's active pokemon
    team1ActivePokemon = 0
    team2ActivePokemon = 0
    # Current Team
    currentTeam = []
    currentTeamActivePokemon = 0
    team = True

    def __init__(self, t1, t2):
        self.team1 = t1
        self.team2 = t2
        self.currentTeam = self.team1

    def swapTeam(self):
        if self.team:
            self.team = False
            self.team1 = self.currentTeam
            self.team1ActivePokemon = self.currentTeamActivePokemon
            self.currentTeamActivePokemon = self.team2ActivePokemon
            self.currentTeam = self.team2
        else:
            self.team = True
            self.team2 = self.currentTeam
            self.team2ActivePokemon = self.currentTeamActivePokemon
            self.currentTeamActivePokemon = self.team1ActivePokemon
            self.currentTeam = self.team1

    def attack(self, move):
        # Physical
        # Special
        # Status
        return True

    # Options 0 through 8 represent all possible choices the NN can make
    def turn(self, choice):
        # Current Pokemon uses a move and tries to attack
        if choice < 4:
            # Ensures current pokemon is not fainted and chosen move has PP
            if self.currentTeam[self.currentTeamActivePokemon].moves[choice].maxPP > 0 and self.currentTeam[
                    self.currentTeamActivePokemon].hp > 0:
                self.attack(self.currentTeam[self.currentTeamActivePokemon].moves[choice])
                self.swapTeam()
                return True
            else:
                return False
        # Switch to a different pokemon on the team if it has health
        elif 5 <= choice < 10:
            if self.currentTeam[choice-5].hp > 0 and self.currentTeamActivePokemon is not (choice-5):
                self.currentTeamActivePokemon = choice-4
                self.swapTeam()
                return True
            else:
                return False
        else:
            return False

    # Returns winner if one exists
    def winner(self):
        one = True
        two = True
        for p in self.team1:
            if p.hp > 0:
                one = False
        for p in self.team2:
            if p.hp > 0:
                two = False
        if one:
            return 1
        if two:
            return 2
        else:
            return -1