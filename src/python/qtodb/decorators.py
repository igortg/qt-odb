__author__ = 'itghisi'


def not_implemented(foo):

    def not_implemented_wrapper(self, *args, **kw):
        function_fullname = "{0}.{1}".format(self.__class__.__name__, foo.func_name)
        raise NotImplementedError("Method '{0}' not implemented".format(function_fullname))

    return not_implemented_wrapper