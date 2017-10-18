import matplotlib.pyplot as plt
import numpy as np
from scipy import misc
from tunepy import tunepy, tunable



@tunepy
def matplotlibTest(fun, amp, title='test', fi=0, grid=False, y_lim=2):
    fig, ax = plt.subplots()
    plt.title(title)
    x = np.linspace(-np.pi, np.pi, 1000)
    y = amp*fun(x-fi)
    ax.plot(x,y)
    if grid: ax.grid()
    ax.set_ylim([-y_lim,y_lim])

fun = tunable(list, [np.sin, np.cos], listDesc=['sin', 'cos'])
amp = tunable(float, [0.5,2], ticks=10)
fi = tunable(float, [0, np.pi])
title = tunable(str, 'test')
grid = tunable(bool)
matplotlibTest(fun, amp, fi=fi, title=title, grid=grid, y_lim=2)
import sys
sys.exit(0)



@tunepy
def pixmapTest(brightness=1):
    return misc.face()*brightness

brightness = tunable(float, [0,1])
pixmapTest(brightness=brightness)



import contextlib, io
zen = io.StringIO()
with contextlib.redirect_stdout(zen):
    import this
text = zen.getvalue().splitlines()

@tunepy
def textTest(line):
    return "\n".join(text[:line])

line = tunable(int, [1, len(text)])
textTest(line)
