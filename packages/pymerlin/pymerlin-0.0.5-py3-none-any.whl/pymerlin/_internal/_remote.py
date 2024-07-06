class Remote:
    def __init__(self, contents):
        self._contents = contents

    def contents(self):
        return self._contents

    class Java:
        implements = ["java.rmi.Remote"]
