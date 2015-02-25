#!/usr/bin/python

import numpy as np
import matplotlib.pyplot as plt

def F(x, rat):
    return np.sqrt((1+4*rat*x)/(x-x**2))

def integrate(rat):
    s = 0
    dx = 0.001
    x = .01
    while x < 0.95:
        s += F(x,rat)*dx
        x += dx
    return s


rats = np.linspace(.1,10,num=50)
vals = []
for rat in rats:
    vals.append( integrate(rat) )
plt.plot(rats, vals)
plt.ylabel("$T_0$")
plt.xlabel(r"$\frac{B}{A}$")
plt.show()
