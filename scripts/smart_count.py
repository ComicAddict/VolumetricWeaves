from itertools import combinations_with_replacement
import more_itertools as mit
import time

def ISHFTC(n, d, N):
	return ((n << d) % (1 << N)) | (n >> (N - d))

def reverseBits(n, N):
	return int('{:0{N}b}'.format(n, N=N)[::-1], 2)

def shiftX(w, d, N):
	if d % 2 == 1:
		return (ISHFTC(w[0], d, N), 2**N-1-w[1] ,2**N-1-w[2])
	else:
		return (ISHFTC(w[0], d, N), w[1] , w[2])

def shiftY(w, d, N):
	if d % 2 == 1:
		return (2**N-1-w[0], ISHFTC(w[1], d, N), 2**N-1-w[2])
	else:
		return (w[0], ISHFTC(w[1], d, N), w[2])

def shiftZ(w, d, N):
	if d % 2 == 1:
		return (2**N-1-w[0], 2**N-1-w[1], ISHFTC(w[2], d, N))
	else:
		return (w[0], w[1], ISHFTC(w[2], d, N))

def rotateX(w, N):
	return (w[0], 2**N-1-reverseBits(w[2], N), 2**N-1-w[1])

def rotateY(w, N):
	return (w[2], w[1], reverseBits(w[0], N))

def rotateZ(w, N):
	return (2**N-1-reverseBits(w[1], N), 2**N-1-w[0], w[2])

def mirrorX(w, N):
	return (2**N-1-reverseBits(w[0], N), 2**N-1-w[1], 2**N-1-w[2])

def mirrorY(w, N):
	return ( 2**N-1-w[0], 2**N-1-reverseBits(w[1], N), 2**N-1-w[2])

def mirrorZ(w,N):
	return (2**N-1-w[0], 2**N-1-w[1], 2**N-1-reverseBits(w[2], N))

for m in range(0, 10):
	all_types = set()
	base_types = []
	type_classes = []
	N = (m+1) * 2
	print("Processing ", N, " length binary sequences")
	#print("t0\tt1\tt2\tt3\tt4\tu\t%\tTotal")
	print("u\t%\tTotal")
	num_sequences = 2**(N)
	i = 0
	u = 0
	t=0
	visx = []
	cyz = combinations_with_replacement(range(num_sequences),2)
	l = len(list(cyz))
	ll = l * num_sequences
	for i in range(num_sequences):
		if i in visx:
			t += l
			print(f"{u}\t{t*100/ll:0.2f}\t{ll}",end='\r')
			continue
		sx = list(map(lambda x: ((i << x) | (i >> N-x)) & (num_sequences-1), range(N)))
		nsx = list(map(lambda x: num_sequences-1-x,sx))
		sx_e = list(map(lambda x: ((i << x) | (i >> N-x)) & (num_sequences-1), range(0,N,2)))
		visx.extend(sx_e)
		visy = []
		visyz = []
		visz = []
		viszy = []
		for j,k in combinations_with_replacement(range(num_sequences),2):
			
			sy = list(map(lambda x: ((j << x) | (j >> N-x)) & (num_sequences-1), range(N)))
			sy_e = list(map(lambda x: ((i << x) | (i >> N-x)) & (num_sequences-1), range(0,N,2)))
			nsy = list(map(lambda x: num_sequences-1-x,sy))
			visy.extend(sy_e)

			sz = list(map(lambda x: ((k << x) | (k >> N-x)) & (num_sequences-1), range(N)))
			sz_e = list(map(lambda x: ((k << x) | (k >> N-x)) & (num_sequences-1), range(0,N,2)))
			nsz = list(map(lambda x: num_sequences-1-x,sz))
			visyz.append(k)

			# if j in visy and k in visyz:
			# 	t +=1
			# 	print(f"{u}\t{t*100/ll:0.2f}\t{ll}",end='\r')
			# 	continue
			
			# if j in visy:
			# 	t +=1
			# 	print(f"{u}\t{t*100/ll:0.2f}\t{ll}",end='\r')
			# 	continue
			t+=1
			
			w = (i,j,k)
			if w in all_types:
				print(f"{u}\t{t*100/ll:0.2f}\t{ll}",end='\r')
				continue
			current_items = set()
			#current_items.update(mit.distinct_permutations((i,j,k)))
			current_items.update(w)
			current_items.update(rotateX(w, N))
			current_items.update(rotateY(w, N))
			current_items.update(rotateZ(w, N))
			
			for ii in range(N):
				for jj in range(N):
					for kk in range(N):
						x = sx[ii] if (jj + kk) % 2 == 0 else nsx[ii]
						y = sy[jj] if (ii + kk) % 2 == 0 else nsy[jj]
						z = sz[kk] if (jj + ii) % 2 == 0 else nsz[kk]
						w = (x,y,z)
						# current_items.update(mit.distinct_permutations((x,y,z)))
						current_items.update(w)
						current_items.update(rotateX(w, N))
						current_items.update(rotateY(w, N))
						current_items.update(rotateZ(w, N))

						# mx = mirrorX(w1, N)
						# my = mirrorY(w1, N)
						# mz = mirrorZ(w1, N)
						# mxy = mirrorY(mx, N)
						# mxz = mirrorZ(mx, N)
						# myz = mirrorZ(my, N)
						# mxyz = mirrorZ(mxy, N)
						# current_items.add(mx)
						# current_items.add(my)
						# current_items.add(mz)
						# current_items.add(mxy)
						# current_items.add(mxz)
						# current_items.add(myz)
						# current_items.add(mxyz)

			if not any(item in all_types for item in current_items):
				u += 1

			all_types.update(current_items)
			print(f"{u}\t{t*100/ll:0.2f}\t{ll}",end='\r')
				

	print()
	print("Number of classes: ", u,"\n")
	# for i, t in enumerate(type_classes):
	# 	print(i, "[ of length ", len(t) ,"]: ", t)
		
    
		