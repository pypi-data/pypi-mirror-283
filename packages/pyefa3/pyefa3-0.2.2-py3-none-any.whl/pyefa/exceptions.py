class ObjectInitException(Exception):
    def __init__(self, obj, name):
        self.name = name
        self.obj = obj.__class__.__name__
        self.value = str(self)

    def __str__(self):
        return f'invalid property {repr(self.name)} for {self.obj}'


class SetupException(Exception):
    """ Exception indicating an invalid Setup for EFA-Requests """

    def __init__(self, option, have, want):
        """Initialize exception

        option -- name of incorect option
        have -- given value
        want -- string, explaining the allowed values
        """
        self.option = option
        self.have = have
        self.want = want
        self.value = str(self)

    def __str__(self):
        return f'invalid argument for {self.option}: expected {self.want}, got {repr(self.have)}'


class NotImplementedException(Exception):
    """ Exception indicating that something is not (yet) implemented """

    def __init__(self, what):
        """Initialize exception:

        what -- string, explaining what exactly is not implemented
        """
        self.what = what
        self.value = str(self)

    def __str__(self):
        return f'Not Implemented: {self.what}'
