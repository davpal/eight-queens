#!/usr/bin/env python

import random
import string

def random_individual(size):
    return [ random.randint(1, 8) for _ in range(8) ]

maxFitness = 28
def fitness(individual):
    collisions = sum([individual.count(queen)-1 for queen in individual])/2
    for i, col in enumerate(individual):
        for j, diagonal in enumerate(individual):
            mod = abs(i-j)
            if mod < 0:
                if diagonal + mod == col or diagonal - mod == col:
                    collisions += 1
    return int(maxFitness - collisions)

def probability(individual, fitness):
    return fitness(individual) / maxFitness

def random_pick(some_list, probabilities):
    x = random.uniform(0, 1)
    cumulative_probability = 0.0
    for item, item_probability in zip(some_list, probabilities):
        cumulative_probability += item_probability
        if x < cumulative_probability: break
    return item

def reproduce(x, y):
    n = len(x)
    c = random.randint(0, n - 1)
    return x[0:c] + y[c:n]

def mutate(x):
    n = len(x)
    c = random.randint(0, n - 1)
    m = random.randint(1, n)
    x[c] = m
    return x

def genetic_queen(population, fitness):
    new_population = []
    probabilities = [probability(n, fitness) for n in population]
    for i in range(len(population)):
        x = random_pick(population, probabilities)
        y = random_pick(population, probabilities)
        child = reproduce(x, y)
        if random.random() < 0.02:
            child = mutate(child)
        new_population.append(child)
    return new_population

if __name__ == "__main__":
    population = [random_individual(8) for _ in range(100)]
    generation = 1
    while not 28 in [fitness(x) for x in population]:
        print("=== Generation {} ===".format(generation))
        population = genetic_queen(population, fitness)
        print("Maximum fitness = {}".format(max([fitness(n) for n in population])))
        generation += 1
    print("Solved in Generation {}!".format(generation-1))
    for x in population:
        if fitness(x) == 28:
            print("{},  fitness = {}, probability = {:.6f}"
            .format(str(x), fitness(x), probability(x, fitness)))
