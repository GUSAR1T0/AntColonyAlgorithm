import math
from dataclasses import dataclass
from typing import List


@dataclass
class Point:
    id: int
    x: float
    y: float

    def __eq__(self, point) -> bool:
        return self.id == point.id

    def __str__(self) -> str:
        return 'Point (ID ' + str(self.id) + '): [' + str(self.x) + '; ' + str(self.y) + ']'


class PointBuilder:
    def __init__(self):
        self.__indexer = 0
        self.__points: List[Point] = []

    def add(self, x: float, y: float):
        self.__indexer += 1
        self.__points.append(Point(self.__indexer, x, y))
        return self

    def build(self) -> List[Point]:
        return self.__points


@dataclass
class Distance:
    point1: Point
    point2: Point
    pheromone: float

    def __eq__(self, distance) -> bool:
        return self.has_points(distance.point1, distance.point2)

    def __str__(self) -> str:
        return 'Distance: [' + str(self.point1) + '; ' + str(self.point2) + '; pheromone = ' + str(self.pheromone) + ']'

    def has_points(self, point1: Point, point2: Point):
        return self.point1 == point1 and self.point2 == point2 or \
               self.point1 == point2 and self.point2 == point1

    def get_distance_length(self) -> float:
        return math.sqrt((self.point1.x - self.point2.x) ** 2 + (self.point1.y - self.point2.y) ** 2)

    def get_visibility(self) -> float:
        return 1 / self.get_distance_length()


class DistanceHelper:
    def __init__(self, points: List[Point]):
        self.points = points
        self.__distances = DistanceHelper.__generate_distances_from_points(points)

    @staticmethod
    def __generate_distances_from_points(points: List[Point]) -> List[Distance]:
        result = []
        for i in range(len(points) - 1):
            for j in range(i + 1, len(points)):
                result.append(Distance(points[i], points[j], 1))
        return result

    def get_distance(self, point1: Point, point2: Point) -> Distance or None:
        for distance in self.__distances:
            if distance.has_points(point1, point2):
                return distance

    def get_point(self, id: int) -> Point or None:
        for point in self.points:
            if point.id == id:
                return point

    def pheromone_recalculation(self, rho: float, q: int, distance_length: float):
        for distance in self.__distances:
            distance.pheromone = (1 - rho) * distance.pheromone + q / distance_length
