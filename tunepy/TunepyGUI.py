from PyQt5 import QtGui, QtWidgets
import numpy as np
import matplotlib
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5 import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt
from tunepy.widgets import TunepyGUICore



class PixmapWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)

        self.label = QtWidgets.QLabel("test")
        
        layout = QtWidgets.QGridLayout()
        layout.addWidget(self.label, 0, 0)

        self.setLayout(layout)


    def setImage(self, img):
        qimage = QtGui.QImage(img.data, img.shape[1], img.shape[0], QtGui.QImage.Format_RGB888)
        pixmap = QtGui.QPixmap(qimage)
        self.label.setPixmap(pixmap)



class MatplotlibWidget(QtWidgets.QWidget):
    def __init__(self, fig, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        canvas = FigureCanvas(fig)
        canvas.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        canvas.updateGeometry()
        toolbar = NavigationToolbar(canvas, self)

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(toolbar)
        layout.addWidget(canvas)
        self.setLayout(layout)



class TunepyGUI(TunepyGUICore):
    def __init__(self, *args):
        TunepyGUICore.__init__(self, *args)
    
    
    def update(self):
        result = self.execFunction()
        if self.mode == 'auto':
            if result is None:
                if plt.gcf().axes: method = self.matplotlib
                else: method = self.unknown
            elif type(result) == np.ndarray:
                if len(result.shape) == 3 and result.shape[-1] == 3:
                    method = self.numpy
                else:
                    method = self.print
            else:
                method = self.print
        else:
            method = getattr(self, mode)
        method(result)
        plt.close()
    
    
    def unknown(self, result):
        self.print("Function output not recognized, check terminal for any output.")
    
    
    def matplotlib(self, result):
        fig = plt.gcf()
        centralWidget = MatplotlibWidget(fig, self)
        self.setCentralWidget(centralWidget)


    def numpy(self, result):
        centralWidget = QtWidgets.QScrollArea()
        pixmapWidget = PixmapWidget()
        pixmapWidget.setImage(np.uint8(result))
        centralWidget.setWidget(pixmapWidget)
        self.setCentralWidget(centralWidget)


    def print(self, result):
        from pprint import pformat
        if type(result) == str:
            toprint = result
        else:
            toprint = pformat(result)
        centralWidget = QtWidgets.QPlainTextEdit()
        centralWidget.setReadOnly(True)
        centralWidget.setPlainText(toprint)
        self.setCentralWidget(centralWidget)

