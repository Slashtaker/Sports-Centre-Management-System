# Coaching & Class Management Module: assigns coaches to private sessions or
# group classes (e.g., swimming lessons, badminton clinics, yoga) as well as
# tracking of coach commissions and working hours.
# JONATHAN

from tkinter import ttk

class CoachingManagement:
	
	def __init__(self):
		self.coaches = []
		self.classes = []
		self.sessions = []

	def draw_tab(self, notebook):
		# tab 3: coaching and classes
		tab3 = ttk.Frame(notebook, padding=10)
		notebook.add(tab3, text="Coaching & Classes")

