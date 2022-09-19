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
        # TODO: Uncomment next line
        # self.orders = [Order() for _ in range(seats)]


class Order:
    pass


class OrderItem:
    pass


class MenuItem:
    pass
