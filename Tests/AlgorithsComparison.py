import json 
import sys
import pandas as pd 
import time 
import multiprocessing

sys.path.insert(1, '../Algorithms')
sys.path.insert(1, '../Generators')
from HungarianAlgorithm import HungarianAlgorithm
from MatchingLP import MatchingLP
from TestHandler import TestGenerator, TestType, RealDataTestType
from MultiplicativeAuction import MultiplicativeAuction
from PathGrowing import PathGrowing

def basic_checker():
    for test_type in TestType:
        print(f'testing {test_type}:')
        for i in range(1, 2):
            test = TestGenerator.get_casual_test(test_type, i)
            matchingLP = MatchingLP(test['n'], test['edges'])
            hungarianAlgorithm = HungarianAlgorithm(test['n1'], test['n2'], test['edges'])
            multiplicativeAuction = MultiplicativeAuction(test['n1'], test['n2'], test['edges'])
            pathGrowing = PathGrowing(test['n'], test['edges'])

            print(f'    test {i}:')
            print(f'        hungarian answer: {hungarianAlgorithm.solve()} ', end='')
            print(f'lp answer: {matchingLP.solve()}', end=' ')
            print(f'pathGrowing answer: {pathGrowing.solve()}', end=' ')
            print(f'multiplicativeAuction answer: {multiplicativeAuction.solve(0.999)}')

