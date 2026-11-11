import tkinter, Finance

class SportsManagementSystem:
	def __init__(self):
		self.name = "Sports Centre Management System"
		self.version = "1.0"

	def run(self):
		# Create the main window
		self.root = tkinter.Tk()
		self.root.title(self.name + " v" + self.version)

		# Create a button to test the Finance module
		test_button = tkinter.Button(self.root, text="Test Finance Module", command=Finance.test)
		test_button.pack(pady=20)

		# Start the main event loop
		self.root.mainloop()


if __name__ == "__main__":
	sports_management_system = SportsManagementSystem()
	sports_management_system.run()