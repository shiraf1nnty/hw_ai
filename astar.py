# astar.py
import math, time, heapq, sys

def parse_graph(path):
    verts = {}
    adj = {}
    S = D = None
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            parts = [p.strip() for p in line.split(',')]
            if parts[0] == 'S':
                S = int(parts[1])
            elif parts[0] == 'D':
                D = int(parts[1])
            elif len(parts) == 2:
                vid = int(parts[0])
                cell = int(parts[1])
                x = cell // 10
                y = cell % 10
                verts[vid] = (x, y)
                adj.setdefault(vid, {})
            elif len(parts) == 3:
                u = int(parts[0])
                v = int(parts[1])
                w = float(parts[2])
                adj.setdefault(u, {})
                adj.setdefault(v, {})
                # store smallest weight if duplicates appear
                adj[u][v] = min(adj[u].get(v, float('inf')), w)
                adj[v][u] = min(adj[v].get(u, float('inf')), w)

    # validate vertices and S/D presence
    if S is None or D is None:
        print("ERROR: Missing S or D definition in input file.")
        sys.exit(1)
    missing = [n for n in adj if n not in verts]
    if missing:
        print(f"ERROR: Vertex definitions missing for IDs {missing}")
        sys.exit(1)
    return verts, adj, S, D

def h_zero(n, g, verts): return 0.0
def h_euclid(n, g, verts):
    xn, yn = verts[n]
    xg, yg = verts[g]
    return math.hypot(xn - xg, yn - yg)
def h_manhattan(n, g, verts):
    xn, yn = verts[n]
    xg, yg = verts[g]
    return abs(xn - xg) + abs(yn - yg)

def astar(verts, adj, S, D, hfunc):
    start = time.perf_counter()
    g_cost = {v: float('inf') for v in verts}
    parent = {}
    g_cost[S] = 0.0
    pushes = 0
    expanded = 0
    max_frontier = 0
    heap = []

    f_start = g_cost[S] + hfunc(S, D, verts)
    heapq.heappush(heap, (f_start, S, 0.0))
    pushes += 1
    max_frontier = max(max_frontier, len(heap))

    while heap:
        f, node, g_at_push = heapq.heappop(heap)
        if abs(g_at_push - g_cost[node]) > 1e-12:
            continue
        expanded += 1
        if node == D:
            runtime = time.perf_counter() - start
            path = reconstruct(parent, S, D)
            return {
                'cost': g_cost[D],
                'path': path,
                'expanded': expanded,
                'pushes': pushes,
                'max_frontier': max_frontier,
                'runtime': runtime
            }
        for nei, w in adj.get(node, {}).items():
            ng = g_cost[node] + w
            if ng + 1e-12 < g_cost[nei]:
                g_cost[nei] = ng
                parent[nei] = node
                f2 = ng + hfunc(nei, D, verts)
                heapq.heappush(heap, (f2, nei, ng))
                pushes += 1
                max_frontier = max(max_frontier, len(heap))

    runtime = time.perf_counter() - start
    return {
        'cost': None,
        'path': None,
        'expanded': expanded,
        'pushes': pushes,
        'max_frontier': max_frontier,
        'runtime': runtime
    }

def reconstruct(parent, S, D):
    if S == D:
        return [S]
    path = []
    cur = D
    while True:
        path.append(cur)
        if cur == S:
            break
        cur = parent.get(cur)
        if cur is None:
            return None
    return list(reversed(path))

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: python astar.py <inputfile> <mode>  # mode: ucs|euclid|manhattan")
        sys.exit(1)
    inp = sys.argv[1]
    mode = sys.argv[2]
    verts, adj, S, D = parse_graph(inp)
    if mode == 'ucs':
        h = h_zero
    elif mode == 'euclid':
        h = h_euclid
    elif mode == 'manhattan':
        h = h_manhattan
    else:
        print("Mode must be ucs|euclid|manhattan")
        sys.exit(1)
    res = astar(verts, adj, S, D, h)
    MODE = {'ucs': 'UCS', 'euclid': 'A* Euclidean', 'manhattan': 'A* Manhattan'}[mode]
    print(f"MODE: {MODE}")
    if res['cost'] is None:
        print("Optimal cost: NO PATH")
    else:
        print(f"Optimal cost: {res['cost']}")
        print("Path:", " -> ".join(map(str, res['path'])))
    print(f"Expanded: {res['expanded']}")
    print(f"Pushes: {res['pushes']}")
    print(f"Max frontier: {res['max_frontier']}")
    print(f"Runtime (s): {res['runtime']:.6f}")
