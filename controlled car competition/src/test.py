import scipy.io as sio
import matplotlib.pyplot as plt
import numpy as np
from scipy.fft import fft, fftfreq, ifft
import os

data_list = os.listdir('../REC/')
#print(data_list)
for i in data_list:
    if i.split('.')[0][-2:] == str(13):
        #print(i)
        data = sio.loadmat('../REC/'+str(i))
        fft_data = np.fft.fft(data['X'][:, 4])
        plt.plot(np.abs(fft_data)[int(len(fft_data)/256*10):int(len(fft_data)/256*20),])
        peak = np.abs(fft_data)[int(len(fft_data)/256*10):int(len(fft_data)/256*20),]
        print(np.max(peak)) 
plt.show()  



# data = sio.loadmat('D:\\nycu\\BCI\\Final competition\\REC\\3_11_03_18_05_2023_freq_20.mat')
# #print(data['X'][4])

# fft_data = np.fft.fft(data['X'][:, 4])
# #print(fft_data.shape)

# plt.plot(np.abs(fft_data)[int(len(fft_data)/256*10):int(len(fft_data)/256*20),])
# #plt.plot(np.abs(fft_data))
# #plt.ylim(1e-5)
# plt.show()

# peak = np.abs(fft_data)[int(len(fft_data)/256*10):int(len(fft_data)/256*20),]
# print(np.max(peak))

