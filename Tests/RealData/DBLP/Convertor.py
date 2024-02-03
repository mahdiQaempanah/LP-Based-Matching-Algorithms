def write_test(path, n1, n2, edges):
        with open(path, 'w') as f:
            f.write(f'{n1} {n2} {len(edges)}\n')
            f.write("\n".join([f"{i} {j} {w}" for (i,j,w) in edges]))


with open('edges.dat', 'r') as f:
    txt = f.read()
infos = txt.split('\n')
edges = [] 
for s in infos:
    try:
        i, j, w = s.split()
    except Exception:
         print(s)
    edges.append((int(i[1:]), int(j[1:]), int(w)))

n1 = max([x[0] for x in edges])+1
n2 = max([x[1] for x in edges])+1
edges = [(i,j+n1, w) for (i,j,w) in edges]
write_test('./v.txt', n1, n2, edges)
