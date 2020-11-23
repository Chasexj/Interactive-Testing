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

col_tuples = itertools.combinations(range(k), t)
val_tuples = itertools.product(range(v), repeat=t)
interactions = list(itertools.product(col_tuples, val_tuples))

def random_permutation():
	s = list(range(N))
	random.shuffle(s)
	return s

def fitness(permutation):
	B = []
	for row_id in permutation:
		B.append(A[row_id][:])
	totals = 0
	for interaction in interactions:
		cols, vals = interaction
		for idx, row in enumerate(B):
			vals_in_row = tuple(row[col] for col in cols)
			if vals_in_row == vals:
				totals += idx
				break
	return totals


population = [random_permutation() for i in range(num_pop)]

# I call this a "gEnEtIc aLgOrItHm"
best = float('inf')
while True:
	fitnesses = []
	for permutation in population:
		fitnesses.append((fitness(permutation), permutation))
	fitnesses.sort()
	m = min(x[0] for x in fitnesses)
	if m < best:
		# this prints the best MTTT (total, not the average)
		# The average can be found by dividing this number
		# 		by (k choose t)*v^t
		print(m)
		best = m

	# Mutation
	# Take the low half of population (i.e., most fit)
	population = [x[1][:] for x in fitnesses[:num_pop//2]]
	for i in range(num_pop//2):
		population.append(random_permutation())

	# Todo: ordered crossover