#test
import numpy as np

import matplotlib.pyplot as plt

import pandas as pd

# 定义常量
p = 0.55  # 螺距(m)
v_head = 1.0  # 龙头速度(m/s)
r_0 = 16 * p  # 螺线初始半径,假设从第16圈开始
num_sections = 223  # 总板凳节数
length_head = 3.41  # 龙头长度(m)
length_body = 2.20  # 龙身和龙尾长度(m)
width = 0.30  # 板凳的宽度,碰撞判定距离(m)
section_lengths = [length_head] + [length_body] * (num_sections - 1)  # 各节板凳长度

# 时间和空间初始化
t_total = 1000  # 总的模拟时间，设置较长时间，模拟碰撞发生时刻
positions = np.zeros((t_total + 1, num_sections, 2))  # 每节板凳在每一秒的x,y位置
velocities = np.zeros((t_total + 1, num_sections))  # 每节板凳在每一秒的速度

# 计算角速度
def calculate_angular_velocity(v_head, r_head):
    return v_head / r_head

# 计算板凳在t时刻的位置
def calculate_position(t, section_index):
    r = r_0 + p * t / (2 * np.pi)  # 半径随时间变化
    theta = t / r  # 极角随时间变化
    if section_index == 0:  # 计算龙头位置
        x = r * np.cos(theta)
        y = r * np.sin(theta)
    else:
        prev_x, prev_y = positions[t, section_index - 1]
        section_length = section_lengths[section_index - 1]
        direction = np.arctan2(prev_y, prev_x) + np.pi  # 板凳在前一节的方向
        x = prev_x + section_length * np.cos(direction)
        y = prev_y + section_length * np.sin(direction)
    return x, y

# 计算板凳在t时刻的速度
def calculate_velocity(t, section_index):
    if t == 0:
        return 0  # 初始速度为0
    prev_pos = positions[t - 1, section_index]
    current_pos = positions[t, section_index]
    dist = np.sqrt((current_pos[0] - prev_pos[0])**2 + (current_pos[1] - prev_pos[1])**2)
    return dist

# 检测相邻板凳之间是否碰撞
def check_collision(t):
    for i in range(num_sections - 1):
        print(positions[t,i,0])
        dist = np.sqrt((positions[t, i, 0] - positions[t, i + 1, 0])**2 +
                       (positions[t, i, 1] - positions[t, i + 1, 1])**2)
        print(dist,width)
        if dist < width:
            return True, t #返回碰撞时间
    return False, None

# 主循环:计算每秒位置信息和速度，检查碰撞
collision_time = None

for t in range(t_total + 1):
    for i in range(num_sections):
        positions[t, i] = calculate_position(t, i)
        velocities[t, i] = calculate_velocity(t, i)
    collision_detected, collision_time = check_collision(t)
    print(t,check_collision(t))
    if collision_detected:
        print(f"Collision detected at t={t} seconds")
        break

# 可视化螺旋运动和碰撞

def plot_positions(collision_time):
    fig, ax = plt.subplots(figsize=(10, 10))
    ax.set_aspect('equal')
    ax.plot(positions[:collision_time, 0, 0], positions[:collision_time, 0, 1],label='龙头轨迹',color='red')
    
    # 绘制发生碰撞时刻的板凳位置
    ax.scatter(positions[collision_time, :, 0], positions[collision_time, :, 1], color='blue', label='碰撞时刻位置')
   
    ax.set_title(f'舞龙队盘入螺旋路径(碰撞发生于t={collision_time}秒)')
    ax.set_xlabel('x位置(m)')
    ax.set_ylabel('y位置(m)')
    ax.legend()
    plt.grid(True)
    plt.show()

# 绘制发生碰撞的路径
plot_positions(collision_time)

# 保存结果到 Excel文件
result = pd.DataFrame(columns=["time", "section", "x_position", "y_position", "velocity"])

for t in range(collision_time + 1):
    for i in range(num_sections):
        result = result.append({
            "time": t,
            "section": i + 1,
            "x_position": positions[t, i, 0],
            "y_position": positions[t, i, 1],
            "velocity": velocities[t, i]
    }, ignore_index=True)

# 保存为 Excel文件
result.to_excel('result2.xlsx', index=False)