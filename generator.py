class CodeGenerator:
    def __init__(self, code):
        self._intermediate_code = code
        self.block_dict = {}
        self.blocks = []
        self.target_code = {}
                        
    def emit(self):
        print(self._assembly_code)

    def isReserved(self, text):
        return False

    def isAssignment(self, text):
        return False

    def add(self, x, y, z): 
        one = f"LD R0, {x} \n"
        two = f"LD R1, {y} \n"
        three = "ADD R0, R0, R1 \n"
        four = f"ST {z}, R0 \n"
        return one + two + three + four

    def sub(self, x, y, z):
        one = f"LD R0, {x} \n"
        two = f"LD R1, {y} \n"
        three = "SUB R0, R0, R1 \n"
        four = f"ST {z}, R0 \n"
        return one + two + three + four

    def mul(self, x, y, z):
        one = f"LD R0, {x} \n"
        two = f"LD R1, {y} \n"
        three = "MUL R0, R0, R1 \n"
        four = f"ST {z}, R0 \n"
        return one + two + three + four

    def div(self, x, y, z):
        one = f"LD R0, {x} \n"
        two = f"LD R1, {y} \n"
        three = "DIV R0, R0, R1 \n"
        four = f"ST {z}, R0 \n"
        return one + two + three + four

    def assign(self, x, z):
        if x[0] == "'" and x[-1] == "'":
            x = x[1:-2]
        elif x == "True":
            x = 1
        elif x == "False":
            x = 0
        
        one = f"LD R0, {x} \n"
        two = f"ST {z}, R0 \n"
        return one + two
    
    def iffalse_jump(self, x, y, z, jump_line):
        
        if y is None or z is None:
            one = f"LD R0, {x} \n"
            two = f"BEQZ R0, ##{jump_line} \n"
            return one + two
        
        else:        
        
            one = f"LD R0, {x} \n"
            if z not in ["True", "False"]:
                two = f"LD R1, {z} \n"
            else:
                two = ""
            
            if y == ">":
                three = f"BLE R0, R1, ##{jump_line} \n"
            elif y == ">=":
                three = f"BLT R0, R1 ##{jump_line} \n"
            elif y == "<":
                three = f"BGE R0, R1, ##{jump_line} \n"
            elif y == "<=":
                three = f"BGT R0, R1, ##{jump_line} \n"
            elif y == "==":
                if z == "True":
                    three = f"BEQZ R0, ##{jump_line} \n"
                elif z == "False":
                    three = f"BNEZ R0, ##{jump_line} \n"
                else:
                    three = f"BNE R0, R1, ##{jump_line} \n"
            elif y == "~=":
                if z == "True":
                    three = f"BNEZ R0, ##{jump_line} \n"
                elif z == "False":
                    three = f"BEQZ R0, ##{jump_line} \n"
                else:
                    three = f"BEQ R0, R1, ##{jump_line} \n"
                
            else:
                raise RuntimeError("Invalid Operator")
                
            return one + two + three
        
    def if_jump(self, x, y, z, jump_line):
        
        if y is None or z is None:
            one = f"LD R0, {x} \n"
            two = f"BNEZ R0, ##{jump_line}## \n"
            return one + two
        
        else:        
        
            one = f"LD R0, {x} \n"
            
            if z not in ["True", "False"]:
                two = f"LD R1, {z} \n"
            else:
                two = ""
            
            if y == ">":
                three = f"BGT R0, R1, ##{jump_line} \n"
            elif y == ">=":
                three = f"BGE R0, R1 ##{jump_line} \n"
            elif y == "<":
                three = f"BLT R0, R1, ##{jump_line} \n"
            elif y == "<=":
                three = f"BLE R0, R1, ##{jump_line} \n"
            elif y == "==":
                if z == "True":
                    three = f"BNEZ R0, ##{jump_line} \n"
                elif z == "False":
                    three = f"BEQZ R0, ##{jump_line} \n"
                else:
                    three = f"BEQ R0, R1, ##{jump_line} \n"
            elif y == "~=":
                if z == "True":
                    three = f"BNEZ R0, ##{jump_line} \n"
                elif z == "False":
                    three = f"BEQZ R0, ##{jump_line} \n"
                else:
                    three = f"BNE R0, R1, ##{jump_line} \n"
            else:
                raise RuntimeError("Invalid Operator")
                
            return one + two + three
        
        
    def containsOperator(self, text):
        ops = ["+", "-", "*", "/"]
        for op in ops:
            if op in text:
                return True
        return False
    
        
    def evaluate(self):
        intermediate_code = self._intermediate_code.split("\n")
        for i in range(len(intermediate_code)):
            line = intermediate_code[i]
            code = line.strip()
            code = line.replace("\t","")
            
            inter_line = code.split(":")
            code = inter_line.pop(-1)
            
            new_block = Block()
            self.blocks.append(new_block)
            
            for line in inter_line:
                self.block_dict[line] = new_block
            
            if len(code) != 0:
                                    
                if "iffalse" in code:
                    
                    left_right_split = code.split(" goto ")
                    jump_line = left_right_split[1]
                    
                    condition = left_right_split[0].replace("iffalse ","").split(" ")
                    
                    if len(condition) > 1:
                        first_value = condition[0]
                        second_value = condition[1]
                        third_value = condition[2]
                        
                        target = self.iffalse_jump(first_value, second_value, third_value, jump_line)
                        
                    else:
                        
                        first_value = condition[0]
                        
                        target = self.iffalse_jump(first_value, None, None, jump_line)
                        
                    new_block.add_code(target)
                    
                elif "if" in code:
                    
                    left_right_split = code.split(" goto ")
                    jump_line = left_right_split[1]
                    
                    condition = left_right_split[0].replace("if ","").split(" ")
                    
                    if len(condition) > 1:
                        first_value = condition[0]
                        second_value = condition[1]
                        third_value = condition[2]
                        
                        target = self.if_jump(first_value, second_value, third_value, jump_line)
                        
                    else:
                        
                        first_value = condition[0]
                        
                        target = self.if_jump(first_value, None, None, jump_line)
                        
                    new_block.add_code(target)
                    
                elif "goto" in code:
                    
                    jump_line = code.replace("goto ", "")
                    
                    target = f"B ##{jump_line} \n"
                    
                    new_block.add_code(target)
                    
                elif "=" in code:
                    left_right_split = code.split(" = ")
                    right_array = left_right_split[1]
    
                    statement_array = right_array.split(' ')
                    assigned = left_right_split[0]
                    if not self.isReserved(assigned) and self.containsOperator(right_array):
                        first_value = statement_array[0]
                        ops = statement_array[1]
                        second_value = statement_array[2]
                        if ops == "+":
                            target = self.add(first_value, second_value, assigned)
                        elif ops == "-":
                            target = self.sub(first_value, second_value, assigned)
                        elif ops == "*":
                            target = self.mul(first_value, second_value, assigned)
                        elif ops == "/":
                            target = self.div(first_value, second_value, assigned)
                    elif not self.containsOperator(right_array):
                        target = self.assign(right_array, assigned)
                        
                    new_block.add_code(target)
                    
    def compile_code(self):
        
        line_num = 0
        
        for block in self.blocks:
            
            block.start_line = line_num
            
            for temp_line in block.lines:
                
                self.target_code[line_num] = temp_line
                line_num += 1
                
        self.target_code[line_num] = ""
        
        for i in self.target_code.keys():
            
            line = self.target_code[i].strip()
            
            line_list = line.split("##")
            
            if not len(line_list) == 1:
                
                target_line = self.block_dict[line_list[1]].start_line
                
                line = line_list[0] + str(target_line)
                
                self.target_code[i] = line
            
        with open("Target Code.txt", "w", encoding="utf-8") as file:
            
            for i in self.target_code.keys():
                
                file.write(str(i)+":" + self.target_code[i] + "\n")
                
                print(i, ":", self.target_code[i])       


class Block:
    
    def __init__(self):
        
        self.lines = []
        self.start_line = 0
        
    def add_code(self, code):
        
        temp = code.split("\n")
        
        for line in temp:
            if line != "":
                self.lines.append(line)


file = open("C:/Users/Arjun/Desktop/Arjun Files/School/Fifth Year/" +
            "Compiling/Compiler/Intermediate/inter 5.txt", 
            encoding="utf-8")
code = file.read()
file.close()
generator = CodeGenerator(code)
generator.evaluate()
generator.compile_code()

