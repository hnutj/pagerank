from preprocess import maxvalue
import numpy as np

#constant
beta=0.85
beta_op=1-beta
epsilon=0.000001

#input M
M=list()
with open("Data_processed.txt","r") as processedata_file:
    entries=processedata_file.readlines()
    for entry in entries:
        figures=entry.split(" ")
        node_id=figures[0]
        node_degree=figures[1]
        del figures[0:2]
        M.append((int(node_id),int(node_degree),list(map(int,figures))))

#initial r
r_old=np.array([1.0/float(maxvalue)]*maxvalue)
r_new=np.array([beta_op/float(maxvalue)]*maxvalue)
#r_weight=np.array([0.0]*maxvalue)

#no.1 calculation
for entry in M:
    for out_node in entry[2]:
        r_new[out_node-1]+=beta*(r_old[entry[0]-1])/float(entry[1])

S=np.sum(r_new)
normalize_constant=(1.0-S)/float(maxvalue)
for i in range(maxvalue):
    r_new[i]+=normalize_constant
while np.linalg.norm(x=r_new-r_old,ord=1)>epsilon:
    r_old=r_new
    r_new=np.array([beta_op/float(maxvalue)]*maxvalue)
    for entry in M:
        for out_node in entry[2]:
            r_new[out_node-1]+=beta*(r_old[entry[0]-1])/float(entry[1])
    S=np.sum(r_new)
    normalize_constant=(1.0-S)/float(maxvalue)
    for i in range(maxvalue):
        r_new[i]+=normalize_constant

rank=list()
for i in range(maxvalue):
    rank.append((r_new[i],i+1))

rank=sorted(rank)
for i in range(100):
    print(i,": ",rank[i][1]," rank: ",rank[i][0])
