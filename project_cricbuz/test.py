with open('toss_winner.txt', 'r') as f:
    counter = 0
    anti_counter = 0
    var = 0
    while 1:
        if var == 0:
            temp1 = f.readline()
            temp2 = f.readline()
        else:
            temp1 = temp2
            temp2 = f.readline()
            var = 0
        if temp1.strip() == temp2.strip():
            counter += 1
        else:
            anti_counter += 1
            var = 1
        if temp1 == '' or temp2 == '':
            break
    print('total match', counter)
    print('total mismatch', anti_counter)
    