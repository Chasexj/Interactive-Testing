import itertools
import random
import pprint

# example CA
A = [0,0,0,1,0,1]
B = [1,1,0,0,1,0]
N = 6

def ordered_crossover(parent1,parent2):
	a, b = random.sample(range(N), 2)
	if a > b:
		a, b = b, a
	# holes indicate which entries of the parents are within the crossover points
	holes1, holes2 = [True] * N, [True] * N
	for i in range(N):
		if i < a or i > b:
			#holes are swaped
			holes1[parent2[i]] = False
			holes2[parent1[i]] = False

	child1, child2 = parent1, parent2
	# k1 and k2 used for iterating
	k1, k2 = b + 1, b + 1
	for i in range(N):
		# if not contained in the hole
		if not holes1[parent1[(i + b + 1) % N]]:
			#append to child after the hole
			child1[k1 % k] = parent1[(i + b + 1) % N]
			k1 += 1
		if not holes2[parent2[(i + b + 1) % N]]:
			child2[k2 % k] = parent2[(i + b + 1) % N]
			k2 += 1
		# if contained in the hole, skip	
	# Swap the content of the holes
	for i in range(a, b + 1):
		child1[i], child2[i] = child2[i], child1[i]

	return child1, child2

print(ordered_crossover(A,B))