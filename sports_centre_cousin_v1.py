# Sports Centre Management System - simple beginner version
# Run with:  python sports_centre_simple.py
# Uses only plain functions, lists, dictionaries and loops (no classes).
# Data is saved in sports_centre_data.json (delete that file to reset the demo data).

import tkinter as tk
from tkinter import ttk, messagebox
import json
from datetime import date, timedelta

DATA_FILE = "sports_centre_data.json"
today = str(date.today())
hours = [8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21]
sports = ["Badminton", "Futsal", "Table Tennis"]
categories = ["Court Rental", "Coaching", "Retail", "Membership"]
rates = {"Badminton": 20, "Futsal": 80}          # price per hour for each sport

# court id, court name, sport
courts = [["B1", "Badminton 1", "Badminton"], ["B2", "Badminton 2", "Badminton"],
          ["B3", "Badminton 3", "Badminton"], ["F1", "Futsal A", "Futsal"], ["F2", "Futsal B", "Futsal"]]

# plan name: [fee, discount on bookings, days valid]
plans = {"Annual": [600, 0.20, 365], "Monthly": [60, 0.10, 30], "Pay-As-You-Go": [0, 0, 0],
         "VIP": [1200, 0.25, 365], "Youth": [40, 0.15, 30], "Senior": [40, 0.15, 30], "Family": [150, 0.15, 365]}


def days_from_now(n):
    return str(date.today() + timedelta(days=n))


def make_demo_data():
    d = {}
    d["next_id"] = 10
    d["members"] = [
        {"id": 1, "name": "Aiman Hakim", "phone": "012-3456789", "dob": "2001-03-12", "plan": "Monthly", "expires": days_from_now(20)},
        {"id": 2, "name": "Mei Ling Tan", "phone": "013-2223344", "dob": "1995-07-30", "plan": "VIP", "expires": days_from_now(200)},
        {"id": 3, "name": "Ravi Kumar", "phone": "016-7788990", "dob": "1988-01-05", "plan": "Annual", "expires": days_from_now(90)},
        {"id": 4, "name": "Siti Aminah", "phone": "011-5566778", "dob": "2008-09-14", "plan": "Pay-As-You-Go", "expires": "-"}]
    d["bookings"] = [
        {"id": 1, "court": "B1", "date": today, "start": 18, "hours": 2, "member": 1, "paid": 36.0},
        {"id": 2, "court": "F1", "date": today, "start": 20, "hours": 1, "member": 0, "paid": 80.0}]
    d["coaches"] = [{"id": 1, "name": "Coach Daniel", "rate": 0.30, "hours": 0, "commission": 0.0},
                    {"id": 2, "name": "Coach Farah", "rate": 0.35, "hours": 0, "commission": 0.0}]
    d["classes"] = [
        {"id": 1, "name": "Badminton Clinic", "type": "Group", "coach": 1, "time": "Sat 09:00", "hours": 2, "max": 8, "fee": 30.0, "enrolled": [1, 2]},
        {"id": 2, "name": "Yoga Flow", "type": "Group", "coach": 2, "time": "Sun 08:00", "hours": 1, "max": 12, "fee": 20.0, "enrolled": [3]},
        {"id": 3, "name": "Private Futsal Drill", "type": "Private", "coach": 1, "time": "Wed 17:00", "hours": 1, "max": 1, "fee": 60.0, "enrolled": []}]
    d["rankings"] = {"Badminton": [{"member": 1, "rating": 1024, "won": 3, "lost": 1}, {"member": 2, "rating": 1011, "won": 2, "lost": 2},
                                   {"member": 3, "rating": 985, "won": 1, "lost": 2}, {"member": 4, "rating": 980, "won": 1, "lost": 2}],
                     "Futsal": [], "Table Tennis": []}
    d["products"] = [{"id": 1, "name": "Mineral Water", "price": 2.0, "stock": 50}, {"id": 2, "name": "Isotonic Drink", "price": 4.0, "stock": 40},
                     {"id": 3, "name": "Shuttlecock Tube", "price": 35.0, "stock": 15}, {"id": 4, "name": "Grip Tape", "price": 8.0, "stock": 25},
                     {"id": 5, "name": "Sports Towel", "price": 15.0, "stock": 12}, {"id": 6, "name": "Energy Bar", "price": 3.5, "stock": 30}]
    d["payments"] = [
        {"date": today, "category": "Court Rental", "amount": 36.0, "reference": "Booking #1"},
        {"date": today, "category": "Court Rental", "amount": 80.0, "reference": "Booking #2"},
        {"date": today, "category": "Retail", "amount": 11.0, "reference": "POS sale"},
        {"date": today, "category": "Membership", "amount": 60.0, "reference": "Monthly - Aiman Hakim"},
        {"date": days_from_now(-1), "category": "Coaching", "amount": 50.0, "reference": "Badminton Clinic"}]
    return d


