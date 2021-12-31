# from: https://github.com/ezstoltz/genetic-algorithm
# import numpy as np, random, operator, pandas as pd, matplotlib.pyplot as plt
import numpy as np
import random
import operator
from shapely.geometry import LineString, Point
#import matplotlib.pyplot as plt


class City:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def distance(self, city):
        xDis = abs(self.x - city.x)
        yDis = abs(self.y - city.y)
        distance = np.sqrt((xDis ** 2) + (yDis ** 2))
        return distance

    def coords(self):
        return (self.x, self.y)

    def __repr__(self):
        return "(" + str(self.x) + "," + str(self.y) + ")"


class Fitness:
    def __init__(self, route):
        self.route = route
        self.distance = 0
        self.fitness = 0.0
    
    def routeDistance(self):
        if self.distance == 0:
            pathDistance = 0
            for i in range(0, len(self.route)):
                fromCity = self.route[i]
                toCity = None
                if i + 1 < len(self.route):
                    toCity = self.route[i + 1]
                else:
                    toCity = self.route[0]
                pathDistance += fromCity.distance(toCity)
            self.distance = pathDistance
        return self.distance
    
    def routeFitness(self):
        if self.fitness == 0:
            self.fitness = 1 / float(self.routeDistance())
        return self.fitness


class Optimizer:

    def __init__(self, points_coord):
        self.points_coord = points_coord
        self.population = []

    @staticmethod
    def createRoute(cityList):
        route = random.sample(cityList, len(cityList))
        return route

    def initialPopulation(self, popSize, cityList):
        population = []
        for i in range(0, popSize):
            population.append(self.createRoute(cityList))
        return population

    @staticmethod
    def check_pop_intersection(population):
        if len(population):
            routes = []
            c = population[0]
            pp = c.coords()
            nc = None
            for i in range(1, len(population)):
                nc = population[i]
                p = nc.coords()
                routes.append(LineString([pp, p]))
                pp = p[:]
            if nc is not None:
                routes.append(LineString([pp, c.coords()]))

            flags = [False for z in range(len(routes))]
            step = 1
            for i in range(len(routes)):
                for j in range(i + 2, len(routes) - step):
                    a = routes[i]
                    b = routes[j]
                    if a.intersects(b):
                        flags[i] = True
                        flags[j] = True
                step = 0
            return flags
        else:
            return [False for z in range(len(population))]

    def rankRoutes(self, population):
        fitnessResults = {}
        for i in range(0, len(population)):
            fitnessResults[i] = Fitness(population[i]).routeFitness()
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
        matingpool = []
        for i in range(0, len(selectionResults)):
            index = selectionResults[i]
            matingpool.append(population[index])
        return matingpool

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
        pool = random.sample(matingpool, len(matingpool))

        for i in range(0, eliteSize):
            children.append(matingpool[i])

        for i in range(0, length):
            child = self.breed(pool[i], pool[len(matingpool)-i-1])
            children.append(child)
        return children

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
        return mutatedPop

    def nextGeneration(self, currentGen, eliteSize, mutationRate):
        popRanked = self.rankRoutes(currentGen)
        selectionResults = self.selection(popRanked, eliteSize)
        matingpool = self.matingPool(currentGen, selectionResults)
        children = self.breedPopulation(matingpool, eliteSize)
        nextGeneration = self.mutatePopulation(children, mutationRate)
        return nextGeneration

    def geneticAlgorithm(self, population, popSize, eliteSize, mutationRate, generations):
        pop = self.initialPopulation(popSize, population)
        print("Initial distance: " + str(1 / self.rankRoutes(pop)[0][1]))

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

        print("Final distance: " + str(1 / self.rankRoutes(pop)[0][1]))
        bestRouteIndex = self.rankRoutes(pop)[0][0]
        bestRoute = pop[bestRouteIndex]
        return bestRoute

    @staticmethod
    def rotate(l, n):
        return l[n:] + l[:n]

    def get_optimized_path(self):
        points_coord = self.points_coord
        cityList = []
        for p in points_coord:
            cityList.append(City(x=p[0], y=p[1]))
        bestRoute = self.geneticAlgorithm(population=cityList, popSize=400, eliteSize=50, mutationRate=0.02, generations=800)
        optimized_coords = []

        for c in bestRoute:
            optimized_coords.append((c.x, c.y))

        # the path is ordered so that it starts from the point closest to 0.0

        min_id = 0
        min_d = Point(optimized_coords[0]).distance(Point((0.0, 0.0)))
        for i in range(len(optimized_coords)):
            d = Point(optimized_coords[i]).distance(Point((0.0, 0.0)))
            if d < min_d:
                min_id = i
                min_d = d

        pre_id = min_id - 1
        post_id = min_id + 1
        if min_id == len(optimized_coords) - 1:
            post_id = 0

        pre_d = Point(optimized_coords[pre_id]).distance(Point((0.0, 0.0)))
        post_d = Point(optimized_coords[post_id]).distance(Point((0.0, 0.0)))

        if pre_d < post_d:
            noc = self.rotate(optimized_coords, min_id)
        else:
            noc = self.rotate(optimized_coords, post_id)

        optimized_coords = noc

        x = []
        y = []
        for c in optimized_coords:
            x.append(c[0])
            y.append(c[1])

        return optimized_coords


if __name__ == "__main__":

    print("Paint")
