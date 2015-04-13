# -*- coding: utf-8 -*-
"""
Created on Sun Apr 12 13:24:38 2015

@author: amamaral
"""

from lab2py.guiBuilder.fastForm import fastForm

import sys
from PyQt4.Qt import QApplication
app = QApplication(sys.argv)

fields = [('First name', 'John'),
          ('Last name', 'Smith'),
          ('Age', 42),
          ('Money', 100.03),
          ('Preferred food', ['Sandwich', 'Lobster', 'Lobster sandwich'])]

out = fastForm(fields, 'fastForm example', 'This is an example')
print(out)