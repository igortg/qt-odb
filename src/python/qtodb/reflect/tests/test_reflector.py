from PySide.QtCore import Qt
from PySide.QtGui import QLineEdit
from qtodb.reflect.reflective import Reflective
from qtodb.reflect.ui_reflector import UiReflector


class Dummy(Reflective):
    def __init__(self):
        super(Dummy, self).__init__()
        self.text = ""
        self.number = 0.0


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

    reflector.disconnect(edit1, instance1)
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
