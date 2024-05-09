#include <iostream>
#include <fstream>
#include <vector>
#include <cmath>
#include <cstdlib>
#include <ctime>
#include <algorithm>

using namespace std;

class CacheBlock
{
public:
    int block_size;
    vector<int> data;
    int tag;
    bool valid;
    double timestamp;
    int access_count;
    double added_timestamp;
    int time;
    int add_time;

    CacheBlock(int block_size) : block_size(block_size), tag(-1), valid(false), timestamp(0.0), access_count(0), added_timestamp(0.0), time(0), add_time(0)
    {
        data.resize(block_size, -1);
    }
};

class CacheSet
{
public:
    vector<CacheBlock> blocks;

    CacheSet(int associativity, int block_size)
    {
        blocks.resize(associativity, CacheBlock(block_size));
    }
};

class Cache
{
public:
    int num_sets;
    int block_size;
    int associativity;
    string replacement_policy;
    vector<CacheSet> sets;
    int access_count;
    int hit_count;

    Cache(int cache_size = 1024, int block_size = 4, int associativity = 1, string replacement_policy = "Random") : block_size(block_size), associativity(associativity), replacement_policy(replacement_policy),
                                                                                                                    access_count(0), hit_count(0)
    {

        num_sets = cache_size / (block_size * associativity);
        sets.resize(num_sets, CacheSet(associativity, block_size));
    }

    void access(string operation, int size, int address)
    {
        int num_blocks = ceil((double)size / block_size);
        for (int i = 0; i < num_blocks; ++i)
        {
            int block_address = address + i * block_size;
            access_block(operation, block_address);
        }
    }

    void access_block(string operation, int address)
    {
        access_count++;
        int set_index = (address / block_size) % num_sets;
        int tag = address / (block_size * num_sets);
        CacheSet &cache_set = sets[set_index];

        for (CacheBlock &block : cache_set.blocks)
        {
            if (block.valid && block.tag == tag)
            {
                hit_count++;
                block.timestamp = ++block.time;
                block.access_count++;
                return;
            }
        }

        for (CacheBlock &block : cache_set.blocks)
        {
            if (!block.valid)
            {
                block.valid = true;
                block.tag = tag;
                block.data = fetch_data(operation, address);
                block.timestamp = ++block.time;
                block.access_count = 1;
                block.added_timestamp = ++block.add_time;
                return;
            }
        }

        CacheBlock &block = choose_block_to_replace(cache_set);
        block.valid = true;
        block.tag = tag;
        block.data = fetch_data(operation, address);
        block.timestamp = ++block.time;
        block.access_count = 1;
        block.added_timestamp = ++block.add_time;
    }

    vector<int> fetch_data(string operation, int address)
    {
        vector<int> data(block_size, -1);
        if (operation == "IFetch")
        {
            // cout << "Instruction at address " << address << endl;
        }
        else if (operation == "Read" || operation == "Write")
        {
            // cout << "Data at address " << address << endl;
        }
        else
        {
            // throw invalid_argument("Unknown operation: " + operation);
        }
        return data;
    }

    double hit_rate()
    {
        return (double)hit_count / access_count;
    }

    CacheBlock &choose_block_to_replace(CacheSet &cache_set)
    {
        if (replacement_policy == "Random")
        {
            return cache_set.blocks[rand() % associativity];
        }
        else if (replacement_policy == "LRU")
        {
            return *min_element(cache_set.blocks.begin(), cache_set.blocks.end(),
                                [](const CacheBlock &a, const CacheBlock &b)
                                {
                                    return a.timestamp < b.timestamp;
                                });
        }
        else if (replacement_policy == "FIFO")
        {
            return *min_element(cache_set.blocks.begin(), cache_set.blocks.end(),
                                [](const CacheBlock &a, const CacheBlock &b)
                                {
                                    return a.added_timestamp < b.added_timestamp;
                                });
        }
        else if (replacement_policy == "LFU")
        {
            return *min_element(cache_set.blocks.begin(), cache_set.blocks.end(),
                                [](const CacheBlock &a, const CacheBlock &b)
                                {
                                    return a.access_count < b.access_count;
                                });
        }
        else
        {
            throw invalid_argument("Unknown replacement policy: " + replacement_policy);
        }
    }

    void parse_instructions(string filename)
    {
        ifstream file(filename);
        if (!file.is_open())
        {
            cerr << "Error: Unable to open file " << filename << endl;
            return;
        }

        string operation;
        int size, address;
        while (file >> operation >> size >> hex >> address)
        {
            access(operation, size, address);
        }
        file.close();
    }
};

int main()
{
    srand(0); // 用于随机数生成的种子
    Cache cache(1024, 4, 16, "LFU");
    cache.parse_instructions("mem.txt");
    cout << "Simulation finished!" << endl;
    cout << "Total access count: " << cache.access_count << endl;
    cout << "Total hit count: " << cache.hit_count << endl;
    cout << "Cache hit rate: " << cache.hit_rate() * 100 << "%" << endl;
    return 0;
}
