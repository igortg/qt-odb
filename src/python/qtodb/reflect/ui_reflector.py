from PySide.QtCore import SIGNAL, QObject
import locale
from qtodb.reflect.reflective import Reflective


class UiReflector(object):

    def __init__(self):
        self._reflections = {}


    def line_text(self, widget, instance, attr_name, convert_to_data=None):
        assert isinstance(instance, Reflective)

        def updateUi(value):
            widget.setText(value)

        def updateData():
            value = widget.text()
            if convert_to_data:
                value = convert_to_data(value)
            setattr(instance, attr_name, value)

        updateUi(getattr(instance, attr_name))
        instance.RegisterAttributeReflection(attr_name, updateUi)
        QObject.connect(widget, SIGNAL("editingFinished()"), updateData)
        widget_reflections = self._reflections.setdefault(widget, [])
        widget_reflections.append((instance, updateUi, updateData))


    def line_float(self, widget, instance, attr_name):
        assert isinstance(instance, Reflective)

        def updateUi(value):
            widget.setText(locale.str(value))

        def updateData():
            value = locale.atof(widget.text())
            setattr(instance, attr_name, value)

        updateUi(getattr(instance, attr_name))
        instance.RegisterAttributeReflection(attr_name, updateUi)
        QObject.connect(widget, SIGNAL("editingFinished()"), updateData)
        widget_reflections = self._reflections.setdefault(widget, [])
        widget_reflections.append((instance, updateUi, updateData))


    def disconnect(self, widget):
        widget.disconnect(widget)
        for instance, updateUi, updateData in self._reflections[widget]:
            instance.UnregisterReflection(updateUi)
