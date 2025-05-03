#Main class
class Cart:
    def __init__(self):
        #At first an empty cart
        #most appropriate data type is dictionary
        self.cart = {}

    #Add a new item but if it is already there just increase the quantity
    #Exception handling can be done to check if the item_name is a string and the quantity is not zero but
    # that is not required in the problem statements / tasks, so we have not added any exception handling checks in this exercise.
    def add_item(self, item_name, quantity):
        if item_name in self.cart:
            self.cart[item_name] += quantity
        else:
            self.cart[item_name] = quantity

    #remove the item if it is present in teh cart
    #otherwise a message can be shown that that item not found but again exception handling is not the purpose
    def remove_item(self, item_name):
        if item_name in self.cart:
            if self.cart[item_name] == 1:
                #pop can also be used
                del self.cart[item_name]
            else:
                self.cart[item_name] = self.cart[item_name] - 1

    #show the contents of the cart
    def show_cart(self):
            i=1
            for item, quantity in self.cart.items():
                print(f"{i} . {item}: {quantity}")
                i+=1


    #To calculate the total quantity, just go through the total values only
    def total(self):
        total = 0
        for quantity in self.cart.values():
            total += quantity
        print(f"Total Items: {total}")