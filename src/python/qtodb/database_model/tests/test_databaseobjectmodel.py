# -*- coding: utf8
from __future__ import unicode_literals, print_function, absolute_import, division

from PySide.QtCore import Qt
from PySide.QtGui import QTableView

from qtodb.database_model.databaseobjectmodel import DatabaseObjectModel
from qtodb.database_model.tests.fixtures import ModelIndexDuck
from qtodb.database_model.tests.schema import Person


def test_database_view(qtbot, session):
    session.add(Person(name="Roger Milla"))
    session.add(Person(name="François Biyik"))
    session.add(Person(name="Salvatore Schillaci"))
    session.commit()

    persons = DatabaseObjectModel(Person, session)
    persons.addAttributeColumn("name", "Name")
    assert persons.data(ModelIndexDuck(0, 0), Qt.DisplayRole) == "Roger Milla"

    view = QTableView()
    view.setModel(persons)
    persons.appendObject(Person(name="Claudio Cannigia"))
    persons.removeObject(0)
    qtbot.addWidget(view)
    view.show()
