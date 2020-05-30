import sys
def set_up_commands():
    global mov, inc, dec, add, sub, mul, div, jmp, cmp, jne, je, jge, jg, jle, jl, call, ret, msg, end, comment, commands
    def mov(args):
        x, y = args[0].strip(', '), args[1]
        registers[x] = get_value(y, registers)
    def inc(args):
        x = args[0]
        registers[x] += 1
    def dec(args):
        x = args[0]
        registers[x] -= 1
    def add(args):
        x, y = args[0].strip(', '), args[1]
        registers[x] += get_value(y, registers)
    def sub(args):
        x, y = args[0].strip(', '), args[1]
        registers[x] -= get_value(y, registers)
    def mul(args):
        x, y = args[0].strip(', '), args[1]
        registers[x] *= get_value(y, registers)
    def div(args):
        x, y = args[0].strip(', '), args[1]
        registers[x] //= get_value(y, registers)
    def jmp(args):
        global line_number
        lbl = args[0]
        line_number = labels[lbl]
    def cmp(args):
        '''
            cmp  = 0 if equal
            cmp = 1 if x > y
            cmp = -1 if x < y
        '''
        global compare
        x, y = args[0].strip(', '), args[1]
        x, y = get_value(x, registers), get_value(y, registers)
        compare = (x > y) - (x < y)
    def jne(args):
        global line_number
        if compare != 0:
            lbl = args[0]
            line_number = labels[lbl]
    def je(args):
        global line_number
        if compare == 0:
            lbl = args[0]
            line_number = labels[lbl]
    def jge(args):
        global line_number
        if compare >= 0:
            lbl = args[0]
            line_number = labels[lbl]
    def jg(args):
        global line_number
        if compare == 1:
            lbl = args[0]
            line_number = labels[lbl]
    def jle(args):
        global line_number
        if compare <= 0:
            lbl = args[0]
            line_number = labels[lbl]
    def jl(args):
        global line_number
        if compare == -1:
            lbl = args[0]
            line_number = labels[lbl]
    def call(args):
        global line_number, line_number_reference, in_a_function
        lbl = args[0]
        if not in_a_function:
            line_number_reference, in_a_function = line_number, True
        line_number = labels[lbl]
    def ret(args):
        global line_number, in_a_function
        line_number = line_number_reference
        in_a_function = False
    def msg(args):
        global output
        output = make_msg(args)
    def end(args):
        global line_number, program_ended_successfully
        program_ended_successfully = True
        line_number = total_lines
    def comment(args): pass
    commands = {
        'mov' : mov,
        'inc' : inc,
        'dec' : dec,
        'add' : add,
        'sub' : sub,
        'mul' : mul,
        'div' : div,
        'jmp' : jmp,
        'cmp' : cmp,
        'jne' : jne,
        'je' : je,
        'jge' : jge,
        'jg' : jg,
        'jle' : jle,
        'jl' : jl,
        'call' : call,
        'ret' : ret,
        'msg' : msg,
        'end' : end,
        ';' : comment,
        '' : comment
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
            if command != 'msg':
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

program = '''
mov   a, 8            ; value
mov   b, 0            ; next
mov   c, 0            ; counter
mov   d, 0            ; first
mov   e, 1            ; second
call  proc_fib
call  print
end

proc_fib: ; generic time label comment
    cmp   c, 2
    jl    func_0
    mov   b, d
    add   b, e
    mov   d, e
    mov   e, b
    inc   c
    cmp   c, a
    jle   proc_fib
    ret

func_0:
    mov   b, c
    inc   c
    jmp   proc_fib

print:
    msg   'Term ', a, ' of Fibonacci series is: ', b        ; output text
    ret
'''
if len(sys.argv) == 1:
    assembler_interpreter(program)
else:
    assembler_interpreter(program, float(sys.argv[1]))
