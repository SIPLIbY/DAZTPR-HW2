from itertools import product
from sys import stdout as out
from mip import Model, xsum, minimize, BINARY, CBC

places = ['Antwerp', 'Bruges', 'C-Mine', 'Dinant', 'Ghent',
            'Grand-Place de Bruxelles', 'Hasselt', 'Leuven',
            'Mechelen', 'Mons', 'Montagne de Bueren', 'Namur',
            'Remouchamps', 'Waterloo']

# distances in an upper triangular matrix
dists = [[83, 81, 113, 52, 42, 73, 44, 23, 91, 105, 90, 124, 57],
        [161, 160, 39, 89, 151, 110, 90, 99, 177, 143, 193, 100],
        [90, 125, 82, 13, 57, 71, 123, 38, 72, 59, 82],
        [123, 77, 81, 71, 91, 72, 64, 24, 62, 63],
        [51, 114, 72, 54, 69, 139, 105, 155, 62],
        [70, 25, 22, 52, 90, 56, 105, 16],
        [45, 61, 111, 36, 61, 57, 70],
        [23, 71, 67, 48, 85, 29],
        [74, 89, 69, 107, 36],
        [117, 65, 125, 43],
        [54, 22, 84],
        [60, 44],
        [97],
        []]

# number of nodes and list of vertices
n, V = len(dists), set(range(len(dists)))

# distances matrix
c = [[0 if i == j
    else dists[i][j-i-1] if j > i
    else dists[j][i-j-1]
    for j in V] for i in V]



def original_code():
    model = Model(solver_name=CBC)
    model.verbose = 0
    x = [[model.add_var(var_type=BINARY) for j in V] for i in V]
    y = [model.add_var() for i in V]

    model.objective = minimize(xsum(c[i][j]*x[i][j] for i in V for j in V))

    for i in V:
        model += xsum(x[i][j] for j in V - {i}) == 1

    for i in V:
        model += xsum(x[j][i] for j in V - {i}) == 1

    for (i, j) in product(V - {0}, V - {0}):
        if i != j:
            model += y[i] - (n+1)*x[i][j] >= y[j]-n

    model.optimize()

    return model.objective_value

#### YOUR CODE HERE

# TASK 1
def task_1():
    model = Model(solver_name=CBC)
    model.verbose = 0
    x = [[model.add_var() for j in V] for i in V]
    y = [model.add_var() for i in V]

    model.objective = minimize(xsum(c[i][j]*x[i][j] for i in V for j in V))

    for i in V:
        model += xsum(x[i][j] for j in V - {i}) == 1

    for i in V:
        model += xsum(x[j][i] for j in V - {i}) == 1

    for (i, j) in product(V - {0}, V - {0}):
        if i != j:
            model += y[i] - (n+1)*x[i][j] >= y[j]-n

    # optimizing
    model.optimize(relax = True)
    
    return model.objective_value

print(f"TASK_1: {task_1()}")

print(f"DIFFERENCE BETWEEN INTEGER AND CONTINUOUS VALUES", original_code() - task_1(), "\n")

# TASK 2
def task_2():
    model = Model(solver_name=CBC)
    model.verbose = 0
    x = [[model.add_var(var_type=BINARY) for j in V] for i in V]
    model.objective = minimize(xsum(c[i][j] * x[i][j] for i in V for j in V))
    for i in V:
        model += xsum(x[i][j] for j in V - {i}) == 1
    for i in V:
        model += xsum(x[j][i] for j in V - {i}) == 1
    model.optimize()
    return model.objective_value

print("TASK_2: ", task_2())

# TASK 3