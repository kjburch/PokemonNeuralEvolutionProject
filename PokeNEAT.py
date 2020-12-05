import os

os.environ["PATH"] += os.pathsep+'E:/Program Files/Graphviz/bin'
import neat
from pokemonAI import *
import visualize
import pickle

gen = 0


def getInputs1(battle):
    inputs = []
    for t in battle.Team1:
        for m in t.moves:
            # Damage
            if m.category is not MoveCategory.Status and m.power is not None:
                inputs.append(
                    int(calcDamage(t, battle.Team2[battle.Team2ActivePokemon], m, randBool=False, critBool=False)[0]))
            else:
                inputs.append(0)
            # PP
            inputs.append(m.maxPP)
            # Accuracy
            if m.accuracy is None:
                inputs.append(1)
            else:
                inputs.append(m.accuracy)
            # Status effects
            if int(m.effect) == 1:
                inputs.append(1)
            else:
                inputs.append(0)
            if int(m.effect) == 2:
                inputs.append(1)
            else:
                inputs.append(0)
            if int(m.effect) == 3:
                inputs.append(1)
            else:
                inputs.append(0)
            if int(m.effect) == 4:
                inputs.append(1)
            else:
                inputs.append(0)
            if int(m.effect) == 5:
                inputs.append(1)
            else:
                inputs.append(0)
            if int(m.effect) == 34:
                inputs.append(1)
            else:
                inputs.append(0)
            if int(m.effect) == 35:
                inputs.append(1)
            else:
                inputs.append(0)
            if int(m.effect) == 36:
                inputs.append(1)
            else:
                inputs.append(0)

            # Status Effect Chance
            if m.effectChance is not None:
                inputs.append(m.effectChance)
            else:
                inputs.append(0)
        #  Pokemon Stats
        # Pokemon Type
        for i in range(0, 17):
            if i in t.type:
                inputs.append(1)
            else:
                inputs.append(0)
        # Attack / Defense / Special / Speed
        inputs.append(t.ev[0])
        inputs.append(t.ev[1])
        inputs.append(t.ev[2])
        inputs.append(t.ev[3])
    for t in battle.Team2:
        for i in range(0, 17):
            if i in t.type:
                inputs.append(1)
            else:
                inputs.append(0)
        # Attack / Defense / Special / Speed
        inputs.append(t.ev[0])
        inputs.append(t.ev[1])
        inputs.append(t.ev[2])
        inputs.append(t.ev[3])
    for t in battle.Team1:
        if t.hp > 0:
            inputs.append(1)
        else:
            inputs.append(0)
    for t in battle.Team2:
        if t.hp > 0:
            inputs.append(1)
        else:
            inputs.append(0)

    return (inputs)


def getInputs2(battle):
    inputs = []
    for t in battle.Team2:
        for m in t.moves:
            # Damage
            if m.category is not MoveCategory.Status and m.power is not None:
                inputs.append(
                    int(calcDamage(t, battle.Team1[battle.Team1ActivePokemon], m, randBool=False, critBool=False)[0]))
            else:
                inputs.append(0)
            # PP
            inputs.append(m.maxPP)
            # Accuracy
            if m.accuracy is None:
                inputs.append(1)
            else:
                inputs.append(m.accuracy)
            # Status effects
            if int(m.effect) == 1:
                inputs.append(1)
            else:
                inputs.append(0)
            if int(m.effect) == 2:
                inputs.append(1)
            else:
                inputs.append(0)
            if int(m.effect) == 3:
                inputs.append(1)
            else:
                inputs.append(0)
            if int(m.effect) == 4:
                inputs.append(1)
            else:
                inputs.append(0)
            if int(m.effect) == 5:
                inputs.append(1)
            else:
                inputs.append(0)
            if int(m.effect) == 34:
                inputs.append(1)
            else:
                inputs.append(0)
            if int(m.effect) == 35:
                inputs.append(1)
            else:
                inputs.append(0)
            if int(m.effect) == 36:
                inputs.append(1)
            else:
                inputs.append(0)

            # Status Effect Chance
            if m.effectChance is not None:
                inputs.append(m.effectChance)
            else:
                inputs.append(0)
        #  Pokemon Stats
        # Pokemon Type
        for i in range(0, 17):
            if i in t.type:
                inputs.append(1)
            else:
                inputs.append(0)
        # Attack / Defense / Special / Speed
        inputs.append(t.ev[0])
        inputs.append(t.ev[1])
        inputs.append(t.ev[2])
        inputs.append(t.ev[3])
    for t in battle.Team1:
        for i in range(0, 17):
            if i in t.type:
                inputs.append(1)
            else:
                inputs.append(0)
        # Attack / Defense / Special / Speed
        inputs.append(t.ev[0])
        inputs.append(t.ev[1])
        inputs.append(t.ev[2])
        inputs.append(t.ev[3])
    for t in battle.Team2:
        if t.hp > 0:
            inputs.append(1)
        else:
            inputs.append(0)
    for t in battle.Team1:
        if t.hp > 0:
            inputs.append(1)
        else:
            inputs.append(0)

    return inputs


