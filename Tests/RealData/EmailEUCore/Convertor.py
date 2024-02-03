def write_test(path, n1, n2, edges):
        with open(path, 'w') as f:
            f.write(f'{n1} {n2} {len(edges)}\n')
            f.write("\n".join([f"{i} {j} 1" for (i,j) in edges]))


with open('email-Eu-core.txt', 'r') as f:
    txt = f.read()
infos = txt.split('\n')
edges = [] 
for s in infos:
    try:
        i, j = s.split()
    except Exception:
         print(s)
    edges.append((int(i), int(j)))

n1 = max([x[0] for x in edges])+1
n2 = max([x[1] for x in edges])+1
edges = [(i,j+n1) for (i,j) in edges]
write_test('./v.txt', n1, n2, edges)
