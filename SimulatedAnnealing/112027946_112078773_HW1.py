import os, sys
import random
import string
import math

# Key Width equal to 1 key
keyWidth = 1.0
# Key coordinate for a 6 rows by 5 column keyboard
cord = [[(x + keyWidth / 2.0, y + keyWidth / 2.0) for x in range(5)] for y in range(6)]

def get_random_layout():
    # Call this function to a a randomized layout.
    # A layout is dictionary of key symbols(a to z) to it's (row, column) index
    cord_shuffle = [(x, y) for x in range(6) for y in range(5)]
    random.shuffle(cord_shuffle)
    layout = {}
    i = 0
    for lt in string.ascii_lowercase:
        layout[lt] = cord_shuffle[i]
        i += 1
    # Since there are 30 slots for a 6*5 keyboard, 
    # we use dummy keys to stuff remaining keys
    layout['1'] = cord_shuffle[-1]
    layout['2'] = cord_shuffle[-2]
    layout['3'] = cord_shuffle[-3]
    layout['4'] = cord_shuffle[-4]
    return layout

def makeDigramTable(data_path):
    # Make a Digram Table , which is a dictionary with key format (letter_i,letter_j) to it's Pij
    # You could safely ignore words that have only 1 character when constructing this dictionary
    keyvalue = dict()
    tbl = {}
    fp = open(data_path)
    content = fp.read()
    lines = content.split("\n")
    for line in lines:
        str = line.split("\t")
        current_word = str[0]
        # print current_word
        if len(current_word) > 1:
            current_count = float(str[1])
            for i in range(0, len(current_word) - 1):
                digram = current_word[i:i + 2]
                if (digram[0], digram[1]) not in tbl:
                    tbl[(digram[0], digram[1])] = current_count
                else:
                    val = tbl[(digram[0], digram[1])] + current_count
                    tbl[(digram[0], digram[1])] = val
    total = sum(tbl.values())
    for key, value in tbl.iteritems():
        tbl[key] = value / total
    fp.close()
    return tbl

def FittsLaw(W, D):
    # implement the Fitt's Law based on the given arguments and constant
    a = 0.083
    b = 0.127
    return a + b * math.log(D*1.0 / W + 1, 2)

def computeAMT(layout, digram_table):
    # Compute the average movement time
    distance = {}

    for key, value in digram_table.iteritems():
        a = key[0]
        b = key[1]
        x1, y1 = layout[a]
        x2, y2 = layout[b]
        distance[key] = math.sqrt(math.pow((x2*1.0 - x1*1.0), 2) + math.pow((y2*1.0 - y1*1.0), 2))

    MT = 0.0
    for key, value in digram_table.iteritems():
        mov_time = FittsLaw(keyWidth, distance[key])
        MT = MT + (mov_time * digram_table[key])

    return MT

def SA(num_iter, num_random_start, tbl):
    # Do the SA with num_iter iterations, you can random start by num_random_start times
    # the tbl arguments were the digram table

    final_result = ({}, 0.0)

    # --------you should return a tuple of (optimal_layout,optimal_MT)----
    counter = 0
    globalMin = 1000000.0
    while counter < num_random_start:

        state = get_random_layout()
        min_cost = computeAMT(state, tbl)
        k = 0
        while k < num_iter :
            key1 = random.choice(state.keys())
            key2 = random.choice(state.keys())
            while key2 == key1:
                key2 = random.choice(state.keys())
            temp = state[key1]
            state[key1] = state[key2]
            state[key2] = temp
            c = computeAMT(state, tbl)
            if c >= min_cost:
                k=k+1
                temp = state[key1]
                state[key1] = state[key2]
                state[key2] = temp
            else:
                min_cost = c
                k=0
        if min_cost < globalMin:
            globalMin = min_cost
            finalState = state
        counter = counter + 1

    return finalState , globalMin

def printLayout(layout):
    # use this function to print the layout
    keyboard = [[[] for x in range(5)] for y in range(6)]
    for k in layout:
        r = layout[k][0]
        c = layout[k][1]
        keyboard[r][c].append(k)
    for r in range(6):
        row = ''
        for c in range(5):
            row += keyboard[r][c][0] + '  '
        print(row)

if __name__ == '__main__':

    if len(sys.argv) != 4:
        print("usage: hw1.py [num_SA_iteration] [num_SA_random_start] [dataset_path]")
        print("hello")

    k = int(sys.argv[1])
    rs = int(sys.argv[2])
    data_path = sys.argv[3]

    # Test Fitt's Law
    print(FittsLaw(10, 10))
    print(FittsLaw(20, 5))
    print(FittsLaw(10.5, 1))

    # Construct Digram Table
    tbl = makeDigramTable(data_path)
    print tbl

    # Run SA
    result, cost = SA(k, rs, tbl)
    print("Optimal MT:", cost)
    printLayout(result)

