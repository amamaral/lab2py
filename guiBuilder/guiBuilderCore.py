# -*- coding: utf-8 -*-
"""
Created on Tue Apr  7 23:57:30 2015

@author: amamaral
"""

from lab2py.guiBuilder.guiBuilderConstants import *


class dataObject(object):
    """dataObject():
    This class contains the relevant characteristics of the data used for
    creating the GUI's. It is a low-level abstraction used for all data types.
    """
    def __init__(self, data=None, dataType=None, name=None, label=None,
                 unit=None, scale=None, helpString=None, default=None,
                 parent=None, widget=None, **kwargs):
        self._name = name  # 'Variable' like name for data
        self._label = label  # Descriptive string for identifying data.
        self._unit = unit  # Unit used for data
        self._scale = scale  # Scale used for data, given self.unit
        self._helpString = helpString  # Further info about data.
        self._default = default  # Store any default value that data might have
        self._parent = parent  # data might be part of a set of parameters
        self.widget = widget  # Stores the widget
        self._readed = False  # Flag to indicate a reading of data
        self._written = False  # Flag to indicate the writing on data
        self._extra_options = kwargs  # Extra options for later specific usage

        self.hasChildren = False  # By design, dataObject has no childs

        self.setData(data, ui_updating=False)  # Adjust the initial the data
        if dataType is not None:
            if dataType not in AvailableDataTypes:
                raise TypeError(dataType, ' is not a valid dataType')
            self.dataType = dataType
        else:
            self.identifyDataType()

    def getData(self, ui_updating=False):
        if not ui_updating:
            self._readed = True
        return self._data

    def setData(self, value, ui_updating=False):
        if not ui_updating:
            self._written = False
        self._data = value

    def delData(self):
        del(self._data)

    data = property(getData, setData,
                    delData, "This contains the data of the widget.")

    def identifyDataType(self):
        data_type = type(self.data)
        if data_type == bool:
            self.dataType = BOOL
        if data_type == int:
            if self.getOption('choices') is not None:
                self.dataType = CHOICE
            else:
                self.dataType = INT
        if data_type == float:
            self.dataType = FLOAT
        if data_type == str:
            isText = self.getOption('isText')
            if isText is True:
                self.dataType = TEXT
            else:
                self.dataType = STRING
        if data_type == list:
            self.dataType = CHOICE
            self.setOption('choices', self.data)
            self.data = 0
        return self.dataType

    def getName(self):
        return self._name

    def setName(self, name):
        self._name = name

    name = property(getName, setName,
                    doc="a 'variable-like' name for data.")

    def getLabel(self):
        return self._label

    def setLabel(self, label):
        self._label = label

    label = property(getLabel, setLabel,
                     doc="A descriptive string for identifying data.")

    def getUnit(self):
        return self._unit

    def setUnit(self, unit):
        self._unit = unit

    unit = property(getUnit, setUnit,
                    doc="The units used for data.")

    def getScale(self):
        return self._scale

    def setScale(self, scale):
        self._scale = scale

    scale = property(getScale, setScale,
                     doc="The scale factor used for data.")

    def getHelp(self):
        return self._helpString

    def setHelp(self, helpString):
        self._helpString = helpString

    helpString = property(getHelp, setHelp,
                          doc="A help string for data")

    def isDefaultValue(self):
        "setToDefaultValue(): Returns true if data has the default value."
        return self._data == self._default

    def setToDefaultValue(self):
        "setToDefaultValue(): Sets data to its default value."
        self._data = self._default

    def setDefaultValue(self, value):
        "setDefaultValue(value): Sets a new default value for data."
        self._default = value

    def getParent(self):
        return self._parent

    def setParent(self, parent):
        self._parent = parent

    parent = property(getParent, setParent,
                      doc="This contains the link to data's parent")

    def getWidget(self):
        return self._widget

    def setWidget(self, widget):
        self._widget = widget

    def delWidget(self):
        del(self._widget)

    widget = property(getWidget, setWidget, delWidget,
                      doc="This contains the link to data's widget")

    def dataReaded(self):
        "dataReaded(): Returns true if data was read since the last call."
        if self._readed:
            self._readed = False
            return True
        else:
            return False

    def dataWritten(self):
        "dataWritten(): Returns True if data was written since the last call."
        if self._written:
            self._written = False
            return True
        else:
            return False

    def setOption(self, option, value):
        "setOption(option, value): Adjust extra options for data"
        self._extra_options[option] = value

    def getOption(self, option):
        "getOption(option): Returns the current value for option, or None"
        try:
            return self._extra_options[option]
        except:
            return None


