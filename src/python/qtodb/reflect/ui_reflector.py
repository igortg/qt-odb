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
        widget_reflections = self._reflections.setdefault(instance, [])
        widget_reflections.append((widget, updateUi, updateData))


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
        widget_reflections = self._reflections.setdefault(instance, [])
        widget_reflections.append((widget, updateUi, updateData))


    def combo_model(self, widget, instance, attr_name):
        assert isinstance(instance, Reflective)

        def updateUi(value):
            try:
                index = widget.model().objectIndex(value)
            except ValueError:
                widget.setCurrentIndex(-1)
            else:
                widget.setCurrentIndex(index)

        def updateData(index):
            value = widget.model()[index]
            setattr(instance, attr_name, value)

        updateUi(getattr(instance, attr_name))
        instance.RegisterAttributeReflection(attr_name, updateUi)
        QObject.connect(widget, SIGNAL("currentIndexChanged(int)"), updateData)
        widget_reflections = self._reflections.setdefault(instance, [])
        widget_reflections.append((widget, updateUi, updateData))


    def disconnect(self, instance):
        for widget, updateUi, updateData in self._reflections[instance]:
            instance.UnregisterReflection(updateUi)
            QObject.disconnect(widget, SIGNAL("editingFinished()"), updateData)
