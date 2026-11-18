# Billing, Payments & Finance Module: generate daily revenue summaries
# separating court rentals, coaching, retail sales, and membership fees.
# YONG ZHENG HANG

import Utils
from tkinter import ttk

class FinanceManagement:
	def __init__(self):
		self.tax = 0.06 # 6% tax rate
		self.retail_products = {
			"mineral water": 1.50,
			"energy drink": 3.00,
			"protein bar": 2.50,
			"towel": 5.00,
			"sportswear": 20.00
		}

		self.payment_methods = ["Cash", "Credit Card", "Debit Card", "Mobile Payment"]

	def draw_tab(self, notebook):
		# ---------- tab 5: billing and finance
		tab5 = ttk.Frame(notebook, padding=10)
		notebook.add(tab5, text="Billing & Finance")

	def calculate_revenue(self, court_rentals, coaching_fees, retail_sales, membership_fees):
		# Calculate total revenue for each category
		total_court_rentals = sum(court_rentals)
		total_coaching_fees = sum(coaching_fees)
		total_retail_sales = sum(retail_sales)
		total_membership_fees = sum(membership_fees)

		# Calculate total revenue before tax
		total_revenue_before_tax = total_court_rentals + total_coaching_fees + total_retail_sales + total_membership_fees

		# Calculate tax amount
		tax_amount = total_revenue_before_tax * self.tax

		# Calculate total revenue after tax
		total_revenue_after_tax = total_revenue_before_tax - tax_amount

		return {
			"total_court_rentals": total_court_rentals,
			"total_coaching_fees": total_coaching_fees,
			"total_retail_sales": total_retail_sales,
			"total_membership_fees": total_membership_fees,
			"total_revenue_before_tax": total_revenue_before_tax,
			"tax_amount": tax_amount,
			"total_revenue_after_tax": total_revenue_after_tax
		}
	



	

