import random
import time
import os
import sys
import math

START = time.time() 

cachesimhelp="\n"+\
" ██████╗ █████╗  ██████╗██╗  ██╗███████╗    ███████╗██╗███╗   ███╗\n"+\
"██╔════╝██╔══██╗██╔════╝██║  ██║██╔════╝    ██╔════╝██║████╗ ████║\n"+\
"██║     ███████║██║     ███████║█████╗      ███████╗██║██╔████╔██║\n"+\
"██║     ██╔══██║██║     ██╔══██║██╔══╝      ╚════██║██║██║╚██╔╝██║\n"+\
"╚██████╗██║  ██║╚██████╗██║  ██║███████╗    ███████║██║██║ ╚═╝ ██║\n"+\
" ╚═════╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝╚══════╝    ╚══════╝╚═╝╚═╝     ╚═╝\n"+\
"\n"+\
"CacheSim 1.0(windows)\n"+\
"Usage: cachesim [options] parameter [options] parameter ...\n"+\
"\n"+\
"CacheSim is a cache simulator with a hit checking mechanism, a mapping display of memory addresses and cache blocks, the implementation of a substitution algorithm, the handling of mismatches between the block size and the data size, and the separation of the data cache from the instruction cache. And with visual interface.\n"+\
"\n"+\
"Most used options:\n"+\
"  -h --help                                                show man page and exit\n"+\
"  -v --version                                             show simulator version\n"+\
"  -a --args {Cache_size,Block_size,Associativity}          initial cache size\n"+\
"  -p --policy 'Replacement_policy'                         initial cache replacement policy\n"+\
"  -s --sequence mem.sequence                               add your memory access sequence file\n"+\
"  -g --graph                                               use visual interface\n"+\
"\n"+\
"For more use please see https://github.com/AlmostGPH/Cache-Simulator-with-Visual-Interface\n"



import msvcrt
def pause():
    while True:
        if msvcrt.kbhit():
            char = msvcrt.getch()
            if char == b'\x1b':  # 如果按下 ESC 键
                print("╔═════════════════════════════════════════╗")
                print("║{:^50}║".format('\033[91m Simulation terminated!\033[0m'))
                print("╚═════════════════════════════════════════╝")
                return True  # 返回 True 退出循环
            else:
                return False  # 返回 False 继续循环

# import tty
# import termios
# def pause():
#     fd = sys.stdin.fileno()
#     old_settings = termios.tcgetattr(fd)
#     try:
#         tty.setraw(sys.stdin.fileno())
#         while True:
#             char = sys.stdin.read(1)
#             if char == '\x1b':  # 如果按下 ESC 键
#                 print("╔═════════════════════════════════════════╗")
#                 print("║{:^50}║".format('\033[91m Simulation terminated!\033[0m'))
#                 print("╚═════════════════════════════════════════╝")
#                 return True  # 返回 True 退出循环
#             else:
#                 return False  # 返回 False 继续循环
#     finally:
#         termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

