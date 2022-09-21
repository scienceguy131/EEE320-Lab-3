"""
    Description:
        This is the main module to the OORMS Lab 3 assignment from the EEE320 Object Oriented Analysis class.
        Running this module will cause a window to appear. Said window simulates people seated at given chairs around a
        table placing orders.

    Task:
        To implement all the sequence diagrams outlined in the lab instructions into the code.
        Testing code has been provided for us.


    Lab Started: September 19, 2022
    Lab Members: OCdt Al-Ansar Mohammed, OCdt Liethan Velasco.


    Notes:

          1 - Velasco: I see when creating an object from a class that inherits from another class,
          if you don't give it its own "overloaded" constructor, it automatically inherits the
          constructor from its parent (duh yea why did I have to mention that). When you do write
          an overloaded constructor though, you have to call the parents constructor with super().__init__(),
          or the console gets mad.

          2 - Velasco: I've asked the prof as to why we have a function definition embedded within the code of a method,
          and the reason for this one specifically is that each table/chair will get its very own handler function.
          I'm guessing because its literally defined and called whenever the create_restaurant_ui() and
          create_seat_ui() methods are called, the function handler for each of the tables/chairs are created right
          then and there, and subsequently used whether the user touches one of the tables/chairs. I'm also presuming
          this function definition needs to be made here in order to use the tag_bind() event binding function provided
          by tkinter right after, as I see a reference to the handler function gets passed this tag_bind() function.
          FurthermoreI'm going to look more into the tkinter documentation for this to see what exactly
          is going on behind the scenes.
          OOHHH I think I see why the reference to the function handlers defined in the methods gets passed through
          the tag_bind() methods xD it's done so that the tkinter program knows what function to call (or simply code
          to run) in the event that an event (a click in this case) is detected. Silly me.

          Just to remember, a handler in programming was defined like this online:
            "...an event handler is a callback routine that operates asynchronously once an event takes place.
            It dictates the action that follows the event. The programmer writes a code for this action to take place."

          Right, so I'm guessing the reason why the code was structured to have a function definition of the handler
          within the method is to ensure that each table/chair object legit got its own specific handler, for
          each and every single object that appears on the screen, whenever their specific interfaces show up.

          Eh, sorry if you've actually read this whole thing doctor xD. I normally write stuff like this to get all
          my thoughts out and try to understand something, while recording it at the same time you know. I tend to
          be rather verbose and repetitive doing it.

          AH I found it (I think)! The tag_bind() function essentially acts as a decorator/wrapper function to our
          function handler, and for this to be possible the function handler needs to passed in through tag_bind()'s
          arguments. There, that should be the case.

    Status:
        - Velasco (Sept 19, 2022) COMPLETED: Reading code for the first time to see what we've got to work with.
        Adding inline comments to organize things. These can be deleted later.
        - Velasco and Mohammed (Sept 20, 2022) COMPLETED: Implementing the Table Touch sequence diagram.
        - Mohammed (Sept 20, 2022) COMPLETED: Implementing the Done button sequence diagram.
        - Velasco (Sept 20, 2022) COMPLETED: Implementing the table touch sequence diagram.
        - Mohammed (Sept 20, 2022) COMPLETED: Implementing the menu item to be ordered sequence diagram.
        - Velasco (Sept 20, 2022) COMPLETED: Implementing Place Order button sequence diagram.
        - Mohammed (Sept 20, 2022) COMPLETED: finished last sequence diagram (cancelling) and tested UI and ran tests.py
        successfully
        - Velasco (Sept 20, 2022): Cleaning up the code for hand in... in the middle of create_restaurant_ui()
        - Mohammed (Sept 20, 2022): Beginning lab report write-up...

"""

# --- Importing Libraries and Modules ---

# Importing from built-in libraries
import math
import tkinter as tk

# Importing from local modules
from constants import *
from controller import RestaurantController
from model import Restaurant


# ------------- Defining Classes ---------------

