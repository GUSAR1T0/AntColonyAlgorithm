from dataclasses import dataclass, field
from typing import List, Dict

import matplotlib.pyplot as plt

from geometry import Point


@dataclass
class Result:
    length: Dict[int, float] = field(default_factory=dict)
    chain: Dict[int, List[Point]] = field(default_factory=dict)

    def __str__(self):
        result = 'The best results are: \n'
        for i, element in enumerate(self.length):
            result += ' - FOR ANT ' + str(element) + '\n'
            result += '       Length: ' + str(self.length[element]) + '\n'
            result += '       Chain: ' + str(self.chain[element][0])
            for j in range(1, len(self.chain[element])):
                result += ' -> ' + str(self.chain[element][j])
            result += '\n'
        return result

    def show_plot(self):
        for id in self.chain:
            plt.subplot()
            for index in range(1, len(self.chain[id])):
                from_ = list(self.chain[id])[index - 1]
                to_ = list(self.chain[id])[index]
                plt.scatter(to_.x, to_.y, marker='o', color='red')
                plt.arrow(from_.x, from_.y, to_.x - from_.x, to_.y - from_.y,
                          head_width=2, head_length=2, linewidth=1, color='green', length_includes_head=True)
                plt.text(to_.x + .05, to_.y + .05, '   p.' + str(to_.id) + ' [' + str(to_.x) + '; ' + str(to_.y) + ']',
                         fontsize=9)

            plt.xlabel('X')
            plt.ylabel('Y')
            plt.title('Ant Colony Optimization – ant ' + str(id))

            plt.show()

    def complete_ant_cycle(self, ant):
        length, chain = ant.complete_cycle()
        if not self.length.__contains__(ant.id) or length < self.length[ant.id]:
            self.length[ant.id] = length
            self.chain[ant.id] = chain
