from PyQt4.QtCore import QAbstractTableModel, Qt


class DictModel(QAbstractTableModel):


    def __init__(self, internal_container=None, parent=None):
        QAbstractTableModel.__init__(self, parent)
        # Set default internal container
        self._header_display = ("Key", "Value")
        if internal_container is not None:
            self._internal_container = internal_container
        else:
            self._internal_container = {}


    def setHeader(self, header_list):
        """
        Set the header labels.

        :param list header_list: list of strings
        """
        self._header_display = header_list


    def __getitem__(self, key):
        return self._internal_container[key]


    def __setitem__(self, key, value):
        self._assertOpenTransaction()
        self._internal_container[key] = value


    def __delitem__(self, key):
        self._assertOpenTransaction()
        del self._internal_container[key]


    def rowCount(self, QModelIndex_parent=None, *args, **kwargs):
        return len(self._internal_container)


    def columnCount(self, QModelIndex_parent=None, *args, **kwargs):
        return 2


    def keys(self):
        return sorted(self._internal_container.keys())


    def data(self, model_index, role=None):
        if role in [Qt.DisplayRole, Qt.EditRole]:
            key = self.keys()[model_index.row()]
            if model_index.column() == 0:
                return key
            elif model_index.column() == 1:
                return self[key]
        else:
            return None


    def headerData(self, column, orientation, role=None):
        if role == Qt.DisplayRole and orientation == Qt.Horizontal:
            return self._header_display[column]
        else:
            return None


    def __contains__(self, item):
        return item in self._internal_container