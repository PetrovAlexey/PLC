import sys
import numpy as np
import config as cfg

class Interpreter:
    def __init__(self, memory):
        self.memory = memory

    def add(self, first_lvl, first_arg, second_lvl, second_arg):
        value = self.dereference(first_lvl, first_arg) + self.dereference(second_lvl, second_arg)
        self.memory.write(self.dereference(first_lvl - 1, first_arg), value)

    def call(self, first_arg):
        self.push(0, self.ip())
        start_point = cfg.NUMBER_OF_REGISTERS + 3 + \
                      self.memory.read(cfg.NUMBER_OF_REGISTERS + 1 + first_arg +
                                       self.memory.read(cfg.NUMBER_OF_REGISTERS + 2))
        self.mov(1, cfg.IP_INDEX, 0, start_point)

    def funcb(self):
        self.memory.write(cfg.NUMBER_OF_REGISTERS, 1)

    def funce(self):
        self.memory.write(cfg.NUMBER_OF_REGISTERS, 0)

    def goto(self, first_lvl, first_arg, second_lvl, second_arg):
        if self.dereference(first_lvl, first_arg) != second_lvl:
            self.add(1, cfg.IP_INDEX, 0, (second_arg - 1) * cfg.IP_OFFSET)

    def mov(self, first_lvl, first_arg, second_lvl, second_arg):
        value = self.dereference(second_lvl, second_arg)
        self.memory.write(self.dereference(first_lvl - 1, first_arg), value)

    def pop(self):
        self.memory.write(self.sp(), 0)
        self.add(1, cfg.SP_INDEX, 0, 1)

    def print(self, first_lvl, first_arg):
        print(self.dereference(first_lvl, first_arg))

    def push(self, first_lvl, first_arg):
        self.sub(1, cfg.SP_INDEX, 0, 1)
        self.mov(2, cfg.SP_INDEX, first_lvl, first_arg)

    def putstr(self, first_lvl, first_arg):
        string = ''
        for i in range(first_arg):
            string += chr(self.memory.read(cfg.NUMBER_OF_REGISTERS + 1 +
                                           self.memory.read(cfg.NUMBER_OF_REGISTERS + 1) +
                                           first_lvl + i))
        print(string)

    def read(self, first_lvl, first_arg):
        value = input()
        self.memory.write(self.dereference(first_lvl - 1, first_arg), value)

    def sub(self, first_lvl, first_arg, second_lvl, second_arg):
        value = self.dereference(first_lvl, first_arg) - self.dereference(second_lvl, second_arg)
        self.memory.write(self.dereference(first_lvl - 1, first_arg), value)
        
    def ip(self):
        return self.memory.read(cfg.IP_INDEX)

    def sp(self):
        return self.memory.read(cfg.SP_INDEX)

    def next(self):
        self.memory.write(cfg.IP_INDEX, self.ip() + cfg.IP_OFFSET)

    def dereference(self, lvl, value):
        for i in range(lvl):
            value = self.memory.read(value)
        return value

    
    def handle(self, command, first_lvl, first_arg, second_lvl, second_arg):
        if self.memory.read(cfg.NUMBER_OF_REGISTERS) and command != cfg.COMMAND_FUNCE:
            self.next()
            return True

        if command == cfg.COMMAND_ADD:
            self.next()
            self.add(first_lvl, first_arg, second_lvl, second_arg)
            return True
        elif command == cfg.COMMAND_CALL:
            self.next()
            self.call(first_arg)
            return True
        elif command == cfg.COMMAND_EXIT:
            return False
        elif command == cfg.COMMAND_FUNCB:
            self.next()
            self.funcb()
            return True
        elif command == cfg.COMMAND_FUNCE:
            self.next()
            self.funce()
            return True
        elif command == cfg.COMMAND_GOTO:
            self.next()
            self.goto(first_lvl, first_arg, second_lvl, second_arg)
            return True
        elif command == cfg.COMMAND_MOV:
            self.next()
            self.mov(first_lvl, first_arg, second_lvl, second_arg)
            return True
        elif command == cfg.COMMAND_POP:
            self.next()
            self.pop()
            return True
        elif command == cfg.COMMAND_PRINT:
            self.next()
            self.print(first_lvl, first_arg)
            return True
        elif command == cfg.COMMAND_PUSH:
            self.next()
            self.push(first_lvl, first_arg)
            return True
        elif command == cfg.COMMAND_PUTSTR:
            self.next()
            self.putstr(first_lvl, first_arg)
            return True
        elif command == cfg.COMMAND_READ:
            self.next()
            self.read(first_lvl, first_arg)
            return True
        elif command == cfg.COMMAND_SUB:
            self.next()
            self.sub(first_lvl, first_arg, second_lvl, second_arg)
            return True
        else:
            return False

    def _run(self):
        command = self.memory.read(self.ip())
        first_lvl = self.memory.read(self.ip() + 1)
        first_arg = self.memory.read(self.ip() + 2)
        second_lvl = self.memory.read(self.ip() + 3)
        second_arg = self.memory.read(self.ip() + 4)

        return self.handle(command, first_lvl, first_arg, second_lvl, second_arg)

    def run(self):
        while self._run():
            continue


class Memory:
    def __init__(self, memory_size):
        self.memory = np.zeros(memory_size, dtype=np.int32)

    def write(self, address, value):
        self.memory[address] = value

    def read(self, address):
        return self.memory[address]




if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Using: vm.py <file>')
    else:
        memory = Memory(cfg.MEMORY_SIZE)
        memory.write(cfg.IP_INDEX, cfg.NUMBER_OF_REGISTERS + 3)
        memory.write(cfg.SP_INDEX, cfg.MEMORY_SIZE)
        memory.write(cfg.NUMBER_OF_REGISTERS, 0)

        bytecode = np.fromfile(sys.argv[1], dtype=np.int32)[::2]

        for i, byte in enumerate(bytecode):
            memory.write(cfg.NUMBER_OF_REGISTERS + i + cfg.START_OFFSET, byte)

        interpreter = Interpreter(memory)
        interpreter.run()


