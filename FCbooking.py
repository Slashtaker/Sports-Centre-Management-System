# Facility & Court Booking Module: provide visual calendar grid showing court/field
# availability per hour, broken down by zone, court number, or sport type.
# LEE WEI CHERN

from tkinter import ttk

class BookingManagement:

    def __init__(self):

        # fill in the venue
        self.venue = []
        self.sport = []

        self.max_hour = 3

        self.min_hour = 1
        
    def draw_tab(self, notebook):
        tab1 = ttk.Frame(notebook, padding=10)
        notebook.add(tab1, text="Court Booking")	