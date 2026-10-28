import sys

from interpreter import interpret_command, interpret_flag

class Interpreter:
    def __init__(self):
        self.lineCount = 0
        self.idx = 0

        self.commands = {
            "mov": "mov",
            "cmp": "cmp",
            "xor": "xor",
            "add": "add",
            "ret": "ret",
        }

        # Variables related to labels
        self.label = {}
        self.stack = []

        self.flags = {
            "jg": "jg",
            "jge": "jge",
            "jl": "jl",
            "jle": "jle",
            "je": "je",
            "jne": "jne",
            "jmp": "jmp",
        }

        self.registerList = {
            "flag": 0,
            "eax": 0,
            "ebx": 0,
            "ecx": 0,
            "edx": 0,
            "esi": 0,
            "edi": 0,
            "ebp": 0,
            "esp": 0,
        }

    def run(self):
        #Read code on all lines, then strip them for whitespaces and split them in an array.
        command = sys.stdin.read()
        instruction = [line.strip() for line in command.splitlines()]
        
        #Total count of lines, and an index
        self.lineCount = len(instruction) 
        self.idx = 0
        
        #Save labels/functions in hashmap, so we can check for them later
        for i, line in enumerate(instruction):
            if (line.endswith(":")):
                self.label[line.strip(":")] = i
                
        while self.idx < self.lineCount:
            #Save index to compare it later
            current_idx = self.idx
            
            if any(key in instruction[self.idx] for key in self.commands):
                interpret_command(instruction[self.idx], self)
                
            elif any(key in instruction[self.idx] for key in self.flags):
                interpret_flag(instruction[self.idx], self)
                
            elif (instruction[self.idx].endswith(":")):
                pass
            
            else:
                raise SyntaxError("Invalid syntax for assembly")
            
            if self.idx == current_idx:
                #Only add if index hasn't jumped
                self.idx += 1
        
        print(self.registerList, self.label, self.stack)
        

if __name__ == "__main__":
    killme = Interpreter()
    killme.run()

# flag:
# mov eax, edi
# cmp edi, esi
# mov eax, esi
# jg fin

# inicio:
#     cmp ecx, 4
#     jg fin
#     add eax, ecx
#     add ecx, 1
#     jmp inicio
# fin:
#     ret

# contar:
#     xor eax, eax
# inicio:
#     cmp eax, 3
#     jge fin
#     add eax, 1
#     jmp inicio
# fin:
#     ret

#     xor eax, eax   
#     mov ecx, 1    
# inicio:
#     cmp ecx, 4
#     jg fin
#     add eax, ecx
#     add ecx, 1
#     jmp inicio
# fin:
#     ret
