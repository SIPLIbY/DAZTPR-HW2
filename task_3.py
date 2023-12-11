def get_loops(nodes):
    loops = []
    seen = set()
    for idx in range(len(nodes)):
        if nodes[idx] not in seen:
            loop = [nodes[idx]]
            seen.add(nodes[idx])
            for next_idx in range(idx+1, len(nodes)):
                loop.append(nodes[next_idx])
                if nodes[next_idx] == nodes[idx]:
                    loops.append(loop[:-1])
                    break
    return loops

def third_task():    
    model = Model(solver_name=CBC)
    model.verbose = 0
    x = [[model.add_var(var_type=BINARY) for j in V] for i in V]
    model.objective = minimize(xsum(c[i][j] * x[i][j] for i in V for j in V))
    
    for i in V:
        model += xsum(x[i][j] for j in V - {i}) == 1
    for i in V:
        model += xsum(x[j][i] for j in V - {i}) == 1
        
    model.optimize()
    while True:
        sn = []
        for n in V:
            if n not in sn:                       
                sn.append(n)
                nn = n
                while True:                    
                    nn = [i for i in V if x[nn][i].x == 1][0]
                    sn.append(nn)
                        
                    if nn == n:
                        break
        sn = get_loops(sn)
        if len(sn) == 1:
            break
        for k in range(len(sn)):
            model += xsum(x[i][j] for i in sn[k] for j in sn[k]) <= len(sn[k]) - 1
        model.optimize()

    print("3", model.objective_value)