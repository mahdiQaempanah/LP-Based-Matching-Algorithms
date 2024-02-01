import math

n, m = map(int, input().split())
edges = []
adjacency_graph = [[] for _ in range(n + 1)]
for i in range(m):
    u, v, w = map(int, input().split())
    adjacency_graph[u].append((v, w, i))
    adjacency_graph[v].append((u, w, i))
    edges.append((u, v, w))

first_match = []
second_match = []
deleted = [False for _ in range(n + 1)]
i = 1

for v in range(1, n + 1):
    if deleted[v]:
        continue
    # start a path from v
    x = v
    connected = True
    while connected:  # while there might be any edge incident to x
        # find the heaviest such edge
        heavy_edge = -1
        heavy_weight = -math.inf
        for u, w, edge in adjacency_graph[x]:
            if not deleted[u] and w > heavy_weight:
                heavy_edge = edge
                heavy_weight = w
        if heavy_weight < 0:
            connected = False
        else:
            if i == 1:
                first_match.append(heavy_edge)
            else:
                second_match.append(heavy_edge)
            i = 3 - i
            deleted[x] = True
            # go to the adjacent vertex
            u, v, _ = edges[heavy_edge]
            x = u + v - x
first_weight = 0
second_weight = 0
for edge in first_match:
    u, v, w = edges[edge]
    first_weight += w
for edge in second_match:
    u, v, w = edges[edge]
    second_weight += w

if first_weight > second_weight:
    print(first_weight)
    print(first_match)
else:
    print(second_weight)
    print(second_match)
