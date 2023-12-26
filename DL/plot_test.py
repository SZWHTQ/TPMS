import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# 示例数据
x = np.linspace(0, 10, 201)
y = np.linspace(0, 5, 108)
x, y = np.meshgrid(x, y)
z = np.sin(x) * np.cos(y)

# 创建一个三维图形对象
fig = plt.figure(figsize=(10, 6))
ax = fig.add_subplot(111, projection='3d')

# 绘制三维曲面图
surf = ax.plot_surface(x, y, z, cmap='viridis')

# 添加颜色条
cbar = fig.colorbar(surf, ax=ax, pad=0.1)

# 设置颜色条的标签
cbar.set_label('Z-values')

# 添加标题和标签
ax.set_title('3D Surface Plot with Color Bar')
ax.set_xlabel('X-axis')
ax.set_ylabel('Y-axis')
ax.set_zlabel('Z-axis')

# 显示图形
plt.show()
