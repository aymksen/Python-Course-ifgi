#Package import
import easy_shopping as es

#Main function
def main():
    #3.2 Package creation and usage
    #check the submodule calculator
    print(es.Calculator(7,5).addition())
    print(es.Calculator(34,21).subtraktion())

    #check the submodule shopping
    new_es_cart = es.Cart()

    new_es_cart.add_item("Apples", 5)
    new_es_cart.add_item("Banana", 3)
    new_es_cart.add_item("Mango", 4)
    new_es_cart.remove_item("Banana")
    new_es_cart.show_cart()
    new_es_cart.total()


# Standard boilerplate to call the main() function.
if __name__ == '__main__':
    main()
