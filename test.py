"""Script for solving and plotting all solutions to the queens puzzle: How to place
n queens on an n x n chessboard in such a way that none of them threaten each other.
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import seaborn
from typing import Generator, List


# The number of queens to place (and thus the size of the board)
num_queens = 1000


# The algorithm is based on backtracking: A "partial solution" is a way to place
# m queens in the first m columns on the chessboard so that none of them threaten
# each other. Starting from the n partial solutions for m = 1, we expand each solution
# one column at a time. If we ever come across an expansion which is no longer a
# partial solution, we throw away that expansion entirely, as it will never lead to
# an actual solution.
#
# Possible partial solutions are represented by lists of m integers between 0 and n - 1,
# so that the j'th entry corresponds to the position of the j'th queen.


def is_partial_solution(possible_solution: List[int]) -> bool:
    """Return true iff the given list of m integers represents a partial solution,
    assuming that the m - 1 first integers in the list represent a partial solution.
    """
    m = len(possible_solution)
    # Figure out the three forbidden squares for the m'th queen, from the perspective
    # of each of the first m - 1 queens.
    forbidden_squares = (possible_solution[i] + x*(m-i-1) for i in range(m - 1)
                         for x in (-1, 0, 1))
    return not possible_solution[m - 1] in forbidden_squares


def expand_solutions(partial_solutions: List[List[int]]) -> Generator[List[int], None, None]:
    """Given a list of partial solutions, yields all partial solutions with one more queen
    than the given ones.
    """
    return (partial_solution + [column] for partial_solution in partial_solutions
            for column in range(num_queens)
            if is_partial_solution(partial_solution + [column]))


def find_all_solutions() -> Generator[List[int], None, None]:
    """Yield all complete solutions with `num_queens` placed."""
    # Start with the trivial solution in the case of 0 queens, and iteratively
    # build it up until all queens have been placed.
    partial_solutions = [[]]
    for _ in range(num_queens):
        partial_solutions = expand_solutions(partial_solutions)
    return partial_solutions


def plot_solution(solution: List[int]) -> None:
    """Given a solution, plot it and save the result to disk."""
    fig = plt.figure()
    ax = fig.add_subplot(111, aspect='equal')
    ax.set_xlim((0, num_queens))
    ax.set_ylim((0, num_queens))

    count = 0
    # print(solution)
    for queen in solution:
        # print(queen)
        ax.add_patch(patches.Rectangle((queen, count), 1, 1))
        count += 1
    fig.savefig('4-puzzle' + '.png', dpi=150, bbox_inches='tight')
    plt.close(fig)


def main() -> None:
    solutions = list(find_all_solutions())
    print('In total: %d solutions' % len(solutions))
    plot_solution(solutions[0])


"""
    count = 1
    #print(solutions)
    
    for solution in solutions:
        print('Plotting solution %d/%d: ' %
              (count, len(solutions)) + str(solution))
    count += 1
"""


if __name__ == '__main__':
    main()
