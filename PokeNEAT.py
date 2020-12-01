import os
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
        genome.fitness = 0  # start with fitness level of 0
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        neuralNets.append(net)
        pokemonTeams.append(getTeam())
        ge.append(genome)

    for i in range(0, len(pokemonTeams)-1, 2):
        battle = Battle(pokemonTeams[i], pokemonTeams[i+1])
        tries = 0
        print("Battle Num:", int(i / 2)+1)
        while battle.winner() == -1 and tries < 500:
            t1 = neuralNets[i].activate(getInputs1(battle))
            t2 = neuralNets[i+1].activate(getInputs2(battle))

            l1 = t1.copy()
            l2 = t2.copy()

            l1.sort()
            l2.sort()

            res = False

            for j in range(0, 9):
                for k in range(0, 9):
                    if not res:
                        tries += 1
                        move1 = t1.index(l1[j])
                        move2 = t2.index(l2[k])
                        res = battle.round(move1, move2, False, False)

        for j in range(0, 6):
            if pokemonTeams[i][j].hp > 0:
                ge[i].fitness += 2
            if pokemonTeams[i][j].hp <= 0:
                ge[i+1].fitness += 4
            if pokemonTeams[i+1][j].hp > 0:
                ge[i+1].fitness += 2
            if pokemonTeams[i+1][j].hp <= 0:
                ge[i].fitness += 4

        if battle.winner() == 1:
            ge[i].fitness += 20
        elif battle.winner() == 2:
            ge[i+1].fitness += 20
        else:
            ge[i].fitness += 1
            ge[i+1].fitness += 1

        if battle.turnNum < 60:
            ge[i].fitness += int(20-battle.turnNum / 3)
            ge[i+1].fitness += int(20-battle.turnNum / 3)


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

    # Run for up to 50 generations.
    winner = p.run(eval_genomes, 3)
    pickle.dump(winner, open("best.pickle", "wb"))

    print("Generating Visualization...")
    print("This could take up to 30 minutes, Please be patient")

    visualize.draw_net(config, winner, True)
    visualize.plot_stats(stats, ylog=False, view=True)
    visualize.plot_species(stats, view=True)

    # show final stats
    print('\nBest genome:\n{!s}'.format(winner))


if __name__ == '__main__':
    # Determine path to configuration file. This path manipulation is
    # here so that the script will run successfully regardless of the
    # current working directory.
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config')
    run(config_path)
