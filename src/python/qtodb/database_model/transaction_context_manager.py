from contextlib import contextmanager
import transaction


# noinspection PyAttributeOutsideInit
class TransactionContextManager(object):
    """
    Add context management to ZODB Model objects

    It's recomended that sub-classes check for _current_transaction attribute before any change in the internal
    container
    """


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
        self._current_transaction = trans = transaction.get()
        try:
            yield trans
            self._internal_container._p_changed = True
            trans.commit()
        except TransactionAbort:
            trans.abort()
        except:
            trans.abort()
            raise
        finally:
            self._current_transaction = None
        if resetModel:
            self.reset()


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


    def _assertOpenTransaction(self):
        assert getattr(self, "_current_transaction", None) is not None, "No transaction currently opened"


class TransactionAbort(BaseException):
    pass
