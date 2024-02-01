import os 
import random 
import math 
from enum import Enum

class TestType(Enum):
    CS = 1
    CD = 2
    WSL = 3
    WSH = 4
    WDL = 5
    WDH = 6

class TestGenerator:
    
    tests_path = {TestType.CS: '../Tests/cs/',
                  TestType.CD: '../Tests/cs/', 
                  TestType.WSL: '../Tests/wsl/',
                  TestType.WSH: '../Tests/wsh/',
                  TestType.WDL: '../Tests/wdl/',
                  TestType.WDH: '../Tests/wdh/'}
    

    def __init__(self) -> None:
        pass 

    @staticmethod
    def generate(test_type, t):
        print(f'making {t} test for {test_type}:')
        base = [10, 100, 500, 1000, 10000]
        n1s = [random.randint(base[i-1]//2, base[i-1]+(base[i-1]//2)) for i in range(1, t+1)]
        n2s = [random.randint(base[i-1]//2, base[i-1]+(base[i-1]//2)) for i in range(1, t+1)]
        n1s[2] = n2s[2] = 500

        edges = [] 
        for test_id in range(1, t+1):
            signle_edges = []
            match test_type:
                case TestType.CS:
                    signle_edges = TestGenerator.cs(n1s[test_id-1], n2s[test_id-1])
                case TestType.CD:
                    signle_edges = TestGenerator.cd(n1s[test_id-1], n2s[test_id-1])
                case TestType.WSL:
                    signle_edges = TestGenerator.wsl(n1s[test_id-1], n2s[test_id-1])
                case TestType.WSH:
                    signle_edges = TestGenerator.wsh(n1s[test_id-1], n2s[test_id-1])
                case TestType.WDL:
                    signle_edges = TestGenerator.wdl(n1s[test_id-1], n2s[test_id-1])
                case TestType.WDH:
                    signle_edges = TestGenerator.wdh(n1s[test_id-1], n2s[test_id-1])
                case _:
                    return Exception(f"invalid test type:{test_type}")
            edges.append(signle_edges)
        for test_id in range(1, t+1):
            TestGenerator.write_test(f'{TestGenerator.tests_path[test_type]}input{test_id}.txt', n1s[test_id-1], n2s[test_id-1], edges[test_id-1])
            print(f'test number {test_id} added succesfully.')
        print()

    @staticmethod
    def write_test(path, n1, n2, edges):
        with open(path, 'w') as f:
            f.write(f'{n1} {n2} {len(edges)}\n')
            f.write("\n".join([f"{i} {j} {k}" for (i,j,k) in edges]))


    @staticmethod
    def sparse(n1, n2):
        m_factor = random.randint(10, 30)
        m = int(min(m_factor*(n1+n2), n1*n2, 1e5))
        edge_tmp = random.sample(range(0, n1*n2), m)
        edge = [(i//n1, (i%n2)+n1) for i in edge_tmp]
        return edge 
    
    @staticmethod
    def dense(n1, n2):
        m_factor = int(math.sqrt(n1+n2)) * random.randint(1, 15)
        m = int(min(m_factor*(n1+n2), n1*n2, 1e5))
        edge_tmp = random.sample(range(0, n1*n2), m)
        edge = [(i//n1, (i%n2)+n1) for i in edge_tmp]
        return edge 

    @staticmethod
    def low_weight(n1, n2, edges):
        answer = [(i, j, random.randint(0, len(edges)*5)) for (i,j) in edges]
        return answer 
    
    @staticmethod
    def high_weight(n1, n2, edges):
        answer = [(i, j, random.randint(0, 1e9)+1) for (i,j) in edges]
        return answer 

    @staticmethod
    def cs(n1, n2):
        edges = TestGenerator.sparse(n1, n2)
        edges = [(i, j, 1) for (i,j) in edges]
        return edges
    
    @staticmethod
    def cd(n1, n2):
        edges = TestGenerator.dense(n1, n2)
        edges = [(i, j, 1) for (i,j) in edges]
        return edges
    
    @staticmethod
    def wsl(n1, n2):
        edges = TestGenerator.sparse(n1, n2)
        answer = TestGenerator.low_weight(n1, n2, edges)
        return answer

    @staticmethod
    def wsh(n1, n2):
        edges = TestGenerator.dense(n1, n2)
        answer = TestGenerator.high_weight(n1, n2, edges)
        return answer

    @staticmethod
    def wdl(n1, n2):
        edges = TestGenerator.sparse(n1, n2)
        answer = TestGenerator.low_weight(n1, n2, edges)
        return answer

    @staticmethod
    def wdh(n1, n2):
        edges = TestGenerator.dense(n1, n2)
        answer = TestGenerator.high_weight(n1, n2, edges)
        return answer
    
    @staticmethod
    def get_test(test_type, test_id):
        test = {}
        with open(f'{TestGenerator.tests_path[test_type]}/input{test_id}.txt', 'r') as f:
            txt = f.read()
            txt_split = txt.split('\n')
            n1n2m , edges_str = txt_split[0], txt_split[1:]
            n1, n2, m = map(int, n1n2m.split())
            edges = []
            for s in edges_str:
                i, j, w = map(int, s.split())
                edges.append((i, j, w))
            test = {'n1':n1, 'n2':n2, 'm':m, 'n':n1+n2, 'edges':edges}
        return test


t = 5
for test_type in TestType:
    TestGenerator.generate(test_type, t)




