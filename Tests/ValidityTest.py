import sys
sys.path.insert(1, '../Algorithms')
sys.path.insert(1, '../Generators')
from HungarianAlgorithm import HungarianAlgorithm
from MatchingLP import MatchingLP
from TestHandler import TestGenerator, TestType
from MultiplicativeAuction import MultiplicativeAuction


for test_type in TestType:
    print(f'testing {test_type}:')
    for i in range(1, 2):
        test = TestGenerator.get_casual_test(test_type, i)
        matchingLP = MatchingLP(test['n'], test['edges'])
        hungarianAlgorithm = HungarianAlgorithm(test['n1'], test['n2'], test['edges'])
        multiplicativeAuction = MultiplicativeAuction(test['n1'], test['n2'], test['edges'])
        print(f'test {i}:')
        print(f'hungarian answer: {hungarianAlgorithm.solve()} ', end='')
        print(f'lp answer: {matchingLP.solve()}', end=' ')
        print(f'multiplicativeAuction answer: {multiplicativeAuction.solve(0.999)}')
