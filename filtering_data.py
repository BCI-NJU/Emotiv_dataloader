from sub_data import BCI_dev
import time
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import butter, filtfilt, iirnotch, lfilter

def butter_bandpass_filter(data, lowcut, highcut, fs, order):
    fa = 0.5 * fs
    low = lowcut / fa
    high = highcut / fa
    b, a = butter(order, [low, high], btype='band')
    ret = []
    for line in data:
        ret.append(filtfilt(b, a, line))
    return ret

def iirnotch_filter(data, fs = 250, Q = 30, f_cut = 50.0):
    ret = []
    b, a = iirnotch(f_cut, Q, fs)
    for line in data:
        ret.append(lfilter(b,a, line))
    return ret


def data_processing(address, butter_order = 2):
    '''
    return data:前14个为节点信号，最后一个是时间信号
    '''
    data = np.load(address)
    time_list = data[:,-1] - data[0,-1]
    eeg_list = data[:,2:-3].T
    filter_data = butter_bandpass_filter(eeg_list, 0.5, 100, 250, butter_order)
    filter_data = iirnotch_filter(filter_data, 250, 30.0, 50.0)
    filter_data.append(time_list)
    return filter_data

def make_data(address ,wait_time, time_len ,streams = ['eeg']):
    time.sleep(wait_time)
    my_BCI = BCI_dev(streams)
    my_BCI.start()
    time.sleep(time_len)
    my_BCI.close()
    my_BCI.save(address + '_orginal.npy')

    data = data_processing(address + '_orginal.npy')

    np.save(address + '_processed.npy',data)



if __name__ =='__main__':
    make_data('./data/leg', 15, 15)
    
    


    
    
    