def load_data():
    try:
        file = open(DATA_FILE)
        loaded = json.load(file)
        file.close()
        return loaded
    except (OSError, ValueError):
        return make_demo_data()


def save_data():
    file = open(DATA_FILE, "w")
    json.dump(data, file, indent=1)
    file.close()


data = load_data()
root = tk.Tk()
root.title("Sports Centre Management System")
root.geometry("1100x720")

# ---------------------------------------------------------------- helper functions

def money(amount):
    return "RM " + format(amount, ".2f")


def warn(message):
    messagebox.showwarning("Check your input", message)


def new_id():
    data["next_id"] = data["next_id"] + 1
    return data["next_id"]


def add_payment(category, amount, reference):
    data["payments"].append({"date": today, "category": category, "amount": amount, "reference": reference})


def member_name(member_id):
    if member_id == 0:
        return "Walk-in guest"
    for m in data["members"]:
        if m["id"] == member_id:
            return m["name"]
    return "Unknown"


def member_discount(member_id):
    # a member only gets the discount while the membership has not expired
    for m in data["members"]:
        if m["id"] == member_id:
            if m["expires"] == "-" or m["expires"] >= today:
                return plans[m["plan"]][1]
    return 0


def member_choices(include_guest):
    choices = []
    if include_guest:
        choices.append("0 - Walk-in guest")
    for m in data["members"]:
        choices.append(str(m["id"]) + " - " + m["name"])
    return choices


def get_id(text):
    # "3 - Ravi Kumar" -> 3
    return int(text.split(" - ")[0])


def set_choices(box, choices):
    box["values"] = choices
    if box.get() not in choices and len(choices) > 0:
        box.set(choices[0])


def make_table(parent, columns, height):
    table = ttk.Treeview(parent, columns=columns, show="headings", height=height)
    for c in columns:
        table.heading(c, text=c)
        table.column(c, width=130)
    return table


def clear_table(table):
    for row in table.get_children():
        table.delete(row)


def read_date(variable):
    text = variable.get().strip()
    try:
        date.fromisoformat(text)
        return text
    except ValueError:
        warn("Enter the date as YYYY-MM-DD.")
        variable.set(today)
        return today


def find_coach(coach_id):
    for k in data["coaches"]:
        if k["id"] == coach_id:
            return k


def find_product(product_id):
    for p in data["products"]:
        if p["id"] == product_id:
            return p


def get_court(court_name):
    for c in courts:
        if c[1] == court_name:
            return c


def find_booking(court_id, day, hour):
    # returns the booking that covers this court, date and hour (or None)
    for b in data["bookings"]:
        if b["court"] == court_id and b["date"] == day and hour >= b["start"] and hour < b["start"] + b["hours"]:
            return b
    return None


def get_rating(player):
    return player["rating"]


# ---------------------------------------------------------------- 1. court booking

cell_info = {}      # remembers which court and hour each calendar cell stands for


def cell_clicked(event):
    # event.widget is the cell that was clicked
    info = cell_info[event.widget]
    if info[0] == "free":
        # free cell: fill in the court and start hour in the booking form
        court_box.set(info[1])
        start_box.set(info[2])
        update_price()
        selected_label.config(text="Selected: " + info[1] + " at " + str(info[2]) + ":00. Choose the hours and customer, then press Book now.")
    else:
        # booked cell: select that booking in the table so it can be cancelled
        booking_table.selection_set(str(info[1]))
        selected_label.config(text="Booking #" + str(info[1]) + " is selected in the table below. Press Cancel to remove it.")


