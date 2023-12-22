import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
import numpy as np
import matplotlib.pyplot as plt
import os

lower_bound = 0
upper_bound = 2 * np.pi


def func(x, params):
    return params[0] * np.sin(params[1] * np.pi * x + params[2]) + np.log(
        params[3] * np.pi * x + params[4]
    )


def test_func(x):
    return (
        np.sqrt(x) + (np.random.randn() + 1) * np.sin(np.pi * x)
    )


# 生成曲线数据
def generate_curve_data(samples=1000, params_num=5, points_num=201):
    np.random.seed(42)
    params = np.random.rand(samples, params_num)
    x = np.linspace(lower_bound, upper_bound, points_num)
    y = np.zeros([samples, points_num])
    for i in range(samples):
        y[i] = func(x, params[i, :])

    return params, y


# 构建神经网络模型
def build_model(points_num):
    act = "relu"
    model = Sequential()
    model.add(Dense(100, activation=act, input_dim=points_num))
    model.add(Dense(100, activation=act))
    model.add(Dense(5, activation=act))
    optimizer = tf.keras.optimizers.Adam(learning_rate=0.001)
    model.compile(optimizer=optimizer, loss="mse")  # 使用均方误差作为损失函数
    return model


def radar_plot(data):
    # 创建示例数据
    categories = ["P_1", "P_2", "P_3", "P_4", "P_5"]

    # 计算角度
    angles = np.linspace(0, 2 * np.pi, len(categories), endpoint=False)
    for _angle in angles:
        _angle -= angles[0]

    # 将第一个数据点重复添加到数据的末尾，以闭合雷达图
    data = np.concatenate((data, [data[0]]))
    angles = np.concatenate((angles, [angles[0]]))
    categories = np.concatenate((categories, [categories[0]]))

    # 创建雷达图
    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
    ax.plot(angles, data, linewidth=2, linestyle="solid", label="Data")
    ax.fill(angles, data, alpha=0.4)

    # 添加刻度标签
    ax.set_thetagrids(angles * 180 / np.pi, labels=categories)

    # 添加标题
    plt.title("Radar Chart", size=14, y=1.1)

    # 显示图例
    ax.legend(loc="upper right", bbox_to_anchor=(0.1, 0.1))


# 参数设置
samples = 1000
params_num = 5
points_num = 201

if os.path.exists("model.keras"):
    model = tf.keras.models.load_model("model.keras")
    model.load_weights("model_weights.keras")
else:
    # 生成数据
    params, y = generate_curve_data(
        samples=samples, params_num=params_num, points_num=points_num
    )
    # 构建模型
    model = build_model(points_num)
    # 训练模型
    model.fit(y, params, epochs=50, batch_size=32, verbose=1)
    model.save("model.keras")
    model.save_weights("model_weights.keras")

# 生成新的参数进行预测
x = np.linspace(lower_bound, upper_bound, points_num)
# new_params = np.random.rand(params_num)
# new_y = func(x, new_params)# + np.random.randn(points_num) * 0.1
new_y = test_func(x)
predicted_params = model.predict(np.reshape(new_y, [1, points_num]))
predicted_y = func(x, predicted_params[0, :])

# radar_plot(predicted_params[0,:] / new_params)

# 绘制原始曲线和预测曲线
plt.figure(figsize=(10, 6))
plt.plot(x, new_y, label="Target Curve", color="blue")
plt.scatter(x, predicted_y, label="Predicted Curve", color="red", marker="x")
plt.title("Target and Predicted Curves")
plt.xlabel("X")
plt.ylabel("Y")
plt.legend()
plt.show()
