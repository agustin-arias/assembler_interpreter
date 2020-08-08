import sys
# erase all lines in program and write your own assembly code.
program = '''
MOV   a, 8            ; value
MOV   b, 0            ; next
MOV   c, 0            ; counter
MOV   d, 0            ; first
MOV   e, 1            ; second
CALL  proc_fib
CALL  print
END

proc_fib: ; generic time label comment
    CMP   c, 2
    JL    func_0
    MOV   b, d
    ADD   b, e
    MOV   d, e
    MOV   e, b
    INC   c
    CMP   c, a
    JLE   proc_fib
    RET

func_0:
    MOV   b, c
    INC   c
    JMP   proc_fib

print:
    MSG   'Term ', a, ' of Fibonacci series is: ', b        ; output text
    RET
'''


def set_up_commands():
    global MOV, INC, DEC, ADD, SUB, MUL, DIV, JMP, CMP, JNE, JE, JGE, JG, JLE, JL, CALL, RET, MSG, END, COMMENT, commands
    def MOV(args):
        x, y = args[0].strip(', '), args[1]
        registers[x] = get_value(y, registers)
    def INC(args):
        x = args[0]
        registers[x] += 1
    def DEC(args):
        x = args[0]
        registers[x] -= 1
    def ADD(args):
        x, y = args[0].strip(', '), args[1]
        registers[x] += get_value(y, registers)
    def SUB(args):
        x, y = args[0].strip(', '), args[1]
        registers[x] -= get_value(y, registers)
    def MUL(args):
        x, y = args[0].strip(', '), args[1]
        registers[x] *= get_value(y, registers)
    def DIV(args):
        x, y = args[0].strip(', '), args[1]
        registers[x] //= get_value(y, registers)
    def JMP(args):
        global line_number
        lbl = args[0]
        line_number = labels[lbl]
    def CMP(args):
        '''
            CMP  = 0 if equal
            CMP = 1 if x > y
            CMP = -1 if x < y
        '''
        global compare
        x, y = args[0].strip(', '), args[1]
        x, y = get_value(x, registers), get_value(y, registers)
        compare = (x > y) - (x < y)
    def JNE(args):
        global line_number
        if compare != 0:
            lbl = args[0]
            line_number = labels[lbl]
    def JE(args):
        global line_number
        if compare == 0:
            lbl = args[0]
            line_number = labels[lbl]
    def JGE(args):
        global line_number
        if compare >= 0:
            lbl = args[0]
            line_number = labels[lbl]
    def JG(args):
        global line_number
        if compare == 1:
            lbl = args[0]
            line_number = labels[lbl]
    def JLE(args):
        global line_number
        if compare <= 0:
            lbl = args[0]
            line_number = labels[lbl]
    def JL(args):
        global line_number
        if compare == -1:
            lbl = args[0]
            line_number = labels[lbl]
    def CALL(args):
        global line_number, line_number_reference, in_a_function
        lbl = args[0]
        if not in_a_function:
            line_number_reference, in_a_function = line_number, True
        line_number = labels[lbl]
    def RET(args):
        global line_number, in_a_function
        line_number = line_number_reference
        in_a_function = False
    def MSG(args):
        global output
        output = make_msg(args)
    def END(args):
        global line_number, program_ended_successfully
        program_ended_successfully = True
        line_number = total_lines
    def COMMENT(args): pass
    commands = {
        'MOV' : MOV,
        'INC' : INC,
        'DEC' : DEC,
        'ADD' : ADD,
        'SUB' : SUB,
        'MUL' : MUL,
        'DIV' : DIV,
        'JMP' : JMP,
        'CMP' : CMP,
        'JNE' : JNE,
        'JE' : JE,
        'JGE' : JGE,
        'JG' : JG,
        'JLE' : JLE,
        'JL' : JL,
        'CALL' : CALL,
        'RET' : RET,
        'MSG' : MSG,
        'END' : END,
        ';' : COMMENT,
        '' : COMMENT
    }

def set_labels(program):
    global labels
    labels = {}
    for index, line in enumerate(program.split('\n')):
        if line != '' and ':' in line and "'" not in line[:line.index(':')+1]:
            lbl = line[:line.index(':')]
            labels[lbl] = index
    return labels

def get_value(x, registers):
    if x in registers.keys():
        return registers[x]
    return int(x)

def make_msg(string):
    import re
    pattern = r"(', '|.|'.*?')"
    remove_comment = string[:string.index(';')].strip(' ') if ';' in string else string.strip(' ')
    message = re.findall(f"{pattern},", remove_comment) + re.findall(f",? {pattern}$", remove_comment)
    output = ''
    for word in message:
        if word[0] == "'":  # if the word is a literal message, we join it with the ouput
            output += word.strip("'")
        else:
            output += str(get_value(word, registers))
    return output

def assembler_interpreter(program, timer = 1):
    set_up_commands()
    set_labels(program)
    visuals = timer > 0
    global registers, total_lines, in_a_function, program_ended_successfully, line_number
    registers = {}
    total_lines = len(program.split('\n'))
    in_a_function = False
    program_ended_successfully = False
    if visuals:
        gui = program.split('\n')
        gui = [line + ' '*10 for line in gui]
        gui.append(f"registers: {registers}")
    line_number = 1
    while line_number < total_lines:
        line = program.split('\n')[line_number]
        if visuals:
            gui[line_number] += '*'
            gui[-1] = f"registers: {registers}"
            print('\n'*5)  # we center the program output (1)
            print('\n'.join(gui))
            gui[line_number] = gui[line_number].strip('*')
        if line != '':
            command, *args = line.strip(' ').strip('\t').split(' ')
            do_command  = commands[command]
            if command != 'MSG':
                args = list(filter(lambda x : x!='', args))
            else:
                args = line
            do_command(args)
        if visuals and not program_ended_successfully and line_number < total_lines: print('\n'*5)  # and dont print if the program ended
        line_number += 1
        import time
        time.sleep(timer)
        sys.stdout.flush()
    if program_ended_successfully:
        if visuals: print('\n',output, '\n'*5)
        else: print(output)
        return output
    return "Error. \nProgram ended with exit code -1"


if len(sys.argv) == 1:
    assembler_interpreter(program)
else:
    assembler_interpreter(program, float(sys.argv[1]))
