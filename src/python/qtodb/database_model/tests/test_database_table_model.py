from PySide.QtCore import Qt
from qtodb.database_model.object_list_model import ObjectListModel
from qtodb.database_model.tests.fixtures import Dummy, ModelIndexDuck


def test_database_table_model():
    model = ObjectListModel([], None)
    model.addAttributeColumn("number", "Number")
    model.addAttributeColumn("text", "Text")
    for i in range(1, 4):
        model.appendObject(Dummy(i, "Object{0}".format(i)))
    assert model.data(ModelIndexDuck(1,0), Qt.DisplayRole) == "2"
    assert model.data(ModelIndexDuck(2,1), Qt.DisplayRole) == "Object3"
