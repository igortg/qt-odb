from PyQt4.QtCore import Qt
from qtodb.database_model.dictmodel import DictModel
from qtodb.database_model.tests.fixtures import ModelIndexDuck


def test_dict_model():
    data = {"AB": "Abel", "CD": "Cordel"}
    model = DictModel(data)
    assert model.rowCount() == 2
    assert model.data(ModelIndexDuck(0,0), Qt.DisplayRole) == "AB"
    assert model.data(ModelIndexDuck(1,1), Qt.DisplayRole) == "Cordel"



