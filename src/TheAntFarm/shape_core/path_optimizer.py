# from: https://github.com/ezstoltz/genetic-algorithm
# import numpy as np, random, operator, pandas as pd, matplotlib.pyplot as plt
import sys
import numpy as np
from scipy.spatial import distance
from operator import itemgetter
from scipy.sparse.csgraph import shortest_path
import random
import operator
from shapely.geometry import LineString, Point
#import matplotlib.pyplot as plt


class Optimizer:
    def __init__(self, coords, optimizer_type="nearest_insertion"):
        self.v = len(coords)
        self.coords = coords
        self.distances = distance.cdist(coords, coords, 'euclidean')
        self.optimizer_type = optimizer_type

    def calculate_path_distance(self, path):
        total_distance = np.sum(self.distances[path[:-1], path[1:]])
        return total_distance

    def nearest_insertion(self, points):
        num_points = len(points)
        unvisited = set(range(num_points))

        first_point_matrix = distance.cdist([(0., 0.)], points, 'euclidean')
        first_point_index = np.argmin(first_point_matrix)

        path = [first_point_index]
        unvisited.remove(first_point_index)

        while unvisited:
            min_distance = float('inf')
            nearest_point = None

            for current_point in path:
                for candidate in unvisited:
                    d = self.distances[current_point, candidate]
                    if d < min_distance:
                        min_distance = d
                        nearest_point = candidate
                        next_point = current_point

            insert_index = path.index(next_point) + 1
            path.insert(insert_index, nearest_point)
            unvisited.remove(nearest_point)

        return path

    def two_opt(self, path):
        new_distance = self.calculate_path_distance(path)
        points = self.coords
        best_path = path
        improved = True
        while improved:
            improved = False
            for i in range(1, len(points) - 2):
                for j in range(i + 1, len(points)):
                    if j - i == 1:
                        continue
                    new_path = path[:]
                    new_path[i:j] = path[i:j][::-1]
                    new_distance = self.calculate_path_distance(new_path)
                    if new_distance < self.calculate_path_distance(best_path):
                        best_path = new_path
                        improved = True
            path = best_path
        # print("Final Distance: ", new_distance)
        return best_path

    def get_optimized_path(self):
        path_ids = list(range(len(self.coords)))

        start_distance = self.calculate_path_distance(path_ids)
        print("Initial Distance: ", start_distance)

        if self.optimizer_type == "genetic":
            path_ids = self.nearest_insertion(self.coords)
            go = GeneticOptimizer(self.coords)
            path_ids = go.get_optimized_path(cityList=path_ids)

        if self.optimizer_type == "two_opt":
            path_ids = self.two_opt(path_ids)

        if self.optimizer_type == "nearest_insertion":
            path_ids = self.nearest_insertion(self.coords)

        final_distance = self.calculate_path_distance(path_ids)
        print("Final Distance: ", final_distance)

        return np.array(self.coords)[path_ids].tolist()


class Cities:

    def __init__(self, coords):
        self.coords = coords
        self.distances = distance.cdist(coords, coords, 'euclidean')

    def length(self, path0, path1):
        return np.sum(self.distances[path0, path1])


class Fitness:
    def __init__(self, route, cities):
        self.route = route
        self.cities = cities
        self.distance = 0
        self.fitness = 0.0

    def routeDistance(self):
        if self.distance == 0:
            route0 = self.route
            route1 = np.roll(self.route, -1)
            self.distance = self.cities.length(route0, route1)
        return self.distance

    def routeFitness(self):
        if self.fitness == 0:
            self.fitness = 1 / float(self.routeDistance())
        return self.fitness


