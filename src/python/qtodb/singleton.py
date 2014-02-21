class Singleton(object):
    _singleton = None


    def __init__(self):
        if self.__class__._singleton is not None:
            raise RuntimeError("Use get_singleton to access this class")
        else:
            self.__class__._singleton = self


    @classmethod
    def get_singleton(cls, *args, **kwargs):
        if cls._singleton is None:
            cls(*args, **kwargs)
        return cls._singleton
