import re 
import csv
import random
import math
from random_address import real_random_address # used to generate random addresses (random-address 1.1.1)
import names # used to generate random driver names (names 0.3.0)

def generate_data(max_addresses, max_drivers):
	"""
	Used open source libraries, random_address and names, to generate random addresses and names.
	Writes addresses and driver names into two separate csv files.

	param max_addresses: int maximum number of addresses to generate
	param max_drivers: int maximum number of driver names to generate 
	"""

	# Generate a random number of addresses and names, from 75% of given max parameter up to the given max parameter
	address_count = random.randint(math.ceil(max_addresses*0.75), max_addresses)
	driver_count = random.randint(math.ceil(max_drivers*0.75), max_drivers)
	addresses = []
	drivers = []

	# generate random addresses and driver names
	for i in range(address_count):
		addresses.append(real_random_address()['address1'])
	for i in range(driver_count):
		drivers.append(names.get_full_name())

	# create two csv files (newline separated files) of addresses and drivers 
	# save these in the directory of this file
	with open('addresses.csv', 'w') as f:
		writer = csv.writer(f)
		for address in addresses:
			writer.writerow([address])
	with open('drivers.csv', 'w') as f:
		writer = csv.writer(f)
		for driver in drivers:
			writer.writerow([driver])

def parse_destinations(file_name):
	"""
	Returns a parsed list of destination or street names without the number or spaces
	and a hashmap of original destination name to the parsed street names. 

	param file_name: csv file name of destinations
	return: list of parsed destinations, dict of original destination to parsed destination name
	"""
	addresses = open(file_name).read().splitlines()
	destinations = []
	destinations_hash = {}
	for address in addresses:
		match = re.search(r'\d+(.*?\s+.+)', address)
		if match:
			matched_address = match.group(1)
			parsed_address = matched_address.replace(' ', '').lower()
			destinations.append(parsed_address)
			destinations_hash[parsed_address] = address
	return destinations, destinations_hash

def parse_drivers(file_name):
	"""
	Returns a parsed list of parsed strings of driver names with no spaces 
	and a hashmap of original driver names to the parsed driver names. 

	param: csv file name of drivers
	return: list of parsed driver names, dict of original driver name to parsed driver name
	"""
	driver_names = open(file_name).read().splitlines()
	drivers = []
	drivers_hash = {}
	for driver in driver_names:
		parsed_driver = driver.replace(' ', '').lower()
		drivers.append(parsed_driver)
		drivers_hash[parsed_driver] = driver
	return drivers, drivers_hash

def count_vowels(string):
	"""
	Returns the number of vowels in string. 

	param: string
	return: number of vowels in string
	"""
	num_vowels = 0
	for char in string:
		if char in "aeiou":
			num_vowels = num_vowels + 1
	return num_vowels

def count_consonants(string):
	"""
	Returns the number of consonants in string.

	param: string
	return: number of consonants in string
	"""
	num_consonants = 0
	for char in string:
		if char not in "aeiou":
			num_consonants = num_consonants + 1
	return num_consonants

def get_common_factors(x, y):
	"""
	Returns the set of common factors of x and y while excluding 1.

	param: int x, int y
	return: set of common factors for ints x and y excluding 1
	"""
	common_factors = set()
	for i in range(2, min(x, y) + 1):
		if x % i == 0 and y % i == 0:
			common_factors.add(i)
	return common_factors

def calculate_base_ss(destination, driver):
	"""
	Returns the base suitibility score of a destination and driver.

	param: parsed destination str
	param: parsed driver str
	return: base suitibility score (float)
	"""
	if len(destination) % 2 == 0:
		return count_vowels(driver) * 1.5
	else:
		return count_consonants(driver)

def calculate_ss(destination, driver):
	"""
	Returns the suitibility score of a destination and driver by taking common factor into account.

	param: parsed destination str
	param: parsed driver str
	return: suitibility score (float)
	"""
	base_score = calculate_base_ss(destination, driver)
	common_factors = get_common_factors(len(destination), len(driver))
	if len(common_factors) > 0:
		return base_score * 1.5
	else:
		return base_score

def assign_shipments(destinations, drivers):
	"""
	Returns the maximum total suitibility score and corresponding destination driver assignments in an array.
	Utilizes the Hungarian algorithm for solving a weighted bipartite assignment problem:
		Time complexity: O(n^3)
		Space complexity: O(n^2)

	param: list of parsed destinations
	param: list of parsed driver names 
	return: total maximum suitibility score (float), list of optimal assignments with parsed destination and driver matches
	"""
	num_destinations = len(destinations)
	num_drivers = len(drivers)

	# create matrix of calculated suitability scores for all possible combinations of destinations to drivers
	ss_matrix = []
	for i in range(num_destinations):
		row = []
		for j in range(num_drivers):
			row.append(calculate_ss(destinations[i], drivers[j]))
		ss_matrix.append(row)
	# create indicies of the matrix to track assignment
	row_indices, col_indices = list(range(num_destinations)), list(range(num_drivers))
	assignments = []
	# loop until all possible destinations or drivers are assigned, whichever is lower
	while len(assignments) < min(num_destinations, num_drivers):
		max_val = -float('inf')
		max_row, max_col = -1, -1
		for i in row_indices:
			for j in col_indices:
				if ss_matrix[i][j] > max_val:
					# trying to find maximum assignment that has not been assigned according to the ss_matrix
					max_val = ss_matrix[i][j]
					max_row, max_col = i, j
		# optimize assignment process by stopping early if there are no more assignments for 
		# the current shipment loop that would increase total suitabililty score 
		if max_val == 0:
			break
		assignments.append((destinations[max_row], drivers[max_col]))
		# remove maxed ss matched row and col 
		row_indices.remove(max_row)
		col_indices.remove(max_col)

	# calculate total score based on optimal assignment array
	total_score = 0
	for destination, driver in assignments:
		total_score += calculate_ss(destination, driver)

	return total_score, assignments

def create_assignment_file(assignments, destinations_hash, drivers_hash):
	"""
	Creates an assignments.csv file that outputs the optimal destination to driver assignments with their original
	names by using hashmaps mapping the parsed destination and driver names with their original counterparts.

	param: list of optimal assignments with parsed destination and driver matches
	param: dict of original driver name to parsed driver name
	param: dict of original destination to parsed destination name
	"""
	headerList = ['destination', 'driver']
	with open('assignments.csv', 'w') as file:
		writer = csv.writer(file)
		writer.writerow(('destination', 'driver'))
		for destination, driver in assignments:
			writer.writerow((destinations_hash[destination], drivers_hash[driver]))

def main():
	generate_data(20, 20)
	destinations, destinations_hash = parse_destinations('addresses.csv')
	drivers, drivers_hash = parse_drivers('drivers.csv')
	total_score, assignments = assign_shipments(destinations, drivers)
	create_assignment_file(assignments, destinations_hash, drivers_hash)
	print(f'Total SS: {total_score}')
	print('Assignments:')
	for destination, driver in assignments:
		print(f'{destinations_hash[destination]} -> {drivers_hash[driver]}')

if __name__ == "__main__":
	main()


