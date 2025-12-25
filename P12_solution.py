from P12_input import PRODUCTION_INPUT

def solve(INPUT):
    shapestr = list()
    current_chunk = list()
    for line in INPUT.strip().splitlines():
        current_chunk.append(line)
        if line == '':
            assert(len(current_chunk) == 5)
            shapestr.extend(current_chunk)
            current_chunk = list()
    puzzles = current_chunk
    assert(len(shapestr) % 5 == 0)
    num_shapes = len(shapestr) // 5
    shapes = list()
    for i in range(num_shapes):
        count = 0
        for j in range(1,4):
            assert len(shapestr[i*5+j]) == 3
            count += shapestr[i*5+j].count('#')
        shapes.append(count)

    good = 0  # certainly fits
    bad = 0   # certainly does not fit
    ugly = 0  # no idea if it fits
    for puzzle in puzzles:
        sizestr, numpiecesstr = puzzle.split(': ')
        w, h = [int(size) for size in sizestr.split('x')]
        numpieces = [int(p) for p in numpiecesstr.split(' ')]
        assert(len(numpieces)==num_shapes)
        area_available = w * h
        area_needed = sum([a*b for a,b in zip(shapes, numpieces)])
        print(f'{w}x{h}={area_available} // {numpieces} requires area {area_needed}')
        if area_available < area_needed:
            print('    NOK')
            bad += 1
            continue
        lowerbound = (w//3) * (h//3)
        if lowerbound >= sum(numpieces):
            print(f'    OK ({w//3}x{h//3}={lowerbound} boxes available; only need {sum(numpieces)}')
            good += 1
            continue
        print('    NO IDEA')
        ugly += 1

    assert ugly == 0
    print(f'\n\nFound a solution!! good(answer)={good}, bad={bad}, ugly={ugly}')

        
solve(PRODUCTION_INPUT)
