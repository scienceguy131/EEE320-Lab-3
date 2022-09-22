"""

    Description:

        Code module that contains the controller classes. These classes are to be used in the
        OORMS lab 3 assignment in the EEE320 class.

    Classes defined in this module:
         - Controller Class (parent class)
         - RestaurantController Class (inherits Controller)
         - TableController Class (inherits Controller)
         - OrderController Class (inherits Controller)

    Modified by: OCdt Al-Ansar Mohammed, OCdt Liethan Velasco

    Notes:
        1 - Velasco: Ahh that's a neat thing I remember learning about class inheritance.
        The Controller class gets inherited by the other three classes in this module, which has
        mapped out methods that each of its children classes share in common (somewhat).

        You could say that we are overloading the methods when they are re-defined in the children
        classes since each of the children classes need to do their own thing when it comes to like
        the create_ui() method they share. The raise exception code statements written in Controller's
        methods never really gets called because each of those methods are re-defined in the children classes
        (yeah I'm rambling on a bit but just want to make sense of it).

        Honestly, you could probably make this code module without ever needing to define the parent Controller
        class. We're probably going to learn in class eventually  that this is a good coding practice-  to create
        a parent class that has "mapped-out" methods if we're creating classes that share similar,
        but not same behaviour.


"""

# --- Importing Libraries ---

from model import Table;   # lol we never really needed this import

class Controller:
    """
    Do not modify this class, just its subclasses. Represents common behaviour of all
    Controllers. Python has a mechanism for explicitly dealing with abstract classes,
    which we haven't seen yet; raising RuntimeError gives a similar effect.

    Ehh I'm going to add a few in-line comments :).
    """

    def __init__(self, view, restaurant):
        """ Constructor of Controller object.

        <view> is a ServerView object that handles all the drawing of the user interfaces, and <restaurant>
        is a Restaurant object which contains all of the data used to draw out the tables, chairs, and orders. """

        self.view = view
        self.restaurant = restaurant

    # -------- Mapping out methods for children classes to re-define ----------

    def add_item(self, item):
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
        raise RuntimeError('place_order: some subclasses must implement');

    def table_touched(self, table_index):
        raise RuntimeError('table_touched: some subclasses must implement')

    def update_order(self):
        raise RuntimeError('update_order: some subclasses must implement');



# ------------------- Creating the Children Classes ----------------------

class RestaurantController(Controller):

    # Inherits its parents constructor

    def create_ui(self):
        """ Calling .create_ui() method from this class back in the ServerView object calls the create_restaurant_ui().
        Essentially calls the method to draw the entire restaurant into the canvas. """
        self.view.create_restaurant_ui()

    def table_touched(self, table_index):
        """ This method is called by the table touch function handler back in the ServerView object.

        Essentially sets the current controller of the ServerView to be the table touched so that
        the table and its associated seatscan be "zoomed in upon". """

        # Retrieving specific table object that was touched from self.restaurant attribute
        this_table = self.restaurant.tables[table_index];

        # Creating a Table Controller Object from table that was touched
        tc = TableController(self.view, self.restaurant, this_table);

        # Switching controller to this current table controller back in ServerView
        self.view.set_controller(tc);


class TableController(Controller):

    def __init__(self, view, restaurant, table):
        """ Constructor of TableController object.

        <view> is a ServerView object that handles all the drawing of the user interfaces, <restaurant>
        is the Restaurant object which contains all the data used to draw out the tables, chairs, and orders,
        <table> is a specific table object that was clicked on (TableController object only gets created
        when that happens). """

        # Calling parent constructor
        super().__init__(view, restaurant);

        # Setting instance vars
        self.view = view;
        self.restaurant = restaurant;
        self.table = table;


    def create_ui(self):
        """ Calling .create_ui() method from this class back in the ServerView object calls the create_table_ui().
        Essentially calls the method to draw the specific table selected and its associated chairs onto the canvas. """
        self.view.create_table_ui(self.table);


    def seat_touched(self, seat_number):
        """ This method is called by the seat touch function handler back in the ServerView object.

        Essentially sets the current controller of the ServerView to be the OrderController object which
        opens up the menu of menu items to be selected by the seat clicked on. The number of the seat
        clicked on is passed through args as <seat_number>. """

        # Create OrderController object
        oc = OrderController(self.view, self.restaurant, self.table, seat_number);

        # Setting current controller to oc back in ServerView
        self.view.set_controller(oc);


    def done(self):
        """ This function gets called when the [done] button gets pressed when viewing the table user interface.
        Essentially switches the current controller in ServerView back to the Restaurant controller. In other
        words, hitting the done button returns us back to seeing the whole restaurant. """
        
        # Making the RestaurantController object
        rc = RestaurantController(view = self.view, restaurant = self.restaurant)

        # Setting current controller to rc back in ServerView
        self.view.set_controller(rc)
        

class OrderController(Controller):

    def __init__(self, view, restaurant, table, seat_number):
        """ Constructor of OrderController object.

        <view> is a ServerView object that handles all the drawing of the user interfaces, <restaurant>
        is the Restaurant object which contains all the data used to draw out the tables, chairs, and orders,
        <table> is a specific table object that was clicked on, <seat_number> is the number of the seat at the table
        that was clicked on. """

        # Calling parent constructor
        super().__init__(view, restaurant);

        # Setting the usual instance vars
        self.view = view;
        self.restaurant = restaurant;
        self.table = table;

        # Getting the list of Order objects (the order made) associated with the clicked-on seat
        self.order = self.table.order_for(seat_number);


    def create_ui(self):
        """ Calling .create_ui() method from this class back in the ServerView object calls the create_order_ui().
        Essentially calls the method to draw the order menu associated with the specific chair selected. """
        self.view.create_order_ui(self.order);


    def add_item(self, item):
        """ Function that adds item to the "to be ordered" list when the order user interface is up.

        Function does this by adding the item through the Order object's .add_item() method, and
        updates the order user_interface() by calling .create_ui().  """
        self.order.add_item(item)
        self.create_ui()


    def update_order(self):
        """ Function is responsible for setting the "to be ordered" items to be ordered - IOW coloured green.

         This function gets called when the 'Place Orders' button gets pressed while in the order user
         interface. Obviously after pressing it returns the view to the table associated with the chair
         whose order was just placed. """

        # Setting the "to be ordered" items to ordered status.
        self.order.place_new_orders();

        # Creating the table controller and setting it to be controller in ServerView
        tc = TableController(self.view, self.restaurant, self.table);
        self.view.set_controller(tc);


    def cancel(self):
        """ Function is responsible for cancelling an order in progress.

        This function gets called when the 'Cancel' button gets pressed while in the order user interface.
        Pressing the button returns the view to the table associated with the chair whose order was just cancelled."""

        # Removing the list of items under "to be ordered" status
        self.order.remove_unordered_items()

        # Switching the current controller in ServerView back to TableController
        tc = TableController(self.view,self.restaurant,self.table)
        self.view.set_controller(tc)


# Siiiick this ones finished too.
