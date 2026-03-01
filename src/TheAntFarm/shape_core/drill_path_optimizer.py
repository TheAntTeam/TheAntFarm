# from: https://github.com/ezstoltz/genetic-algorithm
import logging
import operator
import random
from typing import List, Optional, Tuple, Union

import numpy as np
from scipy.spatial import distance

logger = logging.getLogger(__name__)


class DrillPathOptimizer:
    """
    Optimizes the path for visiting a set of 2D coordinates (Traveling Salesperson Problem).
    Provides multiple algorithms with different trade-offs between speed and optimality.
    """

    OPTIMIZATION_TYPES = ("nearest_insertion", "two_opt", "hybrid_ils")

    def __init__(self, coords: List[Tuple[float, float]], optimizer_type: str = "nearest_insertion") -> None:
        """
        Initialize the Optimizer.

        :param coords: List of (x, y) coordinates to visit.
        :param optimizer_type: The algorithm to use ('nearest_insertion', 'two_opt', 'genetic', 'hybrid_ils').
        """
        self.coords = np.array(coords)
        self.v = len(coords)
        # Pre-calculate distance matrix for efficiency
        self.distances = distance.cdist(self.coords, self.coords, "euclidean")
        self.optimizer_type = optimizer_type

    def set_optimization_type(self, opt_type: str) -> bool:
        """Sets the optimization algorithm."""
        if opt_type in self.OPTIMIZATION_TYPES:
            # TODO: modificare la lista dei tipi di ottimizzazione eliminando genetic ed inserendo hybrid_ils.
            #       Quando fatto rimuovere il codice relativo all'algoritmo genetico.
            if opt_type == "genetic":
                self.optimizer_type = "hybrid_ils"
            else:
                self.optimizer_type = opt_type
            return True
        else:
            return False

    def get_optimization_type(self) -> str:
        """Returns the current optimization algorithm."""
        return self.optimizer_type

    def get_optimization_types(self) -> Tuple[str, ...]:
        """Returns the available optimization algorithms."""
        return self.OPTIMIZATION_TYPES

    def calculate_path_distance(self, path: List[int]) -> float:
        """Calculates the total Euclidean distance of a path (list of indices)."""
        # Use numpy advanced indexing to sum distances between consecutive points
        # path[:-1] are the start points, path[1:] are the end points of segments
        total_distance = np.sum(self.distances[path[:-1], path[1:]])
        return float(total_distance)

    def nearest_insertion(self, points: Union[List[Tuple[float, float]], np.ndarray]) -> List[int]:
        """
        Solves TSP using the Nearest Insertion heuristic.
        Starts with a single point and iteratively inserts the nearest unvisited point
        into the path at the position that minimizes the detour.
        """
        num_points = len(points)
        unvisited = set(range(num_points))

        # Start with the point closest to (0,0)
        first_point_matrix = distance.cdist([(0.0, 0.0)], points, "euclidean")
        first_point_index = int(np.argmin(first_point_matrix))

        path = [first_point_index]
        unvisited.remove(first_point_index)

        while unvisited:
            min_distance = float("inf")
            nearest_point = None
            next_point_in_path = None

            # Find the unvisited point closest to any point in the current path
            for current_point in path:
                for candidate in unvisited:
                    d = self.distances[current_point, candidate]
                    if d < min_distance:
                        min_distance = d
                        nearest_point = candidate
                        next_point_in_path = current_point

            if nearest_point is not None and next_point_in_path is not None:
                # Insert the nearest point after the point it's closest to
                insert_index = path.index(next_point_in_path) + 1
                path.insert(insert_index, nearest_point)
                unvisited.remove(nearest_point)

        return path

    def two_opt(self, path: List[int]) -> List[int]:
        """
        [OPTIMIZED] Refines a path using the 2-opt local search algorithm.
        Iteratively swaps two edges to remove crossings and reduce total distance.
        This version is fast because it calculates only the change in distance (delta).
        """
        best_path = path
        # We assume an open path (not returning to start) based on calculate_path_distance logic
        n = len(path)

        improved = True
        while improved:
            improved = False
            # Range adjusted to allow optimization of the end of the path.
            # Start point (index 0) is fixed.
            for i in range(1, n - 1):
                for j in range(i + 1, n):
                    if j - i == 1:
                        continue

                    # Indices of points involved in the swap
                    # Segment to reverse is path[i:j]
                    # Edges removed: (path[i-1] -> path[i]) and (path[j-1] -> path[j])
                    # Edges added:   (path[i-1] -> path[j-1]) and (path[i] -> path[j])

                    p_a = best_path[i - 1]
                    p_b = best_path[i]
                    p_c = best_path[j - 1]
                    p_d = best_path[j]

                    # Current edges length
                    d_ab = self.distances[p_a, p_b]
                    d_cd = self.distances[p_c, p_d]

                    # New edges length
                    d_ac = self.distances[p_a, p_c]
                    d_bd = self.distances[p_b, p_d]

                    # Calculate delta
                    delta = (d_ac + d_bd) - (d_ab + d_cd)

                    if delta < -1e-9:  # Use a small epsilon for float comparison
                        # Apply the move
                        best_path[i:j] = best_path[i:j][::-1]
                        improved = True
                        # Strategy: Restart scan after improvement (First Improvement)
                        # This is often faster for convergence than Best Improvement
                        # break
                # if improved: break

            path = best_path

        return best_path

    def _perturbation(self, path: List[int]) -> List[int]:
        """
        Applies a 'Double Bridge' move to perturb the solution.
        This move cuts the path into 4 segments and reconnects them in a specific non-sequential order.
        It is known to be effective for escaping local optima in TSP.
        """
        n = len(path)
        if n < 8:
            # Fallback for very small paths
            random.shuffle(path)
            return path

        # Choose 3 random cut points
        # Ensure segments have at least length 1
        cuts = sorted(random.sample(range(1, n - 1), 3))
        i, j, k = cuts

        # Segments: A=[0:i], B=[i:j], C=[j:k], D=[k:n]
        # Reconnect as: A -> D -> C -> B
        return path[:i] + path[k:] + path[j:k] + path[i:j]

    def hybrid_ils(self, path: List[int], max_iterations: int = 50) -> List[int]:
        """
        Iterated Local Search (ILS) algorithm.
        Combines Local Search (2-opt) with Perturbation (Double Bridge) to find high-quality solutions.

        :param path: Initial path.
        :param max_iterations: Number of perturbation-optimization cycles.
        """
        # 1. Initial Local Search
        current_path = self.two_opt(path)
        best_path = current_path
        best_distance = self.calculate_path_distance(best_path)

        logger.info(f"ILS Start Distance: {best_distance:.4f}")

        for i in range(max_iterations):
            # 2. Perturbation
            perturbed_path = self._perturbation(current_path)

            # 3. Local Search on perturbed solution
            optimized_path = self.two_opt(perturbed_path)
            optimized_distance = self.calculate_path_distance(optimized_path)

            # 4. Acceptance Criterion (Simple: Accept if better)
            if optimized_distance < best_distance:
                best_distance = optimized_distance
                best_path = optimized_path
                current_path = optimized_path  # Move to the new basin of attraction
                logger.debug(f"ILS Improvement at iter {i}: {best_distance:.4f}")
            else:
                # If not better, we stay at 'current_path' (which is 'best_path' in this simple version)
                current_path = best_path

        return best_path

    def get_optimized_path(self) -> List[Tuple[float, float]]:
        """
        Executes the selected optimization algorithm and returns the optimized coordinates.
        """
        path_ids = list(range(len(self.coords)))
        start_distance = self.calculate_path_distance(path_ids)

        logger.info(f"Selected OPT type: {self.optimizer_type}")
        logger.info(f"Initial Distance: {start_distance:.4f}")

        if self.optimizer_type == "two_opt":
            # 2-opt is a local search, so it needs an initial path.
            # Start with a good heuristic
            path_ids = self.nearest_insertion(self.coords)
            path_ids = self.two_opt(path_ids)

        elif self.optimizer_type == "nearest_insertion":
            path_ids = self.nearest_insertion(self.coords)

        elif self.optimizer_type == "hybrid_ils":
            # Start with a good construction heuristic
            path_ids = self.nearest_insertion(self.coords)
            # Refine with Iterated Local Search
            # Iterations can be tuned based on available time/performance requirements
            path_ids = self.hybrid_ils(path_ids, max_iterations=100)

        # elif self.optimizer_type == "genetic":
        #     # Genetic algorithm benefits from a decent initial solution
        #     path_ids = self.nearest_insertion(self.coords)
        #     # Pass pre-calculated distances to avoid re-computation
        #     go = GeneticOptimizer(self.coords, self.distances)
        #     path_ids = go.get_optimized_path(city_list=path_ids)

        final_distance = self.calculate_path_distance(path_ids)
        logger.info(f"Final Distance: {final_distance:.4f}")

        return self.coords[path_ids].tolist()