def draw_grid():
    for w in grid_frame.winfo_children():
        w.destroy()
    cell_info.clear()
    day = read_date(book_date)
    col = 1
    for h in hours:
        tk.Label(grid_frame, text=str(h) + ":00").grid(row=0, column=col)
        col = col + 1
    row = 1
    for c in courts:
        tk.Label(grid_frame, text=c[1], width=12, anchor="w").grid(row=row, column=0)
        col = 1
        for h in hours:
            b = find_booking(c[0], day, h)
            if b is None:
                cell = tk.Label(grid_frame, text="", bg="#c8f0d8", width=7, height=2, relief="ridge")
                if day >= today:
                    cell.config(cursor="hand2")
                    cell.bind("<Button-1>", cell_clicked)
                    cell_info[cell] = ["free", c[1], h]
            else:
                text = ""
                if b["start"] == h:
                    text = member_name(b["member"]).split(" ")[0]
                cell = tk.Label(grid_frame, text=text, bg="#f5b7b1", width=7, height=2, relief="ridge", cursor="hand2")
                cell.bind("<Button-1>", cell_clicked)
                cell_info[cell] = ["booked", b["id"]]
            cell.grid(row=row, column=col)
            col = col + 1
        row = row + 1


def calculate_price():
    court = get_court(court_box.get())
    hrs = int(hours_box.get())
    discount = member_discount(get_id(customer_box.get()))
    return rates[court[2]] * hrs * (1 - discount)


def update_price(event=None):
    if customer_box.get() != "":
        price_label.config(text="Total: " + money(calculate_price()))


def book_now():
    day = read_date(book_date)
    if day < today:
        warn("You cannot book a date in the past.")
        return
    court = get_court(court_box.get())
    start = int(start_box.get())
    hrs = int(hours_box.get())
    if start + hrs > 22:
        warn("Bookings must end by 22:00.")
        return
    for h in range(start, start + hrs):
        if find_booking(court[0], day, h) is not None:
            warn("That time overlaps an existing booking.")
            return
    price = calculate_price()
    booking_id = new_id()
    data["bookings"].append({"id": booking_id, "court": court[0], "date": day, "start": start,
                             "hours": hrs, "member": get_id(customer_box.get()), "paid": price})
    add_payment("Court Rental", price, "Booking #" + str(booking_id))
    messagebox.showinfo("Booked", court[1] + " booked on " + day + ".\nPaid: " + money(price))
    refresh_all()


def cancel_booking():
    selected = booking_table.selection()
    if len(selected) == 0:
        warn("Select a booking in the table first.")
        return
    booking_id = int(selected[0])
    for b in data["bookings"]:
        if b["id"] == booking_id:
            if messagebox.askyesno("Cancel booking", "Cancel booking #" + str(booking_id) + " and refund " + money(b["paid"]) + "?"):
                data["bookings"].remove(b)
                add_payment("Court Rental", -b["paid"], "Refund #" + str(booking_id))
                refresh_all()
            return


def refresh_booking():
    draw_grid()
    selected_label.config(text="Click a green cell to choose a time, or a red cell to select that booking.")
    set_choices(customer_box, member_choices(True))
    update_price()
    clear_table(booking_table)
    day = read_date(book_date)
    for b in data["bookings"]:
        if b["date"] == day:
            court = ""
            for c in courts:
                if c[0] == b["court"]:
                    court = c[1]
            time = str(b["start"]) + ":00 - " + str(b["start"] + b["hours"]) + ":00"
            booking_table.insert("", "end", iid=str(b["id"]), values=(b["id"], court, time, member_name(b["member"]), money(b["paid"])))


# ---------------------------------------------------------------- 2. membership

