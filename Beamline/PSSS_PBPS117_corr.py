from bsread import source
import matplotlib.pyplot as plt
import numpy as np

PSSS = 'SARFE10-PSSS059:SPECTRUM_Y'
PBPG = 'SAROP11-PBPS117:INTENSITY'
channels = [PSSS, PBPG]
numShots = 5000
offset_range = [-2,-1,0,1,2]

PSSS_data = []
PBPG_data = []
PSSS_data_good = []
PBPG_data_good = []

pulse_id = []
index_good = []
with source(channels=channels) as stream:
    for i in range(numShots):
        message = stream.receive()
        PSSS_data.append(message.data.data[PSSS].value)
        if message.data.data[PSSS].value is None:
            index_good.append(False)
        else:
            index_good.append(True)
            PSSS_data_good.append(message.data.data[PSSS].value)
            PBPG_data_good.append(message.data.data[PBPG].value)
        PBPG_data.append(message.data.data[PBPG].value)
        pulse_id.append(message.data.pulse_id)
PSSS_data = np.asarray(PSSS_data)
PBPG_data = np.asarray(PBPG_data)
PSSS_data_good = np.asarray(PSSS_data_good)
PBPG_data_good = np.asarray(PBPG_data_good)

pulse_id = np.asarray(pulse_id)
pulse_id = pulse_id[index_good]

index_FEL =[]
for i in pulse_id:
    if i%2 ==0:
        index_FEL.append(True)
    else:
        index_FEL.append(False)
index_FEL = np.asarray(index_FEL) 


plt.figure(figsize=[10,10])
plt.subplot(231)
plt.title('Offset %i'%offset_range[0])
plt.plot(PSSS_data_good.sum(axis=1)[:offset_range[0]], PBPG_data_good[-offset_range[0]:] ,'.')
plt.xlabel('Integrated PSSS signal')
plt.ylabel('PBPS117 signal')
plt.grid(True)

plt.subplot(232)
plt.title('Offset %i'%offset_range[1])
plt.plot(PSSS_data_good.sum(axis=1)[:offset_range[1]], PBPG_data_good[-offset_range[1]:] ,'.')
plt.xlabel('Integrated PSSS signal')
plt.ylabel('PBPS117 signal')
plt.grid(True)

plt.subplot(233)
plt.title('Offset %i'%offset_range[2])
plt.plot(PSSS_data_good.sum(axis=1), PBPG_data_good ,'.')
plt.xlabel('Integrated PSSS signal')
plt.ylabel('PBPS117 signal')
plt.grid(True)

plt.subplot(234)
plt.title('Offset %i'%offset_range[3])
plt.plot(PSSS_data_good.sum(axis=1)[offset_range[3]:], PBPG_data_good[:-offset_range[3]] ,'.')
plt.xlabel('Integrated PSSS signal')
plt.ylabel('PBPS117 signal')
plt.grid(True)

plt.subplot(235)
plt.title('Offset %i'%offset_range[4])
plt.plot(PSSS_data_good.sum(axis=1)[offset_range[4]:], PBPG_data_good[:-offset_range[4]] ,'.')
plt.xlabel('Integrated PSSS signal')
plt.ylabel('PBPS117 signal')
plt.grid(True)

plt.show()
