from qtodb.database_model.abstract_object_database_model import AbstractObjectModel


class ObjectListModel(AbstractObjectModel):

    def __init__(self, internal_container, parent=None):
        AbstractObjectModel.__init__(self, parent)
        self._internal_container = internal_container

    def setInternalContainer(self, internal_container):
        self.beginResetModel()
        self._internal_container = internal_container
        self.endResetModel()


    def _appendToInternalContainer(self, item):
        self._internal_container.append(item)


    def _removeFromInternalContainer(self, index):
        self._internal_container.pop(index)


    def __getitem__(self, index):
        return self._internal_container[index]


    def objectIndex(self, instance):
        return self._internal_container.index(instance)

    def rowCount(self, QModelIndex_parent=None, *args, **kwargs):
        return len(self._internal_container)
