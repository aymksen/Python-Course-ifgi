#Module imports
import calculator
import shopping

#Main function
def main():
    #3.1.1 – Calculator
    #From the calculator module create the instance of the calculator class by
    # initiating the two inputs and the calling the required function
    print(calculator.Calculator(7,5).addition())
    print(calculator.Calculator(34,21).subtraktion())
    print(calculator.Calculator(54, 2).multiplikation())
    print(calculator.Calculator(144, 2).division())
    print(calculator.Calculator(45, 0).division())

    # 3.1.2 – Shopping Cart
    # This time create a new shopping cart instance
    new_cart = shopping.Cart()
    #1.Add 3 different items in different quantities to your cart
    new_cart.add_item("Apples", 5)
    new_cart.add_item("Banana", 3)
    new_cart.add_item("Mango", 4)

    #3.1.2.Display the current items in the cart and calculate the total quantity
    new_cart.show_cart()
    new_cart.total()

    #3.1.3.Remove an item from the cart, display the updated items, and recalculate the total quantity
    new_cart.remove_item("Banana")
    new_cart.show_cart()
    new_cart.total()


# Standard boilerplate to call the main() function.
if __name__ == '__main__':
    main()