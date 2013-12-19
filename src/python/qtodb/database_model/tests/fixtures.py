class Dummy(object):
    def __init__(self, number=0.0, text="Text", integer=0):
        self.number = number
        self.text = text
        self.integer = integer


class ModelIndexMock():

    def __init__(self, row, col):
        self._row = row
        self._col = col

    def row(self):
        return self._row

    def column(self):
        return self._col