
class Player:

    def __init__(self, name="Player"):
        self._name = name       

    def name(self):
        return self._name

    def move(self):
        raise NotImplementedError("Subclasses must implement move()")