class GeneticOptimizer:

    def __init__(self, points_coord):
        self.points_coord = points_coord
        self.population = []
        self.cities = Cities(points_coord)

    @staticmethod
    def createRoute(cityList):
        route = cityList.copy()
        random.shuffle(route)
        return route

    def initialPopulation(self, popSize, cityList):
        population = [cityList]
        for i in range(0, popSize-1):
            population.append(self.createRoute(cityList))
        return np.array(population)

    def rankRoutes(self, population):
        fitnessResults = {}
        for i in range(0, len(population)):
            # print("Population:", population[i])
            fitnessResults[i] = Fitness(population[i], self.cities).routeFitness()
        return sorted(fitnessResults.items(), key=operator.itemgetter(1), reverse=True)

    def selection(self, popRanked, eliteSize):
        selectionResults = []
        n = np.array(popRanked)
        cs = n[1, :].cumsum()
        cp = 100 * cs / n[1, :].sum()
        for i in range(0, eliteSize):
            selectionResults.append(popRanked[i][0])
        for i in range(0, len(popRanked) - eliteSize):
            pick = 100 * random.random()
            for i in range(0, len(popRanked)):
                if pick <= cp[i]:
                    selectionResults.append(popRanked[i][0])
                    break
        return selectionResults

    def matingPool(self, population, selectionResults):
        matingpool = population[selectionResults]
        return matingpool

    def breed(self, parent1, parent2):
        child = []
        childP1 = []
        childP2 = []

        geneA = int(random.random() * len(parent1))
        geneB = int(random.random() * len(parent1))

        startGene = min(geneA, geneB)
        endGene = max(geneA, geneB)

        for i in range(startGene, endGene):
            childP1.append(parent1[i])

        childP2 = [item for item in parent2 if item not in childP1]

        child = childP1 + childP2
        return child

    def breedPopulation(self, matingpool, eliteSize):
        children = []
        length = len(matingpool) - eliteSize
        pool = matingpool.copy()
        random.shuffle(matingpool)
        children = matingpool[range(0, eliteSize)].tolist()

        for i in range(0, length):
            child = self.breed(pool[i], pool[len(matingpool)-i-1])
            children.append(child)
        return np.array(children)

    def mutate(self, individual, mutationRate):
        for swapped in range(len(individual)):
            if random.random() < mutationRate:
                swapWith = int(random.random() * len(individual))

                city1 = individual[swapped]
                city2 = individual[swapWith]

                individual[swapped] = city2
                individual[swapWith] = city1
        return individual

    def mutatePopulation(self, population, mutationRate):
        mutatedPop = []

        for ind in range(0, len(population)):
            mutatedInd = self.mutate(population[ind], mutationRate)
            mutatedPop.append(mutatedInd)
        return np.array(mutatedPop)

    def nextGeneration(self, currentGen, eliteSize, mutationRate):
        popRanked = self.rankRoutes(currentGen)
        selectionResults = self.selection(popRanked, eliteSize)
        matingpool = self.matingPool(currentGen, selectionResults)
        children = self.breedPopulation(matingpool, eliteSize)
        nextGeneration = self.mutatePopulation(children, mutationRate)
        return nextGeneration

    def geneticAlgorithm(self, population, popSize, eliteSize, mutationRate, generations):
        pop = self.initialPopulation(popSize, population)
        # print("Initial distance: " + str(1 / self.rankRoutes(pop)[0][1]))

        x = int(generations/10)
        c = 0
        j = 1
        for i in range(0, generations):
            pop = self.nextGeneration(pop, eliteSize, mutationRate)
            if c >= x:
                c = 0
                print(j * x / generations * 100)
                j += 1
            else:
                c += 1

        # print("Final distance: " + str(1 / self.rankRoutes(pop)[0][1]))
        bestRouteIndex = self.rankRoutes(pop)[0][0]
        bestRoute = pop[bestRouteIndex]
        return bestRoute

    @staticmethod
    def rotate(l, n):
        return l[n:] + l[:n]

    def get_optimized_path(self, cityList=None):
        points_coord = np.array(self.points_coord)
        if cityList is None:
            cityList = np.array(range(0, len(points_coord)))
        bestRoute = self.geneticAlgorithm(population=cityList, popSize=400, eliteSize=50, mutationRate=0.02, generations=800)

        first_point_matrix = distance.cdist([(0., 0.)], points_coord[bestRoute], 'euclidean')
        first_point_index = np.argmin(first_point_matrix)
        # optimized_coords = np.roll(points_coord[bestRoute], -first_point_index)
        optimized_ids = np.roll(bestRoute, -first_point_index)

        return optimized_ids


if __name__ == "__main__":

    print("Paint")