def register_member():
    name = name_var.get().strip()
    phone = phone_var.get().strip()
    dob = dob_var.get().strip()
    plan = plan_box.get()
    if name == "" or phone == "" or dob == "":
        warn("Fill in name, phone and date of birth.")
        return
    if len(phone) < 8 or not phone.replace("-", "").replace("+", "").isdigit():
        warn("Enter a valid phone number, for example 012-3456789.")
        return
    try:
        age = (date.today() - date.fromisoformat(dob)).days // 365
    except ValueError:
        warn("Enter the date of birth as YYYY-MM-DD.")
        return
    if age < 0:
        warn("The date of birth cannot be in the future.")
        return
    if plan == "Youth" and age > 17:
        warn("The Youth plan is for ages 17 and under.")
        return
    if plan == "Senior" and age < 60:
        warn("The Senior plan is for ages 60 and over.")
        return
    fee = plans[plan][0]
    days = plans[plan][2]
    expires = "-"
    if days > 0:
        expires = days_from_now(days)
    data["members"].append({"id": new_id(), "name": name, "phone": phone, "dob": dob, "plan": plan, "expires": expires})
    if fee > 0:
        add_payment("Membership", fee, plan + " - " + name)
    name_var.set("")
    phone_var.set("")
    dob_var.set("")
    messagebox.showinfo("Registered", name + " is now a " + plan + " member.\nFee collected: " + money(fee))
    refresh_all()


def refresh_members():
    clear_table(member_table)
    for m in data["members"]:
        status = "Active"
        if m["expires"] != "-" and m["expires"] < today:
            status = "Expired"
        member_table.insert("", "end", values=(m["name"], m["phone"], m["plan"], m["expires"], status))


# ---------------------------------------------------------------- 3. coaching and classes

def get_selected_class():
    selected = class_table.selection()
    if len(selected) == 0:
        warn("Select a class in the table first.")
        return None
    for c in data["classes"]:
        if c["id"] == int(selected[0]):
            return c


def enrol_member():
    c = get_selected_class()
    if c is None or participant_box.get() == "":
        return
    member_id = get_id(participant_box.get())
    if member_id in c["enrolled"]:
        warn(member_name(member_id) + " is already enrolled.")
        return
    if len(c["enrolled"]) >= c["max"]:
        warn("This class is full.")
        return
    c["enrolled"].append(member_id)
    coach = find_coach(c["coach"])
    coach["commission"] = coach["commission"] + c["fee"] * coach["rate"]     # coach earns a share of the fee
    add_payment("Coaching", c["fee"], c["name"] + " - " + member_name(member_id))
    messagebox.showinfo("Enrolled", member_name(member_id) + " enrolled.\nFee collected: " + money(c["fee"]))
    refresh_all()


def log_session():
    c = get_selected_class()
    if c is None:
        return
    if len(c["enrolled"]) == 0:
        warn("Enrol at least one participant first.")
        return
    coach = find_coach(c["coach"])
    coach["hours"] = coach["hours"] + c["hours"]
    messagebox.showinfo("Session logged", str(c["hours"]) + " hour(s) added for " + coach["name"] + ".")
    refresh_all()


def refresh_classes():
    set_choices(participant_box, member_choices(False))
    selected = class_table.selection()
    clear_table(class_table)
    clear_table(coach_table)
    for c in data["classes"]:
        coach = find_coach(c["coach"])
        class_table.insert("", "end", iid=str(c["id"]),
                           values=(c["name"], c["type"], coach["name"], c["time"], str(len(c["enrolled"])) + "/" + str(c["max"]), money(c["fee"])))
    if len(selected) > 0 and class_table.exists(selected[0]):
        class_table.selection_set(selected[0])
    for k in data["coaches"]:
        coach_table.insert("", "end", values=(k["name"], str(round(k["rate"] * 100)) + "%", k["hours"], money(k["commission"])))


# ---------------------------------------------------------------- 4. player rankings

def find_player(sport, member_id):
    # finds the player's record for a sport, or creates one starting at rating 1000
    for p in data["rankings"][sport]:
        if p["member"] == member_id:
            return p
    new_player = {"member": member_id, "rating": 1000, "won": 0, "lost": 0}
    data["rankings"][sport].append(new_player)
    return new_player


