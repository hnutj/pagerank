from pre_process_withStrip import maxvalue,blocksize
import numpy as np

#constant
beta=0.85
beta_op=1-beta
epsilon=0.0001


with open("block_strip.txt","r") as M_file:
    #parameters init
    load_r=0
    S=0.0
    distance=0.0
    r_old=np.array([1.0/float(maxvalue)]*(maxvalue))
    r_new=np.array([beta_op/float(maxvalue)]*blocksize)

    #calculation for r_new without normalization
    with open("r_.txt","a") as rnew_file:
        rnew_file.truncate(0)
        ##for each strip do:
        while True:
            ###1.read the correspondent block of sparse matrix saved in block_strip.txt
            M=list()
            lines=list()
            while True:
                line=M_file.readline()
                if line[0]=='#':
                    break
                else:
                    lines.append(line)

            ###and save it into the variable M 
            ###with the pattern (<id of node>,<out degree of node>,<adjacent striped nodes>)
            for entry in lines:
                figures=entry.split(" ")
                node_id=figures[0]
                node_degree=figures[1]
                del figures[0:2]
                M.append((int(node_id),int(node_degree),list(map(int,figures))))

            ###2.calculation in the strip
            for entry in M:
                for out_node in entry[2]:
                    r_new[out_node-1-load_r]+=beta*(r_old[entry[0]-1])/float(entry[1])

            ###3.append the strip of r_new to r_.txt
            str_arr=list(map(str,r_new))
            block_data=" ".join(str_arr)
            rnew_file.write(block_data+"\n")

            ###4.update the related parameters S for normalization and load_r for next strip
            S+=np.sum(r_new)
            load_r+=blocksize

            ###5.conditions to jump out
            if load_r<maxvalue-blocksize:
                r_new=np.array([beta_op/float(maxvalue)]*blocksize)
            elif load_r<maxvalue:
                r_new=np.array([beta_op/float(maxvalue)]*(maxvalue-load_r))
            else:
                break
    
    #normalization
    normalize_constant=(1.0-S)/float(maxvalue)
    with open("r_.txt","r") as r0_file,open("r_normalized.txt","a") as r1_file:
        ##clear r1_file
        r1_file.truncate(0)

        rold_counter=0
        line=r0_file.readline()
        line=line.strip("\n")
        ##for each strip do:
        while load_r>0:
            strip_r=np.array(list(map(float,line.split(" "))))
            ###add normalize_constant and accumulate the norm 1
            for i in range(len(strip_r)):
                strip_r[i]+=normalize_constant
                distance+=abs(strip_r[i]-r_old[rold_counter])
                rold_counter+=1

            ###save the normalized strip in r_normalized.txt
            str_arr=list(map(str,strip_r))
            block_data=" ".join(str_arr)
            r1_file.write(block_data+"\n")

            ###update parameters for next round
            load_r-=blocksize
            line=r0_file.readline()
            line=line.strip("\n")
    
    #more iterations
    while distance>epsilon:
        #parameters init and load r_old
        load_r=0
        S=0.0
        distance=0.0
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

        #calculation for r_new without normalization
        with open("r_.txt","a") as rnew_file:
            ##relocate the file pointer
            rnew_file.truncate(0)
            M_file.seek(0)

            ##for each strip do:
            while True:
                ###1.read the correspondent block of sparse matrix saved in block_strip.txt
                M=list()
                lines=list()
                while True:
                    line=M_file.readline()
                    if line[0]=='#':
                        break
                    else:
                        lines.append(line)

                ###and save it into the variable M 
                ###with the pattern (<id of node>,<out degree of node>,<adjacent striped nodes>)
                for entry in lines:
                    figures=entry.split(" ")
                    node_id=figures[0]
                    node_degree=figures[1]
                    del figures[0:2]
                    M.append((int(node_id),int(node_degree),list(map(int,figures))))

                ###2.calculation in the strip
                for entry in M:
                    for out_node in entry[2]:
                        r_new[out_node-1-load_r]+=beta*(r_old[entry[0]-1])/float(entry[1])

                ###3.append the strip of r_new to r_.txt
                str_arr=list(map(str,r_new))
                block_data=" ".join(str_arr)
                rnew_file.write(block_data+"\n")

                ###4.update the related parameters S for normalization and load_r for next strip
                S+=np.sum(r_new)
                load_r+=blocksize

                ###5.conditions to jump out
                if load_r<maxvalue-blocksize:
                    r_new=np.array([beta_op/float(maxvalue)]*blocksize)
                elif load_r<maxvalue:
                    r_new=np.array([beta_op/float(maxvalue)]*(maxvalue-load_r))
                else:
                    break
            
        #normalization
        normalize_constant=(1.0-S)/float(maxvalue)
        with open("r_.txt","r") as r0_file,open("r_normalized.txt","a") as r1_file:
            ##clear r1_file
            r1_file.truncate(0)

            rold_counter=0
            line=r0_file.readline()
            line=line.strip("\n")
            ##for each strip do:
            while load_r>0:
                strip_r=np.array(list(map(float,line.split(" "))))
                ###add normalize_constant and accumulate the norm 1
                for i in range(len(strip_r)):
                    strip_r[i]+=normalize_constant
                    distance+=abs(strip_r[i]-r_old[rold_counter])
                    rold_counter+=1

                ###save the normalized strip in r_normalized.txt
                str_arr=list(map(str,strip_r))
                block_data=" ".join(str_arr)
                r1_file.write(block_data+"\n")

                ###update parameters for next round
                load_r-=blocksize
                line=r0_file.readline()
                line=line.strip("\n")
    

#read the final r into memory   
with open("r_normalized.txt","r") as rnew_file:
    rnew_list=list()
    while True:
        line=rnew_file.readline()
        if line:
            line=line.strip("\n")
            rnew_list=rnew_list+list(map(float,line.split()))
        else:
            break
    r_new=np.array(rnew_list)

#rank the scores of nodes
rank=list()
for i in range(maxvalue):
    rank.append((r_new[i],i+1))
rank=sorted(rank,reverse=True)

#write the result into .txt
with open("striped_result.txt","x") as result_file:
    lines=list()
    for i in range(100):
        line=str(rank[i][1])+" "+str(rank[i][0])+"\n"
        lines.append(line)
    result_file.writelines(lines)