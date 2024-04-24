import sys

for i in range(0, 22):
    types = set()
    d = (i+1) * 2
    print("Processing ", d, " length binary sequences")

    num_sequences = 2**(d-1)

    for i in range(num_sequences):
        num = bin(i)[2:].zfill(d-1)
        x = num.count('1') % 2
        num = num + str(x)
        shift_num = num
        inlist = False

        for i in range(d):
            shift_num = shift_num[-1] + shift_num[:-1]
            if shift_num in types:
                inlist = True
                break
        
        if not inlist:
            types.add(num)
    
    print("There are ", len(types), " different derivative groups for ", d, " length binary sequences")