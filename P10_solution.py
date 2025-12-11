from P10_input import PRODUCTION_INPUT

TEST_INPUT = '''
[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}
[...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}
[.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}
'''

def solve_part1(INPUT, mode):
    problems = list()
    for row in INPUT.strip().splitlines():
        pieces = row.split(' ')
        assert pieces[0][0] == '['
        assert pieces[0][-1] == ']'
        goal = 0
        for i in range(len(pieces[0])-2):
            pos = len(pieces[0])-i-2
            if pieces[0][pos] == '#':
                goal |= 1 << i
        goalsize = len(pieces[0])-2
        buttons = list()
        problem = [goal, buttons]
        for piece in pieces[1:-1]:
            assert piece[0] == '('
            assert piece[-1] == ')'
            value = 0
            for num in piece[1:-1].split(','):
                value |= 1 << (goalsize-1-int(num))
            buttons.append(value)
        problems.append(problem)

    #print(f'Problems: {problems}')

    total = 0
    for goal, buttons in problems:
        #print(f'\n\ngoal {goal} buttons {buttons}')
        num_buttons = len(buttons)
        best_weight = 0
        for s in range(2**num_buttons):
            value = 0
            weight = 0
            for j in range(num_buttons):
                if s & (1<<j):
                    value ^= buttons[j]
                    weight += 1
                    #print(f'Pressed button {j} to get value {value}')
            #print(f'value {value} weight {weight}')
            if weight >= best_weight > 0:
                continue
            if value == goal:
                #print(f'Goal {goal} reached in {weight}: {bin(s)[2:]} * {[bin(button)[2:] for button in buttons]}')
                if best_weight == 0 or weight < best_weight:
                    best_weight = weight
        #print(f'best weight for goal {goal} = {best_weight}')
        total += best_weight
    print(f'{mode}: total={total}')

solve_part1(TEST_INPUT, 'test')
solve_part1(PRODUCTION_INPUT, 'prod')
