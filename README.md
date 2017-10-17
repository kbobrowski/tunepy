# tunepy
Python decorator which allows to interactively tune arguments of a function.

## Example

Code to plot sinus function:

```python
import matplotlib.pyplot as plt

def simpleplot(a):
    x = np.linspace(-np.pi, np.pi, 1000)
    y = a*np.sin(x)
    fig, ax = plt.subplots()
    ax.plot(x,y)
    ax.set_ylim([-1,1])

simpleplot(1)
plt.show()
```

can be easily decorated to allow interactive parameter tuning:

```python
import matplotlib.pyplot as plt
from tunepy import tunepy, tunable

@tunepy
def simpleplot(a):
    x = np.linspace(-np.pi, np.pi, 1000)
    y = a*np.sin(x)
    fig, ax = plt.subplots()
    ax.plot(x,y)
    ax.set_ylim([-1,1])

a = tunable(float, [0, 1])
simpleplot(a)
```