def showcache(prev,curr,inst, cache_size=64, block_size=4, associativity=1, replacement_policy='Random'):
    index_bit = int(math.log2(cache_size / block_size / associativity))
    offset_bit = int(math.log2(block_size))

    sys.stdout.write("\033[H")
    sys.stdout.flush()
    hit = False
    print("╔═════════════════════════════════════════╗")
    print(f"║{'Cache total size: ' + str(cache_size) + ' bytes':^41}║")
    print(f"║{'Cache amount: ' + str(int(cache_size/block_size)):^41}║")
    print(f"║{'Block size: ' + str(block_size) + ' bytes':^41}║")
    print(f"║{'Number of sets: ' + str(associativity):^41}║")
    print(f"║{'Replacement policy: ' + replacement_policy:^41}║")
    print("╚═════════════════════════════════════════╝")

    Head_line = "╦"+"═"*7+"╦"+"═"*20+"╦"+"═"*20+"╦"+"═"*17+"╦"
    print("╔"+"═"*7+Head_line*(associativity-1)+Head_line[:-1]+"╗")
    print('║{0:^7s}'.format('Index'),end='')
    for i in range(associativity):
        if replacement_policy == 'LFU':
            print('║{0:^7s}║{1:^20s}║{2:^20s}║{3:^17s}║'.format('Valid','Tag','Addr','Count'),end='')
        else:
            print("║{0:^7s}║{1:^20s}║{2:^20s}║{3:^17s}║".format('Valid','Tag','Addr','Time'),end='')
    Middle_line = "╬"+"═"*7+"╬"+"═"*20+"╬"+"═"*20+"╬"+"═"*17+"╬"
    print("\n"+"╠"+"═"*7+Middle_line*(associativity-1)+Middle_line[:-1]+"╣")

    if prev == curr:
        line2 = curr
        sets = line2.split('$')
        count = 0
        for set in sets:
            blocks = set.split('|')
            if(len(blocks) == 1): continue
            print("║{0:^7X}".format(count),end='')
            for block in blocks:
                block = block.split()
                if(len(block) != 6): continue
                valid, tag, access_count, added_timestamp, timestamp, hit_count = block
                addr = (((int(tag) << index_bit) | count) << offset_bit) if tag != 'None' else 0
                valid = '\033[92m' + valid + '\033[0m' if valid == 'True' else '\033[91m' + valid + '\033[0m'
                if replacement_policy == 'LFU':
                    if tag == 'None':
                        print("║{0:^16s}║{1:^20X}║{2:^20X}║{3:^17s}║".format(valid, 0, addr, access_count),end='')
                    else:
                        print("║{0:^16s}║{1:^20X}║{2:^20X}║{3:^17s}║".format(valid, int(tag), addr, access_count),end='')
                else:
                    if tag == 'None':
                        print("║{0:^16s}║{1:^20X}║{2:^20X}║{3:^17s}║".format(valid, 0, addr, timestamp),end='')
                    else:
                        print("║{0:^16s}║{1:^20X}║{2:^20X}║{3:^17s}║".format(valid, int(tag), addr, timestamp),end='')
            count += 1
            print()
    else:
        line1 = prev
        line2 = curr
        sets1 = line1.split('$')
        sets2 = line2.split('$')
        count = 0
        for set1, set2 in zip(sets1, sets2):
            blocks1 = set1.split('|')
            blocks2 = set2.split('|')
            if(len(blocks1) == 1): continue
            print("║{0:^7X}".format(count),end='')
            for block1, block2 in zip(blocks1, blocks2):
                block1 = block1.split()
                block2 = block2.split()
                if(len(block1) != 6): continue
                valid1, tag1, access_count1, added_timestamp1, timestamp1, hit_count1 = block1
                valid2, tag2, access_count2, added_timestamp2, timestamp2, hit_count2 = block2
                addr1 = (((int(tag1) << index_bit) | count) << offset_bit) if tag1 != 'None' else 0
                addr2 = (((int(tag2) << index_bit) | count) << offset_bit) if tag2 != 'None' else 0
                valid1 = '\033[92m' + valid1 + '\033[0m' if valid1 == 'True' else '\033[91m' + valid1 + '\033[0m'
                valid2 = '\033[92m' + valid2 + '\033[0m' if valid2 == 'True' else '\033[91m' + valid2 + '\033[0m'
                
                if addr1 != addr2:
                    addr2 = '\033[91m{0:^20X}\033[0m'.format(addr2)
                else:
                    addr2 = '{0:^20X}'.format(addr2)
                if hit_count2 > hit_count1:
                    hit = True
                if replacement_policy == 'LFU':
                    if tag2 == 'None':
                        print("║{0:^16s}║{1:^20X}║{2}║{3:^17s}║".format(valid2, 0, addr2,access_count1),end='')
                    else:
                        print("║{0:^16s}║{1:^20X}║{2}║{3:^17s}║".format(valid2, int(tag2), addr2, access_count2),end='')
                else:
                    if tag2 == 'None':
                        print("║{0:^16s}║{1:^20X}║{2}║{3:^17s}║".format(valid2, 0, addr2,timestamp1),end='')
                    else:
                        print("║{0:^16s}║{1:^20X}║{2}║{3:^17s}║".format(valid2, int(tag2), addr2, timestamp2),end='')
            count += 1
            print()

    Bottom_line = "╩"+"═"*7+"╩"+"═"*20+"╩"+"═"*20+"╩"+"═"*17+"╩"
    print("╚"+"═"*7+Bottom_line*(associativity-1)+Bottom_line[:-1]+"╝")
    if inst[-1] == '\n':
        inst = inst[:-1]   
    if hit:
        print("\033[92m[+]", inst, '\tHit! \033[0m')
    else:
        print("\033[91m[+]", inst, '\tMiss! \033[0m')


