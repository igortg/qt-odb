from PySide.QtCore import Qt, QDate
from PySide.QtGui import QLineEdit, QComboBox, QDateEdit
import datetime
from qtodb.database_model.objectlistmodel import ObjectListModel
from qtodb.reflect.reflective import Reflective
from qtodb.reflect.ui_reflector import UiReflector


class Dummy(Reflective):
    def __init__(self, text="", number=0.0):
        super(Dummy, self).__init__()
        self.text = text
        self.number = number
        self.other = None
        self.date = datetime.date(1990, 1, 1)


def test_text_reflection(qtbot):
    edit1 = QLineEdit()
    edit1.setObjectName("edit1")
    qtbot.addWidget(edit1)
    instance1 = Dummy()
    reflector = UiReflector()
    reflector.line_text(edit1, instance1, "text")
    instance1.text = "Data Text"
    assert edit1.text() == "Data Text"

    edit2 = QLineEdit()
    edit2.setObjectName("edit2")
    qtbot.addWidget(edit2)
    instance2 = Dummy()
    instance2.text = "Data2 Text"
    reflector.line_text(edit2, instance2, "text")
    assert edit2.text() == instance2.text

    edit1.clear()
    edit2.clear()
    qtbot.keyClicks(edit1, "UI Text")
    qtbot.keyClick(edit1, Qt.Key_Enter)
    qtbot.keyClicks(edit2, "UI Text 2")
    qtbot.keyClick(edit2, Qt.Key_Enter)
    assert instance1.text == "UI Text"
    assert instance2.text == "UI Text 2"

    reflector.disconnect(instance1)
    instance1.text = "Disconnected"
    assert edit1.text() == "UI Text"


def test_number_reflection(qtbot):
    edit = QLineEdit()
    qtbot.addWidget(edit)
    edit.show()
    instance = Dummy()
    reflector = UiReflector()
    reflector.line_float(edit, instance, "number")

    edit.clear()
    qtbot.keyClicks(edit, "2.5")
    qtbot.keyClick(edit, Qt.Key_Enter)
    assert instance.number == 2.5

    instance.number = 3.2
    assert edit.text() == str(instance.number)


def test_locale_reflection(qtbot):
    import locale
    locale.setlocale(locale.LC_ALL, "pt_BR.UTF-8")
    try:
        edit = QLineEdit()
        qtbot.addWidget(edit)
        edit.show()
        instance = Dummy()
        reflector = UiReflector()
        reflector.line_float(edit, instance, "number")
        qtbot.keyClicks(edit, "2,3")
        qtbot.keyClick(edit, Qt.Key_Enter)
        assert instance.number == 2.3
    finally:
        locale.resetlocale()


def test_combo_reflection(qtbot):
    options = ObjectListModel([])
    options.addAttributeColumn("text", "Text")
    options.addAttributeColumn("number", "Number")
    options.appendObject(Dummy("Zero", 0))
    options.appendObject(Dummy("One", 1))
    options.appendObject(Dummy("Two", 2))

    combo = QComboBox()
    combo.setModel(options)
    qtbot.addWidget(combo)
    combo.show()
    instance = Dummy()
    instance.other = options[2]
    reflector = UiReflector()
    reflector.combo_model(combo, instance, "other")
    assert combo.currentText() == "Two"
    qtbot.keyClick(combo, "O")
    assert instance.other.text == "One"


def test_date_reflection(qtbot):
    date_widget = QDateEdit()
    qtbot.addWidget(date_widget)
    date_widget.show()
    dummy= Dummy()
    reflector = UiReflector()
    reflector.date(date_widget, dummy, "date")
    assert date_widget.date() == QDate(dummy.date.year, dummy.date.month, dummy.date.day)
    qtbot.keyClicks(date_widget, "09041982")
    assert dummy.date == datetime.date(1982, 4, 9)
