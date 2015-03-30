import pylab as pl
import numpy as np

n = 1024
X = np.random.normal(0, 3, n)
Y = np.random.normal(0, 3, n)
T = np.arctan2(Y, X)

pl.scatter(X, Y, c=T)

pl.show()
