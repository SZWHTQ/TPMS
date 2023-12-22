import tensorflow as tf
from tensorflow.keras.layers import Input, Dense, Lambda, Concatenate
from tensorflow.keras.models import Model
from tensorflow.keras.losses import MeanSquaredError
from tensorflow.keras import backend as K
import numpy as np
import matplotlib.pyplot as plt

# 生成带噪声的曲线数据
def generate_curve_data(samples=1000, input_dim=5):
    np.random.seed(42)
    params = np.random.rand(samples, input_dim)
    x = np.linspace(0, 1, samples)
    y = np.sin(2 * np.pi * x) + 0.1 * np.random.randn(samples)
    return params, y

# 构建 CVAE 模型
def build_cvae(input_dim, latent_dim):
    input_data = Input(shape=(input_dim,))
    condition_input = Input(shape=(input_dim,))
    
    # 编码器
    encoder_input = Concatenate()([input_data, condition_input])
    x = Dense(32, activation='relu')(encoder_input)
    z_mean = Dense(latent_dim)(x)
    z_log_var = Dense(latent_dim)(x)
    
    # 采样层
    def sampling(args):
        z_mean, z_log_var = args
        batch = K.shape(z_mean)[0]
        dim = K.int_shape(z_mean)[1]
        epsilon = K.random_normal(shape=(batch, dim))
        return z_mean + K.exp(0.5 * z_log_var) * epsilon
    
    z = Lambda(sampling, output_shape=(latent_dim,))([z_mean, z_log_var])
    
    # 解码器
    decoder_input = Concatenate()([z, condition_input])
    x = Dense(32, activation='relu')(decoder_input)
    output_data = Dense(input_dim, activation='linear')(x)
    
    # 构建模型
    cvae = Model([input_data, condition_input], output_data)
    
    # 定义损失函数
    reconstruction_loss = MeanSquaredError()(input_data, output_data)
    kl_loss = -0.5 * K.sum(1 + z_log_var - K.square(z_mean) - K.exp(z_log_var), axis=-1)
    cvae_loss = K.mean(reconstruction_loss + kl_loss)
    
    cvae.add_loss(cvae_loss)
    cvae.compile(optimizer='adam')
    
    return cvae

# 参数设置
input_dim = 5
latent_dim = 2

# 生成数据
params, y = generate_curve_data(input_dim=input_dim)

# 构建 CVAE 模型
cvae = build_cvae(input_dim, latent_dim)

# 训练模型
cvae.fit([params, params], epochs=50, batch_size=32, validation_split=0.2)

# 生成新的参数进行预测
new_params = np.random.rand(10, input_dim)
predicted_curve = cvae.predict([new_params, new_params])

# 绘制原始曲线和预测曲线
plt.figure(figsize=(10, 6))
plt.plot(np.linspace(0, 1, len(y)), y, label='Original Curve', color='blue')
plt.scatter(new_params, predicted_curve, label='Predicted Points', color='red')
plt.title('Original and Predicted Curves using CVAE')
plt.xlabel('X')
plt.ylabel('Y')
plt.legend()
plt.show()
