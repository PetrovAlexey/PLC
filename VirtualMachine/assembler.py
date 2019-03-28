import sys
import numpy as np
import config as cfg

class Assembler:
    def __init__(self, input_file, output_file):
        self.static_offset = 0
        self.functions_offset = 0
        self.input = input_file
        self.output = output_file
        self.program = np.array([], dtype=np.int32)
        self.static = np.array([], dtype=np.int32)
        self.functions = {}
        self.functions_startpoints = np.array([], dtype=np.int32)

    def get_arguments(self, word):
        lvl = 0

        for char in word:
            if char == '*':
                lvl += 1
            else:
                arg = word[lvl:]
                try:
                    arg = int(arg)
                except ValueError:
                    arg = cfg.REGISTERS[arg]
                return lvl, arg

    def add(self, words):
        first_lvl, first_arg = self.get_arguments(words[1])
        second_lvl, second_arg = self.get_arguments(words[2])
        return np.array([cfg.COMMAND_ADD, first_lvl, first_arg, second_lvl, second_arg])

    def call(self, words):
        label = self.functions[words[1]]
        return np.array([cfg.COMMAND_CALL, 0, label, 0, 0])


    def exit(self):
        return np.array([cfg.COMMAND_EXIT, 0, 0, 0, 0])

    def funcb(self, i, words):
        label = len(self.functions)
        self.functions[words[1]] = label
        self.functions_startpoints = np.append(self.functions_startpoints, (i + 1) * cfg.IP_OFFSET)
        return np.array([cfg.COMMAND_FUNCB, 0, label, 0, 0])

    def funce(self):
        return np.array([cfg.COMMAND_FUNCE, 0, 0, 0, 0])

    def goto(self, words):
        first_lvl, first_arg = self.get_arguments(words[1])
        second_lvl, second_arg = self.get_arguments(words[2])
        return np.array([cfg.COMMAND_GOTO, first_lvl, first_arg, second_lvl, second_arg])

    def mov(self, words):
        first_lvl, first_arg = self.get_arguments(words[1])
        second_lvl, second_arg = self.get_arguments(words[2])
        return np.array([cfg.COMMAND_MOV, first_lvl, first_arg, second_lvl, second_arg])

    def pop(self):
        return np.array([cfg.COMMAND_POP, 0, 0, 0, 0])

    def print(self, words):
        first_lvl, first_arg = self.get_arguments(words[1])
        return np.array([cfg.COMMAND_PRINT, first_lvl, first_arg, 0, 0])

    def push(self, words):
        first_lvl, first_arg = self.get_arguments(words[1])
        return np.array([cfg.COMMAND_PUSH, first_lvl, first_arg, 0, 0])

    def putstr(self, line):
        words = line.split(maxsplit=1)[1].strip()
        code = np.array([], dtype=np.int32)
        for char in words:
            code = np.append(code, ord(char))
        self.static_offset += len(words)
        self.static = np.append(self.static, code)
        return np.array([cfg.COMMAND_PUTSTR, self.static_offset - len(words), len(words), 0, 0])

    def read(self, words):
        first_lvl, first_arg = self.get_arguments(words[1])
        return np.array([cfg.COMMAND_READ, first_lvl, first_arg, 0, 0])

    def sub(self, words):
        first_lvl, first_arg = self.get_arguments(words[1])
        second_lvl, second_arg = self.get_arguments(words[2])
        return np.array([cfg.COMMAND_SUB, first_lvl, first_arg, second_lvl, second_arg])

    def handle(self, i, line):
        words = line.split()

        if words[0] == cfg.STR_ADD:
            return self.add(words)
        elif words[0] == cfg.STR_CALL:
            return self.call(words)
        elif words[0] == cfg.STR_EXIT:
            return self.exit()
        elif words[0] == cfg.STR_FUNCB:
            return self.funcb(i, words)
        elif words[0] == cfg.STR_FUNCE:
            return self.funce()
        elif words[0] == cfg.STR_GOTO:
            return self.goto(words)
        elif words[0] == cfg.STR_MOV:
            return self.mov(words)
        elif words[0] == cfg.STR_POP:
            return self.pop()
        elif words[0] == cfg.STR_PRINT:
            return self.print(words)
        elif words[0] == cfg.STR_PUSH:
            return self.push(words)
        elif words[0] == cfg.STR_PUTSTR:
            return self.putstr(line)
        elif words[0] == cfg.STR_READ:
            return self.read(words)
        elif words[0] == cfg.STR_SUB:
            return self.sub(words)
        else:
            exit('Wrong function')
            

    def encode(self):
        file = open(self.input, 'r')

        i = 0
        for line in file:
            code = self.handle(i, line)
            self.program = np.append(self.program, code)
            i += 1

        len_static = len(self.program) + 2
        len_functions = len_static + len(self.static)

        self.program = np.array([len_static, len_functions] + list(self.program) + list(self.static) + list(self.functions_startpoints))
        self.program.tofile(self.output)


def main():
    if len(sys.argv) < 3:
        print('Usage: vm.py <input file> <output file>')
    else:
        encoder = Assembler(sys.argv[1], sys.argv[2])

        encoder.encode()


if __name__ == '__main__':
    main()