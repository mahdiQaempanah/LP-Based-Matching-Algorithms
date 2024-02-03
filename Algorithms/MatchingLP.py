import cvxpy as cp


class MatchingLP:
    def __init__(self, n, edges):
        self.n = n
        self.edges = edges.copy()
        self.m = len(edges)

    def solve(self):
        x = cp.Variable(self.m)
        weights = []
        for u, v, w in self.edges:
            weights.append(w)
        constraints = []
        objective = cp.Maximize(weights @ x)
        vertex_edges = [[] for _ in range(self.n)]
        for edge_id, (u, v, w) in enumerate(self.edges):
            vertex_edges[u].append(edge_id)
            vertex_edges[v].append(edge_id)
        for v in range(self.n):
            constraints.append(sum(x[edge_id] for edge_id in vertex_edges[v]) <= 1)
        constraints.append(x >= 0)
        problem = cp.Problem(objective, constraints)
        problem.solve(solver=cp.ECOS)
        return round(problem.value)


# A = MatchingLP(6, [(0, 3, 1), (0, 4, 2), (1, 4, 2), (1, 5, 5), (2, 5, 3)])