#plot ([X], Y, [fmt],_)     #линейный
#X, Y, fmt, color, marker, linestyle

#scatter (X,Y,_)        #точечный
#X, Y, sizes, colors, marker, cmap

#bar(x, height,_)       #колонки
#x, height, width, bottom, align, color

#contour ([X], [Y], Z, _)
#X, Y, Z, levels, colors, extent, origin)

#pie(X,_)
#Z, explode, labels, colors, radius

#text (x, y, text,_)
#x, y, text, va, ha, size, weight, transform

# example

# import matplotlib as mpl
# import matplotlib.pyplot as plt
# import numpy as np
# x = np.linspace(0, 10, 1000)
# y = np.linspace(-1, 1, 1000)
# X, Y = np.meshgrid(x, y)
# Z = X**2 + (Y - np.sqrt(X))**2 -1
# plt.contour(X, Y, Z, [0], color='red')
# plt.xlabel = 'Ось х'
# plt.ylabel = 'Ось У'
# plt.title = 'heart'
# plt.show()