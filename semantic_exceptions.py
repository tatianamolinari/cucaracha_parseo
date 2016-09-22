class Error(Exception):
    def __init__(self, message):
        self.message = message
    
    def __str__(self):
     	return self.__class__.__name__ + " : " + self.message

class TypeError(Error):
	pass

class NotDefinedError(Error):
	pass

class AlreadyDefinedError(Error):
    pass