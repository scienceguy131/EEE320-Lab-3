""" Code module that contains the controller classes, including:

Controller Parent Class
RestaurantController (inherits Controller)
TableController (inherits Controller)
OrderController (inherits Controller) """

# --- Importing Libraries ---
from model import Table;

class Controller:
    """
    Do not modify this class, just its subclasses. Represents common behaviour of all
    Controllers. Python has a mechanism for explicitly dealing with abstract classes,
    which we haven't seen yet; raising RuntimeError gives a similar effect.
    """

    def __init__(self, view, restaurant):
        self.view = view
        self.restaurant = restaurant

    def add_item(self, item):
        """ 1. gets called from ServerView create_ui()
        2. add item from order class
        """
        #self.()
        raise RuntimeError('add_item: some subclasses must implement')

    def cancel(self):
        raise RuntimeError('cancel: some subclasses must implement')

    def create_ui(self):


        raise RuntimeError('create_ui: all subclasses must implement')

    def done(self):
        raise RuntimeError('done: some subclasses must implement')

    def place_order(self):
        raise RuntimeError('place_order: some subclasses must implement')

    def seat_touched(self, seat_number):
        """ Has similar code structure and functionality as the table_touched implementation. """
        pass;

        # raise RuntimeError('seat_touched: some subclasses must implement')

    def table_touched(self, table_index):
        """ 1. Serverview calls table_toched(table_number) in controller
	    2. Controller gets table datalizes a table controller object
	    4. Controller sets t from tables : List[Table]
	    3. Controller initiahe controller using set_controller(Tablecontroller object)
		back in Serverview
	    5. ServerView creates the UI in the TableController object
	    6. TableController object creates the UI back in ServerView"""

        # Retrieving specific table object that was touched from self.restaurant attribute
        this_table = self.restaurant.tables[table_index];

        # Creating a Table Controller Object from table that was touched (damn u can do that lmao)
        tc = TableController(self.view, self.restaurant, this_table);

        # Switching controller to this current table controller back in ServerView
        self.view.set_controller(tc);


        # raise RuntimeError('table_touched: some subclasses must implement')


# ------------------- Classes below are what we modify ----------------------

class RestaurantController(Controller):
    """ A class that inherits Controller class.
     I'm guessing it controls the restaurant? """


    def create_ui(self):
        """ Creates the restaurant user interface with the passed through. """

        # This was defined in oorms.py
        self.view.create_restaurant_ui()


class TableController(Controller):

    def __init__(self, view, restaurant, table):
        """ TableController constructor..."""

        super().__init__(view, restaurant);

        self.view = view;
        self.restaurant = restaurant;
        self.table = table;

    def create_ui(self):
        self.view.create_table_ui(self.table);


    def seat_touched(self, seat_number):
        """ This gets called whenever a seat is touched idk. """

        # Create OrderController object
        oc = OrderController(self.view, self.restaurant, self.table, seat_number);

        # Setting controller to oc back in ServerView
        self.view.set_controller(oc);

    def done(self):
        """ 1. gets called in the ServerView
        2. makes a RestaurantController obj
        3. sets the controller based on the restaurant controller
        """
        
        # Makes a RestaurantController obj
        rc = RestaurantController(view=self.view, restaurant=self.restaurant)

        # sets the controller we just made
        self.view.set_controller(rc)
        

class OrderController(Controller):

    def __init__(self, view, restaurant, table, seat_number):
        """ OrderController constructor..."""

        super().__init__(view, restaurant);

        self.view = view;
        self.restaurant = restaurant;
        self.table = table;

        # Getting the specific order associated with given seat_number
        self.order = self.table.order_for(seat_number);

    def create_ui(self):
        """ Creates the user interface of the given OrderController object. """
        self.view.create_order_ui(self.order);


    def update_order(self):
        """ Updates order I guess idk. """

        # Placing the new orders
        self.order.place_new_orders();

        # Creating the table controller and setting it to be controller in ServerView
        tc = TableController(self.view, self.restaurant, self.table);
        self.view.set_controller(tc);


