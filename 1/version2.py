import numpy as np
import matplotlib.pyplot as plt
import os

# 定义常量
p = 0.55  # 螺距(m)
v_head = 1.0  # 龙头速度(m/s)
t_total = 300  # 总时间(s)
r_0 = 16 * p  # 螺线起始半径，假设起始在第16圈
num_sections = 223  # 总板凳节数
length_head = 3.41  # 龙头长度(m)
length_body = 2.20  # 龙身和龙尾长度(m)
section_lengths = [length_head] + [length_body] * (num_sections - 1)  # 各节板凳长度

# 初始化位置和速度列表
positions = np.zeros((t_total + 1, num_sections, 2))  # x, y坐标
velocities = np.zeros((t_total + 1, num_sections))  # 每节板凳速度

# 计算角速度
def calculate_angular_velocity(v_head, r_head):
    return v_head / r_head

# 计算每节板凳在t时刻的位置
def calculate_position(t, section_index):
    # 半径随时间变化
    r = r_0 + p * t / (2 * np.pi)
    theta = t / r  # 极角随时间变化
    # 计算每节板凳的前把手位置
    if section_index == 0:
        x = r * np.cos(theta)
        y = r * np.sin(theta)
    else:
        prev_x, prev_y = positions[t, section_index - 1]
        section_length = section_lengths[section_index]
        # 与前一节相反的方向
        direction = np.arctan2(prev_y, prev_x) + np.pi
        x = prev_x + section_length * np.cos(direction)
        y = prev_y + section_length * np.sin(direction)
    return x, y

# 计算每节板凳在t时刻的速度
def calculate_velocity(t, section_index):
    if t == 0:
        # 初始时刻速度为0
        return 0
    prev_pos = positions[t - 1, section_index]
    current_pos = positions[t, section_index]
    dist = np.sqrt((current_pos[0] - prev_pos[0])**2 + (current_pos[1] - prev_pos[1])**2)
    return dist

# 主循环：计算每秒的位置信息和速度
for t in range(t_total + 1):
    for i in range(num_sections):
        positions[t, i] = calculate_position(t, i)
        velocities[t, i] = calculate_velocity(t, i)

# 可视化螺线和板凳位置
def plot_positions():
    fig, ax = plt.subplots(figsize=(10, 10))
    ax.set_aspect('equal')

    for t in [0, 60, 120, 180, 240, 300]:
        ax.plot(positions[t, :, 0], positions[t, :, 1], label=f't={t}s')

    # 可视化龙头位置
    ax.scatter(positions[:, 0, 0], positions[:, 0, 1], color='red', s=50, label='龙头轨迹')
    # 设置图表标题和坐标轴标签
    ax.set_title('舞龙队沿螺线运动轨迹')
    ax.set_xlabel('x位置(m)')
    ax.set_ylabel('y位置(m)')

    # 显示图例并添加网格
    ax.legend()
    plt.grid(True)

    # 显示图表
    plt.show()

# 调用绘图函数
plot_positions()

# 保存结果到 Excel 文件
import pandas as pd

# 创建 DataFrame 来存储结果
result = pd.DataFrame(columns=["time", "section", "x_position", "y_position", "velocity"])

for t in range(t_total + 1):
    for i in range(num_sections):
        result = result.append({
            "time": t,
            "section": i + 1,
            "x_position": positions[t, i, 0],
            "y_position": positions[t, i, 1],
            "velocity": velocities[t, i]
        }, ignore_index=True)

# 保存为 Excel 文件
result.to_excel('result1.xlsx', index=False)

# 获取当前工作目录
current_directory = os.getcwd()

# 拼接文件路径
file_path = os.path.join(current_directory, 'result1.xlsx')

# 打印文件路径
print(f"文件已保存到: {file_path}")