import tkinter as tk , Finance
from tkinter import ttk, messagebox

class SportsManagementSystem:
    def __init__(self):
        self.name = "Sports Centre Management System"
        self.version = "1.0"
        self.root = tk.Tk()

        self.is_admin = False

        # Create the main window
        self.root.title(self.name + " v" + self.version)


        self.notebook = ttk.Notebook(self.root)   # pack it later in admin(), after login

    def draw_tab(self):
        # tab 1: court booking
        tab1 = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(tab1, text="Court Booking")

        # tab 2: membership
        tab2 = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(tab2, text="Membership")

        # tab 3: coaching and classes
        tab3 = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(tab3, text="Coaching & Classes")

        # ---------- tab 4: rankings
        tab4 = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(tab4, text="Rankings")

        # ---------- tab 5: billing and finance
        tab5 = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(tab5, text="Billing & Finance")



    def run(self):

        self.login()
        if self.is_admin:
            self.admin()
        else:
            self.user()


        # Start the main event loop (skip it if the window was closed during login)
        if self.root.winfo_exists():
            self.root.mainloop()

    def login(self):

        login_frame = ttk.Frame(self.root, padding=30)
        login_frame.pack(fill="both", expand=True)

        tk.Label(login_frame, text="Username:").grid(row=0, column=1, sticky="w", pady=5)
        tk.Label(login_frame, text="Password:").grid(row=1, column=1, sticky="w", pady=5)
        user_entry = tk.Entry(login_frame, width=20)
        user_entry.grid(row=0, column=2, padx=5)
        pass_entry = tk.Entry(login_frame, width=20, show="*")
        pass_entry.grid(row=1, column=2, padx=5)
        ttk.Button(login_frame, text="Login", command=lambda: self.check_login(login_frame, user_entry, pass_entry)).grid(row=2, column=2, pady=10)
        self.root.resizable(False, False)

        self.root.wait_window(login_frame)

    def check_login(self, frame, user_entry, pass_entry):

        if user_entry.get() == "admin" and pass_entry.get() == "1234":
            self.is_admin = True
            frame.destroy()

        elif user_entry.get() == "user" and pass_entry.get() == "1234":
            frame.destroy()

        else:
            messagebox.showerror("Login failed", "Wrong username or password")



    def admin(self):
        pass

    def user(self):
        self.notebook.pack(fill="both", expand=True)
        self.root.geometry("1300x800")
        self.root.resizable(True, True)

        self.draw_tab()


if __name__ == "__main__":
    sports_management_system = SportsManagementSystem()
    sports_management_system.run()