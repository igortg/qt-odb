from __future__ import unicode_literals, print_function, absolute_import, division
from PySide.QtCore import QAbstractTableModel, QModelIndex
from PySide.QtCore import Qt
from collections import namedtuple
from qtodb.database_model.abstract_object_database_model import AbstractObjectModel


class DatabaseObjectModel(AbstractObjectModel):

    def __init__(self, mapping_class, session, parent=None):
        """

        :param mapping_class:
        :param Session session: a Session instance.
        :param QObject parent: a parent object for the model.
        """
        AbstractObjectModel.__init__(self, parent)
        self._session = session
        self._mapping_class = mapping_class
        self._instances = session.query(mapping_class).all()


    def __getitem__(self, index):
        return self._instances[index]


    def appendObject(self, instance):
        objects_count = len(self._instances)
        self.beginInsertRows(QModelIndex(), objects_count, objects_count)
        self._appendToInternalContainer(instance)
        self.endInsertRows()


    def removeObject(self, index):
        self.beginRemoveRows(QModelIndex(), index, index)
        self._removeFromInternalContainer(index)
        self.endRemoveRows()


    def rowCount(self, QModelIndex_parent=None, *args, **kwargs):
        return len(self._instances)


    def columnCount(self, QModelIndex_parent=None, *args, **kwargs):
        return len(self._object_attributes)


    def _appendToInternalContainer(self, instance):
        self._session.add(instance)
        self._session.commit()
        self._instances.append(instance)


    def _removeFromInternalContainer(self, index):
        instance = self._instances.pop(index)
        self._session.delete(instance)
