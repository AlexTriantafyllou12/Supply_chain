import numpy as np

def check_integer_input(func):
        def wrapper(self, input):
            if not isinstance(input, (int,np.integer)) or input < 0:
                raise ValueError("Expected a positive integer value")

            func(self, input)
        return wrapper
