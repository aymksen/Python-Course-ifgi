#Calculator class with the constructor
class Calculator:
    def __init__(self,a,b):
        self.a = a
        self.b = b

    #function to check if the inputs are valid i.e. either integers or float
    def validate_inputs(self):
        if not (isinstance(self.a, (int, float)) and isinstance(self.b, (int, float))):
            return False
        else:
            return True

    #To avoid writing the whole error statement again and again
    def return_error(self):
        return "Error: Inputs must be numbers"

    #addition function
    def addition(self):
        #check if the inputs are valid, then add, otherwise return an error message
        if self.validate_inputs():
            return self.a + self.b
        else:
            return self.return_error()

    #subtraction function
    def subtraktion(self):
        if self.validate_inputs():
            return self.a - self.b
        else:
            return self.return_error()

    #multiplication function
    def multiplikation(self):
        if self.validate_inputs():
            return self.a * self.b
        else:
            return self.return_error()

    #division function with divide by zero check
    #it will simply return infinity
    def division(self):
        if self.validate_inputs():
            if self.b == 0:
                return "Infinity"
            else:
                return self.a / self.b
        else:
            return self.return_error()
