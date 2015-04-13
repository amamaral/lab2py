# -*- coding: utf-8 -*-
"""A low-level implementation of guiBuilder

Here the dataObjects are used directly. Examples of many features are shown,
as for example the execution of a function upon a button click or when some
data is updated (here when boolean_data changes).

This low-level implementation allows an easy implementation of more common
features, as creating a window to exhibith/edit the data, and also allows
a direct interface to PyQt widgets, by calling
g.getChildAttribute(childName, 'widget')

Created on Sun Apr 12 09:30:03 2015

@author: amamaral
"""
from PyQt4.QtGui import QApplication

from lab2py.guiBuilder.guiBuilder import guiBuilder
from lab2py.guiBuilder.guiBuilderCore import dataObject
from lab2py.guiBuilder.guiBuilderConstants import BUTTON, OK_CANCEL_BUTTONS

import sys

app = QApplication(sys.argv)

# A True/False field. Initial value: True
boolean_data = dataObject(True, name='boolean_data', label='Is it true?',
                          helpString='Bool help')

# Choose options within a list. Initial value: 1 ('Blue pill')
choices_list = ['Red pill', 'Blue pill', 'No pills']
choices_data = dataObject(1, name='choices_data', label='Choice',
                          helpString='choice help', choices=choices_list)

# An integer field. Initial value: 3
integer_data = dataObject(3, min=-5, max=5, step=2, unit=' coins',
                          name='integer_data', label='Int',
                          helpString='integer help')

# A float field. Initial value: 2.7192
float_data = dataObject(2.7192, min=-10, max=10, step=1e-4, decimals=4,
                        unit=' mV',
                        name='float_data', label='Float',
                        helpString='float help')

# A string field. Initial value: "content"
line_data = dataObject("content", name='line_data', label='Line edit',
                       helpString='line help')

# A string field. Initial value: "Text content"
text_data = dataObject("Text content", name='text_data', label='Text edit',
                       helpString='text help', isText=True)

# An executable button example. function() is called when button1 is clicked
# COMMENT: If the user wants to manipulate the user-editable data, it is
# necessary to declare the function after the group. See bool_exec() below
function = lambda: print('Example of button activation!')
button1 = dataObject(dataType=BUTTON, name='button1',
                     label='Button example', execute=function)

# An example of Ok Cancel buttons. Similar to a button as described above
run = lambda: print('returned ok!')
dontrun = lambda: print('returned cancel!')
ok_cancel_button = dataObject(dataType=OK_CANCEL_BUTTONS, name='ok_cancel',
                              execOK=run, execCancel=dontrun)

# children list contains the dataObjects to be added, and in the correct order
# of appeareance.
children_list = [boolean_data, choices_data, integer_data, float_data,
                 line_data, text_data, button1, ok_cancel_button]
g = guiBuilder(name='group', children=children_list, parent=0,
               label='The internal title',  # only appears if parent != None
               title='Low-level implementation 1',
               helpString='An descriptive text for these parameters')

# An example of a function call when the widget data is changed at interface.
# When bool_data is changed, bool_exec is called.


def bool_exec():
    print('Bool data: ', g.getChildData('boolean_data'))
    print('Float data: ', g.getChildData('float_data'))
g.setChildOption('boolean_data', 'execute', bool_exec)

# This must be called only after the interface is all set.
g.buildUI()
g.widget.show()

# An example on how to externally change the data. Notice that bool_exec() is
# called.
g.setChildData('boolean_data', False)

# Printing the names of all fields and their respective data.
print(g.getChildrenNames())
print(g.getChildrenData())

sys.exit(app.exec_())
