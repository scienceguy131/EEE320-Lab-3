""" Module that contains all the models for the restaurant objects.

This will be modified come time. """

from constants import TABLES, MENU_ITEMS


class Restaurant:

    def __init__(self):
        """ Creates the restaurant object. """

        # Getting the table and chair data from TABLES in  constants.py, creating list from it
        self.tables = [Table(seats, loc) for seats, loc in TABLES]

        # Initializing list of menu items for this restaurant object
        self.menu_items = [MenuItem(name, price) for name, price in MENU_ITEMS]


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

    def has_order_for(self, seat_number):

        if (len(self.orders[seat_number].unordered_items()) == 0) and (self.orders[seat_number].total_cost() > 0):
            return True;
        else:
            return False;


class Order:

    def __init__(self):

        # Creating empty list attribute to contain all items to be ordered (aka unordered)
        self.items = [];

    def add_item(self, menu_item):
        item = OrderItem(menu_item);
        self.items.append(item);

    def place_new_orders(self):

        # Get list of unordered items first
        unordered_items = self.unordered_items();

        # Loop through list and set all orders to ordered
        for this_order in unordered_items:
            this_order.mark_as_ordered();

    def unordered_items(self):
        return [this_order for this_order in self.items if this_order.ordered is False];

    def remove_unordered_items(self):
        pass;

    def total_cost(self):
        total = 0
        for selection in self.items:
            total += selection.details.price

        return total;


class OrderItem:

    def __init__(self, menu_item):

        # Defaulting order status of this OrderItem object to false
        self.ordered = False;

        # Giving the given OrderItem object its "details"
        # (hmm this wasn't on the class diagram...)
        self.details = menu_item;


    def mark_as_ordered(self):
        """ Pretty self-explanatory lmao. """
        self.ordered = True;


class MenuItem:

    def __init__(self, name, price):
        """ MenuItem constructor... """
        self.name = name;
        self.price = price;