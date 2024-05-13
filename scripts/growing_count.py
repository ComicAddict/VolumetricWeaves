from itertools import combinations_with_replacement
from itertools import combinations
import more_itertools as mit

def ISHFTC(n, d, N):
	return ((n << d) % (1 << N)) | (n >> (N - d))

def reverseBits(n, N):
	return int('{:0{N}b}'.format(n, N=N)[::-1], 2)

def reverse_mask(x, N):
	x = ((x & 0x55555555) << 1) | ((x & 0xAAAAAAAA) >> 1)
	x = ((x & 0x33333333) << 2) | ((x & 0xCCCCCCCC) >> 2)
	x = ((x & 0x0F0F0F0F) << 4) | ((x & 0xF0F0F0F0) >> 4)
	x = ((x & 0x00FF00FF) << 8) | ((x & 0xFF00FF00) >> 8)
	x = ((x & 0x0000FFFF) << 16) | ((x & 0xFFFF0000) >> 16)
	x = (x << N) | (x >> 32-N)
	return x

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

def calculateTypes(N, mirror=False):
	c = 0
	num_sequences = 2**(N)
	type_classes = []
	complete = set()
	for i in range(num_sequences):
		for j in range(num_sequences):
			for k in range(num_sequences):
				complete.add((i,j,k))

	c = 0 
	rotorder = ['x','x','z','x','x','z']
	while complete:
		c += 1
		w = complete.pop()
		tmp = set()
		i = w[0]
		j = w[1]
		k = w[2]
		sx = list(map(lambda x: ((i << x) | (i >> N-x)) & (num_sequences-1), range(N)))
		nsx = list(map(lambda x: num_sequences-1-x,sx))
		sy = list(map(lambda x: ((j << x) | (j >> N-x)) & (num_sequences-1), range(N)))
		nsy = list(map(lambda x: num_sequences-1-x,sy))
		sz = list(map(lambda x: ((k << x) | (k >> N-x)) & (num_sequences-1), range(N)))
		nsz = list(map(lambda x: num_sequences-1-x,sz))
		for ii in range(N):
			for jj in range(N):
				for kk in range(N):
					x = sx[ii] if (jj + kk) % 2 == 0 else nsx[ii]
					y = sy[jj] if (ii + kk) % 2 == 0 else nsy[jj]
					z = sz[kk] if (jj + ii) % 2 == 0 else nsz[kk]
					w = (x,y,z)
					tmp.add(w)
					if mirror:
						tmp.add(mirrorZ(w,N))
					for r in rotorder:
						for ir in range(4):
							w = rotateY(w, N)
							tmp.add(w)
							if mirror:
								tmp.add(mirrorZ(w,N))
						if r == 'x':
							w = rotateX(w, N)
						elif r == 'z':
							w = rotateZ(w, N)
		complete -= tmp
		type_classes.append(tmp)
	return type_classes, c
	
def find_transformation(w1, w2, N):
	rotorder = ['x','x','z','x','x','z']
	for ii in range(N):
		for jj in range(N):
			for kk in range(N):
				tr = "shift{}-{}-{}".format(ii,jj,kk)
				w = shiftZ(shiftY(shiftX(w2, ii, N), jj, N), kk, N)
				if w1 == w:
					return tr
				# if mirror:
				# 	tmp.add(mirrorZ(w,N))
				for r in rotorder:
					for ir in range(4):
						tr += "-rotY-"
						w = rotateY(w, N)
						if w1 == w:
							return tr
						# if mirror:
						# 	tmp.add(mirrorZ(w,N))
					if r == 'x':
						tr += "-rotX-"
						w = rotateX(w, N)
					elif r == 'z':
						tr += "-rotZ-"
						w = rotateZ(w, N)
	return "no transform"

w = (13,1,2)
print(rotateX(w,4))
print(rotateY(w,4))
print(rotateZ(w,4))

print(find_transformation((1,1,1),(13,1,2), 4))

exit()
for m in range(0, 3):
	
	N = (m+1) * 2
	print("Processing ", N, " length binary sequences")
	type_classes, c = calculateTypes(N, mirror=False)
	
	
	
	# for c1, c2 in combinations(type_classes,2):
	# 	if c1.intersection(c2):
	# 		c1.update(c2)
	# 		c2.update(c1)
	# res = set(map(frozenset, type_classes))

	print("Number of classes: ", c)
	f = open(str(N)+"x"+str(N)+"x"+str(N)+"_classes.txt", "w")
	for i, tc in enumerate(type_classes):
		f.write("type "+ str(i)+ " members:"+ str(len(tc))+"\n")
		for t in tc:
			f.write("\t"+str(t)+"\n")
	f.close()

	f = open(str(N)+"x"+str(N)+"x"+str(N)+"_classes_short.txt", "w")
	for i, tc in enumerate(type_classes):
		f.write("type "+ str(i)+ " members:"+ str(len(tc))+"\n")
		f.write("\t"+str(tc.pop())+"\n")
	f.close()

	# f = open(str(N)+"x"+str(N)+"x"+str(N)+"_classes_derivatives.txt", "w")
	# for i, tc in enumerate(type_classes):
	# 	f.write("type "+ str(i)+ " members:"+ str(len(tc))+"\n")
	# 	for t in tc:
	# 		f.write("\t[[")
	# 		for x in t:
	# 			f.write('{:0{N}b}'.format(x>>N-1, N=1)+",")
	# 		f.write("], \n")
	# 		for x in t:
	# 			f.write("\t\t[")
	# 			f.write('{:0{N}b}'.format(x-ISHFTC(x,1,N), N=N))
	# 			f.write("], \n")
	# 		f.write("\t], \n")
		
	# f.close()
	
		
    
		