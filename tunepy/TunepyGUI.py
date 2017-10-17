from PyQt5 import QtWidgets
import numpy as np
from tunepy.widgets import TunepyGUICore, PixmapWidget, MatplotlibWidget



class TunepyGUI(TunepyGUICore):
    def __init__(self, *args):
        TunepyGUICore.__init__(self, *args)
    
    
    def determineMode(self):
        result = self.execFunction()
        if result is None:
            import matplotlib.pyplot as plt
            if plt.gcf().axes: self.mode = 'matplotlib'
            else: self.mode = 'unknown'
        elif type(result) == np.ndarray:
            if len(result.shape) == 3 and result.shape[-1] == 3:
                self.mode = 'numpyPixmap'
            else:
                self.mode = 'print'
        else:
            self.mode = 'print'
    
    
    def unknown(self, result):
        self.tunerDock.setFeatures(QtWidgets.QDockWidget.NoDockWidgetFeatures)
    
    
    def matplotlib(self, result):
        import matplotlib.pyplot as plt
        fig = plt.gcf()
        centralWidget = MatplotlibWidget(fig, self)
        self.setCentralWidget(centralWidget)
        plt.close()


    def numpyPixmap(self, result):
        centralWidget = QtWidgets.QScrollArea()
        pixmapWidget = PixmapWidget()
        pixmapWidget.setImage(np.uint8(result))
        centralWidget.setWidget(pixmapWidget)
        self.setCentralWidget(centralWidget)


    def print(self, result):
        from pprint import pformat
        centralWidget = QtWidgets.QPlainTextEdit()
        centralWidget.setReadOnly(True)
        centralWidget.setPlainText(pformat(result))
        self.setCentralWidget(centralWidget)

