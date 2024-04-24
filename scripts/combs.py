n_types = [2, 4, 8, 20, 56, 180, 596, 2068, 7316, 26272, 95420, 349716, 1290872, 4794088, 17896832]
n_confs = []

for i, n in enumerate(n_types):
    i += 1
    n_confs.append((n+2)*(n+1)*n/6)
    print(2*i,"x",2*i,"x",2*i,": ", (n+2)*(n+1)*n/6)
    print(n/n_types[i-2])

prev = n_types[0]
for i, n in enumerate(n_confs):
    print(n/n_confs[i-1])