
PROD_INPUT = '''19391-47353,9354357-9434558,4646427538-4646497433,273-830,612658-674925,6639011-6699773,4426384-4463095,527495356-527575097,22323258-22422396,412175-431622,492524-611114,77-122,992964846-993029776,165081-338962,925961-994113,7967153617-7967231799,71518058-71542434,64164836-64292066,4495586-4655083,2-17,432139-454960,4645-14066,6073872-6232058,9999984021-10000017929,704216-909374,48425929-48543963,52767-94156,26-76,1252-3919,123-228'''

TEST_INPUT = '''11-22,95-115,998-1012,1188511880-1188511890,222220-222224,
1698522-1698528,446443-446449,38593856-38593862,565653-565659,
824824821-824824827,2121212118-2121212124'''

INPUT = TEST_INPUT
INPUT = PROD_INPUT

# Find ranges of a fixed length
single_length_ranges = list()
max_len = 0
for a, b in [(a for a in s.strip().split('-')) for s in INPUT.split(',')]:
    assert a[0] != '0'
    assert b[0] != '0'
    lena = len(a)
    lenb = len(b)
    inta = int(a)
    intb = int(b)
    max_len = max(max_len, lenb)
    assert intb > inta > 0
    if lena == lenb:
        single_length_ranges.append((inta, intb))
    elif lena == lenb-1:
        boundary = int('9' * lena)
        single_length_ranges.append((inta, boundary))
        boundary = int('1' + ('0' * (lenb-1)))
        single_length_ranges.append((boundary, intb))
    else:
        raise Exception('wrong range')

print(f'CLEAN RANGES = {single_length_ranges}')
print(f'MAX LEN      = {max_len}')
assert max_len <= 11
MAX_NUM_PARTS = 11

# MAX_NUM_PARTS = 11
# len=1  -> N/A
# len=2  -> 2
# len=3  -> 3 
# len=4  -> 2 (will include 4's)
# len=5  -> 5
# len=6  -> 2 + 3 - 6   => ABCABC  +  ABABAB  - AAAAAA
# len=7  -> 7
# len=8  -> 2 (will include 4's and 8's)
# len=9  -> 3 (will include 9's)
# len=10 -> 2 + 5 - 10  => ABCDEABCDE + ABABABABAB - AAAAAAAAAA
# len=11 -> 11

# Valid number of parts for problems 1 and 2
PART_DICT_p1 = {2:[2], 4:[2], 6:[2], 8:[2], 10:[2]}
PART_DICT_p2 = {2:[2], 3:[3], 4:[2], 5:[5], 6:[2,3,6], 7:[7], 8:[2], 9:[3], 10:[2,5,10], 11:[11]}

for problem, PART_DICT in {"Problem1":PART_DICT_p1, "Problem2":PART_DICT_p2}.items():
    print('=' * 40)
    grand_total = 0

    for a, b in single_length_ranges:
        l = len(str(a))
        assert len(str(b)) == l
        totals = list()
        print(f'\nRANGE {a}-{b}')
        SELECTED_NUMPARTS = PART_DICT.get(l, list())
        for NUMPARTS in SELECTED_NUMPARTS:
            total = 0
            if l % NUMPARTS != 0:
                continue
            lefta = int(str(a)[:l//NUMPARTS])
            leftb = int(str(b)[:l//NUMPARTS])
     
            multiplier = int((('0' * (len(str(lefta))-1)) + '1') * NUMPARTS)
     
            if lefta < leftb:
                # Calculate sum of (lefta+1)_(lefta+1), ..., (leftb-1)_(leftb-1)
                base_sum = (leftb - lefta - 1) * lefta + (leftb - lefta - 1) * (leftb - lefta) // 2
                total += multiplier * base_sum
                print(f'    [{NUMPARTS}] added {multiplier} * {base_sum} = {multiplier * base_sum} (*)')
                if a <= multiplier * lefta:
                    total += multiplier * lefta
                    print(f'    [{NUMPARTS}] added {multiplier * lefta} (<)')
                if b >= multiplier * leftb:
                    total += multiplier * leftb
                    print(f'    [{NUMPARTS}] added {multiplier * leftb} (>)')
            else:
                assert lefta == leftb
                if a <= multiplier * lefta <= b:
                    total += multiplier * lefta
                    print(f'    [{NUMPARTS}] added {multiplier * lefta} (.)')
            totals.append(total)
        print(f'    RESULT FOR NUMPARTS {SELECTED_NUMPARTS} = {totals}')
        if len(totals) == 1:
            grand_total += totals[0]
        elif len(totals) == 0:
            pass
        else:
            assert len(totals) == 3
            # e.g. for len 6 need to count sum(2parts) + sum(3parts) - sum(6parts)
            grand_total += totals[0] + totals[1] - totals[2]
     
    print(f'\n\n{problem}: grand_total = {grand_total}')
