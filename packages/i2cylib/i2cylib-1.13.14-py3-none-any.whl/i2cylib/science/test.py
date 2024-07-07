import numpy as np
import matplotlib.pyplot as plt

dt = 0.001

# 生成长度为N的白噪声信号
N = 1000

# 生成长度为N的蓝噪声信号
alpha = 10.0
f = np.linspace(0, 1, N//2)
P = f**alpha
P = np.concatenate((P, P[-1::-1]))
X = np.fft.fft(np.random.normal(size=N))*np.sqrt(P)
y = np.real(np.fft.ifft(X))

# 绘制时域和频域图像
plt.figure()
plt.subplot(2, 1, 1)
plt.plot(y)
# plt.title('Blue Noise (f{:d})'.format(alpha))
plt.ylabel('Amplitude')
plt.xlabel('Time (samples)')

plt.subplot(2, 1, 2)
plt.psd(y, NFFT=N, Fs=1/dt, color='purple')
plt.title('Power Spectral Density')
plt.ylabel('Power (dB/Hz)')
plt.xlabel('Frequency (Hz)')

plt.show()