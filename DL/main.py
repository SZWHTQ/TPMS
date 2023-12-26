import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams
import os
from scipy.signal import medfilt
from scipy.interpolate import interp1d
from tqdm import tqdm

rcParams['font.family'] = ['serif']
rcParams['font.serif'] = ['Times New Roman']
rcParams['font.size'] = 16

samples_num = 108

def load_force_data():
    data = []
    file = "../dataset/1/ContforcPlot.dat"
    data = np.loadtxt(file)
    time = data[:, 0]
    force = []
    params = []
    volume_frac = []
    for i in tqdm(range(1, samples_num + 1)):
        force_file = "../dataset/" + str(i) + "/ContforcPlot.dat"
        force_data = np.loadtxt(force_file)
        force.append(-force_data[:, 5])
        params_file = "../dataset/" + str(i) + "/parameter.txt"
        try:
            with open(params_file, "r") as file:
                first_line = file.readline().strip().split()
                params.append([float(param) for param in first_line])
                second_line = file.readline().strip().split()
                volume_frac.append([float(param) for param in second_line])
        except FileNotFoundError:
            print("FileNotFoundError: " + params_file)
        except Exception as e:
            print("Error reading file " + params_file + ": " + str(e))
    force = np.array(force)
    params = np.array(params)
    volume_frac = np.array(volume_frac)

    return time, force, params, volume_frac


def preprocess(time, force):
    print("Filtering...")
    force = filter_force_data(force)
    print("Interploting...")
    new_time = np.linspace(np.min(time), np.max(time), 1001)
    new_force = interplot_force_data(time, new_time, force)
    return new_time, new_force


def filter_force_data(data):
    new_data = []
    for force in tqdm(data):
        new_data.append(medfilt(force, 5))
    new_data = np.array(new_data)
    return new_data


def interplot_force_data(time, new_time, data):
    new_data = []
    for force in tqdm(data):
        interplot_function = interp1d(time, force, kind="cubic")
        new_data.append(interplot_function(new_time))
    new_data = np.array(new_data)
    return new_data

# def build_model(points_num):
#     act = "relu"
#     input = tf.keras.layers.Input(shape=(points_num,), name="input")
#     x = tf.keras.layers.Dense(128, activation=act)(input)
#     x = tf.keras.layers.BatchNormalization()(x)
#     x = tf.keras.layers.Dense(256, activation=act)(x)
#     x = tf.keras.layers.BatchNormalization()(x)
#     output = tf.keras.layers.Dense(5, activation="linear", name="output")(x)
#     return tf.keras.models.Model(inputs=input, outputs=output, name="model")

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

def build_model(points_num):
    act = "relu"
    model = tf.keras.models.Sequential(name="model")
    model.add(tf.keras.layers.Dense(128, activation=act, input_dim=points_num, name="input"))
    model.add(tf.keras.layers.BatchNormalization())
    model.add(tf.keras.layers.Dense(256, activation=act))
    model.add(tf.keras.layers.BatchNormalization())
    model.add(tf.keras.layers.Dense(5, activation='linear', name="output"))
    optimizer = tf.keras.optimizers.Adam(learning_rate=0.0001)
    model.compile(optimizer=optimizer, loss="mse")
    return model

@tf.keras.saving.register_keras_serializable()
def loss_function(y_true, y_pred):
    return tf.keras.backend.mean(tf.keras.backend.square(y_true - y_pred))

@tf.keras.saving.register_keras_serializable()
def loss_MAE(y_true, y_pred):
    return tf.keras.backend.mean(tf.keras.backend.abs(y_true - y_pred))

def target_func(x):
    return 10+150*(x-0.1)**2

if os.path.exists("data.npz"):
    try:
        with np.load("data.npz") as data:
            old_time = data["time"]
            force = data["force"]
            params = data["params"]
        print("Data loaded.")
        time, force = preprocess(old_time, force)
    except FileNotFoundError:
        print("FileNotFoundError: data.npz")
        exit
    except Exception as e:
        print("Error reading file data.npz: " + str(e))
        exit
else:
    print("Load data...")
    old_time, force, params, vf = load_force_data()
    np.savez_compressed("data.npz", time=old_time, force=force, params=params, volume_frac=vf)
    time, force = preprocess(old_time, force)

params_num = np.size(params)
points_num = np.size(force, 1)

if os.path.exists("model.keras") and os.path.exists("model_weights.keras"):
    model = tf.keras.models.load_model("model.keras")
    model.load_weights("model_weights.keras")
    print("Model loaded.")
else:
    # Construct model
    model = build_model(points_num)
    model.summary()
    optimizer = tf.keras.optimizers.Adam(learning_rate=0.001)
    # optimizer = tf.keras.optimizers.SGD(learning_rate=0.001, momentum=0.9, nesterov=True)
    model.compile(optimizer=optimizer, loss=loss_function, metrics=[loss_MAE])
    # Train model
    model.fit(force, params, epochs=100, batch_size=16, validation_split=0.2, verbose=1)
    model.save("model.keras")
    model.save_weights("model_weights.keras")

# Generate new curve
# random_index = np.random.randint(0, samples_num, 7)
# new_force = np.average(force[random_index], axis=0)
new_force = target_func(time/1e2)*1e4
np.savetxt("new_force.txt", new_force)
predicted_params = model.predict(np.reshape(new_force, [1, points_num]))
np.savetxt("predicted_params.txt", predicted_params)

# radar_plot(predicted_params[0,:] / new_params)

# Plot
plt.figure(figsize=(8, 6))
plt.plot(time/1e2, new_force/1e4, label="Target Curve", linewidth=2, color="#ff7f0e")
plt.ylim(-2,152)
plt.yticks(np.arange(0, 152, 25))
# plt.scatter(x, predicted_y, label="Predicted Curve", color="red", marker="x")
plt.title("Target")
# plt.title("Target and Predicted Curves")
plt.xlabel("Strain")
plt.ylabel("Stress (MPa)")
plt.legend()
plt.show()