def save_result():
    sport = rank_sport.get()
    if player_a_box.get() == "" or player_b_box.get() == "":
        warn("Register at least two members first.")
        return
    a = get_id(player_a_box.get())
    b = get_id(player_b_box.get())
    if a == b:
        warn("Choose two different players.")
        return
    try:
        score_a = int(score_a_var.get())
        score_b = int(score_b_var.get())
    except ValueError:
        warn("Enter both scores as whole numbers.")
        return
    if score_a == score_b:
        warn("A game needs a winner. Scores cannot be tied.")
        return
    player_a = find_player(sport, a)
    player_b = find_player(sport, b)
    # Elo rating: the lower-rated player gains more for beating a higher-rated player
    expected_a = 1 / (1 + 10 ** ((player_b["rating"] - player_a["rating"]) / 400))
    if score_a > score_b:
        result_a = 1
        player_a["won"] = player_a["won"] + 1
        player_b["lost"] = player_b["lost"] + 1
    else:
        result_a = 0
        player_b["won"] = player_b["won"] + 1
        player_a["lost"] = player_a["lost"] + 1
    player_a["rating"] = round(player_a["rating"] + 32 * (result_a - expected_a))
    player_b["rating"] = round(player_b["rating"] + 32 * ((1 - result_a) - (1 - expected_a)))
    score_a_var.set("")
    score_b_var.set("")
    refresh_all()


def refresh_rankings():
    set_choices(player_a_box, member_choices(False))
    set_choices(player_b_box, member_choices(False))
    clear_table(leaderboard)
    players = list(data["rankings"][rank_sport.get()])
    players.sort(key=get_rating, reverse=True)
    place = 1
    for p in players:
        leaderboard.insert("", "end", values=(place, member_name(p["member"]), p["rating"], p["won"], p["lost"]))
        place = place + 1


def sport_changed(event):
    # called when a different sport is chosen in the drop-down list
    refresh_rankings()


# ---------------------------------------------------------------- 5. billing and finance

cart = []        # each item is [product id, quantity]


def add_to_cart():
    if product_box.get() == "":
        return
    product = find_product(get_id(product_box.get()))
    try:
        qty = int(qty_var.get())
    except ValueError:
        warn("Quantity must be a whole number.")
        return
    if qty < 1:
        warn("Quantity must be at least 1.")
        return
    for item in cart:
        if item[0] == product["id"]:
            if item[1] + qty > product["stock"]:
                warn("Not enough " + product["name"] + " in stock.")
                return
            item[1] = item[1] + qty
            refresh_shop()
            return
    if qty > product["stock"]:
        warn("Not enough " + product["name"] + " in stock.")
        return
    cart.append([product["id"], qty])
    refresh_shop()


def remove_from_cart():
    selected = cart_table.selection()
    if len(selected) == 0:
        warn("Select an item in the cart first.")
        return
    for item in cart:
        if item[0] == int(selected[0]):
            item[1] = item[1] - 1
            if item[1] == 0:
                cart.remove(item)
            break
    refresh_shop()


def checkout():
    if len(cart) == 0:
        warn("Add at least one product first.")
        return
    customer = member_name(get_id(customer_pos_box.get()))
    total = 0
    receipt = ""
    for item in cart:
        product = find_product(item[0])
        line = product["price"] * item[1]
        total = total + line
        product["stock"] = product["stock"] - item[1]
        receipt = receipt + product["name"] + " x " + str(item[1]) + "   " + money(line) + "\n"
    add_payment("Retail", total, "POS sale - " + customer + " (" + method_box.get() + ")")
    messagebox.showinfo("Receipt", today + "\n" + customer + " - " + method_box.get() + "\n\n" + receipt + "\nTotal: " + money(total))
    cart.clear()
    refresh_all()


