from PyQt4.QtCore.QModelIndex import QModelIndex
from qtodb.database_model.dict_model import DictModel
from qtodb.database_model.tests.fixtures import ModelIndexDuck


def test_dict_model():
    model = DictModel()
    model["test1"] = 1
    model["test2"] = 2
    model
    assert 1, model.data(ModelIndexDuck(0,1))
    assert "test2", model.data(ModelIndexDuck(1,0))


