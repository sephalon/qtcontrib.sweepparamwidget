# -*- coding: utf-8 -*-

from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtDesigner
from PyQt5 import QtWidgets

import qtcontrib.sweepparamwidget.widget as widget


class SweepParameterWidgetPlugin(QtDesigner.QPyDesignerCustomWidgetPlugin):
    def __init__(self, parent=None):
        super(SweepParameterWidgetPlugin, self).__init__()

    def name(self):
        return 'SweepParameterWidget'

    def group(self):
        return 'Input Widgets'

    def toolTip(self):
        return ''

    def whatsThis(self):
        return ''

    def includeFile(self):
        return 'qtcontrib.sweepparamwidget.widget'

    def icon(self):
        return QtGui.QIcon()

    def isContainer(self):
        return False
    
    def createWidget(self, parent):
        return widget.SweepParameterWidget(parent)

    def domXml(self):
        return (
            '<ui language="c++" displayname="Sweep Parameter Widget">\n'
            '  <widget class="SweepParameterWidget" name="sweepParameterWidget"/>\n'
            '  <customwidgets>\n'
            '    <customwidget>\n'
            '      <class>SweepParameterWidget</class>\n'
            '      <propertyspecifications>\n'
            '      </propertyspecifications>\n'
            '    </customwidget>\n'
            '  </customwidgets>\n'
            '</ui>'
           )