class CacheBlock:
    def __init__(self, block_size):
        self.block_size = block_size
        self.data = [None] * block_size
        self.tag = None
        self.valid = False
        self.timestamp = time.time()-START
        self.access_count = 0
        self.added_timestamp = time.time()-START

class CacheSet:
    def __init__(self, associativity, block_size):
        self.blocks = [CacheBlock(block_size) for _ in range(associativity)]

class Cache:
    def __init__(self, cache_size=1024, block_size=4, associativity=1, replacement_policy='Random'):
        self.num_sets = cache_size // (block_size * associativity)
        self.block_size = block_size
        self.associativity = associativity
        self.replacement_policy = replacement_policy
        self.sets = [CacheSet(associativity, block_size) for _ in range(self.num_sets)]
        self.access_count = 0
        self.hit_count = 0

    def access_visual(self, operation, size, address):
        num_blocks = -(-size // self.block_size)
        for i in range(num_blocks):
            block_address = address + i * self.block_size
            self.access_block(operation, block_address)

        state = ''
        for set in self.sets:
            set_state = ' '.join(
                f"{block.valid} {'None' if block.tag is None else block.tag} {block.access_count} {block.added_timestamp:.6f} {block.timestamp:.6f} {self.hit_count} |"
                for block in set.blocks
            )
            state += set_state + ' $ '

        # print(state)
        return state
    
    def access(self, operation, size, address):
        num_blocks = -(-size // self.block_size)  # Equivalent to math.ceil(size / self.block_size)
        for i in range(num_blocks):
            block_address = address + i * self.block_size
            self.access_block(operation, block_address)


    def access_block(self, operation, address):
        self.access_count += 1
        set_index = (address // self.block_size) % self.num_sets
        tag = address // (self.block_size * self.num_sets)
        cache_set = self.sets[set_index]

        for block in cache_set.blocks:
            if block.valid and block.tag == tag:
                self.hit_count += 1
                block.timestamp = time.time()-START
                block.access_count += 1
                return True
        
        for block in cache_set.blocks:
            if not block.valid:
                block.valid = True
                block.tag = tag
                block.data = self.fetch_data(operation,  address)
                block.timestamp = time.time()-START
                block.access_count = 1
                block.added_timestamp = time.time()-START
                return False

        if self.replacement_policy == 'Random':
            block = random.choice(cache_set.blocks)
        elif self.replacement_policy == 'LRU':
            block = min(cache_set.blocks, key=lambda block: block.timestamp)
        elif self.replacement_policy == 'FIFO':
            block = min(cache_set.blocks, key=lambda block: block.added_timestamp)
        elif self.replacement_policy == 'LFU':
            block = min(cache_set.blocks, key=lambda block: block.access_count)
        
        block.valid = True
        block.tag = tag
        block.data = self.fetch_data(operation,  address)
        block.timestamp = time.time()-START
        block.access_count = 1
        block.added_timestamp = time.time()-START
        return False

    def fetch_data(self, operation, address):
        if operation == 'IFetch':
            return f"Instruction at address {address}"
        elif operation in ['Read', 'Write']:
            return f'Data at address {address}'
        else:
            raise ValueError(f"Unknown operation: {operation}")

    def hit_rate(self):
        return self.hit_count / self.access_count if self.access_count > 0 else 0

    def parse_instructions_visual(self, filename):
        with open(filename, 'r') as f:
            pre_state = ''
            curr_state = ''
            START = time.time() 
            for line in f:
                operation, size, address = line.split()
                size = int(size)
                address = int(address, 16)
                if pre_state == '':
                    pre_state = self.access_visual(operation, size, address)
                    os.system('cls')
                    showcache(pre_state, pre_state, line, self.num_sets * self.block_size * self.associativity, self.block_size, self.associativity, self.replacement_policy)
                    if pause():
                        exit()
                    continue
                curr_state = self.access_visual(operation, size, address)
                os.system('cls')
                # print(curr_state)
                showcache(pre_state, curr_state, line, self.num_sets * self.block_size * self.associativity, self.block_size, self.associativity, self.replacement_policy)
                pre_state = curr_state
                if pause():
                    exit()

    def parse_instructions(self, filename):
        with open(filename, 'r') as f:
            for line in f:
                operation, size, address = line.split()
                size = int(size)
                address = int(address, 16)
                self.access(operation, size, address)


# Cache_size = 1024
# Block_size = 4
# Associativity = 4
# Replacement_policy = 'LRU' # 'Random', 'LRU', 'FIFO', 'LFU'

import argparse

def check_policy(value):
    if value not in ['Random', 'LRU', 'FIFO', 'LFU']:
        raise argparse.ArgumentTypeError("For now, Replacement_policy can only be choose from:'Random', 'LRU', 'FIFO', 'LFU'")
    return value

def check_args(value):
    try:
        Cache_size, Block_size, Associativity = map(int, value.split(','))
        if Cache_size % (Block_size * Associativity) != 0:
            raise argparse.ArgumentTypeError("Block_size*Associativity must be a factor of Cache_size")
    except ValueError:
        raise argparse.ArgumentTypeError("The format can only be: Cache_size,Block_size,Associativity")
    return Cache_size, Block_size, Associativity

def head_print(Cache_size, Block_size, Associativity, Replacement_policy):
    print("╔═════════════════════════════════════════╗")
    print(f"║{'Cache total size: ' + str(Cache_size) + ' bytes':^41}║")
    print(f"║{'Cache amount: ' + str(int(Cache_size/Block_size)):^41}║")
    print(f"║{'Block size: ' + str(Block_size) + ' bytes':^41}║")
    print(f"║{'Number of sets: ' + str(Associativity):^41}║")
    print(f"║{'Replacement policy: ' + Replacement_policy:^41}║")
    print("╚═════════════════════════════════════════╝")

def result_print(cache):
    print("╔═════════════════════════════════════════╗")
    print("║{:^50}║".format('\033[92m Simulation finished!\033[0m'))
    print(f"║{'Total access count: ' + str(cache.access_count):^41}║")
    print(f"║{'Total hit count: ' + str(cache.hit_count):^41}║")
    print(f"║{'Cache hit rate: ' + str(cache.hit_rate() * 100) + '%':^41}║")
    print("╚═════════════════════════════════════════╝")

parser = argparse.ArgumentParser(description='Cache Simulator', add_help=False)
parser.add_argument('-h', '--help', action='store_true', help='show man page and exit')
parser.add_argument('-v', '--version', action='store_true', help='show simulator version')
parser.add_argument('-a', '--args', type=check_args, help='initial cache size')
parser.add_argument('-p', '--policy', type=check_policy, help='initial cache replacement policy')
parser.add_argument('-s', '--sequence', type=str, help='add your memory access sequence')
parser.add_argument('-g', '--graph', action='store_true', help='whether to use graphical interface')

if __name__ == "__main__":
    # main()

    args = parser.parse_args()

    if not any(vars(args).values()):
        print(cachesimhelp)
        exit()
    if args.help:
        print(cachesimhelp)
        exit()
    if args.version:
        print('CacheSim 1.0(windows)')
        exit()
    if args.args:
        Cache_size, Block_size, Associativity = args.args
    if args.policy:
        Replacement_policy = args.policy
    if args.sequence:
        mem = args.sequence
    if args.graph:
        cache = Cache(Cache_size, Block_size, Associativity, Replacement_policy)
        head_print(Cache_size, Block_size, Associativity, Replacement_policy)
        cache.parse_instructions_visual(mem)
        result_print(cache)
    else:
        cache = Cache(Cache_size, Block_size, Associativity, Replacement_policy)
        head_print(Cache_size, Block_size, Associativity, Replacement_policy)
        cache.parse_instructions(mem)
        result_print(cache)
