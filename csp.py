# csp.py
import sys
from collections import deque

def parse(path):
    k = None
    edges = set()
    vars_set = set()
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'): continue
            if line.startswith('colors='):
                k = int(line.split('=')[1])
            else:
                a,b = [int(x.strip()) for x in line.split(',')]
                if a == b:
                    print("failure")
                    sys.exit(0)
                if a>b: a,b = b,a
                edges.add((a,b))
                vars_set.add(a); vars_set.add(b)
    if k is None:
        print("failure"); sys.exit(0)
    return k, sorted(vars_set), list(edges)

def neighbors(edges):
    neigh = {}
    for u,v in edges:
        neigh.setdefault(u, set()).add(v)
        neigh.setdefault(v, set()).add(u)
    return neigh

def ac3(domains, neigh):
    queue = deque([(xi,xj) for xi in domains for xj in neigh.get(xi,[])])
    pruned = []
    while queue:
        xi,xj = queue.popleft()
        revised = False
        to_remove = []
        for a in list(domains[xi]):
            # need some b in domains[xj] where a != b
            found = False
            for b in domains[xj]:
                if a != b:
                    found = True; break
            if not found:
                to_remove.append(a)
        for a in to_remove:
            domains[xi].remove(a)
            pruned.append((xi,a))
            revised = True
        if revised:
            if not domains[xi]:
                return False, pruned
            for xk in neigh.get(xi, []):
                if xk != xj:
                    queue.append((xk, xi))
    return True, pruned

def select_var(domains, assignment):
    un = [v for v in domains if v not in assignment]
    un.sort(key=lambda v: (len(domains[v]), v))
    return un[0] if un else None

def lcv_order(var, domains, neigh):
    counts = []
    for val in sorted(domains[var]):
        eliminated = 0
        for nb in neigh.get(var,[]):
            if val in domains[nb]:
                eliminated += 1
        counts.append((eliminated, val))
    counts.sort()
    return [v for _,v in counts]

def backtrack(domains, neigh, assignment):
    if len(assignment) == len(domains):
        return dict(assignment)
    var = select_var(domains, assignment)
    order = lcv_order(var, domains, neigh)
    saved = {v:set(domains[v]) for v in domains}
    for val in order:
        assignment[var] = val
        domains[var] = {val}
        ok, pruned = ac3(domains, neigh)
        if ok:
            result = backtrack(domains, neigh, assignment)
            if result:
                return result
        # undo changes
        del assignment[var]
        for v in domains:
            domains[v] = set(saved[v])
    return None

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("usage: python csp.py <file>")
        sys.exit(1)
    k, vars_list, edges = parse(sys.argv[1])
    domains = {v:set(range(1,k+1)) for v in vars_list}
    neigh = neighbors(edges)
    assignment = {}
    res = backtrack(domains, neigh, assignment)
    if res:
        # print in consistent sorted order
        out = " ".join(f"{v}:{res[v]}" for v in sorted(res))
        print("SOLUTION:", out)
    else:
        print("failure")
