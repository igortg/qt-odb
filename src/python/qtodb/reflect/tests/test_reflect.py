from qtodb.reflect.reflective import Reflective


class Dummy(Reflective):

    def __init__(self):
        super(Dummy, self).__init__()
        self._text = ""
        self.number = 0.0


    def get_text(self):
        return self._text

    def set_text(self, value):
        self._text = value

    text = property(get_text, set_text)


def test_reflect():

    def text_changed(value):
        global text
        text = value

    dummy = Dummy()
    dummy.RegisterAttributeReflection("text", text_changed)
    dummy.text = "Text"
    assert text == "Text"

    receiver = Dummy()
    dummy.RegisterAttributeReflection("text", receiver.set_text)
    dummy.text = "received"
    assert receiver.text == "received"
    import gc
    assert len(gc.get_referrers(receiver)) == 1
