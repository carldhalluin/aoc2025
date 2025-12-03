from P03_input import PRODUCTION_INPUT

TEST_INPUT = '''987654321111111
811111111111119
234234234234278
818181911112111
'''

INPUT = TEST_INPUT
INPUT = PRODUCTION_INPUT

banks = list()
for row in INPUT.strip().splitlines():
    row = row.strip()
    bank = [int(battery) for battery in row]
    banks.append(bank)

def find_first_max_offset(bank):
    assert len(bank) > 0
    max_value = bank[0]
    max_offset = 0
    for offset, value in enumerate(bank):
        if value > max_value:
            max_offset = offset
            max_value = value
    return max_offset, max_value

for NUM_ENTRIES in [2, 12]:
    total = 0
    for bank in banks:
        result = 0
        offset = -1
        for counter in range(NUM_ENTRIES):
            rel_offset, value = find_first_max_offset(bank[offset+1:len(bank)-NUM_ENTRIES+counter+1])
            offset += rel_offset + 1
            result = result * 10 + value
        #print(f'{bank} -> {result}')
        total += result

    print(f'Problem for {NUM_ENTRIES} entries: {total}')
