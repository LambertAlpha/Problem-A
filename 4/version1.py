import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib import rcParams

# 设置字体，确保能够显示中文字符
rcParams['font.sans-serif'] = ['SimHei']  # 使用黑体
rcParams['axes.unicode_minus'] = False  # 解决负号'-'显示为方块的问题

# 定义常量
v_head = 1.0  # 龙头行进速度(m/s)
R2 = 4.5  # 后一段圆弧半径，调头空间半径
R1 = 2 * R2  # 前一段圆弧半径
num_sections = 223  # 总板凳节数
length_head = 3.41  # 龙头长度(m)
length_body = 2.20  # 龙身和龙尾长度(m)
section_lengths = [length_head] + [length_body] * (num_sections - 1)  # 各节板凳长度
time_steps = 200  # 调头的时间步数

# 计算第一段圆弧的路径
def calculate_first_arc(t, R1, v_head, start_angle):
    theta = v_head * t / R1 + start_angle  # 角度随时间变化
    x = R1 * np.cos(theta)
    y = R1 * np.sin(theta)
    return x, y, theta

# 计算第二段圆弧的路径
def calculate_second_arc(t, R2, start_angle):
    theta = t / R2 + start_angle  # 角度随时间变化
    x = R2 * np.cos(theta)
    y = R2 * np.sin(theta)
    return x, y

# 计算每节板凳在调头路径上的位置
def calculate_section_position(t, section_index, path_x, path_y, angles):
    prev_x = path_x[section_index - 1]
    prev_y = path_y[section_index - 1]
    section_length = section_lengths[section_index]
    direction = angles[section_index - 1] + np.pi  # 板凳方向
    x = prev_x + section_length * np.cos(direction)
    y = prev_y + section_length * np.sin(direction)
    return x, y

# 模拟调头路径
def simulate_turn_path(time_steps, R1, R2):
    path_x = np.zeros((time_steps, num_sections))
    path_y = np.zeros((time_steps, num_sections))
    angles = np.zeros((time_steps, num_sections))  # 用于计算方向

    # 第一段圆弧
    for t in range(time_steps // 2):
        path_x[t, 0], path_y[t, 0], angles[t, 0] = calculate_first_arc(t, R1, v_head, 0)  # 龙头

        # 计算每节板凳的位置
        for i in range(1, num_sections):
            path_x[t, i], path_y[t, i] = calculate_section_position(t, i, path_x[t], path_y[t], angles[t])

    # 第二段圆弧
    start_angle = angles[time_steps // 2 - 1, 0]  # 第二段圆弧的起始角度
    for t in range(time_steps // 2, time_steps):
        path_x[t, 0], path_y[t, 0] = calculate_second_arc(t - time_steps // 2, R2, start_angle)  # 龙头
    
        # 计算每节板凳的位置
        for i in range(1, num_sections):
            path_x[t, i], path_y[t, i] = calculate_section_position(t, i, path_x[t], path_y[t], angles[t - 1])

    return path_x, path_y

# 可视化调头路径
def plot_turn_path(path_x, path_y):
    fig, ax = plt.subplots(figsize=(10, 10))
    ax.set_aspect('equal')

    # 绘制每个时间步的路径
    for t in range(0, time_steps, 10):
        ax.plot(path_x[t], path_y[t], label=f't={t}s')

    ax.set_title('舞龙队调头路径')
    ax.set_xlabel('x位置(m)')
    ax.set_ylabel('y位置(m)')
    ax.legend()
    plt.grid(True)
    plt.show()

# 计算并绘制调头路径
path_x, path_y = simulate_turn_path(time_steps, R1, R2)
plot_turn_path(path_x, path_y)

# 保存结果到 Excel文件
'''result = pd.DataFrame(columns=["time", "section", "x_position", "y_position"])

for t in range(time_steps):
    for i in range(num_sections):
        result = result.append({
            "time": t,
            "section": i + 1,
            "x_position": path_x[t, i],
            "y_position": path_y[t, i]
        }, ignore_index=True)'''


data = []

for t in range(time_steps):
    for i in range(num_sections):
        data.append({
            "time": t,
            "section": i + 1,
            "x_position": path_x[t, i],
            "y_position": path_y[t, i],
        })

# 将列表转换为 DataFrame
result = pd.DataFrame(data)

# 保存为Excel文件
result.to_excel('result4.xlsx', index=False)