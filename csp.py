# csp.py
import sys
from collections import deque, defaultdict

def parse(path):
    k = None
    edges = set()
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            if line.startswith('colors='):
                k = int(line.split('=')[1])
            else:
                a, b = [int(x.strip()) for x in line.split(',')]
                if a == b:
                    print("failure")
                    sys.exit(0)
                if a > b:
                    a, b = b, a
                edges.add((a, b))
    if k is None:
        print("failure")
        sys.exit(0)
    vars_set = set()
    for a, b in edges:
        vars_set.add(a)
        vars_set.add(b)
    return k, sorted(vars_set), list(edges)

def neighbors(edges):
    neigh = defaultdict(set)
    for u, v in edges:
        neigh[u].add(v)
        neigh[v].add(u)
    return neigh

def ac3(domains, neigh):
    queue = deque((xi, xj) for xi in neigh for xj in neigh[xi])
    while queue:
        xi, xj = queue.popleft()
        if revise(domains, xi, xj):
            if not domains[xi]:
                return False
            for xk in neigh[xi]:
                if xk != xj:
                    queue.append((xk, xi))
    return True

def revise(domains, xi, xj):
    removed = False
    for x in list(domains[xi]):
        if not any(x != y for y in domains[xj]):
            domains[xi].remove(x)
            removed = True
    return removed

def select_var(domains, assignment):
    unassigned = [v for v in domains if v not in assignment]
    unassigned.sort(key=lambda x: (len(domains[x]), x))
    return unassigned[0] if unassigned else None

def lcv_order(var, domains, neigh):
    counts = []
    for val in domains[var]:
        eliminated = 0
        for nb in neigh[var]:
            if val in domains[nb]:
                eliminated += 1
        counts.append((eliminated, val))
    counts.sort()
    return [v for _, v in counts]

def backtrack(domains, neigh, assignment):
    if len(assignment) == len(domains):
        return dict(assignment)
    var = select_var(domains, assignment)
    for val in lcv_order(var, domains, neigh):
        assignment[var] = val
        saved = {v: set(domains[v]) for v in domains}
        domains[var] = {val}
        if ac3(domains, neigh):
            result = backtrack(domains, neigh, assignment)
            if result:
                return result
        assignment.pop(var)
        for v in domains:
            domains[v] = set(saved[v])
    return None

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python csp.py <input_file>")
        sys.exit(1)
    k, vars_list, edges = parse(sys.argv[1])
    neigh = neighbors(edges)
    domains = {v: set(range(1, k + 1)) for v in vars_list}
    res = backtrack(domains, neigh, {})
    if res:
        ordered = {v: res[v] for v in sorted(res)}
        print("SOLUTION:", ordered)
    else:
        print("failure")
