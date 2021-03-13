# Zach Marcus
# CS 361
# Person Generator Project
#
# =======================================================
# This program takes a selected state along with an amount and generates
# a list of random addresses from that state, outputting the list
# into a csv file and displaying the generated data in the GUI.
# With the command line, it can be started with <python person-generator.py input.csv>.
# If using the command line, the layout of the input csv file must be state followed
# by number of addresses to generate.
# =======================================================
import tkinter as tkinter
import tkinter.ttk
import csv
from random import seed
from random import randint
from datetime import datetime
import sys
from subprocess import call


class Settings:
	"""
	This class contains all the attributes
	needed for generating the necessary data.
	"""
	def __init__(self):
		self.output_file = "output.csv"
		self.csv_input_array = []
		self.address_array = []
		self.created_array = []
		self.toy_array = []
		self.content_type = "street address"


class MainWindow:
	"""
	This class has all the functions for the main window
	used in the program.
	"""
	def __init__(self, passed_csv):
		self.window = tkinter.Tk()
		self.window.geometry("850x500")
		self.passed_csv = passed_csv
		self.toys_selected = False

		# widget creation
		self.create_button = tkinter.Button(text="Create Dataset", font=(None, 12), height=3, width=30,
											command=self.create_click)
		self.title = tkinter.Label(text="Person Linear", font=(None, 28), width=27, height=4)
		self.s_state_label = tkinter.Label(text="Select State")
		self.s_state = tkinter.ttk.Combobox(self.window, width=27, state="readonly")
		self.s_state["values"] = ("Alaska", "Arizona", "California", "Colorado", "Hawaii",
								  "Idaho", "Montana", "New Mexico", "Nevada", "Oregon",
								  "Utah", "Washington", "Wyoming")
		self.s_number_label = tkinter.Label(text="Select Amount to Generate")
		self.s_number = tkinter.ttk.Combobox(self.window, width=27, state="readonly")
		self.s_number["values"] = ("10", "20", "30", "40", "50", "100", "200")
		self.display_generated = tkinter.Listbox(width=50, height=13)
		self.display_label = tkinter.Label(text="Generated Data:")
		self.input_received = tkinter.Label(text="Input CSV File Received!", font=(None, 18), fg="Green")
		self.toy_label = tkinter.Label(text="Display Types of Toys sent to Addresses:")
		self.toy_choice_box = tkinter.ttk.Combobox(self.window, width=27, state="readonly")
		self.toy_choice_box["values"] = ("Yes", "No")

		# standard widget placement
		self.create_button.place(x=460, y=350)
		self.title.place(x=-135, y=0)
		self.display_generated.place(x=450, y=110)
		self.display_label.place(x=450, y=81)
		self.toy_label.place(x=50, y=270)
		self.toy_choice_box.place(x=50, y=295)

		# widget placement depending on csv file passed
		if passed_csv == 1:
			# place the options allowing the user to select state and amount
			self.s_state_label.place(x=50, y=150)
			self.s_state.place(x=50, y=175)
			self.s_number_label.place(x=50, y=210)
			self.s_number.place(x=50, y=230)
		else:
			self.input_received.place(x=47, y=175)


	def read_file(self, input_file, array, file_type):
		"""
		Reads from the passed file (file_name)
		and writes appropriate data to array (array).
		"""
		counter = 0
		first_row = True

		try:
			# read the CSV file selected, created an address array to pull from
			with open(input_file) as file_data:
				read_file = csv.reader(file_data, delimiter=',')
				for row in read_file:

					if first_row is True:
						first_row = False
						continue

					if file_type == "address_file":
						# add the current address to address array
						current_address = row[2]
						current_address += ' '
						current_address += row[3]
						array.append(current_address)
						counter += 1
					elif file_type == "input_csv":
						array.append(row[0])
						array.append(row[1])
					elif file_type == "toy_file":
						array.append(row[3])
						counter += 1

					if counter >= 9999:
						break
		except FileNotFoundError:
			self.display_generated.insert(0, "State file not found in directory.")


	def set_state(self, selected_state):
		"""
		Sets the proper values for
		the input_file and state_ac variables depending
		on what's passed for selected.
		"""
		if selected_state == "Alaska":
			return "ak.csv", "AK"
		elif selected_state == "Arizona":
			return "az.csv", "AZ"
		elif selected_state == "California":
			return "ca.csv", "CA"
		elif selected_state == "Colorado":
			return "co.csv", "CO"
		elif selected_state == "Hawaii":
			return "hi.csv", "HI"
		elif selected_state == "Idaho":
			return "id.csv", "ID"
		elif selected_state == "Montana":
			return "mt.csv", "MT"
		elif selected_state == "New Mexico":
			return "nm.csv", "NM"
		elif selected_state == "Nevada":
			return "nv.csv", "NV"
		elif selected_state == "Oregon":
			return "or.csv", "OR"
		elif selected_state == "Utah":
			return "ut.csv", "UT"
		elif selected_state == "Washington":
			return "wa.csv", "WA"
		elif selected_state == "Wyoming":
			return "wy.csv", "WY"
		else:
			# print an error message to the generated data listbox
			self.display_generated.insert(0, "Incorrect data entered.")


	def check_index(self, index):
		"""
		Takes an index in an array and checks
		if it has usable data.
		"""
		if index == 0:
			return False
		elif index.find('-') != -1:
			return False
		elif ord(index[0]) < 49 or ord(index[0]) > 57:
			return False
		elif index.find('.') != -1:
			return False
		elif len(index) < 5:
			return False
		elif index.find('&') != -1:
			return False
		elif index == ' ':
			return False
		elif index[len(index) - 2] == ' ':
			return False
		elif index[len(index) - 1] == 'E':
			return False
		elif index[len(index) - 1] == 'W':
			return False
		elif len(index) != 0:
			return True


	def check_toy_box(self, toy_array):
		"""
		Checks if the user selected "Yes" for displaying
		types of toys sent to addresses. If "Yes" it will attempt to fork
		the life-generator program then read data from its output file.

		"""
		if self.toy_choice_box.get() == "Yes":
			try:
				self.toys_selected = True
				call(["python", "life-generator.py", "2", "3", "4", "5", "6", "7"])
				self.read_file("output.csv", toy_array, "toy_file")
			except FileNotFoundError:
				self.toys_selected = False
		else:
			self.toys_selected = False


	def check_required_data(self):
		"""
		Checks if the user has supplied all necessary data.
		"""
		if len(self.s_state.get()) == 0 or len(self.s_number.get()) == 0 or \
		   len(self.toy_choice_box.get()) == 0:
			self.display_generated.insert(0, "Please make selections before creating dataset")
			return False
		else:
			return True


	def check_if_normal(self, settings):
		"""
		Checks if the user ran the program normally or
		through the command line.
		"""
		if self.passed_csv == 1:
			if self.check_required_data() is False:
				return 0, 0, 0, 0

			# create variables specific to normal program
			settings.total = int(self.s_number.get())
			settings.selected_state = self.s_state.get()
			settings.input_file, settings.state_ac = self.set_state(settings.selected_state)
		else:
			# get the selected state and total from input.csv
			self.read_file(sys.argv[1], settings.csv_input_array, file_type="input_csv")
			settings.selected_state = settings.csv_input_array[0]
			settings.total = int(settings.csv_input_array[1])

			# match the state with the state csv file
			settings.input_file, settings.state_ac = self.set_state(settings.selected_state)


	def display_data(self, settings):
		"""
		Displays generated data in the GUI.
		"""
		array_size = len(settings.created_array)
		while array_size != 0:
			self.display_generated.insert(0, settings.created_array[array_size - 1])
			array_size -= 1


	def write_headers(self, writer):
		"""
		Writes a header to output.csv.
		"""
		# check if toy category row needs to be written
		if self.toys_selected is False:
			writer.writerow(("input_state", "input_number_to_generate",
							 "output_content_type", "output_content_value"))
		else:
			writer.writerow(("input_state", "input_number_to_generate",
							 "output_content_type", "output_content_value",
							 "toy_delivered"))


	def write_file(self, settings):
		"""
		Writes data to an output.csv file.
		"""
		with open(settings.output_file, mode='w', newline='') as output_csv:

			# write the header to the file
			writer = csv.writer(output_csv, delimiter=",")
			self.write_headers(writer)

			# write the addresses to the file
			check = 0
			check_two = 0
			while check != settings.total:
				index = randint(0, 9999)

				# check if the index has usable data
				if self.check_index(settings.address_array[index]) is True:
					# check if user selected for toys to be output as well
					if self.toys_selected is False:
						writer.writerow((settings.state_ac, str(settings.total),
										 "street address", settings.address_array[index]))
						settings.created_array.append(settings.address_array[index])
					else:
						writer.writerow((settings.state_ac, str(settings.total),
										 "street address", settings.address_array[index],
							              settings.toy_array[check_two]))
						settings.created_array.append(settings.address_array[index])
						if check_two == 9:
							check_two = 0
					check += 1
					check_two += 1


	def read_write_display(self, settings):
		"""
		Performs the reading, writing, and displaying for data.
		"""
		self.read_file(settings.input_file, settings.address_array, file_type="address_file")
		self.write_file(settings)
		self.display_data(settings)


	def create_click(self):
		"""
		Reads from the selected CSV state file
		and writes data to output.csv.
		"""

		# reset the display box
		self.display_generated.delete('0', 'end')

		# create variables + seed
		seed(datetime.now())
		settings = Settings()

		# check if user wants to see what toys were sent to addresses
		self.check_toy_box(settings.toy_array)

		# check if program was run normally or by command line
		self.check_if_normal(settings)
		if settings.total == 0:
			return
		self.read_write_display(settings)


def main():
	"""
	Main function for executing the program.
	"""

	# check if user passed in CSV file as an argument
	if len(sys.argv) == 1:
		root = MainWindow(1)
		root.window.mainloop()
	elif len(sys.argv) == 2:
		root = MainWindow(2)
		root.window.mainloop()
	else:
		root = MainWindow(1)
		root.toy_choice_box.set("No")
		root.s_state.set("Alaska")
		root.s_number.set(sys.argv[2])
		root.create_click()


if __name__ == "__main__":
	main()
