import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib import rcParams

# 设置字体，确保能够显示中文字符
rcParams['font.sans-serif'] = ['SimHei']  # 使用黑体
rcParams['axes.unicode_minus'] = False  # 解决负号'-'显示为方块的问题

# 定义常量
r_initial = 4.5  # 调头结束后的螺线起始半径
p = 1.7  # 盘出时的螺距 (m)
v_max_possible = 2.0  # 各节板凳的最大允许速度 (m/s)
num_sections = 223  # 总板凳节数
length_head = 3.41  # 龙头长度 (m)
length_body = 2.20  # 龙身和龙尾长度 (m)
section_lengths = [length_head] + [length_body] * (num_sections - 1)  # 各节板凳长度

# 计算角速度
def calculate_angular_velocity(v_head, r):
    return v_head / r

# 计算螺线位置
def calculate_position(t, r_initial, p, v_head):
    r = r_initial + p * t / (2 * np.pi)
    theta = t / r
    x = r * np.cos(theta)
    y = r * np.sin(theta)
    return x, y, r

# 计算板凳在螺线上各个时刻的位置
def calculate_section_position(t, section_index, path_x, path_y, angles):
    prev_x = path_x[section_index - 1]
    prev_y = path_y[section_index - 1]
    section_length = section_lengths[section_index]
    direction = angles[section_index - 1] + np.pi  # 板凳方向
    x = prev_x + section_length * np.cos(direction)
    y = prev_y + section_length * np.sin(direction)
    return x, y

# 模拟盘出螺线运动，找到最大速度
def simulate_spiral_out(v_head, time_steps):
    path_x = np.zeros((time_steps, num_sections))
    path_y = np.zeros((time_steps, num_sections))
    angles = np.zeros((time_steps, num_sections))  # 用于计算方向
    max_velocities = np.zeros(time_steps)

    # 模拟各个时刻的位置和速度
    for t in range(time_steps):
        path_x[t, 0], path_y[t, 0], r = calculate_position(t, r_initial, p, v_head)
        angles[t, 0] = np.arctan2(path_y[t, 0], path_x[t, 0])  # 计算龙头的方向
        # 计算每节板凳的位置
        for i in range(1, num_sections):
            path_x[t, i], path_y[t, i] = calculate_section_position(t, i, path_x[t], path_y[t], angles[t])
            angles[t, i] = np.arctan2(path_y[t, i], path_x[t, i])
        # 计算每节板凳的速度
        if t > 0:
            velocities = np.sqrt((path_x[t] - path_x[t-1])**2 + (path_y[t] - path_y[t-1])**2)
            max_velocities[t] = np.max(velocities)
        return path_x, path_y, max_velocities

# 找到不超过2m/s的最大速度
def find_maximum_head_velocity(time_steps):
    for v_head in np.arange(0.5, 3.0, 0.01):  # 逐步增加龙头速度
        _, _, max_velocities = simulate_spiral_out(v_head, time_steps)
        if np.all(max_velocities <= v_max_possible):
            print(f"找到最大龙头速度 v_head = {v_head:.2f} m/s")
            return v_head
    return None

# 模拟盘出过程,找到最大龙头速度
time_steps = 500
v_max_head = find_maximum_head_velocity(time_steps)

# 可视化螺线运动和速度
def plot_spiral_out(path_x, path_y, max_velocities):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(18, 9))
    ax1.set_aspect('equal')
    # 绘制螺线轨迹
    for t in range(0, time_steps, 20):  # 每隔20秒绘制一次
        ax1.plot(path_x[t, :], path_y[t, :], label=f't={t}s')
    ax1.set_title('舞龙队螺线盘出路径')
    ax1.set_xlabel('x位置(m)')
    ax1.set_ylabel('y位置(m)')
    ax1.legend()

    # 绘制速度随时间的变化
    ax2.plot(np.arange(time_steps), max_velocities, label='最大速度')
    ax2.axhline(y=v_max_possible, color='r', linestyle='--', label='最大允许速度2m/s')
    ax2.set_title('每节板凳的最大速度随时间变化')
    ax2.set_xlabel('时间(s)')
    ax2.set_ylabel('速度(m/s)')
    ax2.legend()
    plt.grid(True)
    plt.show()

# 绘制找到最大速度后的路径和速度
if v_max_head:
    path_x, path_y, max_velocities = simulate_spiral_out(v_max_head, time_steps)
    plot_spiral_out(path_x, path_y, max_velocities)