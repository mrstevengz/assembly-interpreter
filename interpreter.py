
def interpret_command(command: str, a):
    cmd = command.strip().replace(",", "").split(" ")

    if len(cmd) > 1:
        #Check if numbers are ints or check and assign if they are in the registerList
        num1 = int(cmd[1]) if cmd[1].isdigit() else a.registerList[cmd[1]]       
        num2 = int(cmd[2]) if cmd[2].isdigit() else a.registerList[cmd[2]]
    else:
        if command.startswith("ret"):
            if a.stack:
                #Set index to last element and pop
                a.idx = a.stack.pop()
            else:
                #If stack is empty, end the loop
                a.idx = a.lineCount
            return
        
    if command.startswith("cmp"):
        a.registerList["flag"] = num1 - num2      

        
    elif command.startswith("mov"):    
        a.registerList[cmd[1]] = num2
    
    elif command.startswith("xor"):      
        a.registerList[cmd[1]] = num1 ^ num2

    elif command.startswith("add"):
        a.registerList[cmd[1]] += num2
        

def interpret_flag(command: str, a):
    cmd = command.strip().replace(",", "").split(" ")
    
    if len(cmd) > 1:
        cond = cmd[0]
        label = cmd[1]
    else:
        raise SyntaxError("Wrong syntax for conditional jumps")
    
    result = a.registerList["flag"]
    
    flag_result = {
        "jmp": True,
        "je": result == 0,
        "jne": result != 0,
        "jg": result > 0,
        "jge": result >= 0,
        "jl": result < 0,
        "jle": result <= 0
    }[cond]
    
    if flag_result:
        #Set line count to the label's index
        a.idx = a.label.get(label)