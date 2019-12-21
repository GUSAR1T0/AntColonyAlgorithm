from typing import List, Tuple

from geometry import Point, Distance


class Ant:
    def __init__(self, id: int, first_point: Point):
        self.id = id
        self.first_point = first_point
        self.last_point = first_point
        self.__distances: List[Distance] = []

    def can_go_to(self, point: Point) -> bool:
        if self.last_point == point:
            return False

        for distance in self.__distances:
            if distance.point1 == point or distance.point2 == point:
                return False

        return True

    def go_to(self, new_point: Point, distance: Distance):
        self.__distances.append(distance)
        self.last_point = new_point

    def complete_cycle(self) -> Tuple[float, List[Point]]:
        chain = [self.first_point]
        distance_length = 0
        current_point = self.first_point
        for distance in self.__distances:
            distance_length += distance.get_distance_length()
            current_point = distance.point2 if current_point == distance.point1 else distance.point1
            chain.append(current_point)
        self.last_point = self.first_point
        self.__distances.clear()
        return distance_length, chain


class AntBuilder:
    def __init__(self):
        self.__indexer = 0
        self.__ants: List[Ant] = []

    def add(self, first_point: Point):
        self.__indexer += 1
        self.__ants.append(Ant(self.__indexer, first_point))
        return self

    def build(self) -> List[Ant]:
        return self.__ants
