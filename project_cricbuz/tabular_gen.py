from test import sim_finder
from collections import OrderedDict as od

def comparer(variable):
    for val in variable:
        for value in variable:
            rat = sim_finder(val, value)
            if  0 < rat < 1:
                print(val, '-', value, rat)

def delete_unwanted():
    lis = ['WOMEN', 'XI', 'U19']
    for val in table[:]:
        for value in lis:
            if value in val[2].upper().strip() or value in val[3].upper().strip():
                print(val[len(val) - 1], val[2].upper().strip(), val[3].upper().strip())
                table.remove(val)

table = []
counter = 0
try:
    with open('pre_tabular.txt', 'r') as f:
        for line in f:
            raw = line.split('==')
            raw += [str(counter)]
            counter += 1
            table.append(list(map(str.strip, raw[1:])))
except IOError:
    print('file pre_tabular.txt not found')

delete_unwanted()

teams = []
toss_winners = []
for raw in table:
    teams.append(raw[2])
    teams.append(raw[3])
    toss_winners.append(raw[7])
    toss_winners.append(raw[8])
teams = set(teams)
toss_winners = set(toss_winners)
print(teams)
print(toss_winners)

