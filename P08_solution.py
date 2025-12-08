from collections import defaultdict
from P08_input import PRODUCTION_INPUT

TEST_INPUT = '''162,817,812
57,618,57
906,360,560
592,479,940
352,342,300
466,668,158
542,29,236
431,825,988
739,650,466
52,470,668
216,146,977
819,987,18
117,168,530
805,96,715
346,949,466
970,615,88
941,993,340
862,61,35
984,92,344
425,690,689'''


def solve(INPUT, connect_n, mode):

    boxes = list()
    for line in INPUT.strip().splitlines():
        boxes.append([int(c) for c in line.split(',')])

    num_boxes = len(boxes)

    # Calculate all (squared) distances
    distances = dict()
    for i, box1 in enumerate(boxes[:-1]):
        for j, box2 in enumerate(boxes[i+1:]):
            distance = (box1[0]-box2[0])**2 + (box1[1]-box2[1])**2 + (box1[2]-box2[2])**2
            assert distance not in distances
            distances[distance] = (i, j+i+1)

    # Calculate subnets (= circuits)
    subnets = list()  # List of set of box index
    num_attempts = 0
    for distance, (i,j) in sorted(distances.items()):
        #print(f'\n{distance} : {i}->{j}')
        subnet_i = None 
        subnet_j = None
        subnet_i_offset = -1
        subnet_j_offset = -1
        for counter, subnet in enumerate(subnets):
            if subnet_i is not None and subnet_j is not None:
                break
            if subnet_i is None and i in subnet:
                subnet_i = subnet
                subnet_i_offset = counter
            if subnet_j is None and j in subnet:
                subnet_j = subnet
                subnet_j_offset = counter
        #print(f'{subnet_i} {subnet_j}')
        if subnet_i is None:
            if subnet_j is None:
                # 2 new boxes. Create new subnet
                subnets.append({i,j})
            else:
                # Add new box i to existing subnet
                subnet_j.add(i)
        else:
            if subnet_j is None:
                # Add new box j to existing subnet
                subnet_i.add(j)
            else:
                if subnet_i_offset == subnet_j_offset:
                    # Do nothing; the boxes already are in the same subnet
                    pass
                else:
                    # Merge two subnets
                    subnet_i.update(subnet_j)
                    subnets.pop(subnet_j_offset)
        num_attempts += 1
        if (num_attempts == connect_n):
            subnet_sizes = sorted(map(len, subnets), reverse=True)
            # print(subnets)
            # print(subnet_sizes)
            print(f'{mode} Part 1: {subnet_sizes[0] * subnet_sizes[1] * subnet_sizes[2]}')
        if len(subnets)==1 and len(subnets[0]) == num_boxes:
            print(f'{mode} Part 2: Single circuit reachted at attempt {num_attempts}! Last connection {boxes[i]} -> {boxes[j]}. X_multiplied={boxes[i][0]*boxes[j][0]}')
            break

solve(TEST_INPUT, 10, 'test')
print('='*40)
solve(PRODUCTION_INPUT, 1000, 'prod')