def refresh_shop():
    set_choices(customer_pos_box, member_choices(True))
    choices = []
    for p in data["products"]:
        choices.append(str(p["id"]) + " - " + p["name"] + " (" + money(p["price"]) + ", " + str(p["stock"]) + " left)")
    product_box["values"] = choices
    if product_box.get() == "" or product_box.current() == -1:
        product_box.set(choices[0])
    clear_table(cart_table)
    total = 0
    for item in cart:
        product = find_product(item[0])
        total = total + product["price"] * item[1]
        cart_table.insert("", "end", iid=str(item[0]), values=(product["name"], item[1], money(product["price"] * item[1])))
    total_label.config(text="Total: " + money(total))


def refresh_revenue():
    day = read_date(revenue_date)
    clear_table(payment_table)
    totals = {}
    for c in categories:
        totals[c] = 0
    for p in data["payments"]:
        if p["date"] == day:
            totals[p["category"]] = totals[p["category"]] + p["amount"]
            payment_table.insert("", "end", values=(p["category"], p["reference"], money(p["amount"])))
    grand = 0
    for c in categories:
        category_labels[c].config(text=money(totals[c]))
        grand = grand + totals[c]
    grand_label.config(text="Grand total for " + day + ": " + money(grand))


def refresh_all():
    save_data()
    refresh_booking()
    refresh_members()
    refresh_classes()
    refresh_rankings()
    refresh_shop()
    refresh_revenue()


# ================================================================ build the windows
notebook = ttk.Notebook(root)
notebook.pack(fill="both", expand=True)

# ---------- tab 1: court booking
tab1 = ttk.Frame(notebook, padding=10)
notebook.add(tab1, text="Court Booking")
book_date = tk.StringVar(value=today)
top = ttk.Frame(tab1)
top.pack(fill="x")
ttk.Label(top, text="Date (YYYY-MM-DD):").pack(side="left")
ttk.Entry(top, textvariable=book_date, width=12).pack(side="left", padx=5)
ttk.Button(top, text="Show date", command=refresh_booking).pack(side="left")
ttk.Label(top, text="     Green = free (click to book)     Red = booked (click to select)").pack(side="left")
grid_frame = ttk.Frame(tab1)
grid_frame.pack(anchor="w", pady=8)
selected_label = ttk.Label(tab1, text="")
selected_label.pack(anchor="w")

form = ttk.LabelFrame(tab1, text="New booking", padding=8)
form.pack(fill="x")
court_names = []
for c in courts:
    court_names.append(c[1])
ttk.Label(form, text="Court").grid(row=0, column=0, sticky="w")
court_box = ttk.Combobox(form, values=court_names, state="readonly", width=14)
court_box.grid(row=1, column=0, padx=5)
court_box.current(0)
ttk.Label(form, text="Start hour").grid(row=0, column=1, sticky="w")
start_box = ttk.Combobox(form, values=hours, state="readonly", width=6)
start_box.grid(row=1, column=1, padx=5)
start_box.current(10)
ttk.Label(form, text="Number of hours").grid(row=0, column=2, sticky="w")
hours_box = ttk.Combobox(form, values=[1, 2, 3, 4], state="readonly", width=6)
hours_box.grid(row=1, column=2, padx=5)
hours_box.current(0)
ttk.Label(form, text="Customer").grid(row=0, column=3, sticky="w")
customer_box = ttk.Combobox(form, state="readonly", width=22)
customer_box.grid(row=1, column=3, padx=5)
price_label = ttk.Label(form, text="", font=("Arial", 11, "bold"))
price_label.grid(row=1, column=4, padx=10)
ttk.Button(form, text="Book now", command=book_now).grid(row=1, column=5)
for box in [court_box, start_box, hours_box, customer_box]:
    box.bind("<<ComboboxSelected>>", update_price)

ttk.Label(tab1, text="Bookings on the selected date:").pack(anchor="w", pady=(10, 2))
booking_table = make_table(tab1, ("ID", "Court", "Time", "Customer", "Paid"), 5)
booking_table.pack(fill="x")
ttk.Button(tab1, text="Cancel selected booking", command=cancel_booking).pack(anchor="w", pady=5)