def eval_genomes(genomes, config):
    global gen
    gen += 1

    # start by creating lists holding the genome itself, the
    # neural network associated with the genome and the
    # team object that uses that network to play
    neuralNets = []
    pokemonTeams = []
    ge = []
    for genome_id, genome in genomes:
        # start with fitness level of 0
        genome.fitness = 0
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        neuralNets.append(net)
        pokemonTeams.append(getTeam())
        ge.append(genome)

    # Randomizes the Neural Net order so that they don't always face the same opponents
    tez = list(zip(ge, neuralNets, genomes))
    random.shuffle(tez)
    ge, neuralNets, genomes = zip(*tez)

    for i in range(0, len(pokemonTeams)):
        print("\nHeat Num (", i+1, ")\n--------------")
        for p in range(i+1, i+6):
            if p >= len(pokemonTeams):
                g = p - len(pokemonTeams)
            else:
                g = p

            random.shuffle(pokemonTeams[i])
            random.shuffle(pokemonTeams[g])
            battle = Battle(pokemonTeams[i], pokemonTeams[g])

            team1Errors = 0
            team2Errors = 0

            print("Battle Num:", int(p-i))
            while battle.winner() == -1 and battle.turnNum <= 100 and team1Errors <= 100 and team2Errors <= 100:
                t1 = neuralNets[i].activate(getInputs1(battle))
                t2 = neuralNets[g].activate(getInputs2(battle))

                for j in range(0, len(t1)):
                    t1[j] = [t1[j], j]
                    t2[j] = [t2[j], j]

                res = [-1, -1]
                while res != [0, 0] and battle.winner() == -1:
                    move1 = max(t1)
                    move2 = max(t2)

                    res = battle.round(move1[1], move2[1], False, False)

                    if res[0] == 1:
                        t1.remove(move1)
                    if res[1] == 1:
                        t2.remove(move2)

                    team1Errors += res[0]
                    team2Errors += res[1]

            # fitness
            # 20 for winning the battle
            # 5 for completing the battle
            if battle.winner() == 1:
                ge[i].fitness += 30
                ge[g].fitness += 5
            if battle.winner() == 2:
                ge[g].fitness += 30
                ge[i].fitness += 5

            # penalizes making illegal moves
            ge[i].fitness -= int(team1Errors)
            ge[g].fitness -= int(team2Errors)

            # Punish for long battle lengths
            ge[i].fitness -= int(battle.turnNum)*2
            ge[g].fitness -= int(battle.turnNum)*2

            # 5 for defeating an enemy pokemon
            # 3 for each pokemon left alive
            for r in pokemonTeams[i]:
                if r.hp > 0:
                    ge[i].fitness += 3
                else:
                    ge[g].fitness += 5
            for r in pokemonTeams[g]:
                if r.hp > 0:
                    ge[g].fitness += 3
                else:
                    ge[i].fitness += 5

            # General Battle Fitness Modifiers
            # (Super effective attacks, status effects, healing, etc...)
            ge[i].fitness += int(battle.Team1Fitness)
            ge[g].fitness += int(battle.Team2Fitness)


def run(config_file):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                neat.DefaultSpeciesSet, neat.DefaultStagnation,
                                config_file)

    # Create the population, which is the top-level object for a NEAT run.
    p = neat.Population(config)

    # Add a stdout reporter to show progress in the terminal.
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    # Run for up to 500 generations.
    winner = p.run(eval_genomes, 200)
    pickle.dump(winner, open("best.pickle", "wb"))

    print("Generating Visualization...")
    print("This could take up to 30 minutes, Please be patient")

    # visualize.draw_net(config, winner, True)
    visualize.plot_stats(stats, ylog=False, view=True)
    visualize.plot_species(stats, view=True)

    # show final stats
    print('\nBest genome:\n{!s}'.format(winner))


def replay_genome(config_path, battle, genome_path="best.pickle"):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet,
                                neat.DefaultStagnation, config_path)

    with open(genome_path, "rb") as f:
        genome = pickle.load(f)

    net = neat.nn.FeedForwardNetwork.create(genome, config)
    while battle.winner() == -1:
        t1 = net.activate(getInputs1(battle))
        for j in range(0, len(t1)):
            t1[j] = [t1[j], j]

        res = [-1, -1]
        # print("-----------")
        while res != [0, 0]:
            if res[0] != 0:
                move1 = max(t1)
            if res[1] != 0:
                move2 = getPlayerMove()

            res = battle.round(move1[1], move2, True, True)
            if res[0] == 1:
                t1.remove(move1)
            if res[1] == 1:
                print("Your move is invalid")


def getPlayerMove():
    print("Enter a move integer (0-9): ")
    move = input()
    while not move.isnumeric():
        print("Try again, invalid")
        move = input()
    return int(move)


if __name__ == '__main__':
    # Determine path to configuration file. This path manipulation is
    # here so that the script will run successfully regardless of the
    # current working directory.
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config')
    run(config_path)

    shf1 = copy.deepcopy(team1)
    shf2 = copy.deepcopy(team2)
    random.shuffle(shf1)
    random.shuffle(shf2)
    battle = Battle(shf1, shf2, Out=True)
    replay_genome(config_path, battle)
