"""	string 1 is top, horizontal string
	to make it no gap penalty on the ends, just modify initialization to be all 0s 
	and also make scoring return 0 on gap penalty if on the last row/column
	
	Could have paramters be an input, and make gap_penalty function inputted as well?

	"""

#for gap_penalty scoring go to below function, which is the default
import time

file1 = open("string_crs.txt", "r")
file2 = open("RSRS.txt", "r")

ref_string = file1.read()
query_string = file2.read()

def default_gap_penalty(length): #always positive
	if length <= 0:
		return 0
	return 2 * (length-1) + 1

def abs(input):
	if input < 0:
		return -input
	return input

def needleman_wunsch(string1 = ref_string, string2 = query_string, match_score = 1, mismatch_score = -1, gap_penalty = default_gap_penalty):
	
	start_time = time.time()

	output_file = open("output.txt", "w")
	#strings 1 and 2 are input strings, presumably genomes
	length1 = len(string1)
	length2 = len(string2)
	length1_flag = -1
	if length1 > length2:
		longer_len = length1
		shorter_len = length2
		length1_flag = 1
	else:
		longer_len = length2
		shorter_len = length1

	max_displacement = 3
	row_width = (max_displacement * 2) + 1
	def initialize_grid(value, y_length = shorter_len + 1, x_length = row_width):
	#given two strings, create blank scoring matrix with dimensions 1 greater than each
		A = []
		for _ in range(y_length):
			A.append([])
		for x in range(y_length):
			for y in range(x_length):
				A[x].append(value)
		return A
	def initialize_scoring_grid():
		g = initialize_grid(None)
		for x in range(len(g[0])):
			g[0][x] = -gap_penalty(abs(x - max_displacement))
		return g
	def initialize_path_grid():
		g = initialize_grid(None)
		for x in range(len(g[0])):
			if (x - max_displacement) < 0:
				g[0][x] = -1
			if (x - max_displacement) > 0:
				g[0][x] = 1
		return g
	def print_grid(grid):
		a = len(grid)
		for x in range(a):
			print(grid[x])
	def sub_score(match):
		if match:
			return match_score
		else:
			return mismatch_score
	def get_indexes(row_number, x_loc): #converts from diagonal matrix to string indexes
		if (x_loc - max_displacement) < 0:
			first = row_number - 1
			second = row_number - 1 + (max_displacement - x_loc)
		else:
			first = row_number - 1 + (x_loc - max_displacement)
			second = row_number - 1
		return first, second
	def indexes_to_row_x(string1_index, string2_index):
		if string1_index > string2_index:
			row_number = string2_index + 1
			x_loc = (string1_index - string2_index) + max_displacement
			return row_number, x_loc
		else:
			row_number = string1_index + 1
			x_loc = max_displacement - (string2_index - string1_index) 
			return row_number, x_loc

	def score(row_number, x_loc):
		#Can do non-linear 
		#DICTIONARIES: score is key, location is value
		#FIX GAP PENALTY

		string1_index, string2_index = get_indexes(row_number, x_loc)
		def calc_gaps():
			gap_dict = {}
			#go_down, gaps in string2
			k = 1
			while (string2_index - k) >= 0 and (x_loc + k) < row_width:
				#print(row_number, x_loc)
				#print(string1_index, string2_index)
				a, b = indexes_to_row_x(string1_index, string2_index - k)
				#print(a,b)
				gap_dict[scoring_matrix[a][b] - gap_penalty(k)] = k
				k += 1
			j = 1
			while (string1_index - j) >= 0 and (x_loc - j) >= 0:
				a, b = indexes_to_row_x(string1_index - j, string2_index)
				
				gap_dict[scoring_matrix[a][b] - gap_penalty(j)] = -j
				j += 1
			return gap_dict

		if string1_index >= length1 or string2_index >= length2:
			return None
		score_path_dict = calc_gaps()

		calc_sub = scoring_matrix[row_number - 1][x_loc] + sub_score(string1[string1_index] == string2[string2_index])
		score_path_dict[calc_sub] = 0
		max_key = max(score_path_dict.keys())
		path_grid[row_number][x_loc] = score_path_dict[max_key]

		return max_key

	def align_strings():
		new_string1 = ''
		new_string2 = ''
		current_row = shorter_len
		current_x_loc = max_displacement

		while(path_grid[current_row][current_x_loc+length1_flag]!=None):
			current_x_loc += length1_flag

		current_string1_index, current_string2_index = get_indexes(current_row, current_x_loc)

		
		while(path_grid[current_row][current_x_loc]) != None:
			#k is current_path_pointer
			
			k = path_grid[current_row][current_x_loc]
			if k == 0:
				new_string1 = string1[current_string1_index] + new_string1
				new_string2 = string2[current_string2_index] + new_string2
				current_row -= 1
				current_string1_index -= 1
				current_string2_index -= 1
			elif k > 0:
				new_string2 = string2[(current_string2_index - k)+1:current_string2_index+1] + new_string2
				new_string1 = k*'_' + new_string1
				current_string2_index -= k
				current_row, current_x_loc = indexes_to_row_x(current_string1_index, current_string2_index)
			elif k < 0:
				new_string1 = string1[(current_string1_index - (-k))+1:current_string1_index+1] + new_string1
				new_string2 = (-k)*'_' + new_string2
				current_string1_index -= (-k)
				current_row, current_x_loc = indexes_to_row_x(current_string1_index, current_string2_index)

		return new_string1, new_string2

	scoring_matrix = initialize_scoring_grid()
	path_grid = initialize_path_grid() #negative x means to the left by x, positive x means up by x, 0 means up, left


	for row in range(shorter_len):
		for a in range(max_displacement+1):
			scoring_matrix[row+1][max_displacement+a] = score(row+1, max_displacement + a)
			scoring_matrix[row+1][max_displacement-a] = score(row+1, max_displacement - a)

	new_string1, new_string2 = align_strings()
	#print(new_string1)
	#print(new_string2)
	print(new_string1, file=output_file)
	print(new_string2, file=output_file)
	print(str(time.time() - start_time), file=output_file)

	
	return None

needleman_wunsch()

	




