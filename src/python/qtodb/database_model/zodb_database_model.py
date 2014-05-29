from qtodb.database_model.abstract_object_database_model import AbstractObjectModel
from qtodb.database_model.transaction_context_manager import TransactionContextManager


class ZodbDatabaseModel(AbstractObjectModel, TransactionContextManager):

    def __init__(self, internal_container, parent=None):
        super(ZodbDatabaseModel, self).__init__(internal_container, parent)
        self._key_attribute = None
        self._current_transaction = None


    def setKeyAttribute(self, attribute_name):
        """
        Set an object attribute to be used as model key

        :param str attribute_name: the object attribute name
        """
        self._key_attribute = attribute_name


    def _appendToInternalContainer(self, item):
        self._assertOpenTransaction()
        assert self._key_attribute is not None, \
            "set an attribute to be used as key with {0}".format(self.setKeyAttribute.func_name)
        #TODO: Store a container counter somewhere in the Database?
        if len(self._internal_container):
            key = self._internal_container.keys()[-1] + 1
        else:
            key = 1
        setattr(item, self._key_attribute, key)
        self._internal_container[key] = item


    def _removeFromInternalContainer(self, index):
        self._assertOpenTransaction()
        assert self._key_attribute is not None,\
            "set an attribute to be used as key with {0}".format(self.setKeyAttribute.func_name)
        instance = self[index]
        key = getattr(instance, self._key_attribute)
        del self._internal_container[key]


    def values(self):
        return self._internal_container.values()


    def __getitem__(self, index):
        return self.values()[index]


    def objectIndex(self, instance):
        for index, item in enumerate(self._internal_container.itervalues()):
            if item.uid == instance.uid:
                return index
        else:
            raise ValueError("{0} is not in the model".format(instance))


    def getObjectByKey(self, key):
        return self._internal_container[key]
