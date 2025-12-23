import scipy
import numpy as np

from P10_input import PRODUCTION_INPUT

TEST_INPUT = '''
[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}
[...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}
[.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}
'''

def solve(INPUT, mode):
    problems1 = list()
    problems2 = list()
    for row in INPUT.strip().splitlines():
        pieces = row.split(' ')
        assert pieces[0][0] == '['
        assert pieces[0][-1] == ']'
        goal1 = 0
        for i in range(len(pieces[0])-2):
            pos = len(pieces[0])-i-2
            if pieces[0][pos] == '#':
                goal1 |= 1 << i
        size = len(pieces[0])-2
        buttons1 = list()
        buttons2 = list()
        goal2 = list()
        problem1 = [goal1, buttons1]
        for piece in pieces[1:-1]:
            assert piece[0] == '('
            assert piece[-1] == ')'
            value1 = 0
            value2 = [0] * size
            for num in piece[1:-1].split(','):
                value1 |= 1 << (size-1-int(num))
                value2[int(num)] = 1
            buttons1.append(value1)
            buttons2.append(tuple(value2))
        assert pieces[-1][0] == '{'
        assert pieces[-1][-1] == '}'
        for value in pieces[-1][1:-1].split(','):
            goal2.append(int(value))
        problem2 = [np.ones(len(buttons2)), np.matrix(buttons2).transpose(), np.array(goal2)]
        problems1.append(problem1)
        problems2.append(problem2)

    #print('\nProblem1:', problems1)
    #print('\nProblem2:', problems2)

    total1 = 0
    for goal1, buttons in problems1:
        num_buttons = len(buttons)
        best_weight = 0
        for s in range(2**num_buttons):
            value = 0
            weight = 0
            for j in range(num_buttons):
                if s & (1<<j):
                    value ^= buttons[j]
                    weight += 1
            if weight >= best_weight > 0:
                continue
            if value == goal1:
                if best_weight == 0 or weight < best_weight:
                    best_weight = weight
        total1 += best_weight
    print(f'\nPart1 - {mode}: total={total1}')
    print('='*50)

    # Problem2 is linear programming
    # * Minimize sum of x
    # * A.x = b
    total2 = 0
    for c, A_eq, b_eq in problems2:
        #print(c)
        #print(A_eq)
        #print(b_eq)
        solution = scipy.optimize.linprog(c, A_eq=A_eq, b_eq=b_eq, integrality=True)
        total2 += int(solution.fun)
        #print(f'Solution: {int(solution.fun)}')
    print(f'\nPart2 - {mode}: total={total2}')
    print('='*50)

solve(TEST_INPUT, 'test')
solve(PRODUCTION_INPUT, 'prod')
