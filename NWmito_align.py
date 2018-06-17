#string 1 is top, horizontal string

def needleman_wunsch(string1, string2):
	#strings 1 and 2 are input strings, presumably genomes
	#have to determine rules?
	length1 = len(string1)
	length2 = len(string2)
	def initialize_grid(value, y_length = len(string2) + 1, x_length = len(string1) + 1):
	#given two strings, create blank scoring matrix with dimensions 1 greater than each
		A = []
		for _ in range(y_length):
			A.append([])
		for x in range(y_length):
			for y in range(x_length):
				A[x].append(value)
		return A
	def initialize_scoring_grid(x_length=(len(string1) + 1), y_length=(len(string2)+1)):
		g = initialize_grid(None)
		#g[0][0] = 0
		for x in range(x_length):
			g[0][x] = -gap_penalty(x)
		for y in range(y_length):
			g[y][0] = -gap_penalty(y)
		return g
	def print_grid(grid):
		a = len(grid)
		for x in range(a):
			#if x != 0:
			#	print(string2[x-1])
			print(grid[x])
	def sub_score(match):
		if match:
			return 1
		else:
			return -1
	def gap_penalty(length): #always positive
		return 1 + 2*(length-1)
	def score(y_loc, x_loc):
		#return x_loc + y_loc
		#Can't do nonlinear gap penalties yet
		#DICTIONARIES: score is key, location is value

		def calc_gaps():
			gap_dict = {}
			#go_down
			k = 1
			while (y_loc-k) >= 0 and g[y_loc-k][x_loc] != None:
				gap_dict[g[y_loc-k][x_loc] - gap_penalty(k)] = k

				k = k + 1
			#go left
			j = 1
			while (x_loc-j) >= 0 and g[y_loc][x_loc - j] != None:
				gap_dict[g[y_loc][x_loc-j] - gap_penalty(j)] = -j

				j = j + 1
			return gap_dict

		score_path = calc_gaps()

		calc_sub = g[y_loc-1][x_loc-1] + sub_score((string1[x_loc-1] == string2[y_loc-1]))

		score_path[calc_sub] = 0

		max_key = max(score_path.keys())
		path_grid[y_loc][x_loc] = score_path[max_key]

		return max_key

		"""calc_sub = g[y_loc-1][x_loc-1] + sub_score((string1[x_loc-1] == string2[y_loc-1]))
		calc_go_down = g[y_loc-1][x_loc] - gap_penalty(1)
		calc_go_right = g[y_loc][x_loc-1] - gap_penalty(1)

		new_score = max(calc_sub, calc_go_down, calc_go_right)
		if new_score == calc_sub:
			path_grid[y_loc][x_loc] = 0
		elif new_score == calc_go_down:
			path_grid[y_loc][x_loc] = 1
		elif new_score == calc_go_right:
			path_grid[y_loc][x_loc] = -1

		return new_score"""

	def align_strings():
		new_string1 = ''
		new_string2 = ''
		current_x = len(string1) 
		current_y = len(string2)
		while(path_grid[current_y][current_x] != None):
			#print(current_y, current_x)
			if path_grid[current_y][current_x] == 0:
				new_string1 = string1[current_x-1] + new_string1
				new_string2 = string2[current_y-1] + new_string2
				current_y -= 1
				current_x -= 1
			elif path_grid[current_y][current_x] == 1:
				new_string2 = string2[current_y-1] + new_string2
				new_string1 = '-' + new_string1
				current_y -= 1
			elif path_grid[current_y][current_x] == -1:
				new_string1 = string1[current_x - 1] + new_string1
				new_string2 = '-' + new_string2
				current_x -= 1
		#print(current_y, current_x)
		return new_string1, new_string2


	g = initialize_scoring_grid()
	path_grid = initialize_grid(None) #negative x means to the left by x, positive x means up by x, 0 means up, left


	#x indexes spot in string 1, y indexes spot in string 2, [y+1][x+1] is current spot
	for y in range(length2):
		for x in range(length1):
			g[y+1][x+1] = score(y+1, x+1)
	new_string1, new_string2 = align_strings()
	print_grid(g)
	print()
	print_grid(path_grid)
	print(new_string1)
	print(new_string2)

	#print(string2[6], string1[6], string2[5], string1[5], string2[4], string1[4], string2[3], string1[3], string2[2], string1[2], string2[1], string1[2], string2[0], string1[1], string2[0], string1[0])
	return None


	#return matrix_max, x_max, y_max
	


	




