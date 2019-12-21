import random
from typing import List, Dict

from ant import Ant
from geometry import DistanceHelper, Point, Distance
from result import Result


class Resolver:
    def __init__(self, points, ants, **kwargs):
        self.helper = DistanceHelper(points)
        self.ants = ants
        self.alpha = kwargs["alpha"] if kwargs.__contains__("alpha") else 1
        self.beta = kwargs["beta"] if kwargs.__contains__("beta") else 1
        self.rho = kwargs["rho"] if kwargs.__contains__("rho") else 0.5
        self.q = kwargs["q"] if kwargs.__contains__("q") else 1

    def __define_available_points(self, ant: Ant) -> List[Point]:
        available_points = []
        for point in self.helper.points:
            if ant.can_go_to(point):
                available_points.append(point)
        return available_points

    def __calculate_block(self, distance: Distance) -> float:
        return distance.get_visibility() ** self.beta * distance.pheromone ** self.alpha

    def __get_probabilities(self, ant: Ant, available_points: List[Point]) -> Dict[int, float]:
        probabilities = {}
        for point1 in available_points:
            distance1 = self.helper.get_distance(ant.last_point, point1)
            numerator = self.__calculate_block(distance1)
            denominator = numerator
            for point2 in available_points:
                if point2 != point1:
                    distance2 = self.helper.get_distance(ant.last_point, point2)
                    denominator += self.__calculate_block(distance2)
            probabilities[point1.id] = numerator / denominator
        return probabilities

    @staticmethod
    def __get_new_point(probabilities: Dict[int, float]) -> int or None:
        random_number = random.random()
        start_interval = 0
        for id in probabilities:
            if start_interval <= random_number < start_interval + probabilities[id]:
                return id
            else:
                start_interval += probabilities[id]

    def __add_new_point(self, ant: Ant, point_id: int):
        new_point = self.helper.get_point(point_id)
        new_distance = self.helper.get_distance(ant.last_point, new_point)
        ant.go_to(new_point, new_distance)

    def resolve(self, max_iterations: int = 1) -> Result:
        result = Result()

        for ant in self.ants:
            for iteration in range(max_iterations):
                while True:
                    available_points = self.__define_available_points(ant)
                    count = len(available_points)
                    if count >= 1:
                        if count > 1:
                            probabilities = self.__get_probabilities(ant, available_points)
                            id = self.__get_new_point(probabilities)
                        else:
                            id = available_points[0].id

                        self.__add_new_point(ant, id)
                    else:
                        self.__add_new_point(ant, ant.first_point.id)
                        break

                result.complete_ant_cycle(ant)
                self.helper.pheromone_recalculation(self.rho, self.q, result.length[ant.id])

        return result
