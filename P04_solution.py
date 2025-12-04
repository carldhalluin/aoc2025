
from P04_input import PRODUCTION_INPUT

TEST_INPUT = '''
..@@.@@@@.
@@@.@.@.@@
@@@@@.@.@@
@.@@@@..@.
@@.@@@@.@@
.@@@@@@@.@
.@.@.@.@@@
@.@@@.@@@@
.@@@@@@@@.
@.@.@@@.@.
'''

def solve(input_rows, part_number):

    input_rows = INPUT.strip().splitlines()

    NUM_ROWS = len(input_rows)
    NUM_COLS = len(input_rows[0])
    assert all(len(row) == NUM_COLS for row in input_rows)

    rows = list()
    rows.append([x for x in ('.' * (NUM_COLS+2))])
    for row in input_rows:
        rows.append([x for x in ('.' + row + '.')])
    rows.append([x for x in ('.' * (NUM_COLS+2))])

    NUM_ROWS = len(rows)
    NUM_COLS = len(rows[0])

    total_num_rolls_removed = 0
    num_rolls_removed_in_last_run = -1
    is_first_run = True
    while num_rolls_removed_in_last_run != 0:
        if part_number==1 and not is_first_run:
            break
        is_first_run = False
        rolls_to_remove = list()
        for i in range(1, NUM_ROWS-1):
            for j in range(1, NUM_COLS-1):
                if rows[i][j] == 'x':
                    rows[i][j] = '.'
                    continue
                if rows[i][j] != '@':
                    continue
                s = [rows[i-1][j-1], rows[i-1][j], rows[i-1][j+1], rows[i][j-1], rows[i][j+1], rows[i+1][j-1], rows[i+1][j], rows[i+1][j+1]]
                if s.count('@')<4:
                    rolls_to_remove.append((i, j))
        num_rolls_removed_in_last_run = len(rolls_to_remove)
        total_num_rolls_removed += num_rolls_removed_in_last_run
        for i,j in rolls_to_remove:
            rows[i][j] = 'x'
    return total_num_rolls_removed

for part_number in (1, 2):
    for input_name, INPUT in [('test', TEST_INPUT), ('prod', PRODUCTION_INPUT)]:
        print(f'\n{input_name} Solution of part {part_number}: {solve(INPUT, part_number)}')
