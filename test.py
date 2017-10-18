import matplotlib.pyplot as plt
import numpy as np
from scipy import misc
from tunepy import tunepy, tunable
import contextlib, io


# text for testing
zen = io.StringIO()
with contextlib.redirect_stdout(zen):
    import this
text = zen.getvalue().splitlines()


# image for testing
img = misc.face()


@tunepy
def testall(*args, **kwargs):
    method = args[0]
    if method == 'matplotlib':
        fun = args[1]
        amp = args[2]
        fi = args[3]
        title = args[4]
        grid = args[5]
        y_lim = args[6]
        fig, ax = plt.subplots()
        plt.title(title)
        x = np.linspace(-np.pi, np.pi, 1000)
        y = amp*fun(x-fi)
        ax.plot(x,y)
        if grid: ax.grid()
        ax.set_ylim([-y_lim,y_lim])
    if method == 'numpy':
        brightness = kwargs.get('brightness')
        return img*brightness
    if method == 'print':
        line = kwargs.get('line')
        return "\n".join(text[:line])
    if method == 'unknown':
        print()
        print(kwargs.get('combo_test'))
        print(kwargs.get('str_test'))
        print(kwargs.get('bool_test'))
        print(kwargs.get('const_test'))
    if method == 'error':
        return 2/0



pos_combo = tunable(list, ['matplotlib', 'numpy', 'print', 'unknown', 'error'])
pos_combo_listDesc = tunable(list, [np.sin, np.cos], listDesc=['sin', 'cos'])
pos_int = tunable(int, [1,5], ticks=4)
pos_float = tunable(float, [0, np.pi], ticks=10)
pos_str = tunable(str, 'test')
pos_bool = tunable(bool)
pos_constant = 5

kwa_combo = tunable(list, ['test1', 'test2'])
kwa_int = tunable(int, [1,len(text)])
kwa_float = tunable(float, [0.2,1])
kwa_str = tunable(str)
kwa_bool = tunable(bool)
kwa_constant = {'test':2}

testall(pos_combo,
        pos_combo_listDesc,
        pos_int,
        pos_float,
        pos_str,
        pos_bool,
        pos_constant,
        brightness=kwa_float,
        line=kwa_int,
        combo_test=kwa_combo,
        str_test=kwa_str,
        bool_test=kwa_bool,
        const_test=kwa_constant)
