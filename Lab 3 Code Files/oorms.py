""" This is essentially the main module of the Lab 3 OORMS program.

    Hoooo this is going to be a fun one for sure.

    Task: To implement all the sequence diagrams outlined in the lab instructions
    into the code. Testing code has been provided for us.


    Lab Started: September 19, 2022
    Lab Members: OCdt Al-Ansar Mohammed, OCdt Liethan Velasco.



    Notes:
          - None for now :P


    Status:
        - Velasco: Reading code for the first time to see what we've got to work with.
        Adding inline comments to organize things.


"""

# --- Importing Libaries ---

import math
import tkinter as tk

from constants import *
from controller import RestaurantController
from model import Restaurant


# ------------- Defining Classes ---------------

class ServerView(tk.Frame):

    def __init__(self, master, restaurant):
        """ Constructor to ServerView class. Sets up all the instance variables that
         creates the restaurant view through tkinter. """

        # Note to self: <root> gets passed through master arg.
        # restaurant_info, an object of Restaurant() gets passed through restaurant.

        super().__init__(master)
        self.grid()
        self.canvas = tk.Canvas(self, width=SERVER_VIEW_WIDTH, height=SERVER_VIEW_HEIGHT,
                                borderwidth=0, highlightthickness=0)
        self.canvas.grid()
        self.canvas.update()
        self.restaurant = restaurant
        self.controller = RestaurantController(self, restaurant)
        self.controller.create_ui()

    def set_controller(self, controller):
        self.controller = controller
        self.controller.create_ui()

    def create_restaurant_ui(self):
        self.canvas.delete(tk.ALL)
        view_ids = []
        for ix, table in enumerate(self.restaurant.tables):
            table_id, seat_ids = self.draw_table(table, scale=RESTAURANT_SCALE)
            view_ids.append((table_id, seat_ids))
        for ix, (table_id, seat_ids) in enumerate(view_ids):
            # §54.7 "extra arguments trick" in Tkinter 8.5 reference by Shipman
            # Used to capture current value of ix as table_index for use when
            # handler is called (i.e., when screen is clicked).
            def table_touch_handler(_, table_number=ix):
                self.controller.table_touched(table_number)
            self.canvas.tag_bind(table_id, '<Button-1>', table_touch_handler)
            for seat_id in seat_ids:
                self.canvas.tag_bind(seat_id, '<Button-1>', table_touch_handler)

    def create_table_ui(self, table):
        self.canvas.delete(tk.ALL)
        table_id, seat_ids = self.draw_table(table, location=SINGLE_TABLE_LOCATION)
        for ix, seat_id in enumerate(seat_ids):
            def handler(_, seat_number=ix):
                self.controller.seat_touched(seat_number)

            self.canvas.tag_bind(seat_id, '<Button-1>', handler)
        self.make_button('Done', action=lambda event: self.controller.done())

    def draw_table(self, table, location=None, scale=1):
        offset_x0, offset_y0 = location if location else table.location
        seats_per_side = math.ceil(table.n_seats / 2)
        table_height = SEAT_DIAM * seats_per_side + SEAT_SPACING * (seats_per_side - 1)
        table_x0 = SEAT_DIAM + SEAT_SPACING
        table_bbox = scale_and_offset(table_x0, 0, TABLE_WIDTH, table_height,
                                      offset_x0, offset_y0, scale)
        table_id = self.canvas.create_rectangle(*table_bbox, **TABLE_STYLE)
        far_seat_x0 = table_x0 + TABLE_WIDTH + SEAT_SPACING
        seat_ids = []
        for ix in range(table.n_seats):
            seat_x0 = (ix % 2) * far_seat_x0
            seat_y0 = (ix // 2 * (SEAT_DIAM + SEAT_SPACING) +
                       (table.n_seats % 2) * (ix % 2) * (SEAT_DIAM + SEAT_SPACING) / 2)
            seat_bbox = scale_and_offset(seat_x0, seat_y0, SEAT_DIAM, SEAT_DIAM,
                                         offset_x0, offset_y0, scale)
            # TODO: delete next line, uncomment the line following
            style = EMPTY_SEAT_STYLE
            # style = FULL_SEAT_STYLE if table.has_order_for(ix) else EMPTY_SEAT_STYLE
            seat_id = self.canvas.create_oval(*seat_bbox, **style)
            seat_ids.append(seat_id)
        return table_id, seat_ids

    def create_order_ui(self, order):
        self.canvas.delete(tk.ALL)
        for ix, item in enumerate(self.restaurant.menu_items):
            w, h, margin = MENU_ITEM_SIZE
            x0 = margin
            y0 = margin + (h + margin) * ix

            def handler(_, menuitem=item):
                self.controller.add_item(menuitem)

            self.make_button(item.name, handler, (w, h), (x0, y0))
        self.draw_order(order)
        self.make_button('Cancel', lambda event: self.controller.cancel(), location=BUTTON_BOTTOM_LEFT)
        self.make_button('Place Orders', lambda event: self.controller.update_order())

    def draw_order(self, order):
        x0, h, m = ORDER_ITEM_LOCATION
        for ix, item in enumerate(order.items):
            y0 = m + ix * h
            self.canvas.create_text(x0, y0, text=item.details.name,
                                    anchor=tk.NW)
            dot_style = ORDERED_STYLE if item.ordered else NOT_YET_ORDERED_STYLE
            self.canvas.create_oval(x0 - DOT_SIZE - DOT_MARGIN, y0, x0 - DOT_MARGIN, y0 + DOT_SIZE, **dot_style)
        self.canvas.create_text(x0, m + len(order.items) * h,
                                text=f'Total: {order.total_cost():.2f}',
                                anchor=tk.NW)

    def make_button(self, text, action, size=BUTTON_SIZE, location=BUTTON_BOTTOM_RIGHT,
                    rect_style=BUTTON_STYLE, text_style=BUTTON_TEXT_STYLE):
        w, h = size
        x0, y0 = location
        box = self.canvas.create_rectangle(x0, y0, x0 + w, y0 + h, **rect_style)
        label = self.canvas.create_text(x0 + w / 2, y0 + h / 2, text=text, **text_style)
        self.canvas.tag_bind(box, '<Button-1>', action)
        self.canvas.tag_bind(label, '<Button-1>', action)



# --------- Defining Functions -----------

def scale_and_offset(x0, y0, width, height, offset_x0, offset_y0, scale):
    return ((offset_x0 + x0) * scale,
            (offset_y0 + y0) * scale,
            (offset_x0 + x0 + width) * scale,
            (offset_y0 + y0 + height) * scale)




# --------- Running the main ---------

if __name__ == "__main__":
    restaurant_info = Restaurant()
    root = tk.Tk()
    ServerView(root, restaurant_info)
    root.title('Restaurant Management System v0')
    root.wm_resizable(0, 0)
    root.mainloop()
