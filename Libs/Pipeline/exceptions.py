class InputBloc:
    pass

class ValidationError(Exception):    
    # Constructor or Initializer
    def __init__(self, text):
        self.text = text
   
    # __str__ is to print() the value
    def __str__(self):
        return(repr(self.text))

class PadError(Exception):    
    # Constructor or Initializer
    def __init__(self, instance: InputBloc, pad_expected: str):
        self.instance = instance
        self.pad_expected = pad_expected
   
    # __str__ is to print() the value
    def __str__(self):
        return(f"Pad expected: {self.pad_expected}, pad of class {self.instance.__class__.__name__} is {self.instance.pad}")