from PyQt5 import QtWidgets
from tunepy.TunepyGUI import TunepyGUI



class tunepy_mode(object):
    def __init__(self, mode='auto'):
        self.mode = mode


    def __call__(self, f):
        def wrapped_f(*args, **kwargs):
            app = QtWidgets.QApplication([])
            gui = TunepyGUI(self.mode, f, args, kwargs)
            gui.show()
            app.exec_()
        return wrapped_f



class tunepy(object):
    def __init__(self, f):
        self.f = f

    
    def __call__(self, *args, **kwargs):
        app = QtWidgets.QApplication([])
        gui = TunepyGUI('auto', self.f, args, kwargs)
        gui.show()
        app.exec_()
