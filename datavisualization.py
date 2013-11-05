# -*- coding: utf-8 -*-
"""
Created on Tue Nov 05 17:19:33 2013

@author: CIT-Labs
"""

import numpy as np
import matplotlib.pyplot as plt


#x1 = np.arange(1,10)
#x2 = np.linspace(0.0, 2.0)

#y1 = np.cos(2 * np.pi * x1) * np.exp(-x1)
#y2 = np.cos(2 * np.pi * x2)

y1 = np.array([0.1,0.2,0])
y2 = y1

#(1,1)

for i in range(1,64):
    if i not in (1, 8, 57, 64):
        plt.subplot(8, 8, i)
        plt.plot(y1, 'yo-')
        plt.gca().xaxis.set_major_locator(plt.NullLocator())
        plt.gca().yaxis.set_major_locator(plt.NullLocator())

plt.show()