class dataGroup(object):
    """dataGroup():
    This class contains dataObjects or dataGroups as childs. It organizes their
    appeareance on the screen and in memory. Similarly to dataObject, dataGroup
    is a low-level abstraction.
    """
    def __init__(self, name=None, label=None, children=[], helpString=None,
                 parent=None, widget=None, **kwargs):
        self.name = name  # 'Variable' like name for the group
        self.label = label  # Descriptive string for identifying the group
        self._children = []  # The group's children
        self.hasChildren = False  # This becomes true after adding a child
        for child in children:
            self.addChild(child)
        self.helpString = helpString  # Further info about data.
        self.parent = parent  # data might be part of a set of parameters
        self.widget = widget  # The widget associated with data
        self._extra_options = kwargs  # Extra options for later specific usage

    def getName(self):
        return self._name

    def setName(self, name):
        self._name = name

    name = property(getName, setName,
                    doc="a 'variable-like' name for data.")

    def getLabel(self):
        return self._label

    def setLabel(self, label):
        self._label = label

    label = property(getLabel, setLabel,
                     doc="A descriptive string for identifying data.")

    def getDataChildren(self):
        """getDataChildren(self): Returns a list containing the indices of the
        current group's children which are dataObjects. This is useful to
        simplify the collective assignment of attributes.
        """
        child_index = []
        for i, child in enumerate(self._children):
            if type(child) == dataObject:
                if child.dataType >= 0:
                    child_index.append(i)
        return child_index

    def getChildrenAttribute(self, attrib):
        """getChildrenAttribute(attrib): Returns a (nonrecursive) list of the
        group's dataObject-like children atribute attrib"""
        return [getattr(self._children[child_index], attrib)
                for child_index in self.getDataChildren()]

    def setChildrenAttribute(self, attrib, values):
        """setChildrenAttribute(attrib, values): Sets (nonrecursively) the
        group's dataObject-like children atribute 'attrib' to values. The
        values  must be ordered according to the group's dataObjects."""
        dataChildren = self.getDataChildren()
        for i in range(min([len(values), len(dataChildren)])):
            try:
                setattr(self._children[dataChildren[i]], attrib, values[i])
            except:
                pass

    def getChildrenNames(self):
        """getChildrenNames(): Returns a (nonrecursive) list of the group's
        children names"""
        return self.getChildrenAttribute('name')

    def getChildrenData(self):
        """getChildrenData(): Returns a (nonrecursive) list of the group's
        children data. """
        return self.getChildrenAttribute('data')

    def setChildrenData(self, values):
        """setChildrenData(): Sets (nonrecursive) the group's children data."""
        return self.setChildrenAttribute('data', values)

    def findChild(self, childName):
        """findChild(childName): Returns the index of 'childName'. """
        for i, child in enumerate(self._children):
            if child.name == childName:
                return i
        return None

    def getChildAttribute(self, childName, attrib):
        """getChildAttribute(childName, attrib): Returns the 'attrib' of
        'childName'.
        return child.attrib"""
        child_index = self.findChild(childName)
        if child_index is not None:
            return getattr(self._children[child_index], attrib)
        else:
            return None

    def setChildAttribute(self, childName, attrib, value):
        """setChildAttribute(childName, attrib, value): Sets the 'attrib' in
        'childName' as value.
        child.attrib = value"""
        child_index = self.findChild(childName)
        if child_index is not None:
            setattr(self._children[child_index], attrib, value)
        else:
            pass

    def getChildOption(self, childName, option):
        """getChildAttribute(childName, option): Returns the 'option' of
        'childName'.
        return child.getOption(option)"""
        child_index = self.findChild(childName)
        if child_index is not None:
            return self._children[child_index].getOption(option)

    def setChildOption(self, childName, option, value):
        """setChildOption(childName, option, value): Sets the 'option' in
        'childName' as value.
        child.setOption(value)"""
        child_index = self.findChild(childName)
        if child_index is not None:
            self._children[child_index].setOption(option, value)

    def getChildData(self, childName):
        """getChildData(childName): Returns the data stored by 'childName'. """
        return self.getChildAttribute(childName, 'data')

    def setChildData(self, childName, data):
        """getChildData(childName): Sets the data stored by 'childName'. """
        self.setChildAttribute(childName, 'data', data)
        self.refreshUIvalue(childName)

    def getChildrenNamesTree(self):
        """getChildrenTreeList(self): Returns a (recursive) list of the group's
        children"""
        namesTree = []
        for child in self._children:
            if child.hasChildren is False:
                namesTree.append(child.name)
            else:
                namesTree.append(child.getChildrenNamesTree())
        return namesTree

    def addChild(self, child):
        """addChild(self, child):
        Adds child to the group
        """
        if(child.name not in self.getChildrenNames()):
            self.hasChildren = True
            self._children.append(child)
            self._children[-1].setParent(self)
        else:
            raise ValueError("The child ", child.name, " already exists.")

    def removeChild(self, childName):
        """removeChild(childName):
        Removes the child 'childName' from the group
        """
        if(childName in self.getChildrenNames()):
            for i, name in enumerate(self.getChildrenNames()):
                if name == childName:
                    del(self._children[i])
        else:
            raise ValueError("The child ", childName, " do not exist.")

    def getChild(self, childName):
        """getChild(childName):
        Returns the child 'childName'.
        """
        if(childName in self.getChildrenNames()):
            for i, name in enumerate(self.getChildrenNames()):
                if name == childName:
                    return self._children[i]
        else:
            raise ValueError("The child ", childName, " do not exist.")
            return None

    def getHelp(self):
        return self._helpString

    def setHelp(self, helpString):
        self._helpString = helpString

    helpString = property(getHelp, setHelp,
                          doc="A help string for data")

    def getParent(self):
        return self._parent

    def setParent(self, parent):
        self._parent = parent

    parent = property(getParent, setParent,
                      doc="This contains the link to data's parent")

    def getWidget(self):
        return self._widget

    def setWidget(self, widget):
        self._widget = widget

    def delWidget(self):
        del(self._widget)

    widget = property(getWidget, setWidget,
                      delWidget, "The widget associated with the group.")

    def buildUI(self):
        """
        buildUI():
        This is just the prototype function for UI creation. This must be
        overwritten by each platform-specific class.
        """
        pass

    def refreshUIvalue(self, childName=None):
        """
        refreshUIvalue(childName):
        This is just the prototype function for refreshing child data displayed
        in the UI. If childName = None, all child widgets must be updated.
        This must be overwritten by each platform-specific class.
        """
        pass

    def setOption(self, option, value):
        "setOption(option, value): Adjust extra options for data"
        self._extra_options[option] = value

    def getOption(self, option):
        "getOption(option): Returns the current value for option, or None"
        try:
            return self._extra_options[option]
        except:
            return None