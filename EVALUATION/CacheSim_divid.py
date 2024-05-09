import random
import time

class CacheBlock:
    def __init__(self, block_size):
        self.block_size = block_size
        self.data = [None] * block_size
        self.tag = None
        self.valid = False
        self.timestamp = time.time()  # Add a timestamp field
        self.access_count = 0  # Add an access count field for LFU
        self.added_timestamp = time.time()  # Add an added timestamp field for FIFO

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

    def access(self, operation, size, address):
        num_blocks = -(-size // self.block_size)  # 进一位取整
        for i in range(num_blocks):
            block_address = address + i * self.block_size
            self.access_block(operation, block_address)

    def access_block(self, operation, address):
        self.access_count += 1
        set_index = (address // self.block_size) % self.num_sets
        tag = address // (self.block_size * self.num_sets)
        cache_set = self.sets[set_index]
        # 首先判断有没有miss
        for block in cache_set.blocks:
            if block.valid and block.tag == tag:
                self.hit_count += 1
                block.timestamp = time.time()
                block.access_count += 1
                return True
        # 然后判断有没有空位
        for block in cache_set.blocks:
            if not block.valid:
                block.valid = True
                block.tag = tag
                block.data = self.fetch_data(operation,  address)
                block.timestamp = time.time()
                block.access_count = 1
                block.added_timestamp = time.time()
                return False
        # 迫不得已执行替换策略
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
        block.timestamp = time.time()
        block.access_count = 1
        block.added_timestamp = time.time()
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

    def parse_instructions(self, filename):
        with open(filename, 'r') as f:
            for line in f:
                operation, size, address = line.split()
                size = int(size)
                address = int(address, 16)
                self.access(operation, size, address)

def test_inst(Cache_size, Block_size, Associativity, Replacement_policy):
    cache = Cache(Cache_size, Block_size, Associativity, Replacement_policy)
    cache.parse_instructions('mem_inst.txt')
    print(cache.hit_rate(),end = ' ')

def test_data(Cache_size, Block_size, Associativity, Replacement_policy):
    cache = Cache(Cache_size, Block_size, Associativity, Replacement_policy)
    cache.parse_instructions('mem_data.txt')
    print(cache.hit_rate(),end = ' ')

if __name__ == "__main__":
    test_inst(512, 4, 4, 'LRU')
    test_data(512, 4, 4, 'LRU')
    print()
    test_inst(512, 4, 4, 'Random')
    test_data(512, 4, 4, 'Random')
    print()
    test_inst(512, 4, 4, 'LFU')
    test_data(512, 4, 4, 'LFU')
    print()
    test_inst(512, 4, 4, 'FIFO')
    test_data(512, 4, 4, 'FIFO')
