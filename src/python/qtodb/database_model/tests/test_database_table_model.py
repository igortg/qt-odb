from PySide.QtCore import Qt
from qtodb.database_model.abstract_object_database_model import AbstractObjectDatabaseModel
from qtodb.database_model.tests.fixtures import Dummy, ModelIndexMock


class ObjectListDatabaseModel(AbstractObjectDatabaseModel):

    def _appendToInternalContainer(self, item):
        self._internal_container.append(item)

    def __getitem__(self, index):
        return self._internal_container[index]




def test_database_table_model():
    database = ObjectListDatabaseModel([])
    model = ObjectDatabaseTableModel(database)
    model.addAttributeColumn("number", "Number")
    model.addAttributeColumn("text", "Text")
    for i in range(1, 4):
        model.appendObject(Dummy(i, "Object{0}".format(i)))
    assert model.data(ModelIndexMock(1,0), Qt.DisplayRole) == "2"
    assert model.data(ModelIndexMock(2,1), Qt.DisplayRole) == "Object3"
