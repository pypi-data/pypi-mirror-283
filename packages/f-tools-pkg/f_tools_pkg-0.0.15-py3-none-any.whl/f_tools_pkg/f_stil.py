import re

class f_stil:
    def __init__(self):
        pass
    def get_pattern(self,path):
        f = open(path,"r");
        f_list = f.readlines();
        f.close()
        pattern=[]
        scanchain=[[],[]]
        p = 0
        flag=0
        p_flag=0
        s_flag=0
        chainno=0
        scan_in=""
        scan_out=""
        for i in range(0,len(f_list)):
            # find scan IO
            if p_flag < 2:
                obj = re.match("\s*Scan(.+) \"GPIO\[(\w+)\]\"",f_list[i])
                if obj:
                    if obj.group(1).lower() == "in":
                        scan_in = obj.group(2)
                        p_flag +=1
                    if obj.group(1).lower() == "out":
                        scan_out = obj.group(2)
                        p_flag +=1
                    if p_flag == 2:
                        print("si:%s so:%s" %(scan_in,scan_out))
            #find scanStructures
            if s_flag == 0:
                obj =re.match("\s*ScanChain \"(chain)*(\d+)\" {\s*",f_list[i])
                if obj:
                    s_flag =1
                    chainno = int(obj.group(2))
                    continue
            else:
                obj = re.match("\s*ScanLength (\w+);\s*",f_list[i])
                chainlen = int(obj.group(1))
                if chainlen not in scanchain[0]:
                    scanchain[0].append(chainlen)
                    scanchain[1].append([chainno])
                else:
                    idx = scanchain[0].index(chainlen)
                    scanchain[1][idx].append(chainno)
                s_flag = 0
                
            # find scan pattern
            if flag==0:
                obj=re.match("\s*\"pattern (\w+)\": Call \"load_unload\" {\s*",f_list[i])
                if obj:
                    flag = 1
                    p = int(obj.group(1),10)
                    pattern.append(["",""])
                    # print(p)
                    continue
            if flag>=1:
                if f_list[i].find("; }")!=-1:
                    flag = 0
                    continue
                if flag ==1:
                    obj = re.match("\s*\"GPIO\[(\w+)\]\"=\s*",f_list[i])
                    if obj:
                        if obj.group(1) == scan_in:
                            flag = 2 #scan in
                        elif obj.group(1) == scan_out:
                            flag = 3 #scan out
                        continue
                else:
                    if f_list[i].find(";") != -1:
                        flag =1
                        continue
                    pattern[p][flag-2] += f_list[i].strip()
        totalbits = 0
        for l in scanchain[0]:
            plist = scanchain[1][scanchain[0].index(l)]
            slen = len(plist)
            print(l,slen,plist)
            totalbits += slen * l
        print("total %d pattern, %d bits" %(len(pattern),totalbits))    
        return pattern

    def set_pattern(self,s,e,pattern):
        fi= open("pattern_i.h","w")
        fi.write("#include \"type.h\"\n")
        fo=open("pattern_o.h","w")
        fo.write("#include \"type.h\"\n")
        
        for i in range(s,e):
            fi.write(f"uint8_t pattern_i"+str(i)+"[]={\n")
            n = 0
            v = 0
            for c in pattern[i][0]:
                fi.write(c+",")
                if n %16==15:
                    fi.write("/*"+hex(n>>4)+"*/ \n")
                n+=1
            fi.write("};\n")
            
            fo.write("uint8_t pattern_o"+str(i)+"[]={\n")
            n = 0
            for c in pattern[i][1]:
                if(c=="H"):
                    t = 1;
                elif(c=="L"):
                    t = 0
                else:
                    t = 2

                fo.write(str(t)+",")
                if n %16==15:
                    fo.write("/*"+hex(n>>4)+"*/ \n")
                n+=1
            fo.write("};\n")
        fi.write("uint8_t *pattern_i[] = {")
        for i in range(0,e-s):
            fi.write(f"pattern_i{i},")
        fi.write("};\n")
        
        fo.write("uint8_t *pattern_o[] = {")
        for i in range(0,e-s):
            fo.write(f"pattern_o{i},")
        fo.write("};\n")
        
        fi.close()
        fo.close()   