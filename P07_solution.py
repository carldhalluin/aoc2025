from collections import defaultdict

from P07_input import PRODUCTION_INPUT

TEST_INPUT = '''
.......S.......
...............
.......^.......
...............
......^.^......
...............
.....^.^.^.....
...............
....^.^...^....
...............
...^.^...^.^...
...............
..^...^.....^..
...............
.^.^.^.^.^...^.
...............
'''

def solve(INPUT):
    lines = INPUT.strip().splitlines()
    linelen = len(lines[0])
    assert all(len(line)==linelen for line in lines)
    assert all(line[0]=='.' for line in lines)
    assert all(line[-1]=='.' for line in lines)
    assert lines[0].count('S') == 1
    beams = {lines[0].find('S'):1}   # {beam_offset: effective_num_beams}
    hit_count = 0
    for linenum, line in enumerate(lines):
        if linenum == 0:
            continue
        if linenum % 2 == 1:
            assert all(c=='.' for c in line)
            continue
        new_beams = defaultdict(lambda : 0)
        for beam_offset, beam_count in beams.items():
            if line[beam_offset] == '.':
                new_beams[beam_offset] += beam_count
            elif line[beam_offset] == '^':
                hit_count += 1
                # safe to do -1 and +1 since there are no splitters in first and last column
                new_beams[beam_offset-1] += beam_count
                new_beams[beam_offset+1] += beam_count
        beams = new_beams
    return [("part1", hit_count), ("part2", sum(beams.values()))]


print(f'Test: {solve(TEST_INPUT)}')
print(f'Prod: {solve(PRODUCTION_INPUT)}')
