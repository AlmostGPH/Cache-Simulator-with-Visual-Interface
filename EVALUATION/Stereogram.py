import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

data = pd.read_csv('perf_data_4_4.csv')

x_labels = data.columns[1:]
y_labels = data['size']

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# 创建三角网格
x, y = np.meshgrid(range(len(x_labels)), range(len(y_labels)))
surf = ax.plot_trisurf(x.flatten(), y.flatten(), data.iloc[:, 1:].values.flatten(), cmap='viridis', edgecolor='none')


# 设置标题和轴标签
ax.set_title("Cache Performance Analysis of FIFO")
ax.set_xlabel('Number of Sets')
ax.set_ylabel('Block Size (bytes)')
ax.set_zlabel('Hit Rate')

# 设置轴的刻度和标签
ax.set_xticks(range(len(x_labels)))
ax.set_xticklabels(x_labels)
ax.set_yticks(range(len(y_labels)))
ax.set_yticklabels(y_labels)

# 添加色标
fig.colorbar(surf, ax=ax, shrink=0.5, aspect=5)

plt.show()

