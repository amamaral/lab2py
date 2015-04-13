# -*- coding: utf-8 -*-
"""Another low-level implementation of guiBuilder

This differs from the example 1 by the method in which the data fields are
added, which might be more suitable for a dynamic UI

Here the dataObjects are used directly. Examples of many features are shown,
as for example the execution of a function upon a button click or when some
data is updated (here when boolean_data changes).

This low-level implementation allows an easy implementation of more common
features, as creating a window to exhibith/edit the data, and also allows
a direct interface to PyQt widgets, by calling
g.getChildAttribute(childName, 'widget')

Created on Sun Apr 12 11:33:51 2015

@author: amamaral
"""
from PyQt4.QtGui import QApplication

from lab2py.guiBuilder.guiBuilder import guiBuilder
from lab2py.guiBuilder.guiBuilderCore import dataObject
from lab2py.guiBuilder.guiBuilderConstants import BUTTON, OK_CANCEL_BUTTONS

import sys

app = QApplication(sys.argv)

g = guiBuilder(name='group', parent=0,
               label='The internal title',  # only appears if parent != None
               title='Low-level implementation 1',
               helpString='An descriptive text for these parameters')


def bool_exec():
    print('Bool data: ', g.getChildData('boolean_data'))
    print('Float data: ', g.getChildData('float_data'))

# A True/False field, which calls bool_exec() when the field changes.
# Initial value: True.
boolean_data = dataObject(True, name='boolean_data', label='Is it true?',
                          helpString='Bool help', execute=bool_exec)
g.addChild(boolean_data)

# Choose options within a list. Initial value: 1 ('Blue pill')
choices_list = ['Red pill', 'Blue pill', 'No pills']
choices_data = dataObject(1, name='choices_data', label='Choice',
                          helpString='choice help', choices=choices_list)
g.addChild(choices_data)

# An integer field. Initial value: 3
integer_data = dataObject(3, min=-5, max=5, step=2, unit=' coins',
                          name='integer_data', label='Int',
                          helpString='integer help')
g.addChild(integer_data)

# A float field. Initial value: 2.7192
float_data = dataObject(2.7192, min=-10, max=10, step=1e-4, decimals=4,
                        unit=' mV',
                        name='float_data', label='Float',
                        helpString='float help')
g.addChild(float_data)

# A string field. Initial value: "content"
line_data = dataObject("content", name='line_data', label='Line edit',
                       helpString='line help')
g.addChild(line_data)

# A string field. Initial value: "Text content"
text_data = dataObject("Text content", name='text_data', label='Text edit',
                       helpString='text help', isText=True)
g.addChild(text_data)

# An executable button example. function() is called when button1 is clicked
function = lambda: print('Example of button activation!')
button1 = dataObject(dataType=BUTTON, name='button1',
                     label='Button example', execute=function)
g.addChild(button1)

# An example of Ok Cancel buttons. Similar to a button as described above
run = lambda: print('returned ok!')
dontrun = lambda: print('returned cancel!')
ok_cancel_button = dataObject(dataType=OK_CANCEL_BUTTONS, name='ok_cancel',
                              execOK=run, execCancel=dontrun)
g.addChild(ok_cancel_button)

# An example on how to externally change the data. Notice that bool_exec() is
# called.
g.setChildData('boolean_data', False)

# Printing the names of all fields and their respective data.
print(g.getChildrenNames())
print(g.getChildrenData())

# This must be called only after the interface is all set.
g.buildUI()
g.widget.show()

sys.exit(app.exec_())
