from PyQt5 import QtCore, QtWidgets
import math
import functools
from tunepy.tunable import tunable



class Tuner(QtWidgets.QFrame):
    def __init__(self, kind, definition, parent=None, changeAction=None, addKwargs=None, addDesc=None):
        QtWidgets.QFrame.__init__(self, parent)
        self.kind = kind
        self.changeAction = changeAction
        self.addDesc = addDesc
        self.label = QtWidgets.QLabel(self)
        if addDesc:
            self.label.setText('{} ='.format(addDesc))

        if self.kind == list:
            self.widget = QtWidgets.QComboBox(self)
            self.widget.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
            self.items = definition
            itemsDesc = map(str, self.items)
            if type(addKwargs) == dict:
                if 'listDesc' in addKwargs:
                    if len(addKwargs['listDesc']) == len(self.items):
                        itemsDesc = map(str, addKwargs['listDesc'])
            self.widget.addItems(itemsDesc)
            self.value = self.items[0]
            self.widget.currentIndexChanged.connect(self.comboBoxChanged)
            layout = QtWidgets.QGridLayout()
            if addDesc:
                layout.addWidget(self.label, 0, 0)
                layout.addWidget(self.widget, 0, 1)
            else:
                layout.addWidget(self.widget, 0, 0)


        elif self.kind in [float, int]:
            self.widget = QtWidgets.QSlider(QtCore.Qt.Horizontal, self)
            self.min = definition[0]
            self.max = definition[1]
            if self.kind == float:
                ticks = 100
                if type(addKwargs) == dict:
                    if 'ticks' in addKwargs:
                        if type(addKwargs['ticks']) == int:
                            ticks = addKwargs['ticks']
            elif self.kind == int:
                ticks = self.max - self.min
                if type(addKwargs) == dict:
                    if 'ticks' in addKwargs:
                        if type(addKwargs['ticks']) == int:
                            ticks = addKwargs['ticks']
            self.widget.setRange(0,ticks)
            self.widget.setValue(0)
            self.value = self.min
            self.input = QtWidgets.QLineEdit(self)
            self.sliderChanged(0, kind=self.kind, changeAction=False)
            self.widget.valueChanged.connect(functools.partial(self.sliderChanged, kind=self.kind))
            self.input.returnPressed.connect(functools.partial(self.sliderInputChanged, kind=self.kind))
            self.widget.sliderReleased.connect(self.changeAction)
            layout = QtWidgets.QGridLayout()
            if addDesc:
                layout.addWidget(self.label, 0, 0)
                layout.addWidget(self.input, 0, 1)
                layout.addWidget(self.widget, 1, 0, 1, 2)
            else:
                layout.addWidget(self.input, 0, 0)
                layout.addWidget(self.widget, 1, 0)


        elif self.kind == str:
            self.input = QtWidgets.QLineEdit(self)
            self.input.setText(str(definition))
            self.value = str(definition)
            self.input.returnPressed.connect(self.inputChanged)
            layout = QtWidgets.QGridLayout()
            if addDesc:
                layout.addWidget(self.label, 0, 0)
                layout.addWidget(self.input, 0, 1)
            else:
                layout.addWidget(self.input, 0, 0)

            
        elif self.kind == 'constant':
            if self.addDesc is None:
                desc = str(definition)
            else:
                desc = '{} = {}'.format(self.addDesc, str(definition))
            self.label.setText(desc)
            layout = QtWidgets.QGridLayout()
            layout.addWidget(self.label, 0, 0)
            self.value = definition
            
        self.setLayout(layout)
        self.setFrameShape(QtWidgets.QFrame.StyledPanel)


    def sliderChanged(self, num, kind=None, changeAction=True):
        self.value = float(num)/self.widget.maximum()*(self.max - self.min) + self.min
        if kind == float:
            sig_figs = 6
            self.value = round(self.value, -int(math.floor(math.log10(abs(self.value))) - (sig_figs - 1))) if self.value != 0 else 0
        elif kind == int:
            self.value = int(round(self.value))
        self.input.setText(str(self.value))
        if not self.widget.isSliderDown() and changeAction: self.changeAction()


    def sliderInputChanged(self, kind=None):
        valueSet = False
        if kind == float:
            try:
                self.value = float(self.input.text())
                valueSet = True
            except:
                QtWidgets.QMessageBox.critical(self, "Error", "Could not convert {} to float".format(self.input.text()))
        elif kind == int:
            try:
                self.value = int(self.input.text())
                valueSet = True
            except:
                QtWidgets.QMessageBox.critical(self, "Error", "Could not convert {} to int".format(self.input.text()))
        if valueSet: self.changeAction()
        


    def comboBoxChanged(self, index):
        self.value = self.items[index]
        self.changeAction()

       
    def inputChanged(self):
        self.value = self.input.text()
        self.changeAction()
        