class ServerView(tk.Frame):

    def __init__(self, master, restaurant):
        """ Constructor to ServerView class. Sets up all the instance variables that
         creates the restaurant view through tkinter. """

        # Calling the inherited class's constructor
        super().__init__(master)

        # Creating the window for the server view using tkinter methods and objects.
        # (<root> gets passed through master arg, which is a TK() object from tkinter)
        self.grid()
        self.canvas = tk.Canvas(self, width=SERVER_VIEW_WIDTH, height=SERVER_VIEW_HEIGHT,
                                borderwidth=0, highlightthickness=0)
        self.canvas.grid()
        self.canvas.update()

        # Storing the restaurant object used in the program in an instance var
        self.restaurant = restaurant

        # Setting the initial controller to be the RestaurantController object
        # so that its user interface can be created.
        self.controller = RestaurantController(self, restaurant)
        self.controller.create_ui()


    # -------------- Defining Methods --------------

    def set_controller(self, controller):
        """ Method responsible for switching the current controller in ServerView to <controller> passed
        through args and calls makes it create its own user interface. """

        self.controller = controller
        self.controller.create_ui()


    # Method that gets called in the RestaurantController object
    def create_restaurant_ui(self):
        """ This method gets called in the RestaurantController object.

        When called, uses tkinter's provided canvas methods to create the restaurant's user interface.
        More specifically, it calls the methods that draws out the tables, and defines the function handler
        in the event a table is touched.
        """

        # Wiping canvas of all its current pixels
        self.canvas.delete(tk.ALL)

        # Creating empty list that will contain the IDs of the tables and chairs created.
        view_ids = []

        # Taking table and chair data stored in self.restaurant object attribute, drawing the taables
        # and chairs onto the canvas using self.draw_table(). Filling up view_ids while doing so.
        for ix, table in enumerate(self.restaurant.tables):
            table_id, seat_ids = self.draw_table(table, scale = RESTAURANT_SCALE)
            view_ids.append((table_id, seat_ids))

        # Creating a handler in the event a table is clicked on
        for ix, (table_id, seat_ids) in enumerate(view_ids):

            # Pre-written message here:
            # §54.7 "extra arguments trick" in Tkinter 8.5 reference by Shipman
            # Used to capture current value of ix as table_index for use when
            # handler is called (i.e., when screen is clicked).

            # Refer to Notes - Entry 2 for a comment on this...
            # Creating the handler function for when a table is touched.
            def table_touch_handler(_, table_number = ix):
                self.controller.table_touched(table_number)

            # Refer to Notes - Entry 2 for a comment on this...
            # Binding the table touch event to the tables on the user interface,
            # passing in the table_touch_handler through .tag_bind() wrapper function
            self.canvas.tag_bind(table_id, '<Button-1>', table_touch_handler)

            # Doing the same thing for each seat in the restaurant user interface
            # (Passing in table_touch_handler() function so that touching a particular seat opens
            # up the user interface of the table said seat is associated with. Ha ha I figured it out :D)
            for seat_id in seat_ids:
                self.canvas.tag_bind(seat_id, '<Button-1>', table_touch_handler)


    def create_table_ui(self, table):
        """ This method Is called within the TableController object.

        The Table object that was selected is the <table> passed through the argument.

        When a specific table/chair is clicked, method uses provided tkinter methods to create the clicked upon table's
        user interface by drawing it and its selected chairs onto the canvas, and defines the handler for when a given
        seat is clicked on. """

        # Wiping the canvas of all currently drawn pixels
        self.canvas.delete(tk.ALL)

        # Drawing out the clicked on table and its associated seats in the specified location defined
        # in the constants module (the top left corner of the window lol)
        table_id, seat_ids = self.draw_table(table, location = SINGLE_TABLE_LOCATION)

        # Creating the handler function for each of the table's seats
        for ix, seat_id in enumerate(seat_ids):

            # Creating the seat touched event handler
            def handler(_, seat_number = ix):
                self.controller.seat_touched(seat_number)

            # Binding the click event to each seat around the table. Passing the
            # seat handler function into this wrapper function.
            self.canvas.tag_bind(seat_id, '<Button-1>', handler)

        # Creating the button that will close the current table user interface
        # and return to the restaurant user interface.
        self.make_button('Done', action = lambda event: self.controller.done())


    def draw_table(self, table, location = None, scale = 1):
        """ Uses Tkinter's provided canvas methods to draw a given table object out onto the canvas.

        <table> is the table object to be drawn, <location, defaulted to None> refers to where the table object
        is to be drawn on the canvas, and <scale, defaulted to 1> is how large the table is to be drawn.

        Returns the IDs of the table and seats created by tkinter for event binding with the handlers."""

        # Unpacking the coordinates for the offset depending on arguments passed
        offset_x0, offset_y0 = location if location else table.location

        # DAMN, here's a bunch of variables used to draw out the tables and seats.
        seats_per_side = math.ceil(table.n_seats / 2)
        table_height = SEAT_DIAM * seats_per_side + SEAT_SPACING * (seats_per_side - 1)
        table_x0 = SEAT_DIAM + SEAT_SPACING
        table_bbox = scale_and_offset(table_x0, 0, TABLE_WIDTH, table_height,
                                      offset_x0, offset_y0, scale)

        # Drawing the table here.
        table_id = self.canvas.create_rectangle(*table_bbox, **TABLE_STYLE)

        # Drawing the seats here.
        seat_ids = []
        far_seat_x0 = table_x0 + TABLE_WIDTH + SEAT_SPACING
        for ix in range(table.n_seats):
            seat_x0 = (ix % 2) * far_seat_x0
            seat_y0 = (ix // 2 * (SEAT_DIAM + SEAT_SPACING) +
                       (table.n_seats % 2) * (ix % 2) * (SEAT_DIAM + SEAT_SPACING) / 2)
            seat_bbox = scale_and_offset(seat_x0, seat_y0, SEAT_DIAM, SEAT_DIAM,
                                         offset_x0, offset_y0, scale)
            style = FULL_SEAT_STYLE if table.has_order_for(ix) else EMPTY_SEAT_STYLE
            seat_id = self.canvas.create_oval(*seat_bbox, **style)
            seat_ids.append(seat_id)

        # Returning table_id's and seat_id's
        return table_id, seat_ids


    def create_order_ui(self, order):
        """ This method is called within the OrderController object.

        Uses tkinter's provided methods to create the user interface of the order menu
        when a given seat object is selected from the table user interface.

        <order> is the order object that is to track all the orders made for the selected seat. """

        # Wipe canvas of all currently drawn pixels
        self.canvas.delete(tk.ALL)

        # Creating buttons for the order user interface, and the handler
        # for when each button is clicked on.
        for ix, item in enumerate(self.restaurant.menu_items):

            w, h, margin = MENU_ITEM_SIZE # Data from the constants module
            x0 = margin
            y0 = margin + (h + margin) * ix

            # Creating the handler function for each button
            def handler(_, menuitem=item):
                self.controller.add_item(menuitem)

            # Creating each button, and passing their handler into the wrapper function
            self.make_button(item.name, handler, (w, h), (x0, y0))

        # Literally drawing out the food items put up for order
        self.draw_order(order)

        # Creating the two buttons for the order user interface: Cancel and Place Orders button
        # (ouuu we're passing in unnamed lambda handler functions through the wrapper function :DDD)
        self.make_button('Cancel', lambda event: self.controller.cancel(), location = BUTTON_BOTTOM_LEFT)
        self.make_button('Place Orders', lambda event: self.controller.update_order())


    def draw_order(self, order):
        """ Draws out the orders placed after pressing a menu item button.  """

        x0, h, m = ORDER_ITEM_LOCATION
        for ix, item in enumerate(order.items):
            y0 = m + ix * h
            self.canvas.create_text(x0, y0, text = item.details.name, anchor = tk.NW)
            dot_style = ORDERED_STYLE if item.ordered else NOT_YET_ORDERED_STYLE
            self.canvas.create_oval(x0 - DOT_SIZE - DOT_MARGIN, y0, x0 - DOT_MARGIN, y0 + DOT_SIZE, **dot_style)

        # Drawing the total price below the orders placed.
        self.canvas.create_text(x0, m + len(order.items) * h,  text=f'Total: {order.total_cost():.2f}', anchor=tk.NW)


    def make_button(self, text, action, size = BUTTON_SIZE, location = BUTTON_BOTTOM_RIGHT,
                    rect_style = BUTTON_STYLE, text_style = BUTTON_TEXT_STYLE):
        """ Method that was made to make button drawing onto the canvas more organized.

        Notice: This acts as a wrapper function. The <action> argument is a function (in this program
        will be a handler function) that gets called when a specific button gets clicked. """

        w, h = size
        x0, y0 = location
        box = self.canvas.create_rectangle(x0, y0, x0 + w, y0 + h, **rect_style)
        label = self.canvas.create_text(x0 + w / 2, y0 + h / 2, text=text, **text_style)
        self.canvas.tag_bind(box, '<Button-1>', action)
        self.canvas.tag_bind(label, '<Button-1>', action)



# --------- Defining Functions -----------

def scale_and_offset(x0, y0, width, height, offset_x0, offset_y0, scale):
    """ Function to make the code for drawing more clean and organized. """
    return ((offset_x0 + x0) * scale,
            (offset_y0 + y0) * scale,
            (offset_x0 + x0 + width) * scale,
            (offset_y0 + y0 + height) * scale)




# --------- Running the main ---------

if __name__ == "__main__":

    # Creating a restaurant object which contains all the restaurant's
    # information stored in the constants.py module
    restaurant_info = Restaurant()

    # Initializing the tkinter object that allows us to use its methods
    root = tk.Tk()

    # Creating the ServerView object which basically runs the whole program upon instantiation
    ServerView(root, restaurant_info)

    # Setting attributes regarding the created pop-up window
    root.title('Restaurant Management System v0')
    root.wm_resizable(0, 0)

    # Calling the tkinter's mainloop() method so that the program can run properly
    root.mainloop()



# Damn, now I know how the code works :P. Sicccc.
