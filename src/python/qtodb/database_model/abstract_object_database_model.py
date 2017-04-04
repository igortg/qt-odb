from collections import namedtuple

from PyQt4 import QtCore
from PyQt4.QtCore import QAbstractTableModel, Qt, QModelIndex

from qtodb.decorators import not_implemented


AttributeDisplay = namedtuple("AttributeDisplay", ["attr_name", "header_caption", "format"])


class AbstractObjectModel(QAbstractTableModel):


    def __init__(self, internal_container, parent=None):
        QAbstractTableModel.__init__(self, parent)
        self._internal_container = internal_container
        self._object_attributes = []


    def addAttributeColumn(self, attr_name, header_caption, format_str=None):
        object_display = AttributeDisplay(attr_name, header_caption, format_str)
        self._object_attributes.append(object_display)


    def setInternalContainer(self, internal_container):
        self._internal_container = internal_container
        self.reset()


    @not_implemented
    def _appendToInternalContainer(self, item):
        pass


    @not_implemented
    def _removeFromInternalContainer(self, index):
        pass


    @not_implemented
    def __getitem__(self, index):
        pass


    @not_implemented
    def objectIndex(self, instance):
        pass


    def appendObject(self, instance):
        objects_count = len(self._internal_container)
        self.beginInsertRows(QModelIndex(), objects_count, objects_count)
        self._appendToInternalContainer(instance)
        self.endInsertRows()


    def removeObject(self, index):
        self.beginRemoveRows(QModelIndex(), index, index)
        self._removeFromInternalContainer(index)
        self.endRemoveRows()


    def rowCount(self, QModelIndex_parent=None, *args, **kwargs):
        return len(self._internal_container)


    def columnCount(self, QModelIndex_parent=None, *args, **kwargs):
        return len(self._object_attributes)


    def data(self, model_index, role):
        if role in [Qt.DisplayRole, Qt.EditRole]:
            object_display = self._object_attributes[model_index.column()]
            instance = self[model_index.row()]
            if hasattr(instance, object_display.attr_name):
                value = getattr(instance, object_display.attr_name)
            else:
                value = "<N/A>"
            if object_display.format:
                return object_display.format(value)
            elif isinstance(value, str):
                return value
            else:
                return str(value)
        else:
            return None


    def headerData(self, column, orientation, role=None):
        if role == Qt.DisplayRole and orientation == Qt.Horizontal:
            return self._object_attributes[column][1]
        else:
            return super(AbstractObjectModel, self).headerData(column, orientation, role)


    def updateDisplay(self, index):
        sig = QtCore.SIGNAL("dataChanged(const QModelIndex&, const QModelIndex&)")
        self.emit(sig, self.index(index, 0), self.index(index, self.columnCount()))


    def __iter__(self):
        return iter(self._internal_container)
