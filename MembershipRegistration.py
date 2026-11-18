# Membership Registration Module: enables public to register for various
# membership types (e.g., Annual, Monthly, Pay-As-You-Go, VIP, Youth, Senior,
# Family).
# TAN GAO SHEN

from tkinter import ttk

class MembershipRegistration:

	def __init__(self):
		self.membership_types = ["Annual", "Monthly", "Pay-As-You-Go", "VIP", "Youth", "Senior", "Family"]
		self.membership_fees = {
			"Annual": 500,
			"Monthly": 50,
			"Pay-As-You-Go": 10,
			"VIP": 1000,
			"Youth": 30,
			"Senior": 40,
			"Family": 150
		}

	def draw_tab(self, notebook):
		# tab 2: membership
		tab2 = ttk.Frame(notebook, padding=10)
		notebook.add(tab2, text="Membership")