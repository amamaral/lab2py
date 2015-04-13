# -*- coding: utf-8 -*-
"""fastForm
Created on Sun Apr 12 13:26:03 2015

@author: amamaral
"""

from PyQt4.Qt import QDialog
from lab2py.guiBuilder.guiBuilder import guiBuilder
from lab2py.guiBuilder.guiBuilderCore import dataObject,\
    BUTTON, OK_CANCEL_BUTTONS


def fastForm(fields, title='', helpString='', okcancel=False):
    group = guiBuilder(name='g', title=title, label=title,
                       helpString=helpString, widget=QDialog())
    for i, field in enumerate(fields):
        UIfield = dataObject(field[1], label=field[0], name=('var'+str(i)))
        group.addChild(UIfield)

    if okcancel is True:
        def retOk():
            group.widget.close()
            group.setOption('state', True)

        def retCancel():
            group.widget.close()
            group.setOption('state', False)
        buttons = dataObject(dataType=OK_CANCEL_BUTTONS, name='button',
                             label='Ok', execOk=retOk, execCancel=retCancel)
        group.addChild(buttons)
    else:
        function = lambda: group.widget.close()
        button = dataObject(dataType=BUTTON, name='button',
                            label='Ok', execute=function)
        group.addChild(button)

    group.buildUI()
    group.widget.show()
    group.widget.exec()
    if group.getOption('state') is not None:
        return group.getOption('state'), group.getChildrenData()
    else:
        return group.getChildrenData()

if __name__ == '__main__':
    import sys
    from PyQt4.Qt import QApplication
    app = QApplication(sys.argv)

    fields = [('First name', 'John'),
              ('Last name', 'Smith'),
              ('Age', 42),
              ('Money', 100.03),
              ('Preferred food', ['Sandwich', 'Lobster', 'Lobster sandwich'])]

    print(fastForm(fields, 'fastForm example', 'This is an example',
                   okcancel=True))
