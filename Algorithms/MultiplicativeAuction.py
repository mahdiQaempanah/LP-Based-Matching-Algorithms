import math 

class MultiplicativeAuction():
    def __init__(self, n1, n2, edges) -> None:
        self.n1 = n1
        self.n2 = n2
        self.n = n1 + n2  
        self.main_edges = edges.copy()
        self.m = len(edges)

    def solve(self, epsilon):
        self.main_epsilon = epsilon
        self.w_max = max([edge[2] for edge in self.main_edges])
        self.edges = [edge for edge in self.main_edges if edge[2] >= self.w_max*epsilon/self.n]
        self.edges = [(i, j, w/(self.w_max*epsilon/self.n)) for (i,j,w) in self.edges]

        self.epsilon = 2 / math.ceil(2/(epsilon/2))

        self.y = [0] * self.n
        self.util = [0] * self.m
        self.matched_to = [-1] * self.n 
        self.Q = [[] for i in range(self.n1)]

        L = []  
        max_coefficient = round((1-self.epsilon)/(self.epsilon/2))
        for id, (v1, v2, w) in enumerate(self.edges):
            for coff in range(max_coefficient+1):
                j = coff*(self.epsilon/2) + self.epsilon
                i = math.floor(math.log(j*w, 1+self.epsilon))
                L.append((i, id))
        L = MultiplicativeAuction.RadixSort(L)
        for i, edge_id in L:
            self.Q[self.edges[edge_id][0]].append((i, edge_id))

        for i in range(self.n1):
            self.matchr(i)
        return self.get_answer()

    def matchr(self, i):
        while len(self.Q[i]) > 0:
            j, uv_id = self.Q[i][-1]
            v_, u_, w_ = self.edges[uv_id]
            self.util[uv_id] = w_ - self.y[u_]
            if self.util[uv_id] < math.pow(1+self.epsilon, j):
                self.Q[i].pop()
                continue 
            else:
                self.y[u_] += self.epsilon*w_
                if self.matched_to[u_] == -1:
                    self.matched_to[u_] = v_
                    break 
                else: 
                    previous = self.matched_to[u_]
                    self.matched_to[u_] = v_
                    self.matchr(previous)
                    break 

    @staticmethod
    def RadixSort(L): #sort elements by first value
        mx = max([l[0] for l in L])
        mn = min([l[0] for l in L])
        parts = dict([(i,[]) for i in range(mn, mx+1)])
        for l in L:
            parts[l[0]].append(l)
        ret = []
        for i in range(mn, mx+1):
            ret.extend(parts[i])
        return ret 

    def get_answer(self):
        help = [-1] * self.n
        answer = []
        for i, j, w in self.edges:
            if self.matched_to[j] == i:
                help[j] = max(help[j], w)

        for i, j, w in self.edges:
            if self.matched_to[j] == i and help[j] == w:
                answer.append((i,j,w))
                help[j] = -1
        return sum([i[2] for i in answer])*(self.w_max*self.main_epsilon/self.n)


A = MultiplicativeAuction(1, 2, [(0,1,1), (0,2,1)])




