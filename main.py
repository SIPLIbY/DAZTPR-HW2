import time 
from itertools import product 
from sys import stdout as out 
from networkx import minimum_cut, DiGraph 
from mip import Model, xsum, BINARY, CBC, minimize 
 
start_time = time.time() 
 
places = ['Antwerp','C-Mine', 'Ghent', 'Hasselt', 'Mechelen', 'Montagne de Bueren', 'Remouchamps'] 
 
dists = [[81, 52, 73, 23, 105, 124], 
        [125, 13, 71, 38, 59], 
        [114, 54, 139, 155], 
        [61, 36, 57], 
        [89, 107], 
        [22], 
        []] 
 
n, V = len(dists), set(range(len(dists))) 
c = [[0 if i == j 
      else dists[i][j-i-1] if j > i 
      else dists[j][i-j-1] 
      for j in V] for i in V] 
for i in range(0,6): 
    print(c[i]) 
 
def Assigment(): 
    model = Model(solver_name=CBC) 
    x = [[model.add_var(var_type=BINARY) for j in V] for i in V] 
    model.objective = minimize(xsum(c[i][j] * x[i][j] for i in V for j in V)) 
    for i in V: 
        model += xsum(x[i][j] for j in V - {i}) == 1 
    for i in V: 
        model += xsum(x[j][i] for j in V - {i}) == 1 
    model.optimize() 
    return model.objective_value 
 
def SalesMan(): 
    start_timee = time.time() 
    model = Model(solver_name=CBC) 
    x = [[model.add_var(var_type=BINARY) for j in V] for i in V] 
    y = [model.add_var() for i in V] 
    model.objective = minimize(xsum(c[i][j] * x[i][j] for i in V for j in V)) 
    for i in V: 
        model += xsum(x[i][j] for j in V - {i}) == 1 
    for i in V: 
        model += xsum(x[j][i] for j in V - {i}) == 1 
    for (i, j) in product(V - {0}, V - {0}): 
        if i != j: 
            model += y[i] - (n + 1) * x[i][j] >= y[j] - n 
    model.optimize() 
    print('This Time worked def SalesMan: ', (time.time() - start_timee)) 
    return model.objective_value 
 
def CreateGraph(x): 
    I = DiGraph() 
    for i in V: 
        for j in V: 
                I.add_edge(places[i], places[j], capacity=(x[i][j]).x) 
    return I 
 
def FindCycle(x): 
    counter = 0 
    nc = 0 
    while True: 
        nc = [i for i in V if x[nc][i].x >= 0.99][0] 
        counter += 1 
        if nc == 0: 
            break 
    if (counter == len(places)): 
        return False 
    else: 
        return True 
 
 
def CuttinPlane(model, x): 
    iter = 1 
    Abs = [] 
    Check = FindCycle(x) 
    PPAP = [] 
 
    for i, j in product(places, places): 
        if i != j: 
            PPAP.append((i, j)) 
    if (Check==False): 
        print(model.objective_value) 
    while Check: 
        I = CreateGraph(x) 
 
 
        if (iter == 1): 
            if (model.objective_value == Assigment()): 
                print('Iter First Success') 
            else: 
                print('Iter First NotSuccess') 
 
        for (a, b) in PPAP: 
            cut_value, Abs = minimum_cut(I, a, b) 
            if cut_value <= 0.99: 
                model += (xsum(x[k][q] for k in V for q in V if (places[k] in Abs[1] and places[q] in Abs[1])) <= len(Abs[1]) - 1) 
        if Check != False: 
            cp = model.generate_cuts() 
            if cp.cuts == True: 
                model += cp 
 
 
        model.optimize(relax=True) 
        print(model.objective_value) 
        iter += 1 
        print('КОЛИЧЕСТВО ИТЕРАЦИЙ: ', iter) 
        Check = FindCycle(x) 
        if (Check == False): 
            if (model.objective_value == SalesMan()): 
                print('Iter Last Success') 
            else: 
                print('Iter Last NotSuccess') 
    return model.objective_value 
 
 
def main():

    print(123)

    start_time = time.time() 
 
    model = Model() 
 
    x = [[model.add_var(var_type=BINARY) for j in V] for i in V] 
 
    model.objective = (xsum(c[i][j] * x[i][j] for i in V for j in V)) 
 
    for i in V: 
        model += xsum(x[i][j] for j in V - {i}) == 1 
    for i in V: 
        model += xsum(x[j][i] for j in V - {i}) == 1 
 
    model.optimize(relax=True) 
    print(model.objective_value) 
    Answer = CuttinPlane(model, x) 
    print('This Time worked def main: ', (time.time() - start_time)) 
 
 
main()