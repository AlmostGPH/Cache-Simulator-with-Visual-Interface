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
                block.timestamp = time.time()
                block.access_count += 1
                return True
        
        for block in cache_set.blocks:
            if not block.valid:
                block.valid = True
                block.tag = tag
                block.data = self.fetch_data(operation,  address)
                block.timestamp = time.time()
                block.access_count = 1
                block.added_timestamp = time.time()
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


cache_size = 1024
block_size = 4
associativity = 16
replacement_policy = 'FIFO'


def main():
    cache = Cache(cache_size, block_size, associativity, replacement_policy)
    print("╔═════════════════════════════════════════╗")
    print(f"║{'Cache total size: ' + str(cache_size) + ' bytes':^41}║")
    print(f"║{'Cache amount: ' + str(int(cache_size/block_size)):^41}║")
    print(f"║{'Block size: ' + str(block_size) + ' bytes':^41}║")
    print(f"║{'Number of sets: ' + str(associativity):^41}║")
    print(f"║{'Replacement policy: ' + replacement_policy:^41}║")
    print("╚═════════════════════════════════════════╝")
    cache.parse_instructions('mem.txt')
    print("╔═════════════════════════════════════════╗")
    print("║{:^50}║".format('\033[92m Simulation finished!\033[0m'))
    print(f"║{'Total access count: ' + str(cache.access_count):^41}║")
    print(f"║{'Total hit count: ' + str(cache.hit_count):^41}║")
    print(f"║{'Cache hit rate: ' + str(cache.hit_rate() * 100) + '%':^41}║")
    print("╚═════════════════════════════════════════╝")

if __name__ == "__main__":
    main()