class TunerWidgets(QtWidgets.QWidget):
    def __init__(self, funName, tunerList, tunerDict, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        funNameLabel = QtWidgets.QLabel("{}(".format(funName), self)
        endLabel = QtWidgets.QLabel(")", self)
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(funNameLabel)
        for tuner in tunerList:
            layout.addWidget(tuner)
        for kwarg, tuner in tunerDict.items():
            layout.addWidget(tuner)
        layout.addWidget(endLabel)
        layout.addStretch()
        self.setLayout(layout)



class TunerDock(QtWidgets.QDockWidget):
    def __init__(self, funName, tunerList, tunerDict, parent=None):
        QtWidgets.QDockWidget.__init__(self, parent)
        self.tunerWidgets = TunerWidgets(funName, tunerList, tunerDict)
        scrollArea = QtWidgets.QScrollArea()
        scrollArea.setWidget(self.tunerWidgets)
        self.setWidget(scrollArea)
        self.setAllowedAreas(QtCore.Qt.LeftDockWidgetArea | QtCore.Qt.RightDockWidgetArea)
        self.setFeatures(QtWidgets.QDockWidget.DockWidgetMovable | QtWidgets.QDockWidget.DockWidgetFloatable)



class TunepyGUICore(QtWidgets.QMainWindow):
    def __init__(self, mode, f, args, kwargs):
        QtWidgets.QMainWindow.__init__(self)

        self.f = f
        self.args = args
        self.kwargs = kwargs
        self.mode = mode

        funName = str(f).split()[1]
        self.buildTunerWidgets()
        self.tunerDock = TunerDock(funName, self.tunerList, self.tunerDict)
        self.addDockWidget(QtCore.Qt.LeftDockWidgetArea, self.tunerDock)

        if self.mode == 'auto': self.determineMode()

        self.update = getattr(self, self.mode)
        self.changeAction()


    def buildTunerWidgets(self):
        self.tunerList = []
        self.tunerDict = {}
        for arg in self.args:
            if isinstance(arg, tunable):
                newTuner = Tuner(arg.kind, arg.definition, self, self.changeAction, addKwargs=arg.kwargs)
            else:
                newTuner = Tuner('constant', arg, self)
            self.tunerList.append(newTuner)
        for kwarg, arg in self.kwargs.items():
            if isinstance(arg, tunable):
                newTuner = Tuner(arg.kind, arg.definition, self, self.changeAction, addKwargs=arg.kwargs, addDesc=kwarg)
            else:
                newTuner = Tuner('constant', arg, self, addDesc=kwarg)
            self.tunerDict[kwarg] = newTuner


    def execFunction(self):
        args = []
        kwargs = {}
        for tuner in self.tunerList:
            args.append(tuner.value)
        for kwarg, tuner in self.tunerDict.items():
            kwargs[kwarg] = tuner.value
        return self.f(*args, **kwargs)


    def changeAction(self):
        result = self.execFunction()
        self.update(result)
