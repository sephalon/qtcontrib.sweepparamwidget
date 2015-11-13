# -*- coding: utf-8 -*-

from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

import sys
import os
import inspect
import collections
import importlib

from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtDesigner
from PyQt5 import QtWidgets
from PyQt5 import uic

filename = inspect.getfile(inspect.currentframe())
path = os.path.dirname(os.path.abspath(filename))

ParameterForm, ParameterBase = uic.loadUiType(os.path.join(path,
    'widget.ui'))
class SweepParameterWidget(ParameterForm, ParameterBase):
    FIXED_MODE = 0
    SWEEP_MODE = 1
    modeChanged = QtCore.pyqtSignal('int')

    @QtCore.pyqtProperty(str)
    def specialValueText(self):
        return self._specialValueText

    @specialValueText.setter
    def specialValueText(self, value):
        self._specialValueText = value
        self.fixedSpinBox.setSpecialValueText(value)

    @QtCore.pyqtProperty(str)
    def suffix(self):
        return self._suffix

    @suffix.setter
    def suffix(self, value):
        self._suffix = value
        self._set_suffix()

    def _set_suffix(self):
        try:
            self.fixedSpinBox.setSuffix(self.suffix)
            self.sweepStartSpinBox.setSuffix(self.suffix)
            self.sweepStopSpinBox.setSuffix(self.suffix)
            self.sweepStepSpinBox.setSuffix(self.suffix)
        except AttributeError:
            pass

    @QtCore.pyqtProperty(str)
    def spinBox(self):
        return self._spinBox

    @spinBox.setter
    def spinBox(self, value):
        self._spinBox = value

        widget = getattr(self, 'fixedSpinBox', None)
        if widget: widget.setParent(None)
        if hasattr(self, 'fixedSpinBox'): del self.fixedSpinBox

        elems = value.split('.')
        module_path = elems[:-1]
        print(module_path)
        widget_name = elems[-1]
        print(widget_name)

        #if module_path:
        #    try:
        #        module_path = '.'.join(module_path)
        #        print(module_path)
        #        module = importlib.import_module(module_path)
        #        print(module)
        #    except ImportError as e:
        #        print(e)
        #        return
        #else:
        #    module = QtWidgets
        
        widget = None
        try:
            n = '.'.join(module_path)
            print(sys.modules)
            print('-2342304', n)
            print('##################3', sys.modules[n])
            mod = sys.modules[n]
            widget = getattr(mod, widget_name)()
            print(dir(widget))
        except TypeError as e:
            print(e)
            return
        except AttributeError as e:
            print(e)
            return
        except Exception as e:
            print(e)
            return

        self.fixedSpinBox = widget
        widget.setObjectName('fixedSpinBox')
        widget.valueChanged.connect(self.fixedHorizontalSlider.setValue)
        self.fixedHorizontalSlider.valueChanged.connect(widget.setValue)
        getattr(self, 'fixedPageGridLayout').addWidget(widget, 0, 1)

        layout = getattr(self, 'sweepPageFormLayout')
        for index, label in enumerate(['Start', 'Stop', 'Step']):
            #widget = getattr(self, 'sweep{}SpinBox', None)
            #if widget: widget.setParent(None)
            layout.itemAt(index, QtWidgets.QFormLayout.FieldRole).widget().setParent(None)
            widget = None
            Widget = getattr(QtWidgets, value, None)
            if Widget:
                widget = Widget()
            #widget.setObjectName('sweep{}SpinBox'.format(label))
            layout.setWidget(index, QtWidgets.QFormLayout.FieldRole, widget)
            setattr(self, 'sweep{}SpinBox'.format(label), widget)
            #getattr(self, 'sweepPageFormLayout').addRow(elem, widget)
        self._set_suffix()

    def __init__(self, parent=None):
        super(SweepParameterWidget, self).__init__(parent)

        self.setupUi(self)
        #self.centralLayout = QtWidgets.QGridLayout()
        #self.setLayout(self.centralLayout)
        #self.fixedRadioButton = QtWidgets.QRadioButton('Fixed')
        #self.centralLayout.addWidget(self.fixedRadioButton)
        #self.sweepRadioButton = QtWidgets.QRadioButton('Sweep')
        #self.centralLayout.addWidget(self.sweepRadioButton)
        #self.stackedWidget = QtWidgets.QStackedWidget()
        #self.spinBox = 'QSpinBox'
        #self.fixedSpinBox = getattr(QtWidgets, self.spinBox)()
        #self.centralLayout.addWidget(self.fixedSpinBox)
        self.spinBox = 'QSpinBox'
        self.suffix = ''
        self._specialValueText = ''

    @QtCore.pyqtSlot()
    def on_fixedRadioButton_released(self):
        self.stackedWidget.setCurrentIndex(0)
        self.modeChanged.emit(SweepParameterWidget.FIXED_MODE)
        #self.modeChanged.emit()

    @QtCore.pyqtSlot()
    def on_sweepRadioButton_released(self):
        self.stackedWidget.setCurrentIndex(1)
        self.modeChanged.emit(SweepParameterWidget.SWEEP_MODE)
        #self.modeChanged.emit()

    @QtCore.pyqtSlot(float)
    def on_sweepStopSpinBox_valueChanged(self, value):
        self.sweepStartSpinBox.setMaximum(value)
        self.sweepStepSpinBox.setMaximum(value)

    #@QtCore.pyqtProperty(float, designable=False)
    def value(self):
        if self.fixedRadioButton.isChecked():
            return self.fixedSpinBox.value()
        else:
            return (
                    self.sweepStartSpinBox.value(),
                    self.sweepStopSpinBox.value(),
                    self.sweepStepSpinBox.value()
                    )

    #@value.setter
    #def value(self, value):

    def setMode(self, mode):
        if mode == SweepParameterWidget.FIXED_MODE:
            self.fixedRadioButton.setChecked(True)
            self.stackedWidget.setCurrentIndex(0)
        elif mode == SweepParameterWidget.SWEEP_MODE:
            self.sweepRadioButton.setChecked(True)
            self.stackedWidget.setCurrentIndex(1)

    def setValue(self, value):
        if isinstance(value, collections.Iterable) and len(value) == 3:
            self.sweepStartSpinBox.setValue(value[0]),
            self.sweepStopSpinBox.setValue(value[1]),
            self.sweepStepSpinBox.setValue(value[2])
            self.sweepRadioButton.setChecked(True)
        else:
            self.fixedSpinBox.setValue(value)
            self.fixedRadioButton.setChecked(True)

    def setRange(self, start, stop, step):
        self.fixedHorizontalSlider.setMinimum(start)
        self.fixedSpinBox.setMinimum(start)
        self.fixedHorizontalSlider.setMaximum(stop)
        self.fixedSpinBox.setMaximum(stop)

        self.sweepStartSpinBox.setMinimum(start)
        self.sweepStartSpinBox.setMaximum(stop)

        self.sweepStopSpinBox.setMinimum(start)
        self.sweepStopSpinBox.setMaximum(stop)

        self.sweepStepSpinBox.setMinimum(step)
        self.sweepStepSpinBox.setMaximum(stop)

    #def set_param_limits_and_defaults(self, param, constraint, type_=''):
    #    widgets = [type_ + 'SpinBox', 'HorizontalSlider']

    #    for widget in widgets:
    #        widget = getattr(self, '{param}Fixed{widget}'.format(param=param, widget=widget))
    #        widget.setMinimum(constraint['limits'][0])
    #        widget.setMaximum(constraint['limits'][1])
    #        widget.setSingleStep(constraint['limits'][2])

    #    sweepStartSpinBox = getattr(self,
    #            '{param}SweepStart{type_}SpinBox'.format(param=param, type_=type_))
    #    sweepStopSpinBox = getattr(self,
    #            '{param}SweepStop{type_}SpinBox'.format(param=param, type_=type_))
    #    sweepStepSpinBox = getattr(self,
    #            '{param}SweepStep{type_}SpinBox'.format(param=param, type_=type_))

    #    sweepStartSpinBox.setMinimum(constraint['limits'][0])
    #    sweepStartSpinBox.setMaximum(constraint['limits'][1])
    #    sweepStartSpinBox.setValue(constraint['defaults']['sweep'][0])

    #    sweepStopSpinBox.setMinimum(constraint['limits'][0])
    #    sweepStopSpinBox.setMaximum(constraint['limits'][1])
    #    sweepStopSpinBox.setValue(constraint['defaults']['sweep'][1])

    #    sweepStepSpinBox.setMinimum(constraint['limits'][2])
    #    sweepStepSpinBox.setMaximum(constraint['limits'][1])
    #    sweepStepSpinBox.setValue(constraint['defaults']['sweep'][2])
