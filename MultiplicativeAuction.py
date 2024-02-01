import math 

class MultiplicativeAuction():
    def __init__(self, n1, n2, edges) -> None:
        self.n1 = n1
        self.n2 = n2
        self.n = n1 + n2  
        self.edges = edges.copy()
        self.m = len(edges)

    def solve(self, epsilon):
        self.main_epsilon = epsilon
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
        return answer 


A = MultiplicativeAuction(3, 3, [(0,3,1), (0,4,2), (1,4,2), (1,5,5), (2,5,3)])
print(A.solve(0.5))
exit(0)

n1, n2, m = map(int, input().split())
epsilon = float(input())
n = n1 + n2 
epsilon = 2 / math.floor(2/epsilon)
edges = []

for _ in range(m):
    i, j, w = map(int, input().split())
    edges.append((i, j, w))

y = [0] * n
match = [-1] * n 
Q = [[] for i in range(n1)]
L = []
util = [0] * m 

def RadixSort(L):
    mx = max([i[0] for i in L])
    parts = [[] for i in range(mx+1)]
    for l in L:
        parts[l[0]].append(l)
    ret = []
    for i in range(mx+1):
        ret.extend(parts[i])
    return ret 

def matchr(i):
        while len(Q[i]) > 0:
            j, uv_id = Q[i][-1]
            v_, u_, w_ = edges[uv_id]
            util[uv_id] = w_ - y[u_]
            if util[uv_id] < math.pow(1+epsilon, j):
                Q[i].pop()
            else:
                y[u_] += epsilon*w_
                if match[u_] == -1:
                    match[u_] = v_
                    return 
                else: 
                    previous = match[u_]
                    match[u_] = v_
                    matchr(previous)
                    return
        return 

def MultiplicativeAuction():
    global L, Q
    for id, (v1, v2, w) in enumerate(edges):
        max_ratio = round((1-epsilon)/(epsilon/2))
        for ratio in range(max_ratio+1):
            j = ratio*(epsilon/2) + epsilon
            i = math.floor(math.log(j*w, 1+epsilon))
            L.append((i, id))
    L = RadixSort(L)
    for i, edge in L:
        Q[edges[edge][0]].append((i, edge))

    for i in range(n1):
        matchr(i)

    answer = []
    for i, j, w in edges:
        if match[j] == i:
            answer.append((i,j,w))
    print(f'sum:{sum([i[2] for i in answer])}\n')
    for i in answer:
        print(f'{i[0]}:{i[1]}')

MultiplicativeAuction()







