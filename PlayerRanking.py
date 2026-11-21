# Player Rankings & Ratings Module: logs casual game results to maintain internal
# leaderboard rankings for various games/sports.
# LEE MIN XIAN

from tkinter import ttk

class PlayerRanking:
	
	def __init__(self):
		self.players = []
		self.rankings = {}

	def draw_tab(self, notebook):
		# tab 4: player rankings
		tab4 = ttk.Frame(notebook, padding=10)
		notebook.add(tab4, text="Player Rankings")