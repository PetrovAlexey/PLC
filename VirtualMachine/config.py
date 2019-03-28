NUMBER_OF_REGISTERS = 8
MEMORY_SIZE = 600

IP_INDEX = 0
SP_INDEX = 1

IP_OFFSET = 5
START_OFFSET = 1

REGISTERS = {'ip': 0, 'sp': 1, 'ax': 2, 'bx': 3,
             'cx': 4, 'dx': 5, 'ex': 6, 'fx': 7}

REGISTERS_REVERSE = {0: 'ip', 1: 'sp', 2: 'ax', 3: 'bx',
                     4: 'cx', 5: 'dx', 6: 'ex', 7: 'fx'}

COMMAND_ADD = 0
COMMAND_CALL = 1
COMMAND_EXIT = 2
COMMAND_FUNCB = 3
COMMAND_FUNCE = 4
COMMAND_GOTO = 5
COMMAND_MOV = 6
COMMAND_POP = 7
COMMAND_PRINT = 8
COMMAND_PUSH = 9
COMMAND_PUTSTR = 10
COMMAND_READ = 11
COMMAND_SUB = 12

STR_ADD = 'add'
STR_CALL = 'call'
STR_EXIT = 'stop'
STR_FUNCB = 'fbeg'
STR_FUNCE = 'fend'
STR_GOTO = 'goto'
STR_MOV = 'mov'
STR_POP = 'pop'
STR_PRINT = 'print'
STR_PUSH = 'push'
STR_PUTSTR = 'putstr'
STR_READ = 'read'
STR_SUB = 'sub'
