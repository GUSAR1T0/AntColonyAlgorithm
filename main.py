from ant import AntBuilder
from geometry import PointBuilder
from resolver import Resolver

points = PointBuilder() \
    .add(10, 45) \
    .add(67, 32) \
    .add(25, 25) \
    .add(98, 1) \
    .add(50, 12) \
    .build()

ants = AntBuilder() \
    .add(points[0]) \
    .add(points[1]) \
    .add(points[2]) \
    .add(points[3]) \
    .add(points[4]) \
    .build()

resolver = Resolver(points, ants)
result = resolver.resolve(max_iterations=1)
result.show_plot()
print(result)
