from UserDict import DictMixin
from PySide.QtCore import QAbstractTableModel, Qt
from persistent.mapping import PersistentMapping


class DictModel(QAbstractTableModel):
    def __init__(self, internal_container=PersistentMapping, parent=None):
        QAbstractTableModel.__init__(self, parent)
        self._internal_container = internal_container


    def __getitem__(self, key):
        return self._internal_container[key]


    def __setitem__(self, key, value):
        self._internal_container[key] = value


    def __delitem__(self, key):
        del self._internal_container[key]


    def rowCount(self, QModelIndex_parent=None, *args, **kwargs):
        return len(self._internal_container)


    def columnCount(self, QModelIndex_parent=None, *args, **kwargs):
        return len(2)


    def data(self, model_index, role):
        if role in [Qt.DisplayRole, Qt.EditRole]:
            if model_index.column() == 0:
                keys = self._internal_container.keys()
                return keys[model_index.row()]
            elif model_index.column() == 1:
                return self._internal_container[model_index.row()]
        else:
            return super(QAbstractTableModel, self).data(model_index, role)


    def headerData(self, column, orientation, role=None):
        if role == Qt.DisplayRole and orientation == Qt.Horizontal:
            return self._object_attributes[column][1]
        else:
            return super(QAbstractTableModel, self).headerData(column, orientation, role)
