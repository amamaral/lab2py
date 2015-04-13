# -*- coding: utf-8 -*-
"""guiBuilder
Created on Tue Apr  7 23:12:11 2015

@author: amamaral
"""
from sys import maxsize, float_info

from PyQt4.QtGui import QApplication, QWidget, QGroupBox, QFormLayout,\
    QLabel, QPushButton, QDialogButtonBox, QCheckBox, QComboBox, QSpinBox,\
    QDoubleSpinBox, QLineEdit, QTextEdit

from lab2py.guiBuilder.guiBuilderCore import dataObject, dataGroup
from lab2py.guiBuilder.guiBuilderConstants import *


class guiBuilder(dataGroup):
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
                    if child.dataType == BUTTON:
                        child.widget = QPushButton(child.name)
                        child.widget.setText(child.label)
                        child.widget.clicked.connect(
                            child.getOption('execute'))

                    if child.dataType == OK_CANCEL_BUTTONS:
                        child.widget = QDialogButtonBox()
                        child.widget.addButton(child.widget.Ok)
                        child.widget.addButton(child.widget.Cancel)

                        child.widget.accepted.connect(
                            child.getOption('execOk'))
                        child.widget.rejected.connect(
                            child.getOption('execCancel'))

                    if child.dataType == BOOL:
                        child.widget = QCheckBox(child.name)
                        child.widget.setText(child.label)
                        self.refreshUIvalue(child.name)

                        def updateData(val=0, sibling=child,
                                       sibling_widget=child.widget):
                            sibling.data = val
                            # print('[',sibling.name,', ' , sibling.data, ']')
                        child.widget.stateChanged.connect(updateData)
                        if child.getOption('execute') is not None:
                            child.widget.stateChanged.connect(
                                child.getOption('execute'))

                    if child.dataType == CHOICE:
                        child.widget = QComboBox()
                        for item in child.getOption('choices'):
                            child.widget.addItem(item)
                        self.refreshUIvalue(child.name)

                        def updateData(val=0, sibling=child,
                                       sibling_widget=child.widget):
                            sibling.data = val
                            # print('[',sibling.name,', ' , sibling.data, ']')
                        child.widget.currentIndexChanged.connect(updateData)
                        if child.getOption('execute') is not None:
                            child.widget.currentIndexChanged.connect(
                                child.getOption('execute'))

                    if child.dataType == MULTIPLE_CHOICE:
                        pass

                    if child.dataType == INT:
                        child.widget = QSpinBox()
                        if child.getOption('min') is not None:
                            child.widget.setMinimum(child.getOption('min'))
                        else:
                            child.widget.setMinimum(-1e10)
                        if child.getOption('max') is not None:
                            child.widget.setMaximum(child.getOption('max'))
                        else:
                            child.widget.setMaximum(1e10)
                        if child.getOption('step') is not None:
                            child.widget.setSingleStep(child.getOption('step'))
                        else:
                            child.widget.setSingleStep(1)
                        if child.unit is not None:
                            child.widget.setSuffix(child.unit)
                        self.refreshUIvalue(child.name)

                        def updateData(val=0, sibling=child,
                                       sibling_widget=child.widget):
                            sibling.data = val
                            # print('[',sibling.name,', ' , sibling.data, ']')
                        child.widget.valueChanged.connect(updateData)
                        if child.getOption('execute') is not None:
                            child.widget.valueChanged.connect(
                                child.getOption('execute'))

                    if child.dataType == FLOAT:
                        child.widget = QDoubleSpinBox()
                        if child.getOption('min') is not None:
                            child.widget.setMinimum(child.getOption('min'))
                        else:
                            child.widget.setMinimum(-float_info.max)
                        if child.getOption('max') is not None:
                            child.widget.setMaximum(child.getOption('max'))
                        else:
                            child.widget.setMaximum(float_info.max)
                        if child.getOption('step') is not None:
                            child.widget.setSingleStep(child.getOption('step'))
                        else:
                            child.widget.setSingleStep(0.1)
                        if child.getOption('decimals') is not None:
                            child.widget.setDecimals(
                                child.getOption('decimals'))
                        else:
                            child.widget.setDecimals(3)
                        if child.unit is not None:
                            child.widget.setSuffix(child.unit)
                        self.refreshUIvalue(child.name)

                        def updateData(val=0, sibling=child,
                                       sibling_widget=child.widget):
                            sibling.data = val
                            # print('[',sibling.name,', ' , sibling.data, ']')
                        child.widget.valueChanged.connect(updateData)
                        if child.getOption('execute') is not None:
                            child.widget.valueChanged.connect(
                                child.getOption('execute'))

                    if child.dataType == STRING:
                        child.widget = QLineEdit(child.name)
                        self.refreshUIvalue(child.name)

                        def updateData(val=0, sibling=child,
                                       sibling_widget=child.widget):
                            sibling.data = val
                            # print('[',sibling.name,', ' , sibling.data, ']')
                        child.widget.textChanged.connect(updateData)
                        if child.getOption('execute') is not None:
                            child.widget.textChanged.connect(
                                child.getOption('execute'))

                    if child.dataType == TEXT:
                        child.widget = QTextEdit(child.name)
                        self.refreshUIvalue(child.name)

                        def updateData(val=0, sibling=child,
                                       sibling_widget=child.widget):
                            sibling.data = sibling_widget.toPlainText()
                            # print('[',sibling.name,', ' , sibling.data, ']')
                        child.widget.textChanged.connect(updateData)
                        if child.getOption('execute') is not None:
                            child.widget.textChanged.connect(
                                child.getOption('execute'))

                    child.widget.setToolTip(child.helpString)
                    if child.dataType not in [BUTTON, OK_CANCEL_BUTTONS,
                                              YES_NO_CANCEL_BUTTONS, BOOL]:
                        label = QLabel(child.label)
                    else:
                        label = QLabel('')
                    label.setToolTip(child.helpString)
                    layout.addRow(label, child.widget)
                except Exception as e:
                    print("Error when building ", child.name)
                    print(e)
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
            if child.widget is not None:
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

    boolean_data = dataObject(True, name='boolean_data', label='Is it true?',
                              helpString='Bool help')

    choices_list = ['Red pill', 'Blue pill', 'No pills']
    choices_data = dataObject(1, name='choices_data', label='Choice',
                              helpString='choice help', choices=choices_list)

    integer_data = dataObject(3, min=-5, max=5, step=2, unit=' coins',
                              name='integer_data', label='Int',
                              helpString='integer help')

    float_data = dataObject(2.7192, min=-10, max=10, step=1e-4, decimals=4,
                            unit=' mV',
                            name='float_data', label='Float',
                            helpString='float help')

    line_data = dataObject("content", name='line_data', label='Line edit',
                           helpString='line help')

    text_data = dataObject("Text content", name='text_data', label='Text edit',
                           helpString='text help', isText=True)

    function = lambda: print('Example of button activation!')
    button1 = dataObject(dataType=BUTTON, name='button1',
                         label='Button example', execute=function)

    run = lambda: print('returned ok!')
    dontrun = lambda: print('returned cancel!')
    ok_cancel_button = dataObject(dataType=OK_CANCEL_BUTTONS, name='ok_cancel',
                                  execOk=run, execCancel=dontrun)

    children_list = [boolean_data, choices_data, integer_data, float_data,
                     line_data, text_data, button1, ok_cancel_button]
    g = guiBuilder(name='group', children=children_list, parent=0,
                   label='The internal title',
                   title='This is the window title',
                   helpString='An descriptive text for these parameters')

    def bool_exec():
        print('Bool data: ', g.getChildData('boolean_data'))
        print('Float data: ', g.getChildData('float_data'))
    g.setChildOption('boolean_data', 'execute', bool_exec)
    print(g.getChildOption('boolean_data', 'execute'))

    g.buildUI()

    g.widget.show()

    g.setChildData('boolean_data', False)
    print(g.getChildData('boolean_data'))

    print(g.getChildrenNames(), g.getChildrenData())

    sys.exit(app.exec_())
