import random
import pickle
from pathlib import Path

import numpy as np

from .structures import Polygon
from .config import resources_path


def split_on_intervals(min_val, max_val, n) -> list[float]:
    step = (max_val - min_val) / n
    intervals = [min_val + (step * x) for x in range(n + 1)]
    return intervals


class GeneticOptimizer:
    def __init__(self, model_filename='base_model.pickle', map_config=(55.95, 55.55, 37.3, 37.9)):
        with open(Path(resources_path, model_filename), "rb") as model_file:
            self.model = pickle.load(model_file)

        self.map_config = map_config

    def find_optimum(self, num_polygons: int, num_banners: int, TA: dict[str, ...] = None, iters=50,
                     num_entities=30, top_to_change=10, bottom_to_change=20, cross_iterations=30,
                     mutation_iterations_1=30, mutation_iterations_2=20) -> list[tuple[float, list[int]]]:
                            # sorted list of strategies: float - value (target), list[int] - banner distribution

        self.num_banners = num_banners
        self.num_polygons = num_polygons
        self.num_entities = num_entities

        if TA is None:
            self.TA = {"gender": ["all"], "ageFrom": [18], "ageTo": [100], "income": ["abc"]}
        else:
            self.TA = {}
            for key in TA.keys():
                if key in ["gender", "ageFrom", "ageTo", "income"]:
                    self.TA[key] = [TA[key]]

        n_groups = int(np.sqrt(num_polygons))
        self.x_intervals = split_on_intervals(self.map_config[0], self.map_config[1], n_groups)
        self.y_intervals = split_on_intervals(self.map_config[2], self.map_config[3], n_groups)
        self.n_groups = n_groups

        self.entities_init()

        initial_pop = [(self.get_penalty(self.metric_calculator(i)), i) for i in self.initial_data]

        self.entities_pop = initial_pop.copy()
        self.checked = [x[1] for x in self.entities_pop]

        for i in range(iters):
            # print(f'>> {i}')

            self.search_step(top_to_change, bottom_to_change, cross_iterations, mutation_iterations_1, mutation_iterations_2)

            list_of_scores = [abs(i[0]) for i in self.entities_pop]

            # print('max:', max(list_of_scores), '|', 'avg:', sum(list_of_scores) / len(list_of_scores))

        self.entities_pop.sort()

        return [(abs(float(x[0])), x[1]) for x in self.entities_pop]

    def search_step(self, top_to_change=15, bottom_to_change=15, cross_iterations=20, mutation_iterations_1=40, mutation_iterations_2=40) -> None:
        self.entities_pop.sort()
        best_entities = [x[1] for x in self.entities_pop[:top_to_change]]
        worst_entities = [x[1] for x in self.entities_pop[-bottom_to_change:]]

        # print([int(x[0]) for x in self.entities_pop[:top_to_change]])
        # print()
        # print([int(x[0]) for x in self.entities_pop[-bottom_to_change:]])

        new_entities = self.create_new_entity(
            best_entities, worst_entities,
            bottom_to_change, cross_iterations, mutation_iterations_1, mutation_iterations_2
        )

        entities_pop = new_entities + self.entities_pop
        self.entities_pop = entities_pop[:-bottom_to_change]

        self.checked.extend([x[1] for x in new_entities])
        # self.checked.extend(worst_entities)

    def create_new_entity(self, top_best_entities: list[list[int]], worst_entities: list[list[int]],
                          to_generate, cross_iterations,
                          mutation_iterations_1, mutation_iterations_2) -> list[tuple[float, list[int]]]:

        # current_entities = [x[1] for x in self.entities_pop]
        raw_generation = top_best_entities.copy()

        for _ in range(cross_iterations):  # скрещивание
            parent1 = random.choice(top_best_entities)
            parent2 = random.choice(top_best_entities)

            child1 = parent1[:self.num_polygons // 2] + parent2[self.num_polygons // 2:]
            child2 = parent2[:self.num_polygons // 2] + parent1[self.num_polygons // 2:]

            raw_generation.extend([self.normalize(child1), self.normalize(child2)])

        for _ in range(mutation_iterations_1):
            entity = random.choice(raw_generation)
            pos1 = random.randint(0, self.num_polygons - 1)
            pos2 = random.randint(0, self.num_polygons - 1)
            new_entity = entity.copy()
            new_entity[pos1], new_entity[pos2] = new_entity[pos2], new_entity[pos1]
            raw_generation.append(new_entity)

        for _ in range(mutation_iterations_2):
            entity = random.choice(raw_generation)
            pos1 = random.randint(0, self.num_polygons - 1)
            pos2 = random.randint(0, self.num_polygons - 1)
            if pos1 != pos2:
                new_entity = entity.copy()
                new_entity[pos1] += new_entity[pos2]
                new_entity[pos2] = 0

                raw_generation.append(new_entity)

        clear_generation = [i for i in raw_generation if i[0] not in worst_entities]  # current_entities, checked

        if clear_generation:
            raw_generation = [(self.get_penalty(self.metric_calculator(i)), i) for i in clear_generation]
        else:
            print('Bad situation')
            raw_generation = [(self.get_penalty(self.metric_calculator(i)), i) for i in raw_generation]

        new_entities = sorted(raw_generation)[:to_generate]

        return new_entities

    @staticmethod
    def get_penalty(pred_metric: float) -> float:
        return -pred_metric

    def metric_calculator(self, genome: list[int]) -> float:
        points = self.get_cords(genome)
        return self.model.predict(self.TA, points)

    def normalize(self, bad_genome: list[int]) -> list[int]:
        target = self.num_banners

        if sum(bad_genome) < target:
            pos = random.randint(0, len(bad_genome) - 1)
            bad_genome[pos] += target - sum(bad_genome)

        if sum(bad_genome) > target:
            while sum(bad_genome) > target:
                max_pos = bad_genome.index(max(bad_genome))
                bad_genome[max_pos] -= 1

        return bad_genome

    def get_cords(self, genome: list[int]) -> list[dict[str, float]]:
        points = []
        for i in range(len(genome)):
            try:
                for _ in range(genome[i]):
                    y_i, x_i = i % self.n_groups, i // self.n_groups
                    points.append({'lat': (self.x_intervals[x_i] + self.x_intervals[x_i + 1]) / 2,
                                   'lon': (self.y_intervals[y_i] + self.y_intervals[y_i + 1]) / 2, 'azimuth': 0})

            except:
                print('bad')

        return points

    def get_polygons(self, genome: list[int]) -> list[Polygon]:
        print(genome)

        polygons = []
        for i in range(len(genome)):
            if genome[i] > 0:
                y_i, x_i = i % self.n_groups, i // self.n_groups

                polygons.append(
                    Polygon(
                        lon_left=self.y_intervals[y_i],
                        lon_right=self.y_intervals[y_i + 1],
                        lat_bottom=self.x_intervals[x_i],
                        lat_top=self.x_intervals[x_i + 1],
                        count=genome[i]
                    )
                )

        return polygons

    def entities_init(self):  # n-sum, m-len, k-count
        n = self.num_banners
        m = self.num_polygons
        k = self.num_entities

        ans = []
        for _ in range(k):
            a = [n // m] * m
            ost = n - (n // m * m)

            first = random.randint(0, m - ost)

            for i in range(first, first + ost):
                a[i] += 1

            ans.append(a)

        self.initial_data = ans


genetic_optimizer = GeneticOptimizer()
