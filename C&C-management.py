# Jonathan
# AMCS1034 Software Development Fundamentals Practical Assignment
# Application (E) : Sports Centre Management System
# Module          : Coaching & Class Management Module

import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import os

# ============================================================
#  Section 1 : Constants ( values used by the whole program )
# ============================================================

file_name = "coaching_data.txt"         # Store records in file
max_daily_hours = 8                     # Coach working hours per day
date_format = "%d-%b-%Y"                # Date format : 22-NOV-2026

# Dictionary : Sports available with respective price per hour (RM)
sport_rates = {"Swimming": 50.00, "Badminton": 40.00,
               "Yoga": 30.00, "Pickleball": 45.00}

# Tuple : Tuple is suitable for unchanged session types
session_types = ("Private", "Group")

# =====================================================
#  Section 2 : Classes ( encapsulation + inheritance )
# =====================================================

class Session:

    """Base class : Stores one coaching session details."""
    def __init__(self, session_id, coach, sport, date, hours, participants): 

        # Encapsulation :  Two "__" make these attributes private
        self.__session_id = session_id
        self.__coach = coach
        self.__sport = sport
        self.__date = date
        self.set_hours(hours)
        self.set_participants(participants)

    # Getters : Other code reads private data through these
    def get_session_id(self):
        return self.__session_id

    def get_coach(self):
        return self.__coach

    def get_sport(self):
        return self.__sport

    def get_date(self):
        return self.__date

    def get_hours(self):
        return self.__hours

    def get_participants(self):
        return self.__participants

    # Setters : Data checked before saving
    def set_hours(self, hours):
        if hours < 0.5 or hours > max_daily_hours:
            raise ValueError("Hours must be in between 0.5 and 8.")
        self.__hours = hours

    def set_participants(self, participants):
        if participants < 1 or participants > 20:
            raise ValueError("Participants must be in between 1 and 20.")
        self.__participants = participants

    # Calculation
    def get_type(self):
        return "Session"

    def get_rate_per_hour(self):
        # .get() returns 0 if the sport is not in the dictionary
        return sport_rates.get(self.__sport, 0)

    def get_total_fee(self):
        return self.__hours * self.get_rate_per_hour()

    def get_commission_rate(self):
        return 0.30

    def get_commission(self):
        return self.get_total_fee() * self.get_commission_rate()

    def to_line(self):

        """Convert the record into one line of text for the file."""
        return (f"{self.get_type()}|{self.__session_id}|{self.__coach}|"
                f"{self.__sport}|{self.__date}|{self.__hours}|"
                f"{self.__participants}")

class PrivateSession(Session):

    """Child class : One coach teaches one student."""
    def __init__(self, session_id, coach, sport, date, hours, participants = 1):
        # super() calls __init__ of the parent class
        super().__init__(session_id, coach, sport, date, hours, 1)

    # Override : Replace the parent's version of the method
    def get_type(self):
        return "Private"

    def get_commission_rate(self):
        return 0.40

class GroupClass(Session):

    """Child class : One coach teaches many students."""
    def get_type(self):
        return "Group"

    # Override : Every student pays the hourly rate
    def get_total_fee(self):
        return self.get_hours() * self.get_rate_per_hour() * self.get_participants()

    def get_commission_rate(self):
        return 0.15

# ==========================================================
#  Section 3 : User-Defined Functions ( logic without GUI )
# ==========================================================

def make_session(session_type, session_id, coach, sport, date, hours, participants):

    """Create the correct object depending on the session type."""
    match session_type:
        case "Private":
            return PrivateSession(session_id, coach, sport, date, hours)
        case "Group":
            return GroupClass(session_id, coach, sport, date, hours, participants)
        case _:
            raise ValueError("Session type must be Private or Group.")

def is_valid_date(text):

    """Return True if the text is a real date in DD-MMM-YYYY format."""
    try:
        datetime.strptime(text, date_format)
        return True
    except ValueError:
        return False

def load_sessions():

    """Read every line from the file and return a list of session objects."""
    sessions = []
    if not os.path.exists(file_name):
        return sessions                             # First running : NO file yet

    try:
        with open(file_name, "r") as file:
            for line in file:
                line = line.strip()
                if line == "":
                    continue                        # Skip empty lines
                parts = line.split("|")
                try:
                    session = make_session(parts[0], parts[1], parts[2], parts[3],
                                           parts[4], float(parts[5]), int(parts[6]))
                    sessions.append(session)
                except (ValueError, IndexError):
                    continue                        # Skip a damaged line   
    except IOError:
        messagebox.showwarning("File Error!", "Could not read " + file_name)
    return sessions

def save_sessions(sessions):

    """Write all session records back into the file."""
    try:
        with open(file_name, "w") as file:
            for session in sessions:
                file.write(session.to_line() + "\n")
        return True
    except IOError:
        messagebox.showerror("File Error!", "Could not save " + file_name)
        return False

def generate_id(sessions):

    """Create a new ID such as S001, S002 that is not used yet."""
    used_ids = []
    for session in sessions:
        used_ids.append(session.get_session_id())

    number = 1
    # Keep counting up until the ID is not found in the list
    while "S" + str(number).zfill(3) in used_ids:
        number += 1
    return "S" + str(number).zfill(3)

def find_session(sessions, session_id):

    """Return the session with the given ID, or None if not found."""
    for session in sessions:
        if session.get_session_id() == session_id:
            return session
    return None