# ---------- tab 2: membership
tab2 = ttk.Frame(notebook, padding=10)
notebook.add(tab2, text="Membership")
plan_table = make_table(tab2, ("Plan", "Fee", "Booking discount", "Valid for"), 7)
plan_table.pack(fill="x")
for name in plans:
    fee = plans[name][0]
    days = plans[name][2]
    fee_text = "Pay per visit"
    if fee > 0:
        fee_text = money(fee)
    days_text = "No expiry"
    if days > 0:
        days_text = str(days) + " days"
    plan_table.insert("", "end", values=(name, fee_text, str(round(plans[name][1] * 100)) + "%", days_text))

name_var = tk.StringVar()
phone_var = tk.StringVar()
dob_var = tk.StringVar()
form2 = ttk.LabelFrame(tab2, text="New member", padding=8)
form2.pack(fill="x", pady=8)
ttk.Label(form2, text="Full name").grid(row=0, column=0, sticky="w")
ttk.Entry(form2, textvariable=name_var, width=24).grid(row=1, column=0, padx=5)
ttk.Label(form2, text="Phone").grid(row=0, column=1, sticky="w")
ttk.Entry(form2, textvariable=phone_var, width=16).grid(row=1, column=1, padx=5)
ttk.Label(form2, text="Date of birth (YYYY-MM-DD)").grid(row=0, column=2, sticky="w")
ttk.Entry(form2, textvariable=dob_var, width=16).grid(row=1, column=2, padx=5)
ttk.Label(form2, text="Plan").grid(row=0, column=3, sticky="w")
plan_box = ttk.Combobox(form2, values=list(plans.keys()), state="readonly", width=14)
plan_box.grid(row=1, column=3, padx=5)
plan_box.current(1)
ttk.Button(form2, text="Register and pay", command=register_member).grid(row=1, column=4, padx=5)
member_table = make_table(tab2, ("Name", "Phone", "Plan", "Expires", "Status"), 8)
member_table.pack(fill="both", expand=True)

# ---------- tab 3: coaching and classes
tab3 = ttk.Frame(notebook, padding=10)
notebook.add(tab3, text="Coaching & Classes")
class_table = make_table(tab3, ("Class", "Type", "Coach", "Time", "Enrolled", "Fee"), 6)
class_table.pack(fill="x")
row3 = ttk.Frame(tab3)
row3.pack(fill="x", pady=8)
ttk.Label(row3, text="Participant:").pack(side="left")
participant_box = ttk.Combobox(row3, state="readonly", width=24)
participant_box.pack(side="left", padx=5)
ttk.Button(row3, text="Enrol in selected class", command=enrol_member).pack(side="left")
ttk.Button(row3, text="Log selected session", command=log_session).pack(side="left", padx=5)
ttk.Label(tab3, text="Coach hours and commission:").pack(anchor="w")
coach_table = make_table(tab3, ("Coach", "Commission rate", "Hours worked", "Commission earned"), 4)
coach_table.pack(fill="x")

# ---------- tab 4: rankings
tab4 = ttk.Frame(notebook, padding=10)
notebook.add(tab4, text="Rankings")
rank_sport = ttk.Combobox(tab4, values=sports, state="readonly", width=14)
ttk.Label(tab4, text="Sport:").pack(anchor="w")
rank_sport.pack(anchor="w", pady=4)
rank_sport.current(0)
rank_sport.bind("<<ComboboxSelected>>", sport_changed)
score_a_var = tk.StringVar()
score_b_var = tk.StringVar()
form4 = ttk.LabelFrame(tab4, text="Log a game", padding=8)
form4.pack(fill="x", pady=8)
ttk.Label(form4, text="Player A").grid(row=0, column=0, sticky="w")
player_a_box = ttk.Combobox(form4, state="readonly", width=22)
player_a_box.grid(row=1, column=0, padx=5)
ttk.Label(form4, text="Score A").grid(row=0, column=1, sticky="w")
ttk.Entry(form4, textvariable=score_a_var, width=6).grid(row=1, column=1, padx=5)
ttk.Label(form4, text="Player B").grid(row=0, column=2, sticky="w")
player_b_box = ttk.Combobox(form4, state="readonly", width=22)
player_b_box.grid(row=1, column=2, padx=5)
ttk.Label(form4, text="Score B").grid(row=0, column=3, sticky="w")
ttk.Entry(form4, textvariable=score_b_var, width=6).grid(row=1, column=3, padx=5)
ttk.Button(form4, text="Save result", command=save_result).grid(row=1, column=4, padx=5)
leaderboard = make_table(tab4, ("Rank", "Player", "Rating", "Won", "Lost"), 12)
leaderboard.pack(fill="both", expand=True)

