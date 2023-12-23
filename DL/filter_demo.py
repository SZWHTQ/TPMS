import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import medfilt, butter, lfilter

# 生成示例数据
np.random.seed(42)
data = np.random.randn(100) + 5 * np.sin(np.linspace(0, 4*np.pi, 100))

# 移动平均滤波
def moving_average(data, window_size):
    return np.convolve(data, np.ones(window_size)/window_size, mode='valid')

# 中值滤波
def median_filter(data, kernel_size):
    return medfilt(data, kernel_size=kernel_size)

# 低通滤波器
def butter_lowpass_filter(data, cutoff_frequency, sampling_rate, order=4):
    nyquist = 0.5 * sampling_rate
    normal_cutoff = cutoff_frequency / nyquist
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    y = lfilter(b, a, data)
    return y

# 滤波处理
window_size = 5
kernel_size = 5
cutoff_frequency = 0.1
sampling_rate = 1.0

smoothed_ma = moving_average(data, window_size)
smoothed_median = median_filter(data, kernel_size)
smoothed_butter = butter_lowpass_filter(data, cutoff_frequency, sampling_rate)

# 绘制对比图
plt.figure(figsize=(12, 6))
plt.plot(data, label='Original Data', alpha=0.7)
plt.plot(smoothed_ma, label='Moving Average', linestyle='--')
plt.plot(smoothed_median, label='Median Filter', linestyle='--')
plt.plot(smoothed_butter, label='Butterworth Lowpass Filter', linestyle='--')

plt.title('Comparison of Different Filtering Methods')
plt.xlabel('Sample Index')
plt.ylabel('Value')
plt.legend()
plt.grid(True)
plt.show()
