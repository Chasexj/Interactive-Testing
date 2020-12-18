import itertools
import random
import pprint

# example CA
A = [[0,0,0,1,0,1],
[0,0,1,0,1,0],
[0,1,0,0,0,1],
[0,1,1,1,0,0],
[1,0,0,0,1,1],
[1,0,1,0,0,0],
[1,1,0,1,1,0],
[1,1,1,0,1,1],
[1,0,1,1,1,1],
[1,1,0,1,0,1],
[0,1,0,1,1,1],
[0,0,0,1,0,0],
[0,0,1,0,0,1],
[1,1,0,0,1,0]]

# params of CA
N = len(A)
t = 3
k = len(A[0])
v = 2
num_pop = 30

# interaction population
col_tuples = itertools.combinations(range(k), t)
val_tuples = itertools.product(range(v), repeat=t)
interactions = list(itertools.product(col_tuples, val_tuples))

def ordered_crossover(parent1,parent2):
	a, b = random.sample(range(N), 2)
	if a > b:
		a, b = b, a
	# crossover points
	slice1, slice2 = [True] * N, [True] * N
	for i in range(N):
		if i < a or i > b:
			slice1[parent2[i]] = False
			slice2[parent1[i]] = False
	child1, child2 = parent1, parent2
	# filling
	k1, k2 = b + 1, b + 1
	for i in range(N):
		if not slice1[parent1[(i + b + 1) % N]]:
			child1[k1 % k] = parent1[(i + b + 1) % N]
			k1 += 1
		if not slice2[parent2[(i + b + 1) % N]]:
			child2[k2 % k] = parent2[(i + b + 1) % N]
			k2 += 1
	# slice swap
	for i in range(a, b + 1):
		child1[i], child2[i] = child2[i], child1[i]
	return child1, child2

# return a list with len(A) with randomly row permutation
def random_permutation():
	s = list(range(N))
	random.shuffle(s)
	return s

def fitness(permutation):
	B = []
	for row_id in permutation:
		B.append(A[row_id][:])
	totals = 0
	# finds the interactions' first occurance (row appeared) in B
	for interaction in interactions:
		cols, vals = interaction
		for idx, row in enumerate(B):
			vals_in_row = tuple(row[col] for col in cols)
			if vals_in_row == vals:
				totals += idx
				break
	return totals


population = [random_permutation() for i in range(num_pop)]

# genetic algorithm for min mean-time-to-failure (MTTF)
best = float('inf')
while True:
	fitnesses = []
	for permutation in population:
		fitnesses.append((fitness(permutation), permutation))
	fitnesses.sort()
	m = min(x[0] for x in fitnesses)
	if m < best:
		# prints the best MTTF (total, not the average), 
		# average can be found by dividing this number by (k choose t)*v^t
		print(m)
		best = m

	# Mutation
	# Take the low half of population (i.e., most fit)
	population = [x[1][:] for x in fitnesses[:num_pop//2]]
	half_end = 0
	#ordered crossover for populating the second half
	for i in range(num_pop//2):
		if i % 2 == 0:
			# if i is the last row in the first half, use the first row with it to perform the cross over
			parent1 = population[i]
			if i == (num_pop//2) - 1:
				parent2 = population[0]
				half_end = 1
			else:
				parent2 = population[i+1]
			child1, child2 = ordered_crossover(parent1,parent2)
			population.append(child1)
			if half_end == 0:
				population.append(child2)