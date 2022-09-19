""" Code module that contains the controller classes, including:

Controller Parent Class
RestaurantController (inherits Controller)
TableController (inherits Controller)
OrderController (inherits Controller) """

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
        raise RuntimeError('seat_touched: some subclasses must implement')

    def table_touched(self, table_index):
        raise RuntimeError('table_touched: some subclasses must implement')


# ------------------- Classes below are what we modify ----------------------

class RestaurantController(Controller):
    """ A class that inherits Controller class.
     I'm guessing it controls the restaurant? """

    def create_ui(self):
        """ Creates the restaurant user interface with the passed through. """

        # This was defined in oorms.py
        self.view.create_restaurant_ui()


class TableController(Controller):
    pass


class OrderController(Controller):
    pass
