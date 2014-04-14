from UserDict import DictMixin
from PySide.QtCore import QAbstractTableModel, Qt
from persistent.mapping import PersistentMapping


class DictModel(QAbstractTableModel):
    def __init__(self, internal_container=None, parent=None):
        QAbstractTableModel.__init__(self, parent)
        # Set default internal container
        self._header_display = ("Key", "Value")
        if internal_container:
            self._internal_container = PersistentMapping()
        else:
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
        return 2


    def data(self, model_index, role):
        if role in [Qt.DisplayRole, Qt.EditRole]:
            if model_index.column() == 0:
                keys = self._internal_container.keys()
                return keys[model_index.row()]
            elif model_index.column() == 1:
                values = self._internal_container.values()
                return values[model_index.row()]
        else:
            return None


    def headerData(self, column, orientation, role=None):
        if role == Qt.DisplayRole and orientation == Qt.Horizontal:
            return self._header_display[column]
        else:
            return None
