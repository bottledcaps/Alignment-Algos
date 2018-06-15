#string 1 is top, horizontal string

def smith_waterman(string1, string2):
	#strings 1 and 2 are input strings, presumably genomes
	#have to determine rules?
	length1 = len(string1)
	length2 = len(string2)
	matrix_max = 0
	x_max = None
	y_max = None
	def initialize_grid(value):
	#given two strings, create blank scoring matrix with dimensions 1 greater than each
		A = []
		for _ in range(length2 + 1):
			A.append([])
		for x in range(length2 + 1):
			for y in range(length1+1):
				A[x].append(value)
		return A
	def print_grid(grid):
		a = len(grid)
		for x in range(a):
			#if x != 0:
			#	print(string2[x-1])
			print(grid[x])
	def sub_score(tf):
		if tf:
			return 3
		else:
			return -3
	def gap_penalty(length):
		return length
	def score(y_loc, x_loc):
		#return x_loc + y_loc
		nonlocal matrix_max, x_max, y_max
		max_val = 0

		calc_sub = g[y_loc-1][x_loc-1] + sub_score((string1[x_loc-1] == string2[y_loc-1]))
		calc_string1_gap = g[y_loc-1][x_loc] - 2
		calc_string2_gap = g[y_loc][x_loc-1] - 2

		subst = False
		up = False
		left = False


		if calc_sub > max_val:
			max_val = calc_sub
			#path_x, path_y = x_loc - 1, y_loc - 1
			subst = True

		if calc_string1_gap > max_val:
			max_val = calc_string1_gap
			#path_x = x_loc
			#path_y = y_loc-1
			up = True

		if calc_string2_gap > max_val:
			max_val = calc_string2_gap
			#path_x = x_loc-1
			#path_y = y_loc
			left = True

		if max_val > matrix_max:
			matrix_max = max_val
			x_max = x_loc
			y_max = y_loc



		if left:
			path_grid[y_loc][x_loc] = -1
		elif up:
			path_grid[y_loc][x_loc] = 1
		elif subst:
			path_grid[y_loc][x_loc] = 0 

		return max_val
	def align_strings():
		new_string1 = ''
		new_string2 = ''
		current_x = x_max
		current_y = y_max
		#update messes up the if statements
		while(path_grid[current_y][current_x] != None):
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
				current_x -= 1
		return new_string1, new_string2


	g = initialize_grid(0)
	path_grid = initialize_grid(None) #negative x means to the left by x, positive x means up by x, 0 means up, left


	#x indexes spot in string 1, y indexes spot in string 2, [y+1][x+1] is current spot
	for y in range(length2):
		for x in range(length1):
			g[y+1][x+1] = score(y+1, x+1)
			
	#print_grid(g)
	#print()
	#print_grid(path_grid)
	new_string1, new_string2 = align_strings()
	print(new_string1)
	print(new_string2)
	return None

	#return matrix_max, x_max, y_max
	


	




