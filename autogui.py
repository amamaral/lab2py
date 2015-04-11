# -*- coding: utf-8 -*-
"""autogui
Created on Tue Apr  7 23:12:11 2015

@author: anderson
"""
from PyQt4.QtGui import QApplication, QWidget, QGroupBox, QFormLayout,\
    QLabel, QCheckBox, QComboBox, QSpinBox,\
    QDoubleSpinBox, QLineEdit, QTextEdit
# from PyQt4.QtCore import SIGNAL, pyqtSlot, QObject

from core import dataObject, dataGroup
from coreConstants import *


class UIBuilder(dataGroup):
    """UIBuilder(dataGroup):
    This class creates the high-level access to the data
    """
    def __init__(self, name=None, label=None, children=[], helpString=None,
                 parent=None, widget=None, **kwargs):
        dataGroup.__init__(self, name=name, label=label, children=children,
                           helpString=helpString, parent=parent, widget=widget,
                           **kwargs)

    def buildUI(self):
        """buildUI():
        Builds the user interface using PyQt and the current configurations.
        """
        if self.widget is None:
            if self.parent is None:
                self.widget = QWidget()
            else:
                self.widget = QGroupBox()
                self.widget.setTitle(self.label)
        # TODO: Allow user to set different form layouts
        layout = QFormLayout(self.widget)
        self.widget.setLayout(layout)
        # Setting and user-defined window title
        if self.getOption('title') is not None:
            self.widget.setWindowTitle(self.getOption('title'))
        else:
            self.widget.setWindowTitle(self.label)

        layout.addRow(QLabel(self.helpString))
        for child in self._children:
            if child.hasChildren is False:
                try:
                    if child.dataType == BOOL:
                        child.widget = QCheckBox(child.name)

                        def updateData(val=0, sibling=child,
                                       sibling_widget=child.widget):
                            sibling.data = val
                            # print('[',sibling.name,', ' , sibling.data, ']')
                        child.widget.stateChanged.connect(updateData)

                    if child.dataType == CHOICE:
                        child.widget = QComboBox()
                        for item in child.getOption('choices'):
                            child.widget.addItem(item)

                        def updateData(val=0, sibling=child,
                                       sibling_widget=child.widget):
                            sibling.data = val
                            # print('[',sibling.name,', ' , sibling.data, ']')
                        child.widget.currentIndexChanged.connect(updateData)

                    if child.dataType == MULTIPLE_CHOICE:
                        pass

                    if child.dataType == INT:
                        child.widget = QSpinBox()

                        def updateData(val=0, sibling=child,
                                       sibling_widget=child.widget):
                            sibling.data = val
                            # print('[',sibling.name,', ' , sibling.data, ']')
                        child.widget.valueChanged.connect(updateData)

                    if child.dataType == FLOAT:
                        child.widget = QDoubleSpinBox()
                        child.widget.setSingleStep(0.1)

                        def updateData(val=0, sibling=child,
                                       sibling_widget=child.widget):
                            sibling.data = val
                            # print('[',sibling.name,', ' , sibling.data, ']')
                        child.widget.valueChanged.connect(updateData)

                    if child.dataType == STRING:
                        child.widget = QLineEdit(child.name)

                        def updateData(val=0, sibling=child,
                                       sibling_widget=child.widget):
                            sibling.data = val
                            # print('[',sibling.name,', ' , sibling.data, ']')
                        child.widget.textChanged.connect(updateData)

                    if child.dataType == TEXT:
                        child.widget = QTextEdit(child.name)

                        def updateData(val=0, sibling=child,
                                       sibling_widget=child.widget):
                            sibling.data = sibling_widget.toPlainText()
                            # print('[',sibling.name,', ' , sibling.data, ']')
                        child.widget.textChanged.connect(updateData)

                    self.refreshUIvalue(child.name)
                    child.widget.setToolTip(child.helpString)
                    label = QLabel(child.label)
                    label.setToolTip(child.helpString)
                    layout.addRow(label, child.widget)
                except:
                    pass
            else:
                child.buildUI()
                layout.addRow(child.widget)

    def refreshUIvalue(self, childName=None):
        childList = []
        if childName is None:
            childList = self.getDataChildren()
        else:
            childList = [self.findChild(childName)]
        for child in [self._children[i] for i in childList]:
            if child.dataType == BOOL:
                child.widget.setChecked(child.data)

            if child.dataType == CHOICE:
                child.widget.setCurrentIndex(child.data)

            if child.dataType == MULTIPLE_CHOICE:
                pass

            if child.dataType in (INT, FLOAT):
                child.widget.setValue(child.data)

            if child.dataType in (STRING, TEXT):
                child.widget.setText(child.data)


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)

    a = dataObject(True, name='var1', label='Bool', helpString='Bool help')
    a2 = dataObject(True, name='vara2', label='Bool', helpString='Bool help')
    choices_list = ['Red pill', 'Blue pill', 'No pills']
    b = dataObject(1, name='var2', label='choice', helpString='choice help', choices=choices_list)
    c = dataObject(3, name='var3', label='int', helpString='interim')
    d = dataObject(2.7192, name='var4', label='float', helpString='flota')
    e = dataObject("content", name='var5', label='Line edit', helpString='line help')
    f = dataObject("Text content", name='var6', label='Text edit', helpString='text help', isText=True)

    g = UIBuilder(name='g', children=[a, a2, b, c, d, e, f],
                  label='Testing the WORLD-FAMOUS autogui',
                  title='This is the window title',
                  helpString='This is an example of what can be done...')

    g.buildUI()

    g.widget.show()
    print(g.getChildData('var1'))
    g.setChildData('var1', False)

    print(g.getChildrenNames(), g.getChildrenData())

    sys.exit(app.exec_())
    