# tunepy
Python decorator which allows to interactively tune arguments of a function.

Automatically determines output type (matplotlib / numpy image / return value / console output).

Decorated function can take instances of a "tunable" class instead of constant values as arguments.

## Example

Code to plot a function:

```python
import matplotlib.pyplot as plt

def matplotlibTest(fun, amp, title='test', fi=0, grid=False, y_lim=2):
    fig, ax = plt.subplots()
    plt.title(title)
    x = np.linspace(-np.pi, np.pi, 1000)
    y = amp*fun(x-fi)
    ax.plot(x,y)
    if grid: ax.grid()
    ax.set_ylim([-y_lim,y_lim])

matplotlibTest(np.sin, 0.5, fi=0, title='test', grid=True, y_lim=2)
plt.show()
```

can be easily decorated to allow interactive parameter tuning:

```python
import matplotlib.pyplot as plt
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
```

![example](screenshot.png)

## Tips

Output type can be forced by using tunepy\_mode decorator with output type passed as a first argument ("unknown" / "print" / "matplotlib" / "numpyPixmap")
