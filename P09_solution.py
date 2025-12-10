from P09_input import PRODUCTION_INPUT

TEST_INPUT = '''
7,1
11,1
11,7
9,7
9,5
2,5
2,3
7,3
'''

def solve_part1(INPUT):
    tiles = list()
    for line in INPUT.strip().splitlines():
        i, j = line.strip().split(',')
        tiles.append((int(i),int(j)))
    max_area = 0
    for t1 in range(len(tiles)-1):
        for t2 in range(t1, len(tiles)):
            area = ((abs(tiles[t1][0]-tiles[t2][0])+1) * (abs(tiles[t1][1]-tiles[t2][1])+1))
            max_area = max(max_area, area)
    return max_area


print(f'\nTest part 1: {solve_part1(TEST_INPUT)}')
print(f'\nProd part 1: {solve_part1(PRODUCTION_INPUT)}')
print('='*50)

def merge_into_masks(interval, masks):
    interval_from, interval_to = interval
    if len(masks) == 0:
        # Insert as new (first) mask
        masks.insert(0, interval)
        return
    if interval_from > masks[-1][1]:
        # Insert as new mask at the end
        masks.append(interval)
        return
    processed = False
    NUM_MASKS = len(masks)
    shrunk = False
    for i, (mask_from, mask_to) in enumerate(masks[:]):
        if interval_from > mask_to:
            # look at next mask
            continue
        if interval_to < mask_from:
            # insert before this mask
            masks.insert(i, interval) 
            processed = True
            break
        if interval_to == mask_from:
            processed = True
            # Glue together at left side of mask
            masks[i] = (interval_from, mask_to)
            break
        if interval_from == mask_to:
            processed = True
            # Glue together at right side
            if i < NUM_MASKS-1:
                # Possibly glue also to next mask
                next_mask_from, next_mask_to = masks[i+1]
                if interval_to == next_mask_from:
                    masks.pop(i+1)
                    masks[i] = (mask_from, next_mask_to)
                    break
                if interval_to > next_mask_from:
                    raise Exception('HEELP')
            masks[i] = (mask_from, interval_to)
            break
        if interval_from == mask_from:
            processed = True
            if interval_to == mask_to:
                masks.pop(i)
                shrunk = True
                break
            # Shrink at left side
            assert mask_to >= interval_to
            masks[i] = (interval_to, mask_to)
            shrunk = True
            break
        if interval_to == mask_to:
            processed = True
            # Shrink at right side
            assert mask_from <= interval_from
            masks[i] = (mask_from, interval_from)
            shrunk = True
            break
        if interval_from > mask_from and interval_to < mask_to:
            # Split
            processed = True
            masks[i] = (mask_from, interval_from)
            masks.insert(i+1, (interval_to, mask_to))
            shrunk = True
            break
        raise Exception(f'Wat moet ik nu doen? interval=({interval_from, interval_to}) mask=({mask_from, mask_to})')
    if not processed:
        raise Exception(f'AARGH NIET GEPROCESSD')
    return shrunk

# ram or cam = [((1, 2), [(7, 11)]), ((3, 5), [(2, 11)]), ((6, 7), [(9, 11)])]
def is_legal(rowmin, rowmax, colmin, colmax, row_active_masks, col_active_masks):
    for (maskrowmin, maskrowmax), masks in row_active_masks:
        if maskrowmin <= rowmin <= maskrowmax or maskrowmin <= rowmax <= maskrowmax:
            # at least one overlapping row
            for maskcolmin, maskcolmax in masks:
                if colmin <= maskcolmin <= colmax or colmin <= maskcolmax <= colmax:
                    # at least one overlapping column
                    covered = maskcolmin <= colmin <= colmax <= maskcolmax
                    if not covered:
                        return False
                    else:
                        break
    for (maskcolmin, maskcolmax), masks in col_active_masks:
        if maskcolmin <= colmin <= maskcolmax or maskcolmin <= colmax <= maskcolmax:
            # at least one overlapping col
            for maskrowmin, maskrowmax in masks:
                if rowmin <= maskrowmin <= rowmax or rowmin <= maskrowmax <= rowmax:
                    # at least one overlapping row
                    covered = maskrowmin <= rowmin <= rowmax <= maskrowmax
                    if not covered:
                        return False
                    else:
                        break
    return True

def solve_part2(INPUT):
    rctiles = list()
    crtiles = list()
    for line in INPUT.strip().splitlines():
        col, row = line.strip().split(',')
        rctiles.append((int(row),int(col)))
        crtiles.append((int(col),int(row)))
    rctiles.sort()
    crtiles.sort()
    NUM_TILES = len(rctiles)
    assert len(crtiles) == NUM_TILES
    assert NUM_TILES % 2 == 0

    rowdict = dict()
    coldict = dict()
    for i in range(NUM_TILES//2):
        assert rctiles[i*2][0] == rctiles[i*2+1][0]
        assert crtiles[i*2][0] == crtiles[i*2+1][0] 
        if i>0:
            assert rctiles[i*2][0] != rctiles[i*2-1][0]
            assert crtiles[i*2][0] != crtiles[i*2-1][0]
        assert rctiles[i*2+1][1] - rctiles[i*2][1] > 1
        assert crtiles[i*2+1][1] - crtiles[i*2][1] > 1
        rowdict[rctiles[i*2][0]] = (rctiles[i*2][1], rctiles[i*2+1][1])
        coldict[crtiles[i*2][0]] = (crtiles[i*2][1], crtiles[i*2+1][1])

    rdi = sorted(rowdict.items())
    cdi = sorted(coldict.items())
    # rdi = [(1, (7, 11)), (3, (2, 7)), (5, (2, 9)), (7, (9, 11))]
    # cdi = [(2, (3, 5)), (7, (1, 3)), (9, (5, 7)), (11, (1, 7))]

    def calculate_active_masks(xdi):
        # [(1, (7, 11)), (3, (2, 7)), (5, (2, 9)), (7, (9, 11))]
        result = []

        first_active_row, interval = xdi[0]
        active_masks = [interval]
        for row, interval in xdi[1:]:
            new_masks = active_masks[:]
            shrunk = merge_into_masks(interval, new_masks)
            if shrunk:
                # Keep old mask for this row
                result.append(( (first_active_row,row), active_masks ))
                first_active_row = row + 1
            else:
                # Use new mask for this row
                result.append(( (first_active_row,row-1), active_masks ))
                first_active_row = row
            active_masks = new_masks
        return result

    row_active_masks = calculate_active_masks(rdi)
    col_active_masks = calculate_active_masks(cdi)

    #print(f'ram: {row_active_masks}')
    #print(f'cam: {col_active_masks}')

    max_area = 0
    for i, tile1 in enumerate(rctiles[:-1]):
        for tile2 in rctiles[i+1:]:
            rowmin = min(tile1[0], tile2[0])
            rowmax = max(tile1[0], tile2[0])
            colmin = min(tile1[1], tile2[1])
            colmax = max(tile1[1], tile2[1])
            area = (rowmax-rowmin+1) * (colmax-colmin+1)
            #print(f'Trying tiles {(rowmin, colmin)} to {(rowmax, colmax)} = area {area}')
            if area <= max_area:
                continue
            if not is_legal(rowmin, rowmax, colmin, colmax, row_active_masks, col_active_masks):
                continue
            max_area = area
            print(f'Got a better max area: {max_area} for tiles {(rowmin, colmin)} to {(rowmax, colmax)}')
    return max_area

print(f'\nTest part 2: {solve_part2(TEST_INPUT)}\n\n')
print(f'\nProd part 2: {solve_part2(PRODUCTION_INPUT)}\n\n')
