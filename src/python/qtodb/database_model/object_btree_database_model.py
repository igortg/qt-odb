from contextlib import contextmanager
import transaction
from qtodb.database_model.abstract_object_database_model import AbstractObjectDatabaseModel



class ObjectBTreeDatabaseModel(AbstractObjectDatabaseModel):

    def __init__(self, internal_container, object_factory, parent=None):
        super(ObjectBTreeDatabaseModel, self).__init__(internal_container, object_factory, parent)
        self._key_attribute = None
        if len(internal_container):
            self._item_counter = max(internal_container.keys())
        else:
            self._item_counter = 0


    def setKeyAttribute(self, attribute_name):
        """
        Set an object attribute to be used as model key

        :param str attribute_name: the object attribute name
        """
        self._key_attribute = attribute_name


    def _appendToInternalContainer(self, item):
        assert self._key_attribute is not None, \
            "set an attribute to be used as key with {0}".format(self.setKeyAttribute.func_name)
        self._item_counter += 1
        key = self._item_counter
        setattr(item, self._key_attribute, key)
        self._internal_container[key] = item


    def _removeFromInternalContainer(self, index):
        assert self._key_attribute is not None,\
            "set an attribute to be used as key with {0}".format(self.setKeyAttribute.func_name)
        instance = self[index]
        key = getattr(instance, self._key_attribute)
        del self._internal_container[key]


    def __getitem__(self, index):
        values = self._internal_container.values()
        return values[index]


    def getObjectByKey(self, key):
        return self._internal_container[key]


    @contextmanager
    def openTransaction(self, resetModel=True):
        """
        Context manager to update the Model. Responsable for set the dirty bit on the internal container and
        commit or abort the transaction.

        with model.openTransaction():
            instance = model[0]
            ... modify instance ...

        If you want to abort the transaction inside this context, raise TransactionAbort exception (transaction
        object doesn't have an "Aborted" state, so transaction.abort() souldn't be used
        """
        trans = transaction.get()
        try:
            yield trans
        except TransactionAbort:
            trans.abort()
        except:
            trans.abort()
            raise
        else:
            self._internal_container._p_changed = True
            if resetModel:
                self.reset()
            trans.commit()


    @contextmanager
    def getForEdition(self, index):
        """
        Context manager to modify an instance from the model. Responsable for set the dirty bit on the internal
        container, emit "dataChanged" signal and commit or abort the transaction

        with model.getForEdition(0) as instance:
            ... modify instance ...

        If you want to abort the transaction inside this context, raise TransactionAbort exception (transaction
        object doesn't have an "Aborted" state, so transaction.abort() souldn't be used

        :param int index: object index in the model
        """
        trans = transaction.get()
        try:
            yield self[index]
        except TransactionAbort:
            trans.abort()
        except:
            trans.abort()
            raise
        else:
            self._internal_container._p_changed = True
            self.updateDisplay(index)
            trans.commit()


class TransactionAbort(BaseException):
    pass
