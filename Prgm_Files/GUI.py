import Tkinter as tk
import tkMessageBox
import R_IJK as converter

"""
Responsible for keeping track of all changes in a state for user input
"""

class FA_State:
	"""
	Initialize class variables
	"""

	def __init__(self, num_id):
		self.state_num = num_id
		self.is_start_state = (num_id == 0)
		self.is_final_state = False
		self.transition = []


"""
Responsible for producing the GUI for the program
Calls the Solver
Gets User Input
"""

class RIJK_App:
	"""
	Initialize all constant variables
	Initialize class variables
	Set up all windows (size)
	Set up the first window (main window) for display
	"""

	def __init__(self, master, master_width, master_height):
		#Declaring constants
		self.NUM_OF_STATES_DFA_FINAL_STATE = 2
		self.ALPHABET_DFA_FINAL_STATE = 2
		self.MAX_NUM_OF_WINDOWS = 5
		self.MAIN_WINDOW_INDEX = 0
		self.NUM_STATE_WINDOW_INDEX = 1
		self.ALPHA_WINDOW_INDEX = 2
		self.STATE_STATUS_WINDOW_INDEX = 3
		self.TRANS_FUNC_WINDOW_INDEX = 4
		self.UNION = 'U'
		self.EMPTY_SET = '!'
		self.EMPTY_STRING = 'e'

		#Declaring class variables
		self.screen_width = master_width
		self.screen_height = master_height
		self.num_of_states = 0
		self.state_at = 0
		self.alphabet = []
		self.states = []
		self.windows = [ 0 for x in range(self.MAX_NUM_OF_WINDOWS) ] #Temporary fill with 0

		#Making the first window the master
		self.windows[self.MAIN_WINDOW_INDEX] = master

		#Formatting master window
		msg = "Welcome to the Finite Automata to Regular Expression Converter.\nClick next to use."
		self.mw_ins = tk.Label( self.windows[self.MAIN_WINDOW_INDEX] , text = msg )
		self.mw_btn = tk.Button( self.windows[self.MAIN_WINDOW_INDEX] , text = "Next", command=self.__MW_On_Click )

		self.mw_ins.place(x = self.screen_width / 2, y = ( self.screen_height / 2 ) - ( self.mw_ins.winfo_reqheight() / 2 ), anchor=tk.CENTER)
		self.mw_btn.place(x = self.screen_width, y = self.screen_height, anchor = tk.SE)

		#Hide other windows, Set other windows to be destroyed when master is destroyed
		for x in range (1, self.MAX_NUM_OF_WINDOWS):
			self.windows[x] = tk.Toplevel(master)
			self.windows[x].protocol( "WM_DELETE_WINDOW" , master.destroy )
			self.windows[x].withdraw()

			width = master.winfo_screenwidth()
			height = master.winfo_screenheight()

			x_corner = (width / 2) - (master_width / 2)
			y_corner = (height / 2) - (master_height / 2)

			self.windows[x].geometry(str(master_width) + "x" + str(master_height) + "+" + str(x_corner) + "+" + str(y_corner))
		

	"""
	Moves to the next window (Num State)
	"""	

	def __MW_On_Click(self):
		#Moving to next window
		self.windows[self.MAIN_WINDOW_INDEX].withdraw()
		self.__Create_Num_State_Window()
		self.windows[self.NUM_STATE_WINDOW_INDEX].deiconify()


	"""
	Sets up the last window (main window) for display
	"""

	def __Create_Final_Window(self, expression):
		#Setting up window to be the final window
		msg = "Thank you for using the converter.\n\nYour result is: " + expression + "\n\n"
		msg += "Your step by step and final results has been written to file.\nClick quit to exit."

		self.mw_ins.configure( text = msg )
		self.mw_btn.configure( text = "Quit", command = self.windows[self.MAIN_WINDOW_INDEX].destroy )	
		self.windows[self.MAIN_WINDOW_INDEX].deiconify()
		

	"""
	Sets up the Num State Window for display
	Gets user input for the number of states a FA is
	"""

	def __Create_Num_State_Window(self):
		msg = "Enter the number of states the FA is.\nOnly enter numbers; Don't start with 0."
		ins = tk.Label( self.windows[self.NUM_STATE_WINDOW_INDEX], text = msg )
		self.num_txt = tk.Entry( self.windows[self.NUM_STATE_WINDOW_INDEX] )
		nsw_next_btn = tk.Button( self.windows[self.NUM_STATE_WINDOW_INDEX], text = "Enter", command = self.__NSW_On_Click)
		
		ins.place(x = self.screen_width / 2, y = (self.screen_height / 2) - ( ins.winfo_reqheight() / 2 ), anchor = tk.CENTER)
		self.num_txt.place(x = self.screen_width / 2, y = (self.screen_height / 2) + ( ins.winfo_reqheight() / 2 ), anchor = tk.CENTER)
		nsw_next_btn.place(x = self.screen_width, y = self.screen_height, anchor = tk.SE)


	"""
	Sends input through a DFA
	If it is correct, moves to the next window (alpha window)
	If incorrect, wipes the text box for new input to be collected
	"""

	def __NSW_On_Click(self):
		if ( self.__Get_Num_of_States(self.num_txt.get()) ):
			print (self.num_of_states)
			self.states = [ FA_State(x) for x in range(0, self.num_of_states) ]
			
			self.windows[self.NUM_STATE_WINDOW_INDEX].withdraw()
			self.__Create_Alpha_Window()
			self.windows[self.ALPHA_WINDOW_INDEX].deiconify()
		else:
			self.num_txt.delete(0, tk.END)
			self.num_txt.insert(tk.END, "")


	"""
	Gets the number of states from the input from Num State Window
	If incorrect, it produces an error message
	If correct, it stores the result as a integer
	"""

	def __Get_Num_of_States(self, text_str):
		state = self.__Num_of_States_DFA(text_str)
		state_passed = ( state == self.NUM_OF_STATES_DFA_FINAL_STATE )
		
		if ( state_passed ):
			self.num_of_states = int(text_str)
		else:
			if ( state == 1 ):
				tkMessageBox.showerror("Error", "Entry was blank. Please enter again.")
			elif ( state == 3 ):
				tkMessageBox.showerror("Error", "Started with a 0. Please enter again.")
			elif ( state == 4 ):
				tkMessageBox.showerror("Error", "Non-numeric character entered. Please enter again.")

		return state_passed


	"""
	DFA for the Num State Window
	Only integers allowed
	No 0's can start to prevent 0 or 019 or 0000000... from being entered
	"""

	def __Num_of_States_DFA(self, test_str):
		state = 1

		for x in test_str:
			if ( state == 1 ):
				if ( x >= '1' and x <= '9' ):
					state = 2
				elif ( x == '0' ):
					state = 3
				else:
					state = 4
			elif (state == 2):
				if ( x >= '0' and x <= '9' ):
					state = 2
				else:
					state = 4
			elif ( state == 3 ):
				state = 3
			elif ( state == 4 ):
				state = 4

		return state


	"""
	Sets up the Alpha Window for display
	Gets user input for the alphabet used in the FA
	"""

	def __Create_Alpha_Window(self):
		msg = "Enter the alphabet used in the FA.\nSeperate each character with a comma.\n"
		msg += "Don't include commas (',') , '" + self.EMPTY_STRING + "', '" + self.EMPTY_SET + "', or '" + self.UNION + "\' as characters."
		
		ins = tk.Label(self.windows[self.ALPHA_WINDOW_INDEX], text = msg)
		self.alpha_txt = tk.Entry(self.windows[self.ALPHA_WINDOW_INDEX])
		aw_btn = tk.Button(self.windows[self.ALPHA_WINDOW_INDEX], text = "Enter", command=self.__AW_On_Click)
		
		ins.place(x = self.screen_width / 2, y = (self.screen_height / 2) - ( ins.winfo_reqheight() / 2 ), anchor = tk.CENTER)
		self.alpha_txt.place(x = self.screen_width / 2, y = (self.screen_height / 2) + ( ins.winfo_reqheight() / 2 ), anchor = tk.CENTER)
		aw_btn.place(x = self.screen_width, y = self.screen_height, anchor = tk.SE)


	"""
	Sends input through a DFA
	If it is correct, moves to the next window (state status window)
	If incorrect, wipes the text box for new input to be collected
	"""

	def __AW_On_Click(self):
		if ( self.__Get_Alpha(self.alpha_txt.get()) ):
			print (self.alphabet)

			self.windows[self.ALPHA_WINDOW_INDEX].withdraw()
			self.__Create_State_Status_Window()
			self.windows[self.STATE_STATUS_WINDOW_INDEX].deiconify()
		else:
			self.alpha_txt.delete(0, tk.END)
			self.alpha_txt.insert(tk.END, "")


	"""
	Gets the number of states from the input from Alpha Window
	If incorrect, it produces an error message
	If correct, it stores the result as a list
	"""

	def __Get_Alpha(self, text_str):
		alpha_str = self.__Remove_Blanks( text_str )
		state = self.__Alpha_DFA(alpha_str)
		state_passed = ( state == self.ALPHABET_DFA_FINAL_STATE )
		
		if ( state_passed ):
			self.alphabet = alpha_str.split(',')
		else:
			if ( state == 1 ):
				tkMessageBox.showerror("Error", "Entry was blank. Please enter again.")
			elif ( state == 3 ):
				tkMessageBox.showerror("Error", "Invalid character used. Please enter again.")
			elif ( state == 4 ):
				tkMessageBox.showerror("Error", "Invalid formatting used. Please enter again.")

		return state_passed


	"""
	Removes all blanks from the user input
	"""

	def __Remove_Blanks(self, test_str):
		new_str = ""

		for x in test_str:
			if (x != ' '):
				new_str += x

		return new_str


	"""
	DFA for the Alpha Window
	No 'e', '!', 'U' allowed as they are constants in the solver
	Must be in format of a,b,c,d,e... (Prevents: ',' , 'a,,b', etc)
	"""

	def __Alpha_DFA(self, test_str):
		state = 1

		for x in test_str:
			if (state == 1):
				if ( x == self.EMPTY_SET or x == self.UNION or x == self.EMPTY_STRING ):
					state = 3
				elif ( x == ',' ):
					state = 4
				else:
					state = 2
			elif (state == 2):
				if (x == ','):
					state = 1
				elif ( x == self.EMPTY_SET or x == self.UNION or x == self.EMPTY_STRING ):
					state = 3
				else:
					state = 4
			elif (state == 3):
				state = 3
			elif (state == 4):
				state = 4

		return state


	"""
	Sets up the State Status Window for display
	Gets whether or not a state is a final state or a start state
	http://stackoverflow.com/questions/3085696/adding-a-scrollbar-to-a-group-of-widgets-in-tkinter
	"""

	def __Create_State_Status_Window(self):
		msg = "Which states are final and which are starting?\nState 0 has been selected by default.\nThere must be at least one starting state clicked."
		msg += "\nClick enter to continue."

		#Used for formatting the screen
		#If the scrollbar will be needed, this will show the top of the screen
		#Otherwise, if everything naturally fits on the window, start in the center
		y_coor = self.screen_height if self.num_of_states >= 10 else (self.screen_height / 2)


		self.ssw_canvas = tk.Canvas(self.windows[self.STATE_STATUS_WINDOW_INDEX], borderwidth = 0)
		self.ssw_frame = tk.Frame(self.ssw_canvas)
		self.ssw_vertical_scrollbar = tk.Scrollbar(self.windows[self.STATE_STATUS_WINDOW_INDEX], orient = tk.VERTICAL, command = self.ssw_canvas.yview)
		self.ssw_canvas.configure(yscrollcommand = self.ssw_vertical_scrollbar.set)

		self.ssw_vertical_scrollbar.pack(side = tk.RIGHT, fill = tk.Y)
		self.ssw_canvas.pack(side = tk.TOP, fill = tk.BOTH, expand = True)

		self.ssw_canvas.create_window(((self.screen_width / 2), y_coor), window = self.ssw_frame, anchor = tk.CENTER)

		self.ssw_frame.bind("<Configure>", self.__On_SSW_Frame_Configure)
		
		ins = tk.Label( self.ssw_frame, text = msg )
		ins.grid(row = 0, column = 0, columnspan = 3)

		self.state_status = [ [ tk.BooleanVar(), tk.BooleanVar() ] for x in range(0, self.num_of_states) ]
		self.state_status[0][0].set(True) #Setting the 1st State to true

		for x in range(0, self.num_of_states):
			state_msg = tk.Label( self.ssw_frame, text = "State " + str(x) )
			state_msg.grid(row = x + 1, column = 0)

			if ( x == 0 ):
				check_1 = tk.Checkbutton( self.ssw_frame, text = "Start", variable = self.state_status[x][0], onvalue = True, offvalue = False )
				check_1.grid(row = x + 1, column = 1)
			else:
				check_1 = tk.Checkbutton( self.ssw_frame, text = "Start", variable = self.state_status[x][0], onvalue = True, offvalue = False )
				check_1.grid(row = x + 1, column = 1)

			check_2 = tk.Checkbutton( self.ssw_frame, text = "Final", variable = self.state_status[x][1], onvalue = True, offvalue = False )
			check_2.grid(row = x + 1, column = 2)

		ssw_next_btn = tk.Button( self.windows[self.STATE_STATUS_WINDOW_INDEX], text = "Enter", command = self.__SSW_On_Click)
		ssw_next_btn.place(x = self.screen_width - self.ssw_vertical_scrollbar.winfo_reqwidth(), y = self.screen_height, anchor = tk.SE)


	"""
	Checks to ensure that a start state has been selected
	If one has, moves to the next window (trans func window)
	If not, shows an error message
	"""

	def __SSW_On_Click(self):
		found_start_state = False

		for x in range(0, self.num_of_states):
			self.states[x].is_state_state = self.state_status[x][0].get()
			self.states[x].is_final_state = self.state_status[x][1].get()

			if ( self.state_status[x][0].get() == True ):
				found_start_state = True

			print (x, self.states[x].is_state_state, self.states[x].is_final_state)

		if ( found_start_state ):
			self.windows[self.STATE_STATUS_WINDOW_INDEX].withdraw()
			self.__Create_Trans_Func_Window()
			self.windows[self.TRANS_FUNC_WINDOW_INDEX].deiconify()

			self.ssw_canvas.destroy()
			self.ssw_frame.destroy()
			self.ssw_vertical_scrollbar.destroy()
		else:
			tkMessageBox.showerror("Error", "No state state checked. Please enter again.")
	

	"""
	Resets the scroll region to encompass the inner frame
	http://stackoverflow.com/questions/3085696/adding-a-scrollbar-to-a-group-of-widgets-in-tkinter
	"""

	def __On_SSW_Frame_Configure(self, event):	
		self.ssw_canvas.configure(scrollregion = self.ssw_canvas.bbox(tk.ALL))


	"""
	Sets up the Trans Func Window for display
	Gets what characters are used to move from state to state, if at all
	http://stackoverflow.com/questions/3085696/adding-a-scrollbar-to-a-group-of-widgets-in-tkinter
	"""

	def __Create_Trans_Func_Window(self):
		self.states_path = [ [ tk.BooleanVar() for x in range(0, len(self.alphabet) + 1) ] for y in range(0, self.num_of_states) ]
		self.states_path_copy = [ [ False for x in range(0, len(self.alphabet) + 1) ] for y in range(0, self.num_of_states) ]
		row_index = 0

		y_coor = self.screen_height if ( ( ( len(self.alphabet)  / 3 ) + 1 ) * self.num_of_states + ( 2 * self.num_of_states ) ) >= 14 else (self.screen_height / 2)

		self.tfw_canvas = tk.Canvas(self.windows[self.TRANS_FUNC_WINDOW_INDEX], borderwidth = 0)
		self.tfw_frame = tk.Frame(self.tfw_canvas)
		self.tfw_vertical_scrollbar = tk.Scrollbar(self.windows[self.TRANS_FUNC_WINDOW_INDEX], orient = tk.VERTICAL, command = self.tfw_canvas.yview)
		self.tfw_canvas.configure(yscrollcommand = self.tfw_vertical_scrollbar.set)

		self.tfw_vertical_scrollbar.pack(side = tk.RIGHT, fill = tk.Y)
		self.tfw_canvas.pack(side = tk.LEFT, fill = tk.BOTH, expand = True)
		self.tfw_canvas.create_window(((self.screen_width / 2), y_coor), window = self.tfw_frame, anchor = tk.CENTER)

		self.tfw_frame.bind("<Configure>", self.__On_TFW_Frame_Configure)

		for state_index in range(0, self.num_of_states):
			msg = "Click all letters that are involved in the path (State " + str(self.state_at) + " to State " + str(state_index) + ")" 
			msg += "\nIf no path is clicked, the other checkboxes will be deselected."
		
			ins = tk.Label( self.tfw_frame, text = msg )
			ins.grid(row = row_index, column = 0, columnspan = 3, sticky = tk.N)
			#row_index += 1

			for alpha_index in range(0, len(self.alphabet)):
				if ( alpha_index % 3 == 0 ):
					row_index += 1

				check_alpha = tk.Checkbutton( self.tfw_frame, text = self.alphabet[alpha_index], \
												 variable = self.states_path[state_index][alpha_index], onvalue = True, offvalue = False, \
												 command = self.__TFW_Letter_On_Select )
				check_alpha.grid(row = row_index, column = (alpha_index % 3))

			if ( len(self.alphabet) % 3  == 0):
				row_index += 1

			check_none = tk.Checkbutton( self.tfw_frame, text = "No Path", variable = self.states_path[state_index][len(self.alphabet)], \
											onvalue = True, offvalue = False, command = self.__TFW_No_Path_On_Select )
			check_none.grid(row = row_index, column = 0)
			row_index += 1

		btn_msg = "Next State" if ( self.state_at != self.num_of_states - 1 ) else "Enter"

		tfw_next_btn = tk.Button( self.windows[self.TRANS_FUNC_WINDOW_INDEX], text = btn_msg, command = self.__TFW_On_Click)
		tfw_next_btn.place(x = self.screen_width - self.tfw_vertical_scrollbar.winfo_reqwidth(), y = self.screen_height, anchor = tk.SE)


	"""
	Resets the scroll region to encompass the inner frame
	http://stackoverflow.com/questions/3085696/adding-a-scrollbar-to-a-group-of-widgets-in-tkinter
	"""

	def __On_TFW_Frame_Configure(self, event):	
		self.tfw_canvas.configure(scrollregion = self.tfw_canvas.bbox(tk.ALL))

	"""
	If a charcter checkbox has been selected, scan for the changed element and turn off the No Path checkbox
	"""

	def __TFW_Letter_On_Select(self):
		for x in range(0, self.num_of_states):
			for y in range(0, len(self.alphabet)):
				if ( self.states_path[x][y].get() != self.states_path_copy[x][y] ): #If a change has happened
					self.states_path_copy[x][y] = self.states_path[x][y].get() #Update the tracker
					self.states_path[x][len(self.alphabet)].set(False) #Set the no path checkbox to false
					self.states_path_copy[x][len(self.alphabet)] = False


	"""
	If a No Path checkbox has been selected, turn off all other checkboxes in the same section
	"""

	def __TFW_No_Path_On_Select(self):
		for x in range(0, self.num_of_states):
			if ( self.states_path[x][len(self.alphabet)].get() != self.states_path_copy[x][len(self.alphabet)] ): #If the check box has been changed
				self.states_path_copy[x][len(self.alphabet)] = self.states_path[x][len(self.alphabet)].get() #Update the tracker
				for y in range(0, len(self.alphabet)): #Deselect all other ones in that row
					self.states_path[x][y].set(False)
					self.states_path_copy[x][y] = False


	"""
	Checks to ensure each state has a checkbox active
	If so, formats the results into a string
	Else, produces an error message
	"""

	def __TFW_On_Click(self):
		something_is_checked = True
		checked_arr = [False for x in range(0, self.num_of_states)]

		for x in range(0, self.num_of_states): #Check to ensure something has been clicked
			for y in range(0, len(self.alphabet) + 1):
				if ( self.states_path[x][y].get() ):
					checked_arr[x] = True

		print (checked_arr)

		for x in checked_arr:
			if ( not x ):
				something_is_checked = False

		if ( something_is_checked ): #Format the checkboxes data into a string and store it
			if ( self.state_at != self.num_of_states ):
				for x in range(0, self.num_of_states):
					trans_str = ""

					if ( self.states_path[x][len(self.alphabet)].get() ):
						if ( self.state_at != x ):
							trans_str = self.EMPTY_SET 
						else:
							trans_str = self.EMPTY_STRING
					else:
						for y in range(0, len(self.alphabet)):
							if ( self.states_path[x][y].get() ):
								if ( len(trans_str) == 0 ):
									trans_str += self.alphabet[y]
								else:
									trans_str += " U " + self.alphabet[y]

						if ( self.state_at == x ):
							trans_str = self.EMPTY_STRING + " U " + trans_str

					self.states[self.state_at].transition.append(trans_str)  

				print (self.states[self.state_at].transition)
				self.state_at += 1

				self.tfw_frame.destroy()
				self.tfw_canvas.destroy()
				self.tfw_vertical_scrollbar.destroy()

				if ( self.state_at != self.num_of_states ):
					self.__Create_Trans_Func_Window()
				else: #Out of states to ask for and set up final window
					self.windows[self.TRANS_FUNC_WINDOW_INDEX].withdraw()
					expression = self.__Find_Reg_Expression()
					self.__Create_Final_Window(expression)
		else:
			tkMessageBox.showerror("Error", "A state has been left with nothing checked. Please enter again.")

	"""
	Formats the paths into a dictionary that will be accepted by the solver

	dictionary = { str (state at) + str (state to) : transition string  }
	"""

	def __Format_Dictionary(self):
		path_dict = {}

		for x in range(0, self.num_of_states):
			for y in range(0, self.num_of_states):
				path_dict[str(x + 1) + str(y + 1)] = self.states[x].transition[y]

		return path_dict


	"""
	Formats state data into an R(i,j,k) format and stores in array
	i = all start states
	j = all final states
	k = number of states

	Even if the final state is not the number of k = n is still a valid assumption to grab states beyond the final.
	This converter is used to get the whole expression that can be made by the FA.
	"""

	def __Get_IJK_States(self):
		s_state = []
		f_state = []
		ijk_states = []

		for x in self.states:
			if ( x.is_start_state ):
				s_state.append(x.state_num + 1)

		for x in self.states:
			if ( x.is_final_state ):
				f_state.append(x.state_num + 1)

		for x in s_state:
			for y in f_state:
				ijk_states.append([x, y, self.num_of_states])

		return ijk_states


	"""
	Calls the R(I,J,K) Solver to convert
	Formats the final results and writes it to txt_file
	"""

	def __Find_Reg_Expression(self):
		results = []
		fa = self.__Format_Dictionary()
		ijk_states = self.__Get_IJK_States()

		print(ijk_states)
		print(fa)

		for state in ijk_states:
			solver = converter.R_IJK()
			solver.Create_Recorder( self.num_of_states )

			reg_expression = solver.Solver( state[0], state[1], state[2], fa )
			result = solver.Write_To_File( "results-R(" + str(state[0]) + "," + str(state[1]) + "," + str(state[2]) + ").txt" )
			
			if (reg_expression != ""):
				results.append(reg_expression)

		final_expression = ""

		if (len(results) == 0):
			final_expression = "Regular Expression not found for entered information."
		else:
			results_len = len(results)

			for x in range(0, results_len):
				final_expression += results[x]

				if ((x + 1) != results_len):
					final_expression += " U "

		txt_file = open("results-" + str(ijk_states) + ".txt", 'w')
		txt_file.write(final_expression)
		txt_file.close()

		return final_expression
