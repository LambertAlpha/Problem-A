import numpy as np
import pandas as pd

# 设置初始参数
num_bench = 223  # 板凳总数
head_length = 341  # 龙头长度 (cm)
body_length = 220  # 龙头身和龙尾长度 (cm)
width = 30  # 板凳宽度 (cm)
hole_diameter = 5.5  # 孔径 (cm)
distance_between_benches = body_length / 100  # 板凳间距离 (m)
initial_speed = 1.0  # 龙头前把手速度 (m/s)
螺距 = 0.55  # 螺线的螺距 (m)
time_limit = 3000  # 考察总时间 (s)

# 记录时间、位置与速度
time_steps = np.arange(0, time_limit + 1, 1)
positions = np.zeros((len(time_steps), num_bench, 2))  # 位置 (m)
speeds = np.zeros((len(time_steps), num_bench))  # 速度 (m/s)

# 初始化龙头的位置
angle = 0
z = 0
positions[0, 0, :] = [0, 0]  # 龙头位置

# 计算每个时间点的位置和速度
for t in range(1, len(time_steps)):
    # 更新角度和z的位置
    angle += (initial_speed / (螺距 / 2))  # 每秒转过的角度
    z += initial_speed * 1  # z轴前移的距离

    # 计算位置
    for i in range(num_bench):
        # 计算对应当前角度和z的坐标
        theta = angle - (i * (body_length / 100) / 螺距)  # 当前把手的角度
        x = z * np.cos(theta)  # x坐标
        y = z * np.sin(theta)  # y坐标
        positions[t, i, :] = [x, y]

    # 速度更新
    speeds[t, :] = [initial_speed] * num_bench

    # 检查碰撞
    if t > 1:
        for i in range(num_bench - 1):
            distance = np.linalg.norm(positions[t, i, :] - positions[t, i + 1, :])
            if distance < distance_between_benches:
                end_time = t - 1  # 碰撞发生的时刻
                break
        else:
            continue
        break
else:
    end_time = time_limit  # 没有发生碰撞

# 输出结果
final_positions = pd.DataFrame(positions[end_time])
final_speeds = pd.DataFrame(speeds[end_time])

# 输出到 Excel
with pd.ExcelWriter('result2.xlsx') as writer:
    final_positions.to_excel(writer, sheet_name='Position', index=False, header=False)
    final_speeds.to_excel(writer, sheet_name='Speed', index=False, header=False)

# 在论文中输出特定把手的结果
for i in [0, 1, 51, 101, 151, 201]:
    print(f"Time: {end_time} s - Position of part {i}:", final_positions.iloc[i].values)
    print(f"Time: {end_time} s - Speed of part {i}:", final_speeds.iloc[i].values)