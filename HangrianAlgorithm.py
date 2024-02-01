class HungarianAlgorithm():
    def __init__(self, n1, n2, edges) -> None:
        self.n1 = n1
        self.n2 = n2
        self.n = n1 + n2  
        self.edges = edges.copy()
        self.m = len(edges)
        self.dist = [[0 for i in range(self.n)] for j in range(self.n)]
        for e in self.edges:
            self.dist[e[0]][e[1]] = self.dist[e[1]][e[0]] = e[2] 


    def solve(self):
        self.y = [0] * self.n 
        for i in range(self.n1):
            self.y[i] = max(self.dist[i])+1

        self.M = [[0 for i in range(self.n)] for j in range(self.n)]
        self.is_in_matching = [0] * self.n
        for i in range(self.n1):
            self.start_round()
        answer = 0
        for i in range(self.n1):
            for j in range(self.n):
                if self.M[i][j]:
                    answer += self.dist[i][j]
        return answer


    def start_round(self):
        pass
        self.adj_out = [[] for j in range(self.n)]
        self.candidate_adj_out = [[] for j in range(self.n)]
        for i in range(self.n1):
            for j in range(self.n1, self.n):
                if self.y[j] + self.y[i] == self.dist[i][j]:
                    if self.M[i][j]:
                        self.adj_out[j].append(i)
                    else:
                        self.adj_out[i].append(j)

        for i in range(self.n1):
            for j in range(self.n1, self.n):
                if self.y[j] + self.y[i] > self.dist[i][j]:
                    if self.M[i][j]:
                        continue
                    else:
                        self.candidate_adj_out[i].append((j, self.y[j]-self.dist[i][j]))
        
        for i in range(self.n1):
            self.candidate_adj_out[i].sort(key=lambda x: x[1], reverse=True)
        
        self.par = [-1] * self.n
        for i in range(self.n1):
            if not self.is_in_matching[i]:
                if self.par[i] == -1:
                    self.par[i] = i
                    if self.dfs(i):
                        return 1
        
        while True:
            mn = 1e9 
            for i in range(self.n1):
                if self.par[i] != -1:
                    while len(self.candidate_adj_out[i]) > 0 and self.par[self.candidate_adj_out[i][-1][0]] != -1:
                        self.candidate_adj_out[i].pop()
                    if len(self.candidate_adj_out[i]) > 0:
                        mn = min(mn, self.y[i] + self.candidate_adj_out[i][-1][1])
            for i in range(self.n1):
                if self.par[i] != -1:
                    self.y[i] -= mn 
            for i in range(self.n1, self.n):
                if self.par[i] != -1:
                    self.y[i] += mn 

            for i in range(self.n1):
                if self.par[i] != -1:
                    while len(self.candidate_adj_out[i]) > 0 and self.y[i] + self.candidate_adj_out[i][-1][1] == 0:
                        (j, w) = self.candidate_adj_out[i].pop()
                        if self.par[j] == -1:
                            self.par[j] = i 
                            if self.dfs(j):
                                return 

    def dfs(self, i):
        pass
        if i >= self.n1 and not self.is_in_matching[i]:
            self.change_mathcing(i)
            return 1 
        for j in self.adj_out[i]:
            if self.par[j] == -1:
                self.par[j] = i
                if self.dfs(j):
                    return 1
        return 0 

    def change_mathcing(self, j):
        vs = [j]
        while self.par[j] != j:
            j = self.par[j] 
            vs.append(self.par[j])
        vs = vs[::-1]
        for i in range(len(vs)-1):
            if i % 2 == 0:
                self.M[vs[i]][vs[i+1]] = self.M[vs[i+1]][vs[i]] = 1
            else:
                self.M[vs[i]][vs[i+1]] = self.M[vs[i+1]][vs[i]] = 0
        self.is_in_matching[vs[0]] = self.is_in_matching[vs[-1]] = 1 


A = HungarianAlgorithm(3, 3, [(0,3,1), (0,4,2), (1,4,2), (1,5,5), (2,5,3)])
print(A.solve())

