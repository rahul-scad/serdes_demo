#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr  1 21:25:11 2023

@author: rahul
"""

import serdespy as sdp
import numpy as np
import scipy as sp
import matplotlib.pyplot as plt

#%% Generate ideal , square waveform

#generate pseudo-random binary sequnce with 2**13-1 elements
#for quaternary sequence use prqs10()
binary_data = sdp.prbs13(1)

#standard 2-PAM voltage levels
voltage_levels = np.array([-0.8,1.2])

#baud-rate sampled signal generated from data, using voltage_levels
# for 4-PAM signalling use pam4_input_BR()
signal_BR = sdp.nrz_input_BR(binary_data,voltage_levels)

#number of sample per 2-PAM symbol
samples_per_symbol = 100;

#oversample the baund-rate signal
signal = np.repeat(signal_BR, samples_per_symbol)

#1 Gbps date rate 
data_rate = 1e9

#Time per bit (Unit Interval)
UI =1/data_rate

#Timestep in 2_PAM_signal
dt = UI/samples_per_symbol

#Generate eye diagram for ideal signal with 3UI Shown on X axis and 100 traces plotted
sdp.simple_eye(signal, samples_per_symbol*3, 100, dt, "{}Gbps 2-PAM signal".format(data_rate/1e9))

#%% Low-Pass Filter
    
#500Hz cutoff frequency
freq_bw = 500e6


#max frequency for constructing discrete transfer function
max_f = 1/dt

#max_f in rad/s
max_w = max_f*2*np.pi

#heuristic to get a reasonabel impulse response length 
ir_length =800

#calculate discrate transfer function of low-pass filter with pole at freq_bw
w, H = sp.signal.freqs([freq_bw*(2*np.pi)],[1,freq_bw*(2*np.pi)],np.linspace(0,0.5*max_w,ir_length*4))

#frequency vector for discrete transfer function in hz
f = w/(2*np.pi)

#plot frequency response of the low-pass filter
plt.Figure(dpi=800)
plt.semilogx(1e-9*f, 20*np.log10(abs(H)))
plt.ylabel('Mag, Response [db]')
plt.xlabel('Frequrncy [GHz]')
plt.title("low pass Filter with {}MHz cutoff Magniyude Bode Plot".format(round(freq_bw*1e-6)))
plt.grid()
plt.axvline(x=1e-9*freq_bw,color = 'grey')
plt.show()

#%%

#find impluse respone of low pass filter
h , t = sdp.freq2impulse(H, f)

#confirm t has a timestep dt

#plot impulse response of the low-pass filter 
plt.figure(dpi=800)
plt.plot(t[:400]*1e12,h[:400])
plt.title("Low Pass Filter with{}MHz Cutoff Impulse Response".format(round(freq_bw*1e-6)))
plt.xlabel('Time[ps]')
plt.ylabel('[V]')
plt.show()

#%%

#filtered signal is convolution of the impulse response with the signal
signal_filtered = sp.signal.fftconvolve(signal, h[:400])

#plot eye diagram of the filtered signal
sdp.simple_eye(signal_filtered[samples_per_symbol*100:], samples_per_symbol*3,100,UI/samples_per_symbol,"{}Gbps 2-PAM Signal with {}MHz cutoff Filter Plot".format(data_rate/1e9,freq_bw*1e-6))          

               









 

