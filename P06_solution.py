
from P06_input import PRODUCTION_INPUT
from functools import reduce

TEST_INPUT = '''
123 328  51 64 
 45 64  387 23 
  6 98  215 314
*   +   *   +  
'''

def solve_part1(INPUT):
    lines = INPUT.strip().splitlines()
    operands = [[int(x)] for x in lines[0].strip().split()]
    for line in lines[1:-1]:
        for i, operand in enumerate(line.strip().split()):
            operands[i].append(int(operand))
    operators = lines[-1].strip().split()
    num_operations = len(operands)
    num_operands = len(operands[0])
    assert all(len(operand)==num_operands for operand in operands)
    assert len(operators) == num_operations
    assert all(operator in ('+','*') for operator in operators)
    total = 0
    for i, operands in enumerate(operands):
        if operators[i] == '+':
            value = sum(operands)
        elif operators[i] == '*':
            value = reduce(lambda x,y:x*y, operands)
        total += value
    return total

def solve_part2(INPUT):
    lines = INPUT.strip('\n').splitlines()
    operation_offsets, operators = zip(*[(i,j) for (i,j) in enumerate(lines[-1]) if j!=' '])
    num_operations = len(operators)
    operation_offsets = list(operation_offsets) + [len(lines[-1])+1]
    total = 0
    for i in range(num_operations):
        operator = operators[i]
        value = {'+':0, '*':1}[operator]
        for j in range(operation_offsets[i], operation_offsets[i+1]-1):
            operand = ''
            for line in lines[:-1]:
                operand += line[j]
            operand = int(operand)
            value = (value + operand) if operator=='+' else (value * operand)
        total += value
    return total


print(f'Test: problem 1 = {solve_part1(TEST_INPUT)}')
print(f'Prod: problem 1 = {solve_part1(PRODUCTION_INPUT)}')
print('='*50)
print(f'Test: problem 2 = {solve_part2(TEST_INPUT)}')
print(f'Prod: problem 2 = {solve_part2(PRODUCTION_INPUT)}')
