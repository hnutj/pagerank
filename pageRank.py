#from preprocess import maxvalue,blocksize
import numpy as np

#constant
maxvalue=8297
blocksize=10
beta=0.85
beta_op=1-beta
epsilon=0.15

#initial r
r_old=np.array([1.0/float(maxvalue)]*(maxvalue))
with open("block_strip.txt","r") as M_file:
    #read the block into memory
    load_r=0
    S=0
    distance=0
    r_new=np.array([beta_op/float(maxvalue)]*blocksize)
    with open("r_.txt","a") as rnew_file:
        rnew_file.truncate(0)
        while True:
            M=list()
            lines=list()
            while True:
                line=M_file.readline()
                if line[0]=='#':
                    break
                else:
                    lines.append(line)

            #save in list
            for entry in lines:
                figures=entry.split(" ")
                node_id=figures[0]
                node_degree=figures[1]
                del figures[0:2]
                M.append((int(node_id),int(node_degree),list(map(int,figures))))

            #calculation
            for entry in M:
                for out_node in entry[2]:
                    r_new[out_node-1-load_r]+=beta*(r_old[entry[0]-1])/float(entry[1])
            

            #pre normalization for S
            S+=np.sum(r_new)
            for i in range(len(r_new)):
                distance+=abs(r_new[i]-r_old[load_r+i])

            #pre load next
            load_r+=blocksize
            #save r_new block
            str_arr=list(map(str,r_new))
            block_data=" ".join(str_arr)
            rnew_file.write(block_data+"\n")

            if load_r<maxvalue-blocksize:
                r_new=np.array([beta_op/float(maxvalue)]*blocksize)
            elif load_r<maxvalue:
                r_new=np.array([beta_op/float(maxvalue)]*(maxvalue-load_r))
            else:
                break
        #normalization
        normalize_constant=(1.0-S)/float(maxvalue)
    
    #normalization
    with open("r_.txt","r") as r0_file,open("r_normalized.txt","a") as r1_file:
        r1_file.truncate(0)
        line=r0_file.readline()
        line=line.strip("\n")
        while load_r>0:
            strip=np.array(list(map(float,line.split(" "))))
            for i in range(len(strip)):
                strip[i]+=normalize_constant
            
            #save r_new block
            str_arr=list(map(str,strip))
            block_data=" ".join(str_arr)

            r1_file.write(block_data+"\n")

            load_r-=blocksize
            line=r0_file.readline()
            line=line.strip("\n")
    
    round=1
    while distance>epsilon:
        round+=1
        print("round: ",round,"distance: ",distance)
        load_r=0
        S=0
        distance=0
        rold_list=list()
        with open("r_normalized.txt","r") as rold_file:
            while True:
                line=rold_file.readline()
                if line:
                    line=line.strip("\n")
                    rold_list=rold_list+list(map(float,line.split()))
                else:
                    break
        r_old=np.array(rold_list)
        r_new=np.array([beta_op/float(maxvalue)]*blocksize)

        with open("r_.txt","a") as rnew_file:
            rnew_file.truncate(0)
            M_file.seek(0)
            while True:
                M=list()
                lines=list()
                while True:
                    line=M_file.readline()
                    if line[0]=='#':
                        break
                    else:
                        lines.append(line)

                #save in list
                for entry in lines:
                    figures=entry.split(" ")
                    node_id=figures[0]
                    node_degree=figures[1]
                    del figures[0:2]
                    M.append((int(node_id),int(node_degree),list(map(int,figures))))

                #calculation
                for entry in M:
                    for out_node in entry[2]:
                        r_new[out_node-1-load_r]+=beta*(r_old[entry[0]-1])/float(entry[1])
                

                #pre normalization for S
                S+=np.sum(r_new)
                for i in range(len(r_new)):
                    distance+=abs(r_new[i]-r_old[load_r+i])

                #pre load next
                load_r+=blocksize
                #save r_new block
                str_arr=list(map(str,r_new))
                block_data=" ".join(str_arr)
                rnew_file.write(block_data+"\n")

                if load_r<maxvalue-blocksize:
                    r_new=np.array([beta_op/float(maxvalue)]*blocksize)
                elif load_r<maxvalue:
                    r_new=np.array([beta_op/float(maxvalue)]*(maxvalue-load_r))
                else:
                    break
            #normalization
            normalize_constant=(1.0-S)/float(maxvalue)
        
        #normalization
        with open("r_.txt","r") as r0_file,open("r_normalized.txt","a") as r1_file:
            r1_file.truncate(0)
            line=r0_file.readline()
            line=line.strip("\n")
            while load_r>0:
                strip=np.array(list(map(float,line.split(" "))))
                for i in range(len(strip)):
                    strip[i]+=normalize_constant
                
                #save r_new block
                str_arr=list(map(str,strip))
                block_data=" ".join(str_arr)

                r1_file.write(block_data+"\n")

                load_r-=blocksize
                line=r0_file.readline()
                line=line.strip("\n")
    

rank=list()
for i in range(maxvalue):
    rank.append((r_new[i],i+1))

rank=sorted(rank)
for i in range(100):
    print(i,": ",rank[i][1]," rank: ",rank[i][0])
