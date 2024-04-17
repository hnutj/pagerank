#:pre_process with strip

#load Data.txt
with open("Data.txt","r") as rawdata_file:
    edges=rawdata_file.readlines()

#generate sparse matrix(unsorted)
maxvalue=0
node2relativeEdges=dict()
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

#get the matrix sorted(both adjacent nodes and node id)
for node_id in node2relativeEdges:
    node2relativeEdges[node_id]=sorted(node2relativeEdges[node_id],key=lambda x:int(x))
node2edges_sortedlist=sorted(node2relativeEdges.items())

#write in Data_processed.txt
with open("Data_processed.txt","a") as processedata_file:
    processedata_file.truncate(0)
    lines=list()
    for entry in node2edges_sortedlist:
        dst_nodes=" ".join(entry[1])
        line=str(entry[0])+" "+str(len(entry[1]))+" "+dst_nodes+"\n"
        lines.append(line)
    processedata_file.writelines(lines)

#constant
blocksize=10

#get the sorted matrix striped
with open("block_strip.txt","a") as blockStrip_file:
    blockStrip_file.truncate(0)
    left=1
    right=1+blocksize
    blocks=list()
    while left<maxvalue:
        for entry in node2edges_sortedlist:
            include_nodes=list()
            for node_str in entry[1]:
                if int(node_str)>=left and int(node_str)<right:
                    include_nodes.append(node_str)
            if len(include_nodes)==0:
                continue
            else:
                dst_nodes=" ".join(include_nodes)
                line=str(entry[0])+" "+str(len(entry[1]))+" "+dst_nodes+"\n"
                blocks.append(line)
        blocks.append("#\n")
        blockStrip_file.writelines(blocks)

        left+=blocksize
        right+=blocksize
        blocks=list()