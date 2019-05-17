from PyQt5.QtCore import QObject, QDate
import locale
import datetime
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
        widget.editingFinished.connect(updateData)
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
                index = -1
            widget.setCurrentIndex(index)

        def updateData(index):
            value = widget.model()[index]
            setattr(instance, attr_name, value)

        updateUi(getattr(instance, attr_name))
        instance.RegisterAttributeReflection(attr_name, updateUi)
        QObject.connect(widget, SIGNAL("currentIndexChanged(int)"), updateData)
        widget_reflections = self._reflections.setdefault(instance, [])
        widget_reflections.append((widget, updateUi, updateData))


    def date(self, widget, instance, attr_name):
        assert isinstance(instance, Reflective)

        def updateUi(value):
            widget.setDate(QDate(value.year, value.month, value.day))

        def updateData(index):
            qdate = widget.date()
            value = datetime.date(qdate.year(), qdate.month(), qdate.day())
            setattr(instance, attr_name, value)

        updateUi(getattr(instance, attr_name))
        instance.RegisterAttributeReflection(attr_name, updateUi)
        widget.dateChanged.connect(updateData)
        widget_reflections = self._reflections.setdefault(instance, [])
        widget_reflections.append((widget, updateUi, updateData))



    def disconnect(self, instance):
        for widget, updateUi, updateData in self._reflections[instance]:
            instance.UnregisterReflection(updateUi)
            #TODO: disconnect the correct signal
            QObject.disconnect(widget)
