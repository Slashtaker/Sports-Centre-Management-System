# Billing, Payments & Finance Module: generate daily revenue summaries
# separating court rentals, coaching, retail sales, and membership fees.
# YONG ZHENG HANG

from time import time
from tkinter import ttk, messagebox

import Utils


class FinanceManagement:
    def __init__(self):
        self.tax = 0.06  # 6% tax rate
        self.retail_products = {
            "mineral water": 1.50,
            "energy drink": 3.00,
            "protein bar": 2.50,
            "towel": 5.00,
            "sportswear": 20.00,
        }

        self.read_file = Utils.read_json(".//data//receipts.json")

        self.payment_methods = ["Cash", "Credit Card", "Debit Card", "Mobile Payment"]
        self.items = list(self.retail_products.keys())

        self.var_payment_method = "Cash"
        self.var_items = []
        self.var_quantity = []
        self.var_price = []

    def draw_tab(self, notebook):
        # tab 5: billing and finance
        tab5 = ttk.Frame(notebook, padding=10)
        notebook.add(tab5, text="Billing & Finance")

        payment_combobox = ttk.Combobox(tab5, values=self.payment_methods)
        payment_combobox.grid(row=0, column=0)
        payment_combobox.set(self.payment_methods[0])

        payment_form = ttk.Frame(tab5)
        payment_form.grid(row=5, column=0, columnspan=2, sticky="w", pady=(10, 0))

        payment_combobox.bind(
            "<<ComboboxSelected>>",
            lambda event: self.on_payment_selected(event, payment_form),
        )

    def calculate_revenue(
        self, court_rentals, coaching_fees, retail_sales, membership_fees
    ):
        # Calculate total revenue for each category
        total_court_rentals = sum(court_rentals)
        total_coaching_fees = sum(coaching_fees)
        total_retail_sales = sum(retail_sales)
        total_membership_fees = sum(membership_fees)

        # Calculate total revenue before tax
        total_revenue_before_tax = (
            total_court_rentals
            + total_coaching_fees
            + total_retail_sales
            + total_membership_fees
        )

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
            "total_revenue_after_tax": total_revenue_after_tax,
        }

    def on_payment_selected(self, event, payment_form: ttk.Frame):
        # Remove the previous method widgets before drawing the new form.
        for widget in payment_form.winfo_children():
            widget.destroy()

        selected_payment = event.widget.get()
        self.var_payment_method = selected_payment
        if selected_payment in ["Credit Card", "Debit Card"]:
            fields = ["Card Number:", "Expiry Date:", "CVV:"]
        elif selected_payment == "Mobile Payment":
            fields = ["Phone Number:", "Password:"]
        else:
            return

        for row, label_text in enumerate(fields):
            ttk.Label(payment_form, text=label_text).grid(
                row=row, column=0, sticky="w", padx=(0, 8), pady=3
            )
            ttk.Entry(payment_form, width=20).grid(
                row=row, column=1, sticky="ew", pady=3
            )

        ttk.Button(payment_form, text="Pay", command=lambda: self.pay()).grid(
            row=len(fields), column=0, columnspan=2, pady=(8, 0)
        )

    def pay(self):
        errors = self.card_validation(
            self.var_card_number, self.var_expiry_date, self.var_cvv
        )
        if errors:
            messagebox.showerror("Error", "\n".join(errors))
            return

        receipt, id = self.generate_receipt(
            self.var_payment_method, self.var_items, self.var_quantity, self.var_price
        )
        messagebox.showinfo("Receipt", receipt)

        # Append the new receipt to the existing list
        formated_receipt: dict = self.read_file
        formated_receipt.update({id: {"items": self.var_items, "quantity": self.var_quantity}})

        Utils.write_json(".//data//receipts.json", formated_receipt)

    def generate_receipt(
        self, payment_method, item: list, quantity: list, price: list
    ):
        id = round(time.time())
        receipt = "=" * 40 + f"\nReceipt ID: {id}\n " + "=" * 40 + "\n"
        receipt += f"Payment Method: {payment_method}\n"

        for z in range(len(item)):
            receipt += f" {z + 1}. {item[z]}: {quantity[z]} x {price[z]} = {quantity[z] * price[z]}\n"

        receipt += (
            f" Total Price: {sum([quantity[i] * price[i] for i in range(len(item))])}\n"
        )

        return receipt, id

    def card_validation(self, card_number, expiry_date, cvv) -> list[str]:
        errors = [
            Utils.validate_card_number(card_number),
            Utils.validate_expiry(expiry_date),
            Utils.validate_cvv(cvv, card_number),
        ]
        return [error for error in errors if error]
