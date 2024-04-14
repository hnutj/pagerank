#preprocess
with open("Data.txt","r") as rawdata_file:
    edges=rawdata_file.readlines()

node2relativeEdges=dict()
maxvalue=0
for e in edges:
    tmp=e.split(" ")
    tmp[1]=tmp[1].strip('\n')
    rE_list=node2relativeEdges.get(int(tmp[0]))
    if rE_list==None:
        rE_list=node2relativeEdges[int(tmp[0])]=list()
    rE_list.append(tmp[1])

    if maxvalue<max(int(tmp[0]),int(tmp[1])):
        maxvalue=max(int(tmp[0]),int(tmp[1]))

print("maxvalue=",maxvalue)
node2edges_sortedlist=sorted(node2relativeEdges.items())

with open("Data_processed.txt","x") as processedata_file:
    lines=list()
    for entry in node2edges_sortedlist:
        dst_nodes=" ".join(entry[1])
        line=str(entry[0])+" "+str(len(entry[1]))+" "+dst_nodes+"\n"
        lines.append(line)
    processedata_file.writelines(lines)


