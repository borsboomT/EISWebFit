import pandas as pd
import numpy as np
import cmath
import matplotlib.pyplot as plt
'''
This is a simple script for simulating clean electrochemical impedance data.
'''


#Select some parameters for the equivalent circuit to be simulated.
Rs = 10
C = 1e-6
alpha = 0.75
Rct = 500

C2 = 1e-5
R2 = 800

#Generate a logarithmically spaced list of frequencies.
freqList = np.logspace(-1,6,num=100)

#For each frequency, calculated the impedance for various circuits of interest.
impedList = []
for freq in freqList:
    #Calcuated the angular frequency from the given frequency.
    w = 2*np.pi*freq
    s = complex(0,2*np.pi*freq)

    #Create the transfer function for the circuit of interest. A few standard circuits are shown here.
    Z = Rs + 1 / (s*C+1/Rct) #RCR
    # Z = Rs + 1 / (C*(s**alpha) + 1 / Rct) #RQR
    # Z = Rs + 1 / (s * C + 1 / (Rct+1/(s*C2+1/(R2)))) #RCRCR
    # Z = Rs + 1 / (C*(s**alpha) + 1 / (Rct + 1 / (s * C2 + 1 / (R2))))  # RQRCR

    #Collect all the frequencies into a list to describe the whole frequency spectrum.
    impedList.append([freq,Z.real,Z.imag])

#Add all data to a dataframe for ease of use.
df = pd.DataFrame(impedList, columns=["f","Re","Im"])

#Show the Nyquist plot for the spectrum
fig,ax = plt.subplots()
ax.plot(df["Re"], -df["Im"])
ax.set_aspect("equal")
# plt.show()

#Save the simulated data to disk
df.to_csv("RQRCRDat.txt",index=False)