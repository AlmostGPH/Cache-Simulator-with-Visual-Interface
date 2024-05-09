import matplotlib.pyplot as plt

block_sizes = ['Data cache','Inst cache']
policies = ['LRU', 'Random', 'LFU', 'FIFO']
hit_rates = [
    [0.7503233916222984 ,0.9728920089078803],
    [0.7410769932261226,0.9675450198392512],
    [0.5659650761828885,0.8954247257736931],
    [0.72213411211653,0.9689128542521563]
]

plt.figure(figsize=(10, 6))

# Calculate the width of each bar
bar_width = 0.2

# Set the x positions of the bars
x_positions = [i for i in range(len(block_sizes))]

# Plot the bars for each policy
for i in range(len(policies)):
    plt.bar([x + i * bar_width for x in x_positions], hit_rates[i], width=bar_width, label=policies[i])

plt.xlabel('Cache Type')
plt.ylabel('Hit Rate')
plt.title('Cache Performance Analysis')
plt.xticks([x + bar_width for x in x_positions], block_sizes)
plt.legend()
plt.grid(True)
plt.show()