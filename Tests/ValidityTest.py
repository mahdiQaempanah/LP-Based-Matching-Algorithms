import sys
sys.path.insert(1, '../Algorithms')
sys.path.insert(1, '../Generators')
from HungarianAlgorithm import HungarianAlgorithm
from MatchingLP import MatchingLP
from TestHandler import TestGenerator, TestType
from MultiplicativeAuction import MultiplicativeAuction

for i in range(1, 3):
    test = TestGenerator.get_test(TestType.CS, i)
    matchingLP = MatchingLP(test['n'], test['edges'])
    hungarianAlgorithm = HungarianAlgorithm(test['n1'], test['n2'], test['edges'])
    multiplicativeAuction = MultiplicativeAuction(test['n1'], test['n2'], test['edges'])
    print(f'test {i}:')
    print(f'hungarian algorithm answer: {hungarianAlgorithm.solve()}')
    print(f'lp answer: {matchingLP.solve()}')
    print(f'multiplicativeAuction algorithm answer: {multiplicativeAuction.solve(0.1)}')