def advanced_comparison():
    t, casual_t = 5, 10
    time_threshold = 20
    datas = []
    with open('./result.txt', 'r') as f:
        txt = f.read()
        try: 
            datas = json.loads(txt)
        except Exception as e:
            return e
    
    for test_type in TestType:
        for i in range(1, t+1):
            if len([1 for x in datas if x['test'] == f'{test_type.value}_t{i}']) > 0:
                continue 
            print(f'{test_type}: {i}')
            test = TestGenerator.get_test(test_type, i)
            solver = MatchingLP(test['n'], test['edges']); result_matchingLp = get_solver_results(solver, time_threshold)
            solver = HungarianAlgorithm(test['n1'], test['n2'], test['edges']); result_hungarianAlgorithm = get_solver_results(solver, time_threshold)
            solver = MultiplicativeAuction(test['n1'], test['n2'], test['edges']); result_multiplicativeAuction = get_solver_results(solver, time_threshold)
            solver = PathGrowing(test['n'], test['edges']); result_pathGrowing = get_solver_results(solver, time_threshold)

            real_answer = None
            if result_hungarianAlgorithm['is_finished']:
                real_answer = result_hungarianAlgorithm['answer']
            if result_matchingLp['is_finished']:
                real_answer = result_matchingLp['answer']
            
            result_matchingLp['ratio'] = '-'
            result_hungarianAlgorithm['ratio'] = '-'
            if real_answer != None:
                result_multiplicativeAuction['ratio'] = result_multiplicativeAuction['answer'] / real_answer
                result_pathGrowing['ratio'] = result_pathGrowing['answer'] / real_answer
            else:
                result_multiplicativeAuction['ratio'] = '-'
                result_pathGrowing['ratio'] = '-'

            datas.append({'test':f'{test_type.value}_t{i}', 'n':test['n'], 'm':test['m'], 'algorithm':'hungarian', **result_hungarianAlgorithm})
            datas.append({'test':f'{test_type.value}_t{i}', 'n':test['n'], 'm':test['m'], 'algorithm':'Lp', **result_matchingLp})
            datas.append({'test':f'{test_type.value}_t{i}', 'n':test['n'], 'm':test['m'], 'algorithm':'path growing', **result_pathGrowing})
            datas.append({'test':f'{test_type.value}_t{i}', 'n':test['n'], 'm':test['m'], 'algorithm':'multiplicativeAuction', **result_multiplicativeAuction})
            save_data(datas)

        for i in range(1, casual_t+1):
            if len([1 for x in datas if x['test']==f'{test_type.value}_ct{i}']) > 0:
                continue 
            print(f'{test_type}: casual{i}')
            test = TestGenerator.get_casual_test(test_type, i)
            solver = MatchingLP(test['n'], test['edges']); result_matchingLp = get_solver_results(solver, time_threshold)
            solver = HungarianAlgorithm(test['n1'], test['n2'], test['edges']); result_hungarianAlgorithm = get_solver_results(solver, time_threshold)
            solver = MultiplicativeAuction(test['n1'], test['n2'], test['edges']); result_multiplicativeAuction = get_solver_results(solver, time_threshold)
            solver = PathGrowing(test['n'], test['edges']); result_pathGrowing = get_solver_results(solver, time_threshold)

            real_answer = None
            if result_hungarianAlgorithm['is_finished']:
                real_answer = result_hungarianAlgorithm['answer']
            if result_matchingLp['is_finished']:
                real_answer = result_matchingLp['answer']
            
            result_matchingLp['ratio'] = '-'
            result_hungarianAlgorithm['ratio'] = '-'
            if real_answer != None:
                result_multiplicativeAuction['ratio'] = result_multiplicativeAuction['answer'] / real_answer
                result_pathGrowing['ratio'] = result_pathGrowing['answer'] / real_answer
            else:
                result_multiplicativeAuction['ratio'] = '-'
                result_pathGrowing['ratio'] = '-'

            datas.append({'test':f'{test_type.value}_ct{i}', 'n':test['n'], 'm':test['m'], 'algorithm':'hungarian', **result_hungarianAlgorithm})
            datas.append({'test':f'{test_type.value}_ct{i}', 'n':test['n'], 'm':test['m'], 'algorithm':'Lp', **result_matchingLp})
            datas.append({'test':f'{test_type.value}_ct{i}', 'n':test['n'], 'm':test['m'], 'algorithm':'path growing', **result_pathGrowing})
            datas.append({'test':f'{test_type.value}_ct{i}', 'n':test['n'], 'm':test['m'], 'algorithm':'multiplicativeAuction', **result_multiplicativeAuction})
            save_data(datas)

    
    for test_type in RealDataTestType:
        if len([1 for x in datas if x['test']==test_type.value]) > 0:
                continue 
        print(f'{test_type}:')
        test = TestGenerator.get_real_data_test(test_type)
        solver = MatchingLP(test['n'], test['edges']); result_matchingLp = get_solver_results(solver, time_threshold)
        solver = HungarianAlgorithm(test['n1'], test['n2'], test['edges']); result_hungarianAlgorithm = get_solver_results(solver, time_threshold)
        solver = MultiplicativeAuction(test['n1'], test['n2'], test['edges']); result_multiplicativeAuction = get_solver_results(solver, time_threshold)
        solver = PathGrowing(test['n'], test['edges']); result_pathGrowing = get_solver_results(solver, time_threshold)

        real_answer = None
        if result_hungarianAlgorithm['is_finished']:
            real_answer = result_hungarianAlgorithm['answer']
        if result_matchingLp['is_finished']:
            real_answer = result_matchingLp['answer']
        
        result_matchingLp['ratio'] = '-'
        result_hungarianAlgorithm['ratio'] = '-'
        if real_answer != None:
            result_multiplicativeAuction['ratio'] = result_multiplicativeAuction['answer'] / real_answer
            result_pathGrowing['ratio'] = result_pathGrowing['answer'] / real_answer
        else:
                result_multiplicativeAuction['ratio'] = '-'
                result_pathGrowing['ratio'] = '-'
        datas.append({'test':f'{test_type.value}', 'n':test['n'], 'm':test['m'], 'algorithm':'hungarian', **result_hungarianAlgorithm})
        datas.append({'test':f'{test_type.value}', 'n':test['n'], 'm':test['m'], 'algorithm':'Lp', **result_matchingLp})
        datas.append({'test':f'{test_type.value}', 'n':test['n'], 'm':test['m'], 'algorithm':'path growing', **result_pathGrowing})
        datas.append({'test':f'{test_type.value}', 'n':test['n'], 'm':test['m'], 'algorithm':'multiplicativeAuction', **result_multiplicativeAuction})
        save_data(datas)

    save_data(datas)

def save_data(datas):
    columns = datas[0].keys()
    new_arrange = dict([(key,[data[key] for data in datas]) for key in columns])
    df = pd.DataFrame(new_arrange)
    df.to_csv('./out.csv')
    with open('./result.txt','w') as f:
        f.write(json.dumps(datas))

def get_solver_results(solver, threshold):
    answer = dict()
    queue = multiprocessing.Queue()
    p = multiprocessing.Process(target=run_solver, args=(solver, queue))
    p.start()
    p.join(threshold)

    if p.is_alive():
        p.terminate()
        p.join()
        answer['is_finished'] = False
        answer['t'], answer['answer'] = '-', '-'
        return answer
    else:
        result = queue.get()
        answer['is_finished'] = True
        answer['t'], answer['answer'] = result
        return answer

def run_solver(solver, queue):
    start_time = time.time()
    answer = solver.solve()
    finish_time = time.time()
    queue.put(((finish_time - start_time)*1000, answer))

advanced_comparison()