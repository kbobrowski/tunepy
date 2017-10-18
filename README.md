# tunepy
Python decorator which allows to interactively tune arguments of a function using a simple GUI.

Automatically determines output type (matplotlib / numpy image / return value / console output).

## Installation

```
pip install tunepy
```

Dependencies:
- python3
- numpy
- matplotlib
- PyQt5

## Usage

Function decorated with ```@tunepy``` can accept instances of ```tunable``` class as arguments:

```
tunable_int = tunable.int([lower_bound, upper_bound],
                          ticks=number_of_ticks)

tunable_float = tunable.float([lower_bound, upper_bound],
                              ticks=number_of_ticks)

tunable_list = tunable.list([object_1, object_2, ...],
                            listDesc=[object_1_str, object_2_str, ...])

tunable_str = tunable.str(default_string)

tunable_bool = tunable.bool()
```

where:

- ```number_of_ticks```: number of ticks for a slider bar (optional)
- ```object_1_str, object_2_str, ...```: string representations of ```object_1, object_2, ...``` (optional)

## Examples
### matplotlib

Note that there is no call to ```plt.show()``` and no return value.

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

fun = tunable.list([np.sin, np.cos], listDesc=['sin', 'cos'])
amp = tunable.float([0.5,2], ticks=10)
fi = tunable.float([0, np.pi])
title = tunable.str('test')
grid = tunable.bool()
matplotlibTest(fun, amp, fi=fi, title=title, grid=grid, y_lim=2)
```

![example](screenshot.png)

### numpy image

```python
from scipy import misc
from tunepy import tunepy, tunable

@tunepy
def pixmapTest(brightness=1):
    return misc.face()*brightness

brightness = tunable.float([0,1])
pixmapTest(brightness=brightness)
```

![example2](screenshot2.png)

### text output

```python
import contextlib, io
zen = io.StringIO()
with contextlib.redirect_stdout(zen):
    import this
text = zen.getvalue().splitlines()

@tunepy
def textTest(line):
    return "\n".join(text[:line])

line = tunable.int([1, len(text)])
textTest(line)
```

![example3](screenshot3.png)

## Tips

- Output type can be forced by using ```tunepy_mode``` decorator with output type passed as a first argument (```"unknown"``` / ```"print"``` / ```"matplotlib"``` / ```"numpy"```):

```python
from scipy import misc
from tunepy import tunepy_mode, tunable

@tunepy_mode("numpy")
def pixmapTest(brightness=1):
    return misc.face()*brightness

brightness = tunable(float, [0,1])
pixmapTest(brightness=brightness)
```

- Preserving order of kwargs in GUI requires python3.6.
