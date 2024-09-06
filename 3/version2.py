import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib import rcParams

# 设置字体，确保能够显示中文字符
rcParams['font.sans-serif'] = ['SimHei']  # 使用黑体
rcParams['axes.unicode_minus'] = False  # 解决负号'-'显示为方块的问题

# 定义常量
v_head = 1.0  # 龙头行进速度(m/s)
r_turn_space = 4.5  # 调头空间半径(9m直径, 4.5m半径)
r_0 = 16 * 0.55  # 螺线初始半径, 假设从第16圈开始
num_sections = 223  # 总板凳节数
length_head = 3.41  # 龙头长度(m)
length_body = 2.20  # 龙身和龙尾长度(m)
section_lengths = [length_head] + [length_body] * (num_sections - 1)  # 各节板凳长度

# 调整螺距
p_initial = 0.55  # 螺距初始值
p_min = None  # 用于记录最小螺距

# 计算角速度
def calculate_angular_velocity(v_head, r_head):
    return v_head / r_head

# 计算龙头在时刻t的位置信息
def calculate_position(t, p):
    r = r_0 - p * t / (2 * np.pi)  # 半径随时间减少
    theta = t / r  # 极角随时间变化
    x = r * np.cos(theta)
    y = r * np.sin(theta)
    return x, y, r

# 计算板凳在t时刻的位置
def calculate_section_position(t, section_index, p):
    if section_index == 0:
        return calculate_position(t, p)  # 龙头位置
    prev_x, prev_y, prev_r = calculate_position(t, p)  # 前一节的位置
    section_length = section_lengths[section_index]
    direction = np.arctan2(prev_y, prev_x) + np.pi  # 板凳方向
    x = prev_x + section_length * np.cos(direction)
    y = prev_y + section_length * np.sin(direction)
    return x, y, np.sqrt(x**2 + y**2)

# 检测是否到达调头空间边界
def check_turn_space_boundary(t, p):
    x, y, r = calculate_position(t, p)  # 龙头在t时刻的位置
    if r <= r_turn_space:  # 到达调头空间边界
        return True, t
    return False, None

# 进行模拟，寻找最小螺距
def find_minimum_p(p_initial):
    global p_min
    t_total = 500  # 模拟的最大时刻
    for p in np.linspace(p_initial, 0.1, 100):  # 尝试不同螺距
        for t in range(t_total + 1):
            reached_boundary, boundary_time = check_turn_space_boundary(t, p)
            if reached_boundary:
                p_min = p
                print(f"找到最小螺距 p={p:.3f}, 龙头在 t={boundary_time}秒时到达调头空间边界")
                return p, boundary_time
    return None, None

# 寻找最小螺距
p_min, boundary_time = find_minimum_p(p_initial)

# 计算所有节板凳在盘入时的路径，并可视化
def plot_positions(p_min, boundary_time):
    fig, ax = plt.subplots(figsize=(10, 10))
    ax.set_aspect('equal')

    for t in range(0, boundary_time + 1, 10):  # 每隔10秒绘制一次
        x_vals = []
        y_vals = []
        for i in range(num_sections):
            x, y, _ = calculate_section_position(t, i, p_min)
            x_vals.append(x)
            y_vals.append(y)
        ax.plot(x_vals, y_vals, label=f't={t}s')

    # 绘制调头空间边界
    turn_circle = plt.Circle((0, 0), r_turn_space, color='r', fill=False, linestyle='--', label='调头空间边界')
    ax.add_artist(turn_circle)

    ax.set_title(f'舞龙队盘入螺旋路径(最小螺距)')
    ax.set_xlabel('x位置(m)')
    ax.set_ylabel('y位置(m)')
    ax.legend()
    plt.grid(True)
    plt.show()

# 绘制路径
if p_min is not None:
    plot_positions(p_min, boundary_time)
