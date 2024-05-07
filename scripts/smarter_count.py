from itertools import combinations_with_replacement
import more_itertools as mit
import time

INT_BITS = 32

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

def rotateX(w):
	return (w[0], w[2], w[1])

def rotateY(w):
	return (w[2], w[1], w[0])

def rotateZ(w):
	return (w[1], w[0], w[2])

def mirrorX(w,N):
	return (2**N-1-reverseBits(w[0], N), 2**N-1-w[1], 2**N-1-w[2])

def mirrorY(w,N):
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
	t = 0
	u = 0
	t0 = 0
	t1 = 0
	t2 = 0
	t3 = 0
	t4 = 0
	visx = []
	
	visz = []
	# for w in combinations_with_replacement(range(num_sequences), 3):
	for i in range(num_sequences):
		if i in visx:
			continue
		sx = list(map(lambda x: ((i << x) | (i >> N-x)) & (num_sequences-1), range(N)))
		nsx = list(map(lambda x: num_sequences-1-x,sx))
		sx_e = list(map(lambda x: ((i << x) | (i >> N-x)) & (num_sequences-1), range(0,N,2)))
		nsx_e = list(map(lambda x: num_sequences-1-((i << x) | (i >> N-x)) & (num_sequences-1), range(1,N,2)))
		visx.extend(sx_e)
		visx.extend(nsx_e)
		# visx.extend(nsx_e)
		visy = []
		for j in range(num_sequences):
			if j in visy:
				continue
			sy = list(map(lambda x: ((j << x) | (j >> N-x)) & (num_sequences-1), range(N)))
			nsy = list(map(lambda x: num_sequences-1-x,sy))
			sy_e = list(map(lambda x: ((j << x) | (j >> N-x)) & (num_sequences-1), range(0,N,2)))
			nsy_e = list(map(lambda x: num_sequences-1-((j << x) | (j >> N-x)) & (num_sequences-1), range(1,N,2)))
			visy.extend(sy_e)
			visy.extend(nsy_e)
			# visy.extend(nsy_e)
			# visx.extend(sy_e)
			# visx.extend(nsy_e)
			visz = []
			for k in range(num_sequences):
				if k in visz:
					continue
				sz = list(map(lambda x: ((k << x) | (k >> N-x)) & (num_sequences-1), range(N)))
				nsz = list(map(lambda x: num_sequences-1-x,sz))
				sz_e = list(map(lambda x: ((k << x) | (k >> N-x)) & (num_sequences-1), range(0,N,2)))
				nsz_e = list(map(lambda x: num_sequences-1-((k << x) | (k >> N-x)) & (num_sequences-1), range(1,N,2)))
				visz.extend(sz_e)
				visz.extend(nsz_e)
				# visz.extend(nsz_e)
				# visy.extend(sz_e)
				# visy.extend(nsz_e)
				# visx.extend(sz_e)
				# visx.extend(nsz_e)
				t+=1
				# w = (i,j,k)
				#tic0 = time.perf_counter()
				# if w in all_types:
					#print(f"{t0:0.4f}\t{t1:0.4f}\t{t2:0.4f}\t{t3:0.4f}\t{t4:0.4f}\t{u}\t{i*100/l:0.2f}\t{l}",end='\r')
					# continue
				#t0 += time.perf_counter() - tic0
				# current_items = set()
				#tic1 = time.perf_counter()
				# current_items.update(mit.distinct_permutations(w))
				# toc1 = time.perf_counter()
				# t1 += toc1-tic1
				# mx = mirrorX(w, N)
				# my = mirrorY(w, N)
				# mz = mirrorZ(w, N)
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

				# tic2 = time.perf_counter()
				
				
				
				# # toc4 = time.perf_counter()
				# perms = []
				# for ii in range(N):
				# 	for jj in range(N):
				# 		for kk in range(N):
				# 			x = sx[ii] if (jj + kk) % 2 == 0 else nsx[ii]
				# 			y = sy[jj] if (ii + kk) % 2 == 0 else nsy[jj]
				# 			z = sz[kk] if (jj + ii) % 2 == 0 else nsz[kk]
				# 			w1 = (x,y,z)
							# current_items.update(mit.distinct_permutations(w1))
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
				# toc2 = time.perf_counter()
				# t3 += toc2-toc4
				# t2 += toc4-tic2
				
				# tic3 = time.perf_counter()
				#if not any(item in all_types for item in current_items):
				u += 1
				# toc3 = time.perf_counter()
				# t4 += toc3-tic3

				# print(f"{t0:0.4f}\t{t1:0.4f}\t{t2:0.4f}\t{t3:0.4f}\t{t4:0.4f}\t{u}\t{i*100/l:0.2f}\t{l}",end='\r')
				print(f"{u}\t{t*100/num_sequences**3:0.2f}\t{num_sequences**3}",end='\r')
				# all_types.update(current_items)

	print()
	print("Number of classes: ", u,"\n")
	# for i, t in enumerate(type_classes):
	# 	print(i, "[ of length ", len(t) ,"]: ", t)
		
    
		