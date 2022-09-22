"""

    Description:
        This is the module that contains all the restaurant's models, including that of the Restaurant itself,
        the Tables, the Orders made with a selected chair, and the OrderItems and MenuItems. These were all
        modeled with the use of classes and instantiating objects from them (duh).

    Modified by: OCdt Al-Ansar Mohammed, OCdt Liethan Velasco

    Notes:
        - None for now :P.

"""

# ---- Importing from other modules -----

from constants import TABLES, MENU_ITEMS


# --------------- Defining the classes of the Restaurant objects -------------

class Restaurant:

    def __init__(self):
        """ Constructor to the Restaurant Class.

        Upon instantiation, retrieves table and menu item data, creates a list of each of the objects
        and stores the lists in instance variables. """

        # Getting the table and chair data from TABLES in  constants.py
        # and creating a list of Table objects
        self.tables = [Table(seats, loc) for seats, loc in TABLES]

        # Initializing list of menu items for this restaurant object
        self.menu_items = [MenuItem(name, price) for name, price in MENU_ITEMS]


class Table:

    def __init__(self, seats, location):
        """ Constructor to the Table Class.

        <seats> argument refers to the number of seats the Table object to be created will have.
        <location> argument refers to the location the Table object is to placed on the canvas. """

        # Setting the instance vars of the Table object to be created
        self.n_seats = seats
        self.location = location

        # Creating the list of Order objects associated with each seat at the table.
        # Storing it in an instance var attribute.
        self.orders = [Order() for _ in range(seats)]


    def order_for(self, seat_number):
        """ Function returns the specific Order object associated with the seat whose
        number <seat_number> has been passed through the arguments. """
        return self.orders[seat_number];


    def has_order_for(self, seat_number):
        """ Function returns a boolean that indicates whether the given
        seat of number <seat_number> has ordered yet. """

        # Storing the specific order for the given seat in a dummy var
        this_order = self.orders[seat_number];

        # Return True if there are 0 orders pending to be ordered, and the total cost
        # of the given order is greater than 0, insinuating that this chair has already placed an order.
        return (len(this_order.unordered_items()) == 0) and (this_order.total_cost() > 0);



class Order:

    def __init__(self):
        """ Constructor for Order object.

        In short, this object is responsible for keeping track of the orders placed by a given
        seat in the restaurant.

        Every chair gets their own Order object associated with it. """

        # Creating empty list attribute to contain all items
        # that were ordered and that are pending to be ordered.
        self.items = [];


    def add_item(self, menu_item):
        """ Function simply adds the OrderItem object <menu_item> passed through
        the arguments into the self.items list attribute of the Order object. """
        item = OrderItem(menu_item);
        self.items.append(item);


    def place_new_orders(self):
        """ Function goes through the list attribute self.items of the given Order object and
        sets all OrderItem objects in the list from "unordered" to "ordered" status. """

        # Get list of unordered items f
        unordered_items = self.unordered_items();

        # Loop through list and set all orders to "ordered" status
        for this_order in unordered_items:
            this_order.mark_as_ordered();


    def unordered_items(self):
        """ Function returns a list of all OrderItem objects in self.items that have yet
        to have their order status be set to 'ordered' """
        return [this_order for this_order in self.items if this_order.ordered is False];


    def remove_unordered_items(self):
        """ Function removes all the items in the list attribute self.items that have an "unordered" status. """
        unordered = self.unordered_items()
        for item in unordered:
            self.items.remove(item)


    def total_cost(self):
        """ Function simply calculates the total cost of all the OrderItem
        objects currently in the self.items list attribute. """
        total = 0
        for selection in self.items:
            total += selection.details.price
        return total


class OrderItem:

    def __init__(self, menu_item):
        """ Constructor for the OrderItem class.

        Upon instantiation, sets the order status of the OrderItem object to False (obviously).
        Also stores the <menu_item> MenuItem object (object that contains the information
        regarding the given OrderItem object) in the instance var self.details. """

        # Defaulting order status of this OrderItem object to False
        self.ordered = False;

        # Giving the given OrderItem object its information
        # (hmm this wasn't on the class diagram... oh well)
        self.details = menu_item;


    def mark_as_ordered(self):
        """ Sets the self.ordered instance boolean var to true.  """
        self.ordered = True;


class MenuItem:
    """ Objects of this class hold the information pertaining to each OrderItem set on the menu. """

    def __init__(self, name, price):
        """ Constructor of MenuItem class.

        Upon instantiation, sets the name of the MenuItem to <name> and the
        price of the menu item to <price>. """
        self.name = name;
        self.price = price;


# End of this code module. Nice, that's the last one.