class _Cities:
    """Helper class for GeneticOptimizer to manage city coordinates and distances."""

    def __init__(self, coords: np.ndarray, distances: Optional[np.ndarray] = None) -> None:
        self.coords = coords
        if distances is not None:
            self.distances = distances
        else:
            self.distances = distance.cdist(coords, coords, "euclidean")

    def length(self, path0: np.ndarray, path1: np.ndarray) -> float:
        return float(np.sum(self.distances[path0, path1]))


class _Fitness:
    """Helper class for GeneticOptimizer to calculate fitness of a route."""

    def __init__(self, route: np.ndarray, cities: _Cities) -> None:
        self.route = route
        self.cities = cities
        self.distance = 0.0
        self.fitness = 0.0

    def route_distance(self) -> float:
        if self.distance == 0:
            route0 = self.route
            route1 = np.roll(self.route, -1)
            self.distance = self.cities.length(route0, route1)
        return self.distance

    def route_fitness(self) -> float:
        if self.fitness == 0:
            dist = self.route_distance()
            if dist == 0:
                self.fitness = float("inf")
            else:
                self.fitness = 1 / dist
        return self.fitness


class GeneticOptimizer:
    """
    Solves TSP using a Genetic Algorithm.
    """

    def __init__(self, points_coord: np.ndarray, distances: Optional[np.ndarray] = None) -> None:
        self.points_coord = points_coord
        self.population: List[np.ndarray] = []
        # Pass pre-calculated distances to _Cities
        self.cities = _Cities(points_coord, distances)

    @staticmethod
    def create_route(city_list: np.ndarray) -> np.ndarray:
        route = city_list.copy()
        random.shuffle(route)
        return route

    def initial_population(self, pop_size: int, city_list: np.ndarray) -> List[np.ndarray]:
        population = [city_list]
        for _ in range(0, pop_size - 1):
            population.append(self.create_route(city_list))
        return population

    def rank_routes(self, population: List[np.ndarray]) -> List[Tuple[int, float]]:
        fitness_results = {}
        for i in range(0, len(population)):
            fitness_results[i] = _Fitness(population[i], self.cities).route_fitness()
        return sorted(fitness_results.items(), key=operator.itemgetter(1), reverse=True)

    def selection(self, pop_ranked: List[Tuple[int, float]], elite_size: int) -> List[int]:
        selection_results = []
        df = np.array(np.array(pop_ranked))
        cumsum = df[:, 1].cumsum()
        cum_perc = 100 * cumsum / df[:, 1].sum()

        for i in range(0, elite_size):
            selection_results.append(int(pop_ranked[i][0]))

        for _ in range(0, len(pop_ranked) - elite_size):
            pick = 100 * random.random()
            for i in range(0, len(pop_ranked)):
                if pick <= cum_perc[i]:
                    selection_results.append(int(pop_ranked[i][0]))
                    break
        return selection_results

    def mating_pool(self, population: List[np.ndarray], selection_results: List[int]) -> List[np.ndarray]:
        return [population[i] for i in selection_results]

    def breed(self, parent1: np.ndarray, parent2: np.ndarray) -> np.ndarray:
        child_p1 = []

        gene_a = int(random.random() * len(parent1))
        gene_b = int(random.random() * len(parent1))

        start_gene = min(gene_a, gene_b)
        end_gene = max(gene_a, gene_b)

        for i in range(start_gene, end_gene):
            child_p1.append(parent1[i])

        child_p2 = [item for item in parent2 if item not in child_p1]

        return np.array(child_p1 + child_p2)

    def breed_population(self, matingpool: List[np.ndarray], elite_size: int) -> List[np.ndarray]:
        children = []
        length = len(matingpool) - elite_size
        pool = matingpool.copy()
        random.shuffle(pool)

        # Keep elite
        children.extend(matingpool[:elite_size])

        for i in range(0, length):
            child = self.breed(pool[i], pool[len(matingpool) - i - 1])
            children.append(child)
        return children

    def mutate(self, individual: np.ndarray, mutation_rate: float) -> np.ndarray:
        for swapped in range(len(individual)):
            if random.random() < mutation_rate:
                swap_with = int(random.random() * len(individual))

                city1 = individual[swapped]
                city2 = individual[swap_with]

                individual[swapped] = city2
                individual[swap_with] = city1
        return individual

    def mutate_population(self, population: List[np.ndarray], mutation_rate: float) -> List[np.ndarray]:
        mutated_pop = []
        for ind in range(0, len(population)):
            mutated_ind = self.mutate(population[ind], mutation_rate)
            mutated_pop.append(mutated_ind)
        return mutated_pop

    def next_generation(self, current_gen: List[np.ndarray], elite_size: int, mutation_rate: float) -> List[np.ndarray]:
        pop_ranked = self.rank_routes(current_gen)
        selection_results = self.selection(pop_ranked, elite_size)
        matingpool = self.mating_pool(current_gen, selection_results)
        children = self.breed_population(matingpool, elite_size)
        next_generation = self.mutate_population(children, mutation_rate)
        return next_generation

    def genetic_algorithm(
        self, population: np.ndarray, pop_size: int, elite_size: int, mutation_rate: float, generations: int
    ) -> np.ndarray:
        pop = self.initial_population(pop_size, population)

        # Progress logging
        log_interval = max(1, int(generations / 10))

        for i in range(0, generations):
            pop = self.next_generation(pop, elite_size, mutation_rate)
            if (i + 1) % log_interval == 0:
                progress = (i + 1) / generations * 100
                logger.debug(f"Genetic Algorithm Progress: {progress:.1f}%")

        best_route_index = self.rank_routes(pop)[0][0]
        best_route = pop[best_route_index]
        return best_route

    def get_optimized_path(self, city_list: Optional[List[int]] = None) -> List[int]:
        points_coord = np.array(self.points_coord)
        if city_list is None:
            city_list_arr = np.array(range(0, len(points_coord)))
        else:
            city_list_arr = np.array(city_list)

        best_route = self.genetic_algorithm(
            population=city_list_arr, pop_size=400, elite_size=50, mutation_rate=0.02, generations=800
        )

        # Removed the rotation logic (np.roll) as it is incorrect for open paths.
        # The path should respect the order found by the genetic algorithm.

        return best_route.tolist()


if __name__ == "__main__":
    pass
