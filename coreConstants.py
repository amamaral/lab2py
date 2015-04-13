# -*- coding: utf-8 -*-
"""
Created on Tue Apr  7 23:57:30 2015

@author: anderson
"""

# Defines the currently available data objects
# Negative values represent non-data GUI features

SEPARATOR = -1
BUTTON = -2
OK_CANCEL_BUTTONS = -3
YES_NO_CANCEL_BUTTONS = -4

BOOL = 0
CHOICE = 1
MULTIPLE_CHOICE = 2

INT = 20
FLOAT = 21

STRING = 40
TEXT = 41

AvailableDataTypes = [SEPARATOR,
                      BUTTON,
                      OK_CANCEL_BUTTONS,
                      YES_NO_CANCEL_BUTTONS,
                      BOOL,
                      CHOICE,
                      MULTIPLE_CHOICE,
                      INT,
                      FLOAT,
                      STRING,
                      TEXT]
