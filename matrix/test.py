import re 
# decleration of registors
registors = {
    "eax": "000",
    "ecx": "001",
    "edx": "010", 
    "ebx": "011",
    "edp": "100", 
    "ebp": "101", 
    "esi": "110",
    "edi": "111"
        }
#Decleration of mod and byte
mod = {
    "1" : "00",
    "2" : "01", 
    "4" : "10",
    "8" : "11" 
}



filename = "24111066.asm"
 
with open(filename, "r") as file:
    for line in file:
       # content = line.strip();
        token = re.split(r"[ ,\t]+",line.strip())
        
        if token: 
            if token[0] in ('mov', 'add', 'sub', 'mul'):
                t = [ch for word in token[2] for ch in word ]
            
                reg = str(t[0]+t[1]+t[2]) 
                if t[3] == "*" and t[4] == "4" :
                    k = mod["4"] +  registors[reg]   + registors[token[1]]
                    sib = hex(int(k,2))
                    print(sib)
                elif t[3] == "*" and t[4] == "1" : 
                    k = mod["1"] + registors[reg] + registors[token[1]]
                    sib = hex(int(k,2))
                    print(sib)
                elif t[3] == "*" and t[4] == "3": 
                    k = mod["3"] + registors[reg] + registors[token[1]]
                    sib = hex(int(k,2))
                    print(sib) 
                else: 
                    k = mod["4"] + registors[reg] + registors[token[1]] 
                    sib = hex(int(k,2))
                    print(sib) 
                with open("sib_output.txt", "a") as f: 
                    f.write(sib+"\n");
            else : 
                pass
            
                
