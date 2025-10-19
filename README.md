# Homework 1 — A* (Three Modes) + CSP (Graph Coloring)

## How to Run

### A* Search
Run in three modes (UCS, Euclidean, Manhattan):

python astar.py inputs/astar_small.txt ucs  
python astar.py inputs/astar_small.txt euclid  
python astar.py inputs/astar_small.txt manhattan  

### CSP Solver
Run graph-coloring solver:

python csp.py inputs/csp_small.txt  
python csp.py inputs/csp_tight.txt  

Each program prints results directly in the required format.

---

## Implementation Details

### A* Search
- Implemented a single A* function with a **pluggable heuristic**.  
- Heuristics used:
  - UCS: h(n)=0  
  - Euclidean: sqrt((x_n - x_g)² + (y_n - y_g)²)  
  - Manhattan: |x_n - x_g| + |y_n - y_g|
- Graph is parsed from text input; edges are undirected and non-negative.  
- The algorithm uses a **min-heap (heapq)** with duplicate entries allowed and expands a node only when the popped `g` equals the best-known cost (to avoid stale entries).  
- Tie-breaking is deterministic using the node ID to ensure reproducibility.  
- Statistics collected: `expanded`, `pushes`, `max_frontier`, and `runtime`.

### CSP (Graph Coloring)
- Implemented using **Backtracking + MRV + LCV + AC-3**.  
- MRV: selects the unassigned variable with the smallest domain.  
- LCV: orders colors to minimize constraint violations.  
- AC-3: enforces arc consistency after every assignment using a queue-based propagation.  
- Self-loops immediately return “failure.”  
- Duplicate edges are normalized automatically.

---

## Analysis (A*)

### 1. Optimality
All three modes return the same optimal path cost, confirming that both Euclidean and Manhattan heuristics are **admissible and consistent** (since all edge weights ≥ heuristic distance).

### 2. Efficiency
As expected:  
UCS (h=0) ≥ Euclidean ≥ Manhattan  
The stronger the heuristic, the fewer nodes expanded and the lower runtime.

### 3. Heuristic Validity
For the provided graphs:
- Edge weights satisfy:  
  w(u,v) ≥ Euclidean(u,v) and w(u,v) ≥ Manhattan(u,v)  
Hence, both heuristics are admissible.

---

## Repository Structure

 - astar.py → A* search (UCS / Euclidean / Manhattan)
- csp.py → CSP solver (Graph Coloring)
- inputs/astar_small.txt
- inputs/astar_medium.txt
- inputs/csp_small.txt
- inputs/csp_tight.txt
- README.md




