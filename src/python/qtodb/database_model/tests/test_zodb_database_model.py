from persistent.mapping import PersistentMapping
import transaction
from BTrees.IOBTree import IOBTree
from PySide.QtCore import Qt
from ZODB import DB
from ZODB.FileStorage import FileStorage
from qtodb.database_model.zodb_database_model import ZodbDatabaseModel
from qtodb.database_model.tests.fixtures import Dummy, ModelIndexDuck


def create_dummy_database_model(container):
    db_model = ZodbDatabaseModel(container)
    db_model.setKeyAttribute("integer")
    db_model.addAttributeColumn("number", "Number")
    db_model.addAttributeColumn("text", "Text")
    return db_model


def test_zodb_database_model():
    db_model = create_dummy_database_model(IOBTree())
    for i in range(1,4):
        dummy = Dummy()
        dummy.text = "Object{0}".format(i)
        dummy.number = i
        with db_model.openTransaction():
            db_model.appendObject(dummy)
    assert db_model.data(ModelIndexDuck(0,0), Qt.DisplayRole) == "1"
    assert db_model.data(ModelIndexDuck(1,1), Qt.DisplayRole) == "Object2"
    dummy1 = db_model.getObjectByKey(1)
    assert dummy1.text == "Object1"
    with db_model.openTransaction():
        db_model.removeObject(0)
    assert db_model.data(ModelIndexDuck(0,0), Qt.DisplayRole) == "2"
    dummy5 = Dummy()
    with db_model.openTransaction():
        db_model.appendObject(dummy5)
    assert dummy5.integer == 4


def open_database(filename):
    storage = FileStorage(filename)
    db = DB(storage)
    return db


def test_open_transaction(tmpdir):
    db_filepath = tmpdir.mkdir("test_storage").join("tests.db")
    db = open_database(db_filepath.strpath)
    root = db.open().root()

    root["Test"] = IOBTree()
    transaction.commit()
    db_model = create_dummy_database_model(root["Test"])
    with db_model.openTransaction() as t:
        db_model.appendObject(Dummy())
    with db_model.openTransaction() as t:
        dummy = db_model[0]
        dummy.text = "Dummy1"

    db.close()

    db = open_database(db_filepath.strpath)
    root = db.open().root()
    assert root["Test"][1].text == "Dummy1"
    db.close()


def test_get_for_edition(tmpdir):
    db_filepath = tmpdir.mkdir("test_object_btree_database_model").join("test.db")
    db = open_database(db_filepath.strpath)
    root = db.open().root()
    root["Test"] = IOBTree()
    db_model = create_dummy_database_model(root["Test"])
    with db_model.openTransaction():
        db_model.appendObject(Dummy())
    with db_model.getForEdition(0) as instance:
        instance.text = "Dummy0"
    db.close()

    db = open_database(db_filepath.strpath)
    root = db.open().root()
    assert root["Test"][1].text == "Dummy0"
    db.close()
