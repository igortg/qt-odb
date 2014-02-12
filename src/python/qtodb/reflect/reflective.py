import weakref
from types import MethodType, BuiltinMethodType
from qtodb.reflect.weakmethod import WeakMethod


class Reflective(object):
    """
    Reflect changes in instance attributes for registered callbacks
    """


    def RegisterAttributeReflection(self, attr_name, callback):
        if not hasattr(self, "_v_callbacks"):
            self._v_callbacks = {}
        if not hasattr(self, attr_name):
            import warnings
            warnings.warn("{0} has no attribute '{1}'".format(self.__class__.__name__, attr_name))
        if isinstance(callback, (MethodType, BuiltinMethodType)):
            callback_ref = WeakMethod(callback)
        else:
            callback_ref = weakref.ref(callback)
        attr_callbacks = self._v_callbacks.setdefault(attr_name, [])
        attr_callbacks.append(callback_ref)


    def UnregisterReflection(self, callback):
        for callback_list in self._v_callbacks.values():
            for callback_ref in callback_list:
                if callback == callback_ref():
                    callback_list.remove(callback_ref)


    def __setattr__(self, key, value):
        super(Reflective, self).__setattr__(key, value)
        if hasattr(self, "_v_callbacks") and key in self._v_callbacks:
            for callback_weakref in self._v_callbacks[key]:
                callback = callback_weakref()
                if callback:
                    callback(value)
                else:
                    self._v_callbacks[key].remove(callback_weakref)
