import itertools

import random

import pprint

import copy

import numpy.random as npr

import sys



filename = sys.argv[1]

with open(filename) as f:

	halfway = filename[3:-4]

	t = int(halfway.split('.')[0])

	v = int(halfway.split('.')[1].split('^')[0])

	k = int(halfway.split('^')[1])

	print(t,k,v)

	lines = [l.strip() for l in f.readlines()]

	A = []

	for line in lines[1:]:

		s = line.split(' ')

		for idx, elem in enumerate(s):

			if elem == '-':

				s[idx] = random.choice(range(v))

			else:

				s[idx] = int(elem)

		A.append(s)

	N = len(A)



# params of CA

# N = len(A)

# t = 3

# k = len(A[0])

# v = 2

num_pop = 100



# interaction population

col_tuples = itertools.combinations(range(k), t)

val_tuples = itertools.product(range(v), repeat=t)

interactions = list(itertools.product(col_tuples, val_tuples))



#fitness proportionate selection
def selectOne(fitnesses):
    max_f = sum(x[0] for x in fitnesses)
    selection_probs = [x[0]/max_f for x in fitnesses]
    return fitnesses[npr.choice(len(fitnesses), p=selection_probs)]

def ordered_crossover(parent1,parent2):
	a, b = random.sample(range(N), 2)
	#print(str(a)+" "+str(b))
	if a > b:
 		a, b = b, a
	#print(str(a)+" "+str(b))
	# crossover points
	sparent1 = copy.deepcopy(parent1)
	sparent2 = copy.deepcopy(parent2)
	child = []
	for _ in range(N):
		child.append('*')
	for i in range(a,b+1):
		child[i]=sparent1[i]
	for i in range(N):
		item = sparent2[i]
		if item not in child:
			for j in range(N):
				if child[j] == '*':
					child[j]=item
					break
	return child


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

def init_fitness():

	totals = 0

	for interaction in interactions:

		cols, vals = interaction

		for idx, row in enumerate(A):

			vals_in_row = tuple(row[col] for col in cols)

			if vals_in_row == vals:

				totals += idx

				break

	return totals

print("Intial total mttf: "+ str(init_fitness()))

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
		#print(population)

	# Mutation
	# Take the low half of population (i.e., most fit)
	population = [x[1][:] for x in fitnesses[:num_pop//2]]
	#ordered crossover for populating the second half
	#print(population)
	for i in range(num_pop//2):
		# if i is the last row in the first half, use the first row with it to perform the cross over
		#print('----')
		#print(i)
		parent1 = copy.deepcopy(selectOne(fitnesses)[1])
		parent2 = copy.deepcopy(selectOne(fitnesses)[1])
		child = ordered_crossover(parent1,parent2)
		while True:
			parent1 = copy.deepcopy(selectOne(fitnesses)[1])
			parent2 = copy.deepcopy(selectOne(fitnesses)[1])
			child = ordered_crossover(parent1,parent2)
			if parent1 != parent2 and child != (parent1 or parent2) and (child not in population):
				break
		population.append(child)
