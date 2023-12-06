
def check_lists_same_length(func):
        def wrapper(self, input1, input2):
            if len(input1) != len(input2):
                raise ValueError("Input lists must be of the same length")

            func(self, input1, input2)
        return wrapper