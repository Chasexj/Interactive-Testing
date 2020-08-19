import itertools
import math
from scipy.special import comb
import sys
import random

t,k,v,l,end_val = [int(i) for i in sys.argv[1:]]

p = 1/(v**t)

N = 1

a = 0
cov_dict = {(cols, vals) : 0 for cols in itertools.combinations(range(k), t) for vals in itertools.product(range(v), repeat=t)}

def g(x, T):
	s = 0.0
	for i in range(0, l-cov_dict[T]-x+1):
		prod = comb(N-len(ca)-1, i)
		prod *= p**i
		prod *= (1-p)**(N-len(ca)-i-1)
		s += prod
	return s

def h():
	s = 0.0
	for i in range(0, l):
		prod = comb(N, i)
		prod *= p**i
		prod *= (1-p)**(N-i)
		s += prod
	return s

def find_smallest_N_that_works_init():
	global N
	while True:
		s = comb(k,t)*(v**t)*h()
		if s > 1:
			N += 1
			# print(N, s)
		else:
			break

def find_smallest_N_that_works_dec():
	global N
	while True:
		s = 0.0
		for t_set,num_times in cov_dict.items():
			if num_times < l:
				s += g(1,t_set)
		if s < 1:
			N -= 1
		else:
			N += 1
			break


it = 0
find_smallest_N_that_works_init()
#print('Initial Estimate:', N)
ca = [[0 for val in range(k)]]
for cols in itertools.combinations(range(k), t):
	vals = tuple(0 for i in range(t))
	cov_dict[(cols,vals)] = 1

###############
counter_end = 1
###############
while True:
	t_sets_left = {elem : val for elem,val in cov_dict.items() if val < l}
	if len(t_sets_left) == 0:
		break
	row = [-1 for i in range(k)]
	
	for col in range(k):
		expec_dict = dict()
		for val in range(v):
			expectations = []
			some_t_set = False
			items = list(t_sets_left.items())
			for idx, t_set in enumerate(items):
				t_set = t_set[0]
				cols,vals = t_set
				d = {c:v for c,v in zip(cols, vals)}
				fixed_cols = [i for i in cols if row[i] != -1]
				if col in cols:
					some_t_set = True
					vals_in_row = [row[i] for i in fixed_cols] + [val]
					vals_in_set = [d[i] for i in fixed_cols] + [d[col]]
					if vals_in_row != vals_in_set:
						prob = 0.0
					else:
						f = t - len(fixed_cols)
						prob = 1/v**f
				else:
					fixed_cols = [i for i in cols if row[i] != -1]
					if any(d[i] != row[i] for i in fixed_cols):
						prob = 0.0
					else:
						f = t - len(fixed_cols)
						prob = 1/v**f
				expectations.append(prob*g(2,t_set) + (1-prob)*g(1,t_set))
			expec_dict[val] = sum(i for i in sorted(expectations))
		best_val = min(expec_dict, key=expec_dict.get)

		row[col] = best_val
	it += 1
	ca.append(row)
	if counter_end == end_val:
		break
	else:
		counter_end = counter_end + 1
	for t_set in t_sets_left:
		cols, vals = t_set
		vals_in_row = tuple(row[col] for col in cols)
		if vals_in_row == vals and cov_dict[t_set] < l:
			cov_dict[t_set] += 1
	if any(val < l for val in cov_dict.values()):
		curr_N = N
		find_smallest_N_that_works_dec()
		if curr_N > N:
			#print('Updated Estimate:', N)
			a=1


with open("dca.txt","w") as f:
	for rows in ca:
		for i in rows:
			f.write(str(i))
import pprint
#pprint.pprint(ca)