def get_coach_hours_on_date(sessions, coach, date, ignore_id = ""):

    """Add up the hours a coach already works on one date."""
    total = 0
    for session in sessions:
        same_coach = session.get_coach() == coach
        same_date = session.get_date() == date
        if same_coach and same_date and session.get_session_id() != ignore_id:
            total += session.get_hours()
    return total

def search_sessions(sessions, field, keyword):

    """Return the sessions that contain the keyword in the chosen field."""
    keyword = keyword.strip().lower()
    results =[]
    for session in sessions:
        match field:
            case "Session ID":
                text = session.get_session_id()
            case "Coach":
                text = session.get_coach()
            case "Sport":
                text = session.get_sport()
            case _:
                # ALL : Join every field into one long string
                text = (session.get_session_id() + " " + session.get_coach() + 
                        " " + session.get_sport() + " " + session.get_type() +
                        " " + session.get_date())

        if keyword in text.lower():
            results.append(session)
    return results

def build_coach_summary(sessions):

    """Return a dictionary : Coach name --> [total hours, total commission]."""
    # A set keeps only unique names
    coach_set = set()
    for session in sessions:
        coach_set.add(session.get_coach())

    summary = {}
    for coach in sorted(coach_set):
        summary[coach] = [0, 0]
    for session in sessions:
        summary[session.get_coach()][0] += session.get_hours()
        summary[session.get_coach()][1] += session.get_commission()
    return summary

# =======================
#  Section 4 : GUI Class
# =======================

class CoachingApp:

    """Main window of the Class & Coaching Management Module."""
    def show_records(self, session_list):
        pass
      
    def __init__(self, window):
        self.window = window
        self.window.title("Class & Coaching Management")
        self.window.geometry("780x720")

        self.sessions = load_sessions()      # list of Session objects

        # StringVar holds the value chosen by a group of radio buttons
        self.type_var = tk.StringVar(value = "Private")
        self.sport_var = tk.StringVar(value = "Swimming")
        self.search_var = tk.StringVar(value = "Coach")

        self.create_widgets()
        self.show_records(self.sessions)

    # Building the screen
    def create_widgets(self):
        tk.Label(self.window, text = "Class & Coaching Management", 
                 font = ("Times New Roman", 16, "bold")).pack(pady = 10)

        # Form area by using grid geometry manager
        form = tk.Frame(self.window)
        form.pack()

        tk.Label(form, text = "Session ID: ").grid(row = 0, column = 0, sticky = "e", pady = 3)
        self.id_entry = tk.Entry(form, width = 25)
        self.id_entry.grid(row = 0, column = 1, sticky = "w")
        tk.Label(form, text = "(Only for Load / Update / Delete)",
                 fg = "gray").grid(row = 0, column = 2, sticky = "w")

        tk.Label(form, text = "Session Type: ").grid(row = 1, column = 0, sticky = "e", pady = 3)
        type_frame = tk.Frame(form)
        type_frame.grid(row = 1, column = 1, columnspan = 2, sticky = "w")
        for session_type in session_types:
            tk.Radiobutton(type_frame, text = session_type, variable = self.type_var, 
                           value = session_type).pack(side = "left")
        
        tk.Label(form, text = "Sport: ").grid(row = 2, column = 0, sticky = "e", pady = 3)
        sport_frame = tk.Frame(form)
        sport_frame.grid(row = 2, column = 1, columnspan = 2, sticky = "w")
        for sport in sport_rates:
            tk.Radiobutton(sport_frame, text = sport, variable = self.sport_var,
                           value = sport).pack(side = "left")

        tk.Label(form, text = "Coach Name: ").grid(row = 3, column = 0, sticky = "e", pady = 3)
        self.coach_entry = tk.Entry(form, width = 25)
        self.coach_entry.grid(row = 3, column = 1, sticky = "w")

        tk.Label(form, text = "Date (DD-MMM-YYYY): ").grid(row = 4, column = 0, sticky = "e", pady = 3)
        self.date_entry = tk.Entry(form, width = 25)
        self.date_entry.grid(row = 4, column = 1, sticky = "w")
        tk.Label(form, text = "(E.g. : 01-JAN-2026)",
                 fg = "gray").grid(row = 4, column = 2, sticky = "w")

        tk.Label(form, text = "Hours: ").grid(row = 5, column = 0, sticky = "e", pady = 3)
        self.hours_entry = tk.Entry(form, width = 25)
        self.hours_entry.grid(row = 5, column = 1, sticky = "w")

        tk.Label(form, text = "Participants: ").grid(row = 6, column = 0, sticky = "e", pady = 3)
        self.people_entry = tk.Entry(form, width = 25)
        self.people_entry.grid(row = 6, column = 1, sticky = "w")
        tk.Label(form, text = "(Group only, 2 - 20)",
                 fg = "gray").grid(row = 6, column = 2, sticky = "w")

################################################## TO BE CONTINUED ##################################################

# ==============================
#  Section 5 : Start the module
# ==============================

def open_coaching_module(parent = None):

    """Called by the group's main mane. Open this module in a new window."""
    if parent is None:
        window = tk.Tk()
    else:
        window = tk.Toplevel(parent)
    CoachingApp(window)
    if parent is None:
        window.mainloop()

# Runs only when this file executed directly
if __name__ == "__main__":
    open_coaching_module()
