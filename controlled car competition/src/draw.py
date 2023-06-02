import scipy.io as sio
from matplotlib import pyplot as plt
import numpy as np
import time


data = sio.loadmat('./REC/3_04_32_26_05_2023_freq_20.mat')
fft_data = np.fft.fft(np.array(data['X'])[:, 4])
plt.plot(np.abs(fft_data)[int(len(fft_data)/256*10):int(len(fft_data)/256*20),])
plt.savefig("test_17.png")
peak = np.abs(fft_data)[int(len(fft_data)/256*10):int(len(fft_data)/256*20),]
print("peak value:", np.max(peak))