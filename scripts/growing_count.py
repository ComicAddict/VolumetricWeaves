from itertools import combinations_with_replacement
from itertools import combinations
import more_itertools as mit

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

def mirrorX(w,N):
	return (2**N-1-reverseBits(w[0], N), 2**N-1-w[1], 2**N-1-w[2])

def mirrorY(w,N):
	return ( 2**N-1-w[0], 2**N-1-reverseBits(w[1], N), 2**N-1-w[2])

def mirrorZ(w,N):
	return (2**N-1-w[0], 2**N-1-w[1], 2**N-1-reverseBits(w[2], N))

def toint(w, N):
	return (N**2 * w[2]) + (N * w[1]) + w[0]

for m in range(0, 1):
	all_types = set()
	base_types = []
	type_classes = []
	N = (m+1) * 2
	print("Processing ", N, " length binary sequences")
	c = 0
	num_sequences = 2**(N)
	visx = []
	for i in range(num_sequences):
		if i in visx:
			continue
		sx = list(map(lambda x: ((i << x) | (i >> N-x)) & (num_sequences-1), range(N)))
		nsx = list(map(lambda x: num_sequences-1-x,sx))
		sx_e = list(map(lambda x: ((i << x) | (i >> N-x)) & (num_sequences-1), range(0,N,2)))
		visx.extend(sx_e)
		for j in range(num_sequences):
			sy = list(map(lambda x: ((j << x) | (j >> N-x)) & (num_sequences-1), range(N)))
			nsy = list(map(lambda x: num_sequences-1-x,sy))
			for k in range(num_sequences):
				sz = list(map(lambda x: ((k << x) | (k >> N-x)) & (num_sequences-1), range(N)))
				nsz = list(map(lambda x: num_sequences-1-x,sz))

				current_items = set()
				w = (i,j,k)
				current_items.add(w)
				wx = rotateX(w, N)
				wy = rotateY(w, N)
				wz = rotateZ(w, N)
				wxx = rotateX(wx, N)
				wyy = rotateY(wy, N)
				wzz = rotateZ(wz, N)
				wxy = rotateY(wx, N)
				wyz = rotateZ(wy, N)
				wzx = rotateX(wz, N)
				current_items.add(wx)
				current_items.add(wy)
				current_items.add(wz)
				current_items.add(wxx)
				current_items.add(wyy)
				current_items.add(wzz)
				current_items.add(wxy)
				current_items.add(wyz)
				current_items.add(wzx)
				# current_items.add(mirrorX(w, N))
				# current_items.add(mirrorY(w, N))
				# current_items.add(mirrorZ(w, N))
				for ii in range(N):
					for jj in range(N):
						for kk in range(N):
							x = sx[ii] if (jj + kk) % 2 == 0 else nsx[ii]
							y = sy[jj] if (ii + kk) % 2 == 0 else nsy[jj]
							z = sz[kk] if (jj + ii) % 2 == 0 else nsz[kk]
							w1 = (x,y,z)
							current_items.add(w1)
							wx = rotateX(w1, N)
							wy = rotateY(w1, N)
							wz = rotateZ(w1, N)
							wxx = rotateX(wx, N)
							wyy = rotateY(wy, N)
							wzz = rotateZ(wz, N)
							wxy = rotateY(wx, N)
							wyz = rotateZ(wy, N)
							wzx = rotateX(wz, N)
							current_items.add(wx)
							current_items.add(wy)
							current_items.add(wz)
							current_items.add(wxx)
							current_items.add(wyy)
							current_items.add(wzz)
							current_items.add(wxy)
							current_items.add(wyz)
							current_items.add(wzx)

							# current_items.add(mirrorX(w1, N))
							# current_items.add(mirrorY(w1, N))
							# current_items.add(mirrorZ(w1, N))
				embed = list(map(lambda x: toint(x, num_sequences), current_items))
				isUniqueClass = True
				for t in type_classes:
					itemFound = False
					if t.intersection(current_items):
						t.update(current_items)
						isUniqueClass = False

				if isUniqueClass:
					type_classes.append(current_items)
				if any(item in all_types for item in embed):
					all_types.update(embed)
				else:
					c += 1
					all_types.update(embed)
	
	# for c1, c2 in combinations(type_classes,2):
	# 	if c1.intersection(c2):
	# 		c1.update(c2)
	# 		c2.update(c1)
	# res = set(map(frozenset, type_classes))
	print("Number of classes: ", len(type_classes))
	# print(type_classes)
	for i, tc in enumerate(type_classes):
		print("type ", i, " members:", len(tc))
		for t in tc:
			print("\t",t) 
	# print("Number of classes: ", c)

	# all_types1 = set()
	# base_types = []
	# type_classes1 = []
	# N = (m+1) * 2
	# print("Processing ", N, " length binary sequences")
	# c = 0
	# num_sequences = 2**(N)
	# for i in range(num_sequences):
	# 	for j in range(num_sequences):
	# 		for k in range(num_sequences):
	# 			current_items = set()
	# 			w = (i,j,k)
	# 			current_items.update(mit.distinct_permutations(w))
	# 			current_items.add(w)
	# 			wx = rotateX(w, N)
	# 			wy = rotateY(w, N)
	# 			wz = rotateZ(w, N)
	# 			wxx = rotateX(wx, N)
	# 			wyy = rotateY(wy, N)
	# 			wzz = rotateZ(wz, N)
	# 			wxy = rotateY(wx, N)
	# 			wyz = rotateZ(wy, N)
	# 			wzx = rotateX(wz, N)
	# 			current_items.add(wx)
	# 			current_items.add(wy)
	# 			current_items.add(wz)
	# 			current_items.add(wxx)
	# 			current_items.add(wyy)
	# 			current_items.add(wzz)
	# 			current_items.add(wxy)
	# 			current_items.add(wyz)
	# 			current_items.add(wzx)
	# 			# current_items.add(mirrorX(w, N))
	# 			# current_items.add(mirrorY(w, N))
	# 			# current_items.add(mirrorZ(w, N))
	# 			for ii in range(N):
	# 				for jj in range(N):
	# 					for kk in range(N):
	# 						w1 = shiftZ(shiftY(shiftX(w,ii,N),jj,N),kk,N)
	# 						current_items.add(w1)
	# 						wx = rotateX(w1, N)
	# 						wy = rotateY(w1, N)
	# 						wz = rotateZ(w1, N)
	# 						wxx = rotateX(wx, N)
	# 						wyy = rotateY(wy, N)
	# 						wzz = rotateZ(wz, N)
	# 						wxy = rotateY(wx, N)
	# 						wyz = rotateZ(wy, N)
	# 						wzx = rotateX(wz, N)
	# 						current_items.add(wx)
	# 						current_items.add(wy)
	# 						current_items.add(wz)
	# 						current_items.add(wxx)
	# 						current_items.add(wyy)
	# 						current_items.add(wzz)
	# 						current_items.add(wxy)
	# 						current_items.add(wyz)
	# 						current_items.add(wzx)

	# 						# current_items.add(mirrorX(w1, N))
	# 						# current_items.add(mirrorY(w1, N))
	# 						# current_items.add(mirrorZ(w1, N))
	# 						current_items.update(mit.distinct_permutations(w1))

	# 			isUniqueClass = True
	# 			for t in type_classes1:
	# 				itemFound = False
	# 				if any(item in t for item in current_items):
	# 					t.update(current_items)
	# 					itemFound = True
	# 					isUniqueClass = False

	# 			if isUniqueClass:
	# 				type_classes1.append(current_items)
	# 			# if any(item in all_types for item in current_items):
	# 			# 	all_types.update(current_items)
	# 			# else:
	# 			# 	c += 1
	# 			# 	all_types.update(current_items)
	# for i in range(len(type_classes)):
	# 	for j in range(len(type_classes)):
	# 		if type_classes[i].intersection(type_classes[j]):
	# 			type_classes[i].update(type_classes[j])
	# 			type_classes[j].update(type_classes[i])
	# res1 = set(map(frozenset, type_classes1))
	# print("Number of classes: ", len(res1))
	# t = res.difference(res1)
	# for t1 in t:
	# 	print(t1)
	# for i, t in enumerate(res):
	# 	print(i, "[ of length ", len(t) ,"]: ", t)
		
    
		