# ---------- tab 5: billing and finance
tab5 = ttk.Frame(notebook, padding=10)
notebook.add(tab5, text="Billing & Finance")
finance_tabs = ttk.Notebook(tab5)
finance_tabs.pack(fill="both", expand=True)

pos_tab = ttk.Frame(finance_tabs, padding=10)
finance_tabs.add(pos_tab, text="Retail point of sale")
qty_var = tk.StringVar(value="1")
ttk.Label(pos_tab, text="Product").grid(row=0, column=0, sticky="w")
product_box = ttk.Combobox(pos_tab, state="readonly", width=44)
product_box.grid(row=1, column=0, padx=5)
ttk.Label(pos_tab, text="Quantity").grid(row=0, column=1, sticky="w")
ttk.Entry(pos_tab, textvariable=qty_var, width=6).grid(row=1, column=1, padx=5)
ttk.Button(pos_tab, text="Add to cart", command=add_to_cart).grid(row=1, column=2, padx=5)
cart_table = make_table(pos_tab, ("Item", "Qty", "Amount"), 8)
cart_table.grid(row=2, column=0, columnspan=3, pady=8, sticky="ew")
ttk.Button(pos_tab, text="Remove one of selected item", command=remove_from_cart).grid(row=3, column=0, sticky="w")
total_label = ttk.Label(pos_tab, text="Total: RM 0.00", font=("Arial", 14, "bold"))
total_label.grid(row=4, column=0, sticky="w", pady=6)
ttk.Label(pos_tab, text="Customer").grid(row=5, column=0, sticky="w")
customer_pos_box = ttk.Combobox(pos_tab, state="readonly", width=24)
customer_pos_box.grid(row=6, column=0, sticky="w", padx=5)
ttk.Label(pos_tab, text="Payment method").grid(row=5, column=1, sticky="w")
method_box = ttk.Combobox(pos_tab, values=["Cash", "Card", "E-wallet"], state="readonly", width=12)
method_box.grid(row=6, column=1, padx=5)
method_box.current(0)
ttk.Button(pos_tab, text="Charge and show receipt", command=checkout).grid(row=6, column=2, padx=5)

rev_tab = ttk.Frame(finance_tabs, padding=10)
finance_tabs.add(rev_tab, text="Daily revenue summary")
revenue_date = tk.StringVar(value=today)
rev_top = ttk.Frame(rev_tab)
rev_top.pack(fill="x")
ttk.Label(rev_top, text="Date (YYYY-MM-DD):").pack(side="left")
ttk.Entry(rev_top, textvariable=revenue_date, width=12).pack(side="left", padx=5)
ttk.Button(rev_top, text="Show summary", command=refresh_revenue).pack(side="left")
summary_box = ttk.LabelFrame(rev_tab, text="Revenue by category", padding=8)
summary_box.pack(fill="x", pady=8)
category_labels = {}
row = 0
for c in categories:
    ttk.Label(summary_box, text=c, width=16).grid(row=row, column=0, sticky="w")
    category_labels[c] = ttk.Label(summary_box, text="RM 0.00", font=("Arial", 11, "bold"))
    category_labels[c].grid(row=row, column=1, sticky="w")
    row = row + 1
grand_label = ttk.Label(summary_box, text="", font=("Arial", 13, "bold"))
grand_label.grid(row=row, column=0, columnspan=2, sticky="w", pady=(8, 0))
payment_table = make_table(rev_tab, ("Category", "Reference", "Amount"), 8)
payment_table.pack(fill="both", expand=True)

# ---------- start the program
refresh_all()
root.mainloop()
