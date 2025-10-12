# astar.py
import math, time, heapq, sys

def parse_graph(path):
    verts = {}
    adj = {}
    S = D = None
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'): continue
            parts = [p.strip() for p in line.split(',')]
            if parts[0] == 'S':
                S = int(parts[1])
            elif parts[0] == 'D':
                D = int(parts[1])
            elif len(parts) == 2:
                vid = int(parts[0]); cell = int(parts[1])
                x = cell // 10; y = cell % 10
                verts[vid] = (x,y)
                adj.setdefault(vid, [])
            elif len(parts) == 3:
                u = int(parts[0]); v = int(parts[1]); w = float(parts[2])
                adj.setdefault(u, []).append((v,w))
                adj.setdefault(v, []).append((u,w))
    return verts, adj, S, D

def h_zero(n, g, verts): return 0
def h_euclid(n, g, verts):
    xn,yn = verts[n]; xg,yg = verts[g]
    return math.hypot(xn-xg, yn-yg)
def h_manhattan(n, g, verts):
    xn,yn = verts[n]; xg,yg = verts[g]
    return abs(xn-xg) + abs(yn-yg)

def astar(verts, adj, S, D, hfunc):
    start = time.perf_counter()
    g_cost = {v: float('inf') for v in verts}
    parent = {}
    g_cost[S] = 0
    pushes = 0
    expanded = 0
    heap = []
    heapq.heappush(heap, (hfunc(S,D,verts), S, S, 0.0))  # (f, tie, node, g_at_push)
    pushes += 1
    max_frontier = 1
    while heap:
        if len(heap) > max_frontier: max_frontier = len(heap)
        f, tie, node, g_at_push = heapq.heappop(heap)
        # only expand if this entry has current best g
        if abs(g_at_push - g_cost[node]) > 1e-12:
            continue
        expanded += 1
        if node == D:
            runtime = time.perf_counter() - start
            path = reconstruct(parent, S, D)
            return {'cost': g_cost[D], 'path': path, 'expanded': expanded, 'pushes': pushes, 'max_frontier': max_frontier, 'runtime': runtime}
        for nei, w in adj.get(node,[]):
            ng = g_cost[node] + w
            if ng + 1e-12 < g_cost[nei]:
                g_cost[nei] = ng
                parent[nei] = node
                f2 = ng + hfunc(nei, D, verts)
                heapq.heappush(heap, (f2, nei, nei, ng))
                pushes += 1
    runtime = time.perf_counter() - start
    return {'cost': None, 'path': None, 'expanded': expanded, 'pushes': pushes, 'max_frontier': max_frontier, 'runtime': runtime}

def reconstruct(parent, S, D):
    if S == D: return [S]
    path = []
    cur = D
    while True:
        path.append(cur)
        if cur == S: break
        cur = parent.get(cur)
        if cur is None: return None
    return list(reversed(path))

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: python astar.py <inputfile> <mode>  # mode: ucs|euclid|manhattan")
        sys.exit(1)
    inp = sys.argv[1]; mode = sys.argv[2]
    verts, adj, S, D = parse_graph(inp)
    if mode == 'ucs': h = h_zero
    elif mode == 'euclid': h = h_euclid
    elif mode == 'manhattan': h = h_manhattan
    else:
        print("mode must be ucs|euclid|manhattan")
        sys.exit(1)
    res = astar(verts, adj, S, D, h)
    MODE = {'ucs':'UCS','euclid':'A* Euclidean','manhattan':'A* Manhattan'}[mode]
    print(f"MODE: {MODE}")
    if res['cost'] is None:
        print("Optimal cost: NO PATH")
        print("Expanded:",res['expanded'],"Pushes:",res['pushes'],"Max frontier:",res['max_frontier'],"Runtime (s):",res['runtime'])
    else:
        print("Optimal cost:",res['cost'])
        print("Path:", " -> ".join(map(str,res['path'])))
        print("Expanded:",res['expanded'],"Pushes:",res['pushes'],"Max frontier:",res['max_frontier'],"Runtime (s):",res['runtime'])
