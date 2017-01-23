"""
Responsible for producing the regular expression for a given R(i,j,k)
Simplyfies the regular expression produced
Returns a string
"""

class R_IJK:
	"""
	Initalize all constant variables
	"""

	def __init__(self):
		self.EMPTY_SET = '!'
		self.UNION_SYMBOL = 'U'
		self.EMPTY_STRING = 'e'
		self.IGNORE = True
		self.result_recorder = {}


	"""
	Creates a blank record to record results
	"""

	def Create_Recorder(self, num_of_states):
		for x in range(0, num_of_states + 1):
			self.result_recorder[str(x)] = []


	"""
	Called by an outside source to solve R(i,j,k)
	Creates a dictionary to record the results of solver
	Returns the dictionary with the result stored in it
	"""

	def Solver(self, i, j, k, path_values):
		if (k == 0):
			search_str = str(i) + str(j)
			formatted_return_str = path_values[search_str]
			recorded_str = "R(" + str(i) + ", " + str(j) + ", " + str(k) + ")" 
			saved_str = recorded_str + " = " + formatted_return_str + "\n"

			if saved_str not in self.result_recorder[str(k)]:
				self.result_recorder[str(k)].append(saved_str)

			return formatted_return_str

		else:
			str_1 = self.Solver(i, j, k - 1, path_values)
			str_2 = self.Solver(i, k, k - 1, path_values)
			str_3 = self.Solver(k, k, k - 1, path_values)
			str_4 = self.Solver(k, j, k - 1, path_values)

			curr_case_str = "R(" + str(i) + "," + str(j) + "," + str(k) + ")"
			rec_eq_str = "R(" + str(i) + "," + str(j) + "," + str(k) + ") = " + \
						"R(" + str(i) + "," + str(j) + "," + str(k - 1) + ") " + self.UNION_SYMBOL + " " + \
						"R(" + str(i) + "," + str(k) + "," + str(k - 1) + ")" + \
						"R(" + str(k) + "," + str(k) + "," + str(k - 1) + ")*" + \
						"R(" + str(k) + "," + str(j) + "," + str(k - 1) + ")"

			formatted_return_str = self.EMPTY_SET
			unformated_formatted_return_str = (" " * len(curr_case_str)) + " = (" + str_1 + " " + self.UNION_SYMBOL + " " + str_2 + str_3 + '*' + str_4 + ')'

			part_1_is_empty = (str_1 == self.EMPTY_SET)
			part_2_is_empty = (str_2 == self.EMPTY_SET or str_3 == self.EMPTY_SET or str_4 == self.EMPTY_SET)

			if (not part_1_is_empty and part_2_is_empty):
				formatted_return_str = str_1
			elif (part_1_is_empty and not part_2_is_empty):
				formatted_return_str = self.Formatter(str_1, str_2, str_3, str_4, self.IGNORE)
			elif (not part_1_is_empty and not part_2_is_empty):
				formatted_return_str = self.Formatter(str_1, str_2, str_3, str_4)

			saved_str = rec_eq_str + "\n" + unformated_formatted_return_str + "\n" + curr_case_str + " = " + formatted_return_str + "\n\n"

			if saved_str not in self.result_recorder[str(k)]:
				self.result_recorder[str(k)].append(saved_str)

			return formatted_return_str


	"""
	Formats the second porition of the string
	"""

	def Formatter(self, str_1, str_2, str_3, str_4, ignore_str_1 = False):
		kleene_star = '*'
		resulting_str = ""

		my_str_1 = str_1
		my_str_2 = str_2
		my_str_3 = str_3
		my_str_4 = str_4

		if (my_str_2 == my_str_3):
			kleene_star = '*' if (self.EMPTY_STRING in my_str_3 and self.UNION_SYMBOL in my_str_3) else '+'
			my_str_2 = ""
		elif (my_str_4 == my_str_3):
			kleene_star = '*' if (self.EMPTY_STRING in my_str_3 and self.UNION_SYMBOL in my_str_3) else '+'
			my_str_4 = ""
		elif (my_str_2 == my_str_3 and my_str_4 == my_str_3 and self.EMPTY_STRING in my_str_3 and self.UNION_SYMBOL in my_str_3):
			my_str_4 = ""
			my_str_2 = ""
			kleene_star = '*'

		if (self.EMPTY_STRING in my_str_3 and self.UNION_SYMBOL in my_str_3):
			e_index = my_str_3.find(self.EMPTY_STRING)
			u_index = my_str_3.find(self.UNION_SYMBOL)

			my_str_3 = my_str_3[u_index + 2:] #Guarenteed that 'e' is always before union

			if (my_str_3[-1] == ')'):
				my_str_3 = my_str_3[:-1]

			if (my_str_2 == my_str_3):
				kleene_star = '+'
				my_str_2 = ""
			elif (my_str_4 == my_str_3):
				kleene_star = '+'
				my_str_4 = ""

		if (my_str_3 == self.EMPTY_STRING):
			kleene_star = ""
			my_str_3 = ""
		if (my_str_2 == self.EMPTY_STRING):
			my_str_2 = ""
		if (my_str_4 == self.EMPTY_STRING):
			my_str_4 = ""

		if (len(my_str_3) != 1):
			my_str_3 = '(' + my_str_3 + ')'


		rhs_str = my_str_2 + my_str_3 + kleene_star + my_str_4

		if (rhs_str == ""):
			rhs_str = self.EMPTY_STRING

		if ignore_str_1:
			resulting_str = rhs_str
		else:
			rhs_has_left = False

			if (kleene_star == '*'):
				rhs_has_left = ((my_str_4 == "" and (my_str_1 == my_str_2)) or (my_str_2 == "" and (my_str_1 == my_str_4)))

			if (my_str_1 == rhs_str or rhs_has_left):
				resulting_str = rhs_str
			else:
				resulting_str = '(' + my_str_1 + " " + self.UNION_SYMBOL + " " + rhs_str + ')'

		return resulting_str
		

	"""
	Writes the results to a file
	"""

	def Write_To_File(self, file_name):
		txt_file = open(file_name, 'w')
		
		for y in range(len(self.result_recorder) - 1, -1, -1):
			if y != 0:
				txt_file.write("\n\nPassing through " + str(y) + " intermediate states.\n\n")
			else:
				txt_file.write("\n\nPassing through no intermediate states.\n\n")

			for z in self.result_recorder[str(y)]:
				txt_file.write(z + "\n")

		txt_file.close()
