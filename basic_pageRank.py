import pre_process as pre
import numpy as np

#constant
beta=0.85
beta_op=1-beta
epsilon=0.0001

#read M in memory
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
r_old=np.array([1.0/float(pre.maxvalue)]*pre.maxvalue)
r_new=np.array([beta_op/float(pre.maxvalue)]*pre.maxvalue)

#no.1 calculation
for entry in M:
    for out_node in entry[2]:
        r_new[out_node-1]+=beta*(r_old[entry[0]-1])/float(entry[1])

#normalization
S=np.sum(r_new)
normalize_constant=(1.0-S)/float(pre.maxvalue)
for i in range(pre.maxvalue):
    r_new[i]+=normalize_constant

#iteration to converge
while np.linalg.norm(x=r_new-r_old,ord=1)>epsilon:
    ##initial r
    r_old=r_new
    r_new=np.array([beta_op/float(pre.maxvalue)]*pre.maxvalue)
    ##calculation
    for entry in M:
        for out_node in entry[2]:
            r_new[out_node-1]+=beta*(r_old[entry[0]-1])/float(entry[1])
    ##normalization
    S=np.sum(r_new)
    normalize_constant=(1.0-S)/float(pre.maxvalue)
    for i in range(pre.maxvalue):
        r_new[i]+=normalize_constant

#rank the scores of nodes
rank=list()
for i in range(pre.maxvalue):
    rank.append((r_new[i],i+1))
rank=sorted(rank,reverse=True)

#write the result into .txt
with open("basic_result.txt","x") as result_file:
    lines=list()
    for i in range(100):
        line=str(rank[i][1])+" "+str(rank[i][0])+"\n"
        lines.append(line)
    result_file.writelines(lines)
