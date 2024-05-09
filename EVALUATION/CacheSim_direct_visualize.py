import os
import sys
import tty
import termios
import math

def pause():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        while True:
            char = sys.stdin.read(1)
            if char == '\x1b':  # 如果按下 ESC 键
                return True  # 返回 True 退出循环
            else:
                return False  # 返回 False 继续循环
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

def showcache(prev,curr,inst, cache_size=64, block_size=4, associativity=1, replacement_policy='Random'):
    # cache_size = 64
    # block_size = 4
    # associativity = 1
    # replacement_policy = 'Random'
    index_bit = int(math.log2(cache_size / block_size / associativity))
    offset_bit = int(math.log2(block_size))

    sys.stdout.write("\033[H")
    sys.stdout.flush()
    hit = False
    print
    print(f"Cache size: {cache_size} bytes\t Block size: {block_size} bytes\t\n Number of sets: {associativity}\t Replacement policy: {replacement_policy}")
    print("="*(8 + 69*associativity))
    print('|{0:^7s}'.format('Index'),end='')
    for i in range(associativity):
        print("|{0:^7s}|{1:^20s}|{2:^20s}|{3:^17s}|".format('Valid','Tag','Addr','Time'),end='')
    print("\n"+"-"*(8 + 69*associativity))

    if prev == curr:
        line2 = curr
        sets = line2.split('$')
        count = 0
        for set in sets:
            blocks = set.split('|')
            if(len(blocks) == 1): continue
            print("|{0:^7X}".format(count),end='')
            for block in blocks:
                block = block.split()
                if(len(block) != 6): continue
                valid, tag, access_count, added_timestamp, timestamp, hit_count = block
                addr = (((int(tag) << index_bit) | count) << offset_bit) if tag != 'None' else 0
                valid = '\033[92m' + valid + '\033[0m' if valid == 'True' else '\033[91m' + valid + '\033[0m'
                if tag == 'None':
                    print("|{0:^16s}|{1:^20X}|{2:^20X}|{3:^10s}|".format(valid, 0, addr, timestamp),end='')
                else:
                    print("|{0:^16s}|{1:^20X}|{2:^20X}|{3:^10s}|".format(valid, int(tag), addr, timestamp),end='')
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
            print("|{0:^7X}".format(count),end='')
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
                if tag2 == 'None':
                    print("|{0:^16s}|{1:^20X}|{2}|{3:^16s}|".format(valid2, 0, addr2,timestamp1),end='')
                else:
                    print("|{0:^16s}|{1:^20X}|{2}|{3:^16s}|".format(valid2, int(tag2), addr2, timestamp2),end='')
            count += 1
            print()

    print("="*(8 + 69*associativity))
    #inst = inst[:-1]
    if hit:
        print("\033[92m[+]", inst[:-1], '\tHit! \033[0m')
    else:
        print("\033[91m[+]", inst[:-1], '\tMiss! \033[0m')
        

insts = []
states = []
with open('benchmark.direct', 'r') as f:
    for line in f:
        insts.append(line)
with open('result_direct.txt', 'r') as file:
    for line in file:
        states.append(line)

while True:
        
    
    for i in range(len(states)):
        if i == 0:
            showcache(states[i], states[i], insts[i])
        else:
            showcache(states[i-1], states[i], insts[i])
        if pause():
            exit(0)
        os.system('clear')