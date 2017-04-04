from qtodb.database_model.abstract_object_database_model import AbstractObjectModel


class ObjectListModel(AbstractObjectModel):

    def _appendToInternalContainer(self, item):
        self._internal_container.append(item)


    def _removeFromInternalContainer(self, index):
        self._internal_container.pop(index)


    def __getitem__(self, index):
        return self._internal_container[index]


    def objectIndex(self, instance):
        return self._internal_container.index(instance)