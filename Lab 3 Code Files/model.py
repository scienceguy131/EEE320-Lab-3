""" Module that contains all the models for the restaurant objects.

This will be modified come time. """

from constants import TABLES, MENU_ITEMS


class Restaurant:

    def __init__(self):
        """ Creates the restaurant object. """

        # Getting the table and chair data from TABLES in  constants.py, creating list from it
        self.tables = [Table(seats, loc) for seats, loc in TABLES]


        # TODO: uncomment next line
        # self.menu_items = [MenuItem(name, price) for name, price in MENU_ITEMS]


class Table:

    def __init__(self, seats, location):
        """ Creates a table object. """

        # Setting the instance vars of a given table object
        self.n_seats = seats
        self.location = location


        # Creating the list of orders for each seat
        self.orders = [Order() for _ in range(seats)]


    def order_for(self, seat_number):
        """ Returns the specific order associated with a given seat. """
        return self.orders[seat_number];


class Order:
    def add_item(self,menu_item):
        pass
    pass




class OrderItem:
    pass


class MenuItem:
    pass
