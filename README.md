# Cache-Simulator-with-Visual-Interface
A cache simulator with a hit checking mechanism, a mapping display of memory addresses and cache blocks, the implementation of a substitution algorithm, the handling of mismatches between the block size and the data size, and the separation of the data cache from the instruction cache. And with visual interface.

## Features

- Hit check mechanism
- Mapping of memory address and cache block
  - Full associativity
  - Set associativity
  - Direct mapping
- Implementation of some replacement algorithms
  - LRU
  - Random
  - LFU
  - FIFO
- Handling of mismatch between block size and data size
- Visual Cache

## Installation

Just download  CacheSimulator.py and run.

## Usage

- -h --help:                                                show man page and exit
- -v --version:                                             show simulator version
- -a --args {Cache_size,Block_size,Associativity}:          initial cache size
- -p --policy 'Replacement_policy':                         initial cache replacement policy
- -s --sequence mem.sequence:                               add your memory access sequence file
- -g --graph:                                               use visual interface
- When performing a visual simulation, press ESC to exit and other keys to continue
- help page:
![image](https://github.com/AlmostGPH/Cache-Simulator-with-Visual-Interface/assets/60679801/d47e7399-0a63-46d4-b3ad-365de2328dc9)

**PLEASE NOTE**

Each line of your memory access sequence file should be of the following form

``<instruction> <size> <address> ``

And the 'instruction' part must choose from Read, IFerch or Write

For example：
```txt
Read 4 0x70700
IFetch 4 0x1b4d0
Write 8 0x6bab8
```


## Examples
If there exists a access sequence file called 'mem.txt', you can simulate cache like this:

```powershell
python CacheSimulator.py -a 1024,4,4 -p 'LRU' -s mem.txt
```

Than you will get follow result:
![image](https://github.com/AlmostGPH/Cache-Simulator-with-Visual-Interface/assets/60679801/0998795a-159f-433a-8c06-56777d6610fc)

It will statistics and calculation the hit rate of this access sequence in the cache you modified. 

Or you can add "-g" for visual interface:
```powershell
python CacheSimulator.py -a 1024,4,4 -p 'LRU' -s mem.txt -g
```
![image](https://github.com/AlmostGPH/Cache-Simulator-with-Visual-Interface/assets/60679801/55a06446-9d52-44a6-b7d3-203ffe0667ed)

It will show the entire cache, and each time you press a key other than ESC, it will execute the next command. If a cache miss occurs, the cache update will be marked in red. You can press ESC to exit midway.

![image](https://github.com/AlmostGPH/Cache-Simulator-with-Visual-Interface/assets/60679801/8c0316a7-ef7b-4522-b500-09f2829a1ee7)



## Future work

- Include a running alert and a progress bar when running in a non-graphical interface.
- Let the user choose whether to display the full command sequence

![6bbfa25f-df0f-464b-ad47-9d56e49a687d](https://github.com/AlmostGPH/Cache-Simulator-with-Visual-Interface/assets/60679801/ac148752-b2e8-4e66-a54c-f89d8a8b7cca)

- Data cache and instruction cache can be separated
- More replacement policy
