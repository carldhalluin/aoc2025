from P05_input import PRODUCTION_INPUT

TEST_INPUT = '''
3-5
10-14
16-20
12-18

1
5
8
11
17
32
'''

def solve(modus, INPUT):
    ranges = list()
    ingredients = set()
    mode = 'ranges'
    for line in INPUT.strip().splitlines():
        if mode == 'ranges':
            if line.strip() == '':
                mode = 'ingredients'
                continue
            from_, to_ = map(int, line.split('-'))
            assert from_ <= to_
            ranges.append((from_, to_))
        else:
            ingredient = int(line)
            assert ingredient not in ingredients
            ingredients.add(ingredient)

    clean_ranges = list()
    for from_, to_ in ranges:
        for cfrom_, cto_ in clean_ranges[:]:  # A copy of clean_ranges
            if (from_ <= cfrom_ <= to_) or (cfrom_ <= from_ <= cto_):
                # overlapping range
                from_ = min(from_, cfrom_)
                to_ = max(to_, cto_)
                clean_ranges.remove((cfrom_, cto_))
        clean_ranges.append((from_, to_))
    #print(clean_ranges)

    count = 0
    for ingredient in ingredients:
        for from_, to_ in clean_ranges:
            if from_ <= ingredient <= to_:
                #print(f'{from_} <= {ingredient} <= {to_}')
                count += 1
                break
    print(f'part 1 {modus}: {count}')

    count = 0
    for from_, to_ in clean_ranges:
        count += (to_ - from_ + 1)
    print(f'part 2 {modus}: {count}')

solve('test', TEST_INPUT)
solve('prod', PRODUCTION_INPUT)
