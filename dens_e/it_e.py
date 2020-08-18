import math
import random
import matplotlib.pyplot as plt
import itertools
import os

def row_covers_the_interaction(row,interaction):
    cols,vals = interaction
    for col,val in zip(cols,vals):
        if row[col] != val:
            return False
    return True

def run(t,k,v):
    ca = []
    interactions = []
    for cols in itertools.combinations(range(k), t):
        for vals in itertools.product(range(v), repeat=t):
            interactions.append((cols,vals))
    # record all possible interactions
    all_interactions = interactions
    while True:
        if len(interactions) == 0:
            # we are  done
            break
        expectation = math.ceil(len(interactions)/v**t)

        # loop to find at least  the  expected  number
        while True:
            # generate a random  row
            row = [random.choice(range(v)) for i in range(k)]
            # now  check if it gets at  least the expectation
            num_cov = 0
            for interaction in interactions:
                if row_covers_the_interaction(row,interaction):
                    num_cov += 1
            if num_cov >= expectation:
                break
        ca.append(row)
        interactions = [i for i in interactions if not row_covers_the_interaction(row ,i)]
    return ca, all_interactions

def ld_percent_check(result_ca,all_interactions,ld,t,k,v):
    #times covered for each interaction
    ld_coverage = [0]*len(all_interactions)

    for rows in result_ca:
        #interate through all possible interactions
        for j in range(len(all_interactions)):
            interactions = all_interactions[j]
            cols = interactions[0]
            vals = interactions[1]
            interaction_cover_check = 1
            for i in range(len(cols)):
                #check if the row examining fails to match the interaction examining
                if rows[cols[i]] != vals[i]:
                    interaction_cover_check = 0
            if interaction_cover_check == 1:
                ld_coverage[j] = ld_coverage[j]+1
    #number of interactions covered at least ld times
    int_sat = 0
    #finding the percent of interactions covered at least ld times
    for covered_times in ld_coverage:
        if covered_times >= ld:
            int_sat = int_sat+1
    return int(100*(int_sat/len(all_interactions)))

def ca_trimmer(n,k):
    dens_ca_n = [[0 for i in range(k)] for j in range(n)]
    with open("dca.txt","r") as f:
        dca = f.readline()
    count = 0
    dens_ca_rows = len(dens_ca_n)/k
    if dens_ca_rows >= n:
        for i in range(n):
            for j in range(k):
                dens_ca_n[i][j] = int(dca[count])
                count=count+1
    #print(dens_ca_n)
    return dens_ca_n

def scatter(changing_para, random_p, dens_p,changing_param):
    title = "changing "+changing_param+", random = green, dens = red"
    plt.scatter(changing_para,random_p, c="g")
    plt.scatter(changing_para,dens_p, c="r")
    plt.title(title)
    plt.xlabel(changing_param)
    plt.ylabel("P")
    fig = plt.gcf()
    plt.show()
    fig.savefig(title+'.png')
    return 0

def testing(params_to_run,ldl,num_runs_each,changing_param):
    ##values for changing non ld
    values = [0]*len(params_to_run)
    random_p = [0]*len(params_to_run)
    dens_p = [0]*len(params_to_run)

    ##values for changing ld
    #values = [0]*len(ldl)
    #random_p = [0]*len(ldl)
    #dens_p = [0]*len(ldl)

    counter = 0
    prg = 0
    for t,k,v in params_to_run:
        print(t,k,v)
        ##t changing
        #values[counter] = t
        ##k changing
        values[counter] = k
        ##v changing
        #values[counter] = v
        for ld in ldl:
            #ld changing
            #values[counter] = ld
            prg = prg + 1
            t_random_p = 0
            t_dens_p = 0
            print("Progress: "+str(100*(prg/(len(params_to_run)*len(ldl)*num_runs_each)))+"%")
            for i in range(num_runs_each):
                result_ca, all_interactions = run(t,k,v)
                t_random_p = t_random_p+ ld_percent_check(result_ca,all_interactions,ld,t,k,v)
                args = str(t)+" "+str(k)+" "+ str(v)+" "+str(ld)
                os.system("python3 density_e.py "+args)
                dens_ca_n = ca_trimmer(len(result_ca),k)
                t_dens_p = t_dens_p + ld_percent_check(dens_ca_n,all_interactions,ld,t,k,v)
            av_random_p = t_random_p/num_runs_each
            av_dens_p = t_dens_p/num_runs_each
            random_p[counter] = av_random_p
            dens_p[counter] = av_dens_p
            ##ld changing
            #counter = counter + 1

        ##non ld changing
        counter = counter + 1
    print(counter)
    scatter(values,random_p,dens_p,changing_param)

def main():

    ##k changing
    params_to_run = [(2,5,2),(2,6,2),(2,7,2),(2,8,2),(2,9,2),(2,10,2),(2,11,2),(2,12,2),(2,13,2),(2,14,2),(2,15,2),(2,16,2),(2,17,2),(2,18,2),(2,19,2),(2,20,2)]

    ##t changing
    #params_to_run = [(2,8,2),(3,8,2),(4,8,2),(5,8,2),(6,8,2),(7,8,2),(8,8,2)]

    ##v changing
    #params_to_run = [(2,5,2),(2,5,3),(2,5,4),(2,5,5),(2,5,6),(2,5,7),(2,5,8)]
    num_runs_each = 1
    
    #lamda used to check
    ldl = [2]

    ##changing lamda
    #params_to_run=[(2,13,2)]
    #ldl=[1,2,3,4,5,6,7,8,9,10,11,12,13]

    changing_param = "ld"
    testing(params_to_run,ldl,num_runs_each,changing_param)



main()