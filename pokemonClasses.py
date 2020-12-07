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
        return ("Name:"+str(self.name)+"\nType: "+str(self.type)+"\nCategory: "+str(
            self.category)+"\nPP: "+str(self.maxPP)+"\nPower: "+str(self.power)+"\nAccuracy: "+str(
            self.accuracy)
                +"\nUser Status: "+str(self.userStatus)+"\nEnemy Status: "+str(
                    self.enemyStatus)+"\nEffect: "+str(
                    self.effect)+"\nEffect Chance: "+str(self.effectChance)
                +"\nSpecial Effect: "+str(self.specialEffect)+"\nUser Health Change: "+str(
                    self.userHealthChange)+"\nTurn Delay: "+str(self.turnDelay)
                +"\nID: "+str(self.id))


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
    seen = False

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
        return ("Name:"+str(self.name)+"\nHP:"+str(self.hp)+"\nEV:"+str(self.ev)+"\nMoves:"+str(
            self.moves)+"\nType:"+str(self.type)+"\nLevel:"+
                str(self.level)+"\nStatus Modifier:"+str(self.statusModifier)+"\nStatus Effects:"+str(
                    self.statusEffects)+"\nID:"+str(self.id)+"\nWeight:"+str(self.weight))

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
    currentTeamFitness = 0
    # Other team
    otherTeam = []
    otherTeamActivePokemon = 0
    otherTeamFitness = 0
    # used for Flinch
    firstTurn = True
    output = False
    # Tracks team fitness ove the battle
    Team1Fitness = 0
    Team2Fitness = 0

    def __init__(self, t1, t2, Out=False):
        self.Team1, self.currentTeam = t1, t1
        self.Team2, self.otherTeam = t2, t2
        self.output = Out
        self.Team2[0].seen = True
        self.Team1[0].seen = True
        if self.output:
            print("Enemy Team:")
            for pk in self.Team1:
                print(pk.name)
            print("-------------------")
            print("Your team:")
            for pk in self.Team2:
                print(pk.name)
            print("Enemy active pokemon: "+self.Team1[self.Team1ActivePokemon].name)
            print("Your active pokemon: "+self.Team2[self.Team2ActivePokemon].name)
            print("Your moves: ", end="")
            for mv in self.Team2[self.Team2ActivePokemon].moves:
                print(mv.name, end=", ")
            print()

    # Swaps the current team with the other team
    def swapTeam(self):
        # Stores team data temporarily
        tempTeam = self.currentTeam
        tempActive = self.currentTeamActivePokemon
        tempFitness = self.currentTeamFitness
        # Switches current team and with non-active team
        self.currentTeam = self.otherTeam
        self.currentTeamActivePokemon = self.otherTeamActivePokemon
        self.currentTeamFitness = self.otherTeamFitness
        self.otherTeam = tempTeam
        self.otherTeamActivePokemon = tempActive
        self.otherTeamFitness = tempFitness

    # Processes a valid attack
    def attack(self, move, out, display, team):
        # Not fully implemented yet
        # Physical Moves
        # simulate status effects that occur before turn
        skipTurn = self.simulateStatusEffect(self.currentTeam[self.currentTeamActivePokemon], True, out, display, team)
        if skipTurn:
            return True

        # Uses the moves PP
        if move.name != "struggle" and PokemonStatusEffect.Recharging not in self.currentTeam[
            self.currentTeamActivePokemon].statusEffects:
            move.maxPP -= 1

        # Check to see if any of user's moves have PP
        # If not replace moves with struggle
        allZero = True
        for mv in self.currentTeam[self.currentTeamActivePokemon].moves:
            if mv.maxPP > 0:
                allZero = False
                break
        if allZero:
            struggle = PokemonMove(Name="struggle", Type=PokemonType.Normal, Category=MoveCategory.Status, PP=100,
                                   Power=50, Accuracy=100,
                                   UserStatus=[0, 0, 0, 0], EnemyStatus=[0, 0, 0, 0], Effect=PokemonStatusEffect.Error,
                                   EffectChance=None,
                                   SpecialEffect=SpecialMoveEffect.Struggle, UserHealthChange=0, TurnDelay=0, Id=-1)
            self.currentTeam[self.currentTeamActivePokemon].moves = [struggle] * 4

        # Check to see if the move hits (Accuracy and Evasion)
        if move.accuracy is not None:
            hitChance = move.accuracy * statModifier[
                self.currentTeam[self.currentTeamActivePokemon].statusModifier[4]] / \
                        statModifier[self.otherTeam[self.otherTeamActivePokemon].statusModifier[5]] * 100
            if random.randint(0, 10000) > hitChance:
                if out:
                    print(self.currentTeam[self.currentTeamActivePokemon].name+" misses.")
                if display:
                    showBattle(self.currentTeam, self.currentTeamActivePokemon, self.otherTeam,
                               self.otherTeamActivePokemon, "The attack missed!", team,
                               self.turnNum)
                return True

        if move.category == MoveCategory.Physical:
            temp = calcDamage(
                self.currentTeam[self.currentTeamActivePokemon], self.otherTeam[self.otherTeamActivePokemon], move,
                True)
            damage = temp[0]
            # Adds on fitness
            self.currentTeamFitness += temp[2]
            # Everything else
            self.otherTeam[self.otherTeamActivePokemon].hp -= damage
            if display:
                showBattle(self.currentTeam, self.currentTeamActivePokemon, self.otherTeam,
                           self.otherTeamActivePokemon, "The attack did " + str(damage) + " points of damage", team,
                           self.turnNum)
            self.otherTeam[self.otherTeamActivePokemon].lastMoveHitBy = move
            self.rollStatusEffect(self.otherTeam[self.otherTeamActivePokemon], move, out, display, team)
            if move.userHealthChange == -1:
                # Punish for using explosion while at max hp
                if self.currentTeam[self.currentTeamActivePokemon].hp == self.currentTeam[
                    self.currentTeamActivePokemon].maxHp:
                    self.currentTeamFitness -= 3
                # explosion
                self.currentTeam[self.currentTeamActivePokemon].hp = 0
        # Special Moves
        elif move.category == MoveCategory.Special:
            temp = calcDamage(
                self.currentTeam[self.currentTeamActivePokemon], self.otherTeam[self.otherTeamActivePokemon], move,
                True)
            damage = temp[0]
            # Adds on fitness
            self.currentTeamFitness += temp[2]
            # Everything else
            self.otherTeam[self.otherTeamActivePokemon].hp -= damage
            if display:
                showBattle(self.currentTeam, self.currentTeamActivePokemon, self.otherTeam,
                           self.otherTeamActivePokemon, "The attack did "+str(damage)+" points of damage", team,
                           self.turnNum)
            self.otherTeam[self.otherTeamActivePokemon].lastMoveHitBy = move
            self.rollStatusEffect(self.otherTeam[self.otherTeamActivePokemon], move, out, display, team)
        # Status Moves
        elif move.category == MoveCategory.Status:
            if move.specialEffect == 0:
                if move.effect not in self.otherTeam[self.otherTeamActivePokemon].statusEffects:
                    # Increase fitness for causing status effect
                    self.currentTeamFitness += 1
                    # roll status
                    self.rollStatusEffect(self.otherTeam[self.otherTeamActivePokemon], move, out , display, team)
                else:
                    # Punishes for attempting to status affect when one already exists
                    self.currentTeamFitness -= 1
                    o = str(move.name)+" fails as "+str(self.otherTeam[self.otherTeamActivePokemon].name)+" is already affected by the status effect."
                    if out:
                        print(0)
                    if display:
                        showBattle(self.currentTeam, self.currentTeamActivePokemon, self.otherTeam,
                                   self.otherTeamActivePokemon, o, team,
                                   self.turnNum)

            else:
                self.specialMove(move, self.currentTeam[self.currentTeamActivePokemon],
                                 self.otherTeam[self.otherTeamActivePokemon], out, display, team)

        # simulate status effects that occur after turn (poison, burn)
        self.simulateStatusEffect(self.currentTeam[self.currentTeamActivePokemon], False, out, display, team)

        if display:
            if self.otherTeam[self.otherTeamActivePokemon].hp <= 0:
                showBattle(self.currentTeam, self.currentTeamActivePokemon, self.otherTeam,
                           self.otherTeamActivePokemon, str(self.otherTeam[self.otherTeamActivePokemon].name)+ " has fainted!", team,
                           self.turnNum)
            if self.currentTeam[self.currentTeamActivePokemon].hp <= 0:
                showBattle(self.currentTeam, self.currentTeamActivePokemon, self.otherTeam,
                           self.otherTeamActivePokemon, str(self.currentTeam[self.currentTeamActivePokemon].name)+ " has fainted!", team,
                           self.turnNum)
        if out:
            if self.otherTeam[self.otherTeamActivePokemon].hp <= 0:
                print(" ", self.otherTeam[self.otherTeamActivePokemon].name, "has fainted!")
            if self.currentTeam[self.currentTeamActivePokemon].hp <= 0:
                print(" ", self.currentTeam[self.currentTeamActivePokemon].name, "has fainted!")

        return True

    # Process a special move
    def specialMove(self, move, user, enemy, out, display, team):
        if move.specialEffect == SpecialMoveEffect.HealHalfMaxHP:
            # punish for healing when health is full
            # reward for healing when health is below half
            if user.hp > user.maxHp / 1.5:
                self.currentTeamFitness -= 2
            else:
                self.currentTeamFitness += 2
            # process move
            heal = math.floor(user.maxHp / 2)
            if user.hp+heal > user.maxHp:
                user.hp = user.maxHp
                o = str(user.name)+" has healed to full health!"
            else:
                user.hp += heal
                o = str(user.name)+" has healed for "+str(heal)+" health!"
            if out:
                print(o)
            if display:
                showBattle(self.currentTeam, self.currentTeamActivePokemon, self.otherTeam,
                           self.otherTeamActivePokemon, "Team "+str(team)+"'s "+o, team,
                           self.turnNum)
        elif move.specialEffect == SpecialMoveEffect.Rest:
            # punish for healing when health is full
            # reward for healing when health is below half
            if user.hp > user.maxHp / 2:
                self.currentTeamFitness -= 3
            else:
                self.currentTeamFitness += 2
            if user.hp == user.maxHp:
                o = str(user.name)+" is already at full health and therefore " + str(move.name) + " fails!"
                if out:
                    print(o)
                if display:
                    showBattle(self.currentTeam, self.currentTeamActivePokemon, self.otherTeam,
                               self.otherTeamActivePokemon, "Team "+str(team)+"'s "+o, team,
                               self.turnNum)
                return
            user.hp = user.maxHp
            if len(user.statusEffects) > 0:
                for i in range(0, len(user.statusEffects)):
                    effect = user.statusEffects[i]
                    if effect in nonVolatileStatusEffects:
                        del user.statusEffects[i]
                        del user.firstEffectRound[i]
                        break
            user.statusEffects.append(PokemonStatusEffect.Sleep)
            user.firstEffectRound.append(2)
            o = user.name+" has healed to full health!"
            if out:
                print(o)
            if display:
                showBattle(self.currentTeam, self.currentTeamActivePokemon, self.otherTeam,
                           self.otherTeamActivePokemon, "Team "+str(team)+"'s "+o, team,
                           self.turnNum)
        elif move.specialEffect == SpecialMoveEffect.Struggle:
            damage = calcDamage(user, enemy, move, True)[0]
            recoil = math.floor(damage / 2)
            user.hp -= recoil
            enemy.hp -= damage
            enemy.lastMoveHitBy = move
            o = str(user.name)+" struggles, doing "+str(damage)+" points of damage and suffers "+str(recoil)+"points of recoil damage"
            if out:
                print(o)
            if display:
                showBattle(self.currentTeam, self.currentTeamActivePokemon, self.otherTeam,
                           self.otherTeamActivePokemon, "Team "+str(team)+"'s "+o, team,
                           self.turnNum)
        elif move.specialEffect == SpecialMoveEffect.Recharge:
            damage = calcDamage(user, enemy, move, True)[0]
            if out:
                print("  The attack did", damage, "points of damage")
            enemy.hp -= damage
            enemy.lastMoveHitBy = move
            # does not recharge if attack is lethal
            if enemy.hp > 0:
                user.statusEffects.append(PokemonStatusEffect.Recharging)
                user.firstEffectRound.append(0)
        elif move.specialEffect == SpecialMoveEffect.DoubleDefense:
            if PokemonStatusEffect.Reflect not in user.statusEffects:
                # Reward for increasing defense
                self.currentTeamFitness += 1
                # process
                user.statusEffects.append(PokemonStatusEffect.Reflect)
                user.firstEffectRound.append(0)
                o = str(user.name)+" gained armor!"
                if out:
                    print(o)
                if display:
                    showBattle(self.currentTeam, self.currentTeamActivePokemon, self.otherTeam,
                               self.otherTeamActivePokemon, "Team "+str(team)+"'s "+o, team,
                               self.turnNum)
            else:
                # Punish for using at a bad time
                self.currentTeamFitness -= 2
                o = str(user.name)+" is already affected by Reflect causing the move to fail"
                if out:
                    print(o)
                if display:
                    showBattle(self.currentTeam, self.currentTeamActivePokemon, self.otherTeam,
                               self.otherTeamActivePokemon, "Team "+str(team)+"'s "+o, team,
                               self.turnNum)
        else:
            raise Exception("Move "+move.name+" not yet implemented")

    def rollStatusEffect(self, pokemon, move, out, display, team):
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
            elif move.effect == PokemonStatusEffect.Paralysis and move.type == PokemonType.Electric and \
                    PokemonType.Ground in pokemon.type:
                # Punish for attempting to use a bad effect
                self.currentTeamFitness -= 5
                if out:
                    print("The move fails as ground type pokemon cannot be paralyzed!")
                return
            elif move.effect in nonVolatileStatusEffects:
                for effect in pokemon.statusEffects:
                    if effect in nonVolatileStatusEffects:
                        # Punish for attempting to add a status effect when one already exists
                        self.currentTeamFitness -= 5
                        if out:
                            print("The status effect fails as the pokemon is already affected by a non-volatile status "
                                  "effect")
                        return
            if move.effectChance is None:
                pokemon.statusEffects.append(move.effect)
                pokemon.firstEffectRound.append(0)
                if out:
                    print("Effect "+str(move.effect)+" has been applied to "+pokemon.name)
                if display:
                    showBattle(self.currentTeam, self.currentTeamActivePokemon, self.otherTeam,
                               self.otherTeamActivePokemon, "Team "+str(team)+"'s " + str(pokemon.name) + " is " + str(move.effect), team,
                               self.turnNum)
            else:
                rnum = random.randint(0, 100)
                if out:
                    print("rnum: "+str(rnum)+", chance="+str(move.effectChance))
                if rnum <= move.effectChance:
                    pokemon.statusEffects.append(move.effect)
                    pokemon.firstEffectRound.append(0)
                    if out:
                        print("Effect "+str(move.effect)+" has been applied to "+pokemon.name)
                    if display:
                        showBattle(self.currentTeam, self.currentTeamActivePokemon, self.otherTeam,
                                   self.otherTeamActivePokemon,
                                   "Team "+str(team)+"'s "+str(pokemon.name)+" is "+str(move.effect), team,
                                   self.turnNum)

    # simulate status effect (burn, freeze, etc)
    # returns true if move skipped (frozen, paralyzed, etc), false otherwise
    # firstEffectRound
    def simulateStatusEffect(self, pokemon, before, out, display, team):
        for i in range(0, len(pokemon.statusEffects)):
            effect = pokemon.statusEffects[i]
            firstRound = pokemon.firstEffectRound[i]
            if effect == PokemonStatusEffect.Freeze and before:
                # frozen until hit by fire type move other than fire spin or opponent uses Haze
                if pokemon.lastMoveHitBy.type == PokemonType.Fire:
                    del pokemon.statusEffects[i]
                    del pokemon.firstEffectRound[i]
                    i -= 1
                    # Punish for thawing a frozen pokemon
                    self.otherTeamFitness -= 3
                    if out:
                        print(pokemon.name+" thaws out!")
                    if display:
                        showBattle(self.currentTeam, self.currentTeamActivePokemon, self.otherTeam,
                                   self.otherTeamActivePokemon,
                                   "Team "+str(team)+"'s "+str(pokemon.name)+" thaws out!", team,
                                   self.turnNum)
                    return False
                if out:
                    print(pokemon.name+" is frozen solid!")
                if display:
                    showBattle(self.currentTeam, self.currentTeamActivePokemon, self.otherTeam,
                               self.otherTeamActivePokemon, "Team "+str(team)+"'s " + str(pokemon.name) + " frozen solid!", team,
                               self.turnNum)
                return True
            elif effect == PokemonStatusEffect.Paralysis and before:
                # speed reduced 75%
                if firstRound == 0:
                    pokemon.ev[3] *= 0.25
                    if out:
                        print(pokemon.name+"'s speed is reduced to "+str(pokemon.ev[3])+" because of paralysis.")
                    pokemon.firstEffectRound[i] += 1
                rand = random.randint(0, 100)
                if rand <= 25:
                    if out:
                        print(pokemon.name+" is paralyzed and unable to move!")
                    if display:
                        showBattle(self.currentTeam, self.currentTeamActivePokemon, self.otherTeam,
                                   self.otherTeamActivePokemon,
                                   "Team "+str(team)+"'s "+str(pokemon.name)+" is Paralyzed and unable to move!", team,
                                   self.turnNum)
                    return True
                return False
            elif effect == PokemonStatusEffect.Poison and not before:
                decrease = math.floor(pokemon.maxHp / 16.0)
                if decrease < 1:
                    decrease = 1
                pokemon.hp -= decrease
                if out:
                    print(pokemon.name+" loses "+str(decrease)+" health to poison.")
                if display:
                    showBattle(self.currentTeam, self.currentTeamActivePokemon, self.otherTeam,
                               self.otherTeamActivePokemon, "Team "+str(team)+"'s " + str(pokemon.name) + " loses "+str(decrease)+" health to due to poison!", team,
                               self.turnNum)
                return False
            elif effect == PokemonStatusEffect.BadlyPoisoned and not before:
                decrease = math.floor(pokemon.maxHp / 16.0+pokemon.maxHp * firstRound / 16.0)
                if decrease < 1:
                    decrease = 1
                pokemon.hp -= decrease
                if out:
                    print(pokemon.name+"loses"+str(decrease)+"health to bad poison.")
                    if display:
                        showBattle(self.currentTeam, self.currentTeamActivePokemon, self.otherTeam,
                                   self.otherTeamActivePokemon, "Team "+str(team)+"'s "+str(pokemon.name)+" loses "+str(
                                decrease)+" health to due being badly poisoned!", team,
                                   self.turnNum)
                pokemon.firstEffectRound[i] += 1
                return False
            elif effect == PokemonStatusEffect.Sleep and before:
                # intial round when rolling
                if firstRound == 0:
                    pokemon.firstEffectRound[i] = random.randint(1, 7)
                    if pokemon.firstEffectRound[i] == 1:
                        if out:
                            print(pokemon.name+" awakens!")
                        if display:
                            showBattle(self.currentTeam, self.currentTeamActivePokemon, self.otherTeam,
                                       self.otherTeamActivePokemon,
                                       "Team "+str(team)+"'s "+str(pokemon.name)+" wakes up!", team,
                                       self.turnNum)
                        del pokemon.firstEffectRound[i]
                        del pokemon.statusEffects[i]
                        i -= 1
                        return True
                    if out:
                        print(pokemon.name+" is fast asleep")
                    if display:
                        showBattle(self.currentTeam, self.currentTeamActivePokemon, self.otherTeam,
                                   self.otherTeamActivePokemon, "Team "+str(team)+"'s "+str(pokemon.name)+" is fast asleep...", team,
                                   self.turnNum)
                    return True
                # last round when 1
                elif firstRound == 1:
                    del pokemon.firstEffectRound[i]
                    del pokemon.statusEffects[i]
                    i -= 1
                    if out:
                        print(pokemon.name+" awakens!")
                    if display:
                        showBattle(self.currentTeam, self.currentTeamActivePokemon, self.otherTeam,
                                   self.otherTeamActivePokemon,
                                   "Team "+str(team)+"'s "+str(pokemon.name)+" wakes up!", team,
                                   self.turnNum)
                    return True
                else:
                    pokemon.firstEffectRound[i] -= 1
                    if out:
                        print(pokemon.name+" is fast asleep")
                    if display:
                        showBattle(self.currentTeam, self.currentTeamActivePokemon, self.otherTeam,
                                   self.otherTeamActivePokemon, "Team "+str(team)+"'s "+str(pokemon.name)+" is fast asleep...", team,
                                   self.turnNum)
                    return True
            elif effect == PokemonStatusEffect.Flinch and before and not self.firstTurn:
                if out:
                    print(pokemon.name+" flinches!")
                if display:
                    showBattle(self.currentTeam, self.currentTeamActivePokemon, self.otherTeam,
                               self.otherTeamActivePokemon,
                               "Team "+str(team)+"'s "+str(pokemon.name)+" flinched!", team,
                               self.turnNum)
                return True
            elif effect == PokemonStatusEffect.Confusion and before:
                if firstRound == 0:
                    pokemon.firstEffectRound[i] = random.randint(2, 5)
                    if out:
                        print("Confusion on "+pokemon.name+" for "+str(pokemon.firstEffectRound[i])+" rounds")
                    if display:
                        showBattle(self.currentTeam, self.currentTeamActivePokemon, self.otherTeam,
                                   self.otherTeamActivePokemon, "Team "+str(team)+"'s "+str(pokemon.name)+" is confused...", team,
                                   self.turnNum)
                elif firstRound == 1:
                    del pokemon.firstEffectRound[i]
                    del pokemon.statusEffects[i]
                    i -= 1
                    if out:
                        print(pokemon.name+" has snapped out of confusion!")
                    if display:
                        showBattle(self.currentTeam, self.currentTeamActivePokemon, self.otherTeam,
                                   self.otherTeamActivePokemon, "Team "+str(team)+"'s "+str(pokemon.name)+" snapped out of its confusion!", team,
                                   self.turnNum)
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
                        if out:
                            print(pokemon.name+" hurt itself in confusion for "+str(dmg)+" damage!")
                        if display:
                            showBattle(self.currentTeam, self.currentTeamActivePokemon, self.otherTeam,
                                       self.otherTeamActivePokemon,
                                       "Team "+str(team)+"'s "+str(pokemon.name)+" hurt itself in its confusion! Team "+str(team)+"'s "+str(pokemon.name)+" took "+str(dmg)+" points of damage!", team,
                                       self.turnNum)
                        pokemon.firstEffectRound[i] -= 1
                        return True
                    pokemon.firstEffectRound[i] -= 1
                    return False
            elif effect == PokemonStatusEffect.Burn:
                decrease = math.floor(pokemon.maxHp / 16.0)
                if before and pokemon.hp-decrease <= 0:
                    pokemon.hp -= decrease
                    if out:
                        print(pokemon.name+" loses "+str(decrease)+" health to burn.")
                        print("It is applied before the pokemon's turn when it is lethal.")
                    showBattle(self.currentTeam, self.currentTeamActivePokemon, self.otherTeam,
                               self.otherTeamActivePokemon, "Team "+str(team)+"'s "+str(pokemon.name)+" loses "+str(
                            decrease)+" health to due its Burn!", team,
                               self.turnNum)
                    self.swapTeam()
                    return True
                elif not before:
                    if decrease < 1:
                        decrease = 1
                    pokemon.hp -= decrease
                    if out:
                        print(pokemon.name+" loses "+str(decrease)+" health to burn.")
                    showBattle(self.currentTeam, self.currentTeamActivePokemon, self.otherTeam,
                               self.otherTeamActivePokemon, "Team "+str(team)+"'s "+str(pokemon.name)+" loses "+str(
                            decrease)+" health to due its Burn!", team,
                               self.turnNum)
                    return False
            elif effect == PokemonStatusEffect.Recharging and before:
                del pokemon.firstEffectRound[i]
                del pokemon.statusEffects[i]
                i -= 1
                if out:
                    print(pokemon.name+" is recharging.")
                showBattle(self.currentTeam, self.currentTeamActivePokemon, self.otherTeam,
                           self.otherTeamActivePokemon, "Team "+str(team)+"'s "+str(pokemon.name)+" is recharging and unable to attack...", team,
                           self.turnNum)
                return True
            elif effect == PokemonStatusEffect.Bound and before:
                raise Exception("Bound effect not yet implemented")

    def round(self, choiceTeam1, choiceTeam2, out=False, display=False):
        if self.turnNum == 0:
            self.turnNum += 1

        if out:
            print("Your active pokemon: "+self.Team2[self.Team2ActivePokemon].name)
            print("Enemy active pokemon: "+self.Team1[self.Team1ActivePokemon].name)

        if display:
            showBattle(self.Team1, self.Team1ActivePokemon, self.Team2, self.Team2ActivePokemon, "New Round", 1,
                       self.turnNum)

        # set up team 1
        self.currentTeam = self.Team1
        self.currentTeamActivePokemon = self.Team1ActivePokemon
        self.currentTeamFitness = self.Team1Fitness
        # set up team 2
        self.otherTeam = self.Team2
        self.otherTeamActivePokemon = self.Team2ActivePokemon
        self.otherTeamFitness = self.Team2Fitness

        # If a pokemon is currently fainted and must be swapped before the round can continue
        if self.currentTeam[self.currentTeamActivePokemon].hp <= 0:
            r = self.turn(choiceTeam1, 1, out, display)
            self.Team1 = self.currentTeam
            self.Team1ActivePokemon = self.currentTeamActivePokemon
            self.Team1Fitness = self.currentTeamFitness
            if r:
                return [0, 0]
            else:
                return [1, 0]

        if self.otherTeam[self.otherTeamActivePokemon].hp <= 0:
            self.swapTeam()
            r = self.turn(choiceTeam2, 2, out, display)
            self.swapTeam()
            self.Team2 = self.otherTeam
            self.Team2ActivePokemon = self.otherTeamActivePokemon
            self.Team2Fitness = self.otherTeamFitness
            if r:
                return [0, 0]
            else:
                return [0, 1]

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
            self.firstTurn = True
            if self.turn(choiceTeam1, 1, out, display):
                self.swapTeam()
                self.firstTurn = False
                if self.currentTeam[self.currentTeamActivePokemon].hp > 0:
                    r = self.turn(choiceTeam2, 2, out, display)
                    if not r:
                        return [0, 1]
            else:
                return [1, 0]
            self.swapTeam()

        elif team1Speed < team2Speed:
            # team 2 goes first
            self.firstTurn = True
            self.swapTeam()
            if self.turn(choiceTeam2, 2, out, display):
                self.swapTeam()
                self.firstTurn = False
                if self.currentTeam[self.currentTeamActivePokemon].hp > 0:
                    r = self.turn(choiceTeam1, 1, out, display)
                    if not r:
                        return [1, 0]
            else:
                return [0, 1]
        else:
            # team that goes first is random
            if random.randint(0, 1) == 1:
                # Team 1 is first
                self.firstTurn = True
                if self.turn(choiceTeam1, 1, out, display):
                    self.swapTeam()
                    self.firstTurn = False
                    if self.currentTeam[self.currentTeamActivePokemon].hp > 0:
                        r = self.turn(choiceTeam2, 2, out, display)
                        if not r:
                            return [0, 1]
                else:
                    return [1, 0]
                self.swapTeam()
            else:
                # Team two is first
                self.firstTurn = True
                self.swapTeam()
                if self.turn(choiceTeam2, 2, out, display):
                    self.swapTeam()
                    self.firstTurn = False
                    if self.currentTeam[self.currentTeamActivePokemon].hp > 0:
                        r = self.turn(choiceTeam1, 1, out, display)
                        if not r:
                            return [1, 0]
                else:
                    return [0, 1]

        self.Team1 = self.currentTeam
        self.Team1ActivePokemon = self.currentTeamActivePokemon
        self.Team1Fitness = self.currentTeamFitness
        self.Team2 = self.otherTeam
        self.Team2ActivePokemon = self.otherTeamActivePokemon
        self.Team2Fitness = self.otherTeamFitness

        self.turnNum += 1
        return [0, 0]

    # Process a single turn of battle using the current active team and a valid move/swap choice
    # Choices 0 through 9 represent all possible choices the NN can make
    # Out results in a verbose output of the turn
    def turn(self, choice, team, out=False, display=False):
        if out:
            print("\nTurn Number", self.turnNum, ":")
        # Current Pokemon uses a move and tries to attack
        # choice represents which of the pokemon's four moves is used
        if choice < 4:
            # Increase fitness for using the highest damage move
            maxD = 0
            place = -1
            for i in range(0, 4):
                if self.currentTeam[self.currentTeamActivePokemon].moves[i].category != MoveCategory.Status and \
                        self.currentTeam[self.currentTeamActivePokemon].moves[i].maxPP > 0 and self.currentTeam[
                    self.currentTeamActivePokemon].hp > 0:
                    d = calcDamage(
                        self.currentTeam[self.currentTeamActivePokemon], self.otherTeam[self.otherTeamActivePokemon],
                        self.currentTeam[self.currentTeamActivePokemon].moves[i],
                        False, False)[0]
                    if d > maxD:
                        maxD = d
                        place = i
            if choice == place:
                self.currentTeamFitness += 4

            # Process the choice
            # Ensures current pokemon is not fainted and chosen move has PP
            if len(self.currentTeam[self.currentTeamActivePokemon].moves) > choice and \
                    self.currentTeam[self.currentTeamActivePokemon].moves[choice].maxPP > 0 and self.currentTeam[
                self.currentTeamActivePokemon].hp > 0:
                if team == 1:
                    t = 2
                else:
                    t = 1
                # verbose output for successful move execution
                o = "Team "+str(team)+"'s "+str(
                    self.currentTeam[self.currentTeamActivePokemon].name).capitalize()+" used the move "+str(
                    self.currentTeam[self.currentTeamActivePokemon].moves[choice].name)+" on Team "+str(t)+"'s "+str(
                    self.otherTeam[self.otherTeamActivePokemon].name).capitalize()
                if out:
                    print(o)
                if display:
                    showBattle(self.currentTeam, self.currentTeamActivePokemon, self.otherTeam,
                               self.otherTeamActivePokemon, o, team,
                               self.turnNum)
                # attacks the opponent using the desired move
                self.attack(self.currentTeam[self.currentTeamActivePokemon].moves[choice], out, display, team)
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
                # Reward for switching into a type advantage, punish for switching into a bad matchup
                c = calcTypeAdvantage(self.currentTeam[choice-4], self.otherTeam[self.otherTeamActivePokemon])
                if c > 1:
                    self.currentTeamFitness += 7
                if c < 1:
                    self.currentTeamFitness -= 2

                # Verbose output for when the swap is successful

                o = "Team "+str(team)+" swapped out "+str(
                    self.currentTeam[self.currentTeamActivePokemon].name).capitalize()+" and swapped in "+str(
                    self.currentTeam[choice-4].name).capitalize()
                if out:
                    print(o)

                self.currentTeam[choice-4].seen = True
                self.currentTeamActivePokemon = choice-4
                if display:
                    showBattle(self.currentTeam, self.currentTeamActivePokemon, self.otherTeam,
                               self.otherTeamActivePokemon, o, team,
                               self.turnNum)
                return True
            else:
                # Verbose output for when swap does not work properly
                if out:
                    # If the pokemon being swapped to does not exist
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
            raise Exception(" ", choice, "is not a valid Pokemon Battle command")

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
