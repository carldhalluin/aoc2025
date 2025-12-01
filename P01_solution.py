
INPUT = '''L68
L30
R48
L5
R60
L55
L1
L99
R14
L82'''

from P01_input import INPUT

commands = INPUT.strip().splitlines()

def solve():
    value = 50 # Initial value
    count1 = 0
    count2 = 0
    for command in commands:
        delta = int(command[1:])
        assert delta != 0
        if command[0] == 'L':
            delta = -delta
        else:
            assert command[0] == 'R'
        oldvalue = value
        value = value + delta

        if value % 100 == 0:
            count1 += 1

        oldrange = oldvalue // 100
        newrange = value // 100
        count2 += abs(newrange - oldrange)
        if delta < 0:
            # Move to the left
            if oldvalue % 100 == 0:
                # source started at a boundary -> do not count (e.g. going from 200 to 180)
                count2 -= 1
            if value % 100 == 0:
                # target is at a boundary -> do count (e.g. going from 10 to 0)
                count2 += 1
       
        result = {'part1':count1, 'part2':count2}
        print(f'{command} : {oldvalue}->{value} / {oldrange}->{newrange} / {result}')

    return result

print(f'\nresult = {solve()}')
