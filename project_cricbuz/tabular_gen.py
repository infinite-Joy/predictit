from test import sim_finder, ground_country_mapping
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
            if value in val[3].upper().strip() or value in val[4].upper().strip():
                table.remove(val)

def ground_match(name, mapping):
    ret = 0
    for key, value in mapping.items():
        ratio = sim_finder(key, name)
        if ratio >= 0.6:
            ret += 1
            res = value
    if ret:
        return [ret, res]
    else:
        return 0

def compression(table):
    new_table = []
    for raw in table:
        new_table.append([raw[0], raw[5], raw[8], raw[9]])
    return new_table

def delete_incon(selraws):
    checker = 0
    out = []
    for val in selraws:
        value = val.upper()
        if value in baseframe.keys():
            out.append(baseframe[value])
        else:
            checker = 1
    if checker == 1:
        return 0
    else:
        return out



table = []
counter = 0
try:
    with open('pre_tabular.txt', 'r') as f:
        for line in f:
            raw = line.split('==')
            raw += [str(counter)]
            counter += 1
            table.append(list(map(str.strip, raw)))
except IOError:
    print('file pre_tabular.txt not found')

print('size of table before delete_unwanted', len(table))
delete_unwanted()
print('size of table after delete_unwanted', len(table))

with open('val_required.txt', 'r') as f:
    baseframe = {}
    for line in f:
        baseframe[line.split(':')[0].strip()] = line.split(':')[1].strip()


print('size of table before loop for ratio', len(table))
mapping = ground_country_mapping()
for raw in table[:]:
    res = ground_match(raw[5], mapping)
    if not res:
        #rethink about this removal. YOu are removing all the games that doesnt have 0.6 mapping ratio
        table.remove(raw)
    else:
        raw[5] = res[1].upper()
        out = delete_incon([raw[5], raw[8], raw[9]])
        if out:
            raw[5], raw[8], raw[9] = out
        else:
            table.remove(raw)

print('size of table after ratio', len(table))

with open('prefinal.txt', 'w+') as f:
    for val in table:
        f.write(str(val) + '\n\n\n')
#table = compression(table)

#tabular data generation starts here
X = []
for raw in table:
    #every game generate two raws of data
    temp = []
    temp.append([])
    temp.append([])

    #variables for readabiltiy
    t1 = raw[3]
    t2 = raw[4]
    ground = raw[5]
    toss_winner = raw[8]
    match_winner = raw[9]

    #variables for debugging
    toss_winner_d = 0
    match_winner_d = 0

    #doing the cases saperatly to avoid errors
    
    #################################
    #CASE TEAM 1
    if t1 == match_winner:
        temp[0].append(1)
        match_winner_d = 1
    else:
        temp[0].append(0)

    if t1 == ground:
        temp[0].append(1)
    else:
        temp[0].append(0)

    if t1 == toss_winner:
        temp[0].append(1)
        toss_winner_d = 1
    else:
        temp[0].append(0)

    ################################
    #CASE TEAM 2
    if t2 == match_winner:
        temp[1].append(1)
        match_winner_d = 1
    else:
        temp[1].append(0)

    if t2 == ground:
        temp[1].append(1)
    else:
        temp[1].append(0)

    if t2 == toss_winner:
        toss_winner_d = 1
        temp[1].append(1)
    else:
        temp[1].append(0)

    temp[0].append(raw)
    temp[1].append(raw)
    #debugging
    if toss_winner_d != 1:
        print('error with toss winner')
    if match_winner_d != 1:
        print('error with match winner')

    X.append(temp[0])
    X.append(temp[1])


with open('tabular.txt', 'w+') as f:
    for val in X:
        f.write(str(val[0]) + ' ' + str(val[1]) + ' ' + str(val[2]) + '\n')
        #f.write(str(val) + '\n\n')