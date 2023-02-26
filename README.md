# Platform-Science-SDE-Assignment

## Setup and Execution
1. Install open source libraries ([**random_address**](https://pypi.org/project/random-address/) and [**names**](https://pypi.org/project/names/)) by running:
```console
pip install -r requirements.txt
```
2. Run the following command to execute script: 
```console
python shipments_to_drivers.py
```
3. Final output will be printed like: 
```
Total SS: float (xx.xx)
Assignments:
destination_1 -> driver_1
destination_2 -> driver_2
...
destination_i -> driver_j
```
4. Script will also create an **assignments.csv** file with the optimal destination to driver assignments.

## Assumptions
* Street addresses only contain the street name and no other information such as city, zip code, or receiver name. 
* There are no characters other than numbers and letters for both street and driver names. 
* Street numbers are not part of the street name. 
* First and last names are both considered for the driver's name. 
* Street names such as "1st Street" are part of the street name. 
* The letter *y* is not a vowel.
* Common factors are where lengths of strings share a common divisor other than 1.

## Code Commentary 

```python
generate_data(20, 20)
```
Utilize open source libraries, random_address and names, to generate random addresses and names to use for destinations and drivers.
Generate a random number of destinations and drivers from 75% of given parameter up to given parameter, in this example from 15 to 20 randomized names. 
This is done to create a realistic scenario where there are likely to be an uneven number of destinations to drivers. 
Output the generated data into csv files, **addresses.csv** and **drivers.csv**. 
```python
destinations, destinations_hash = parse_destinations('addresses.csv')
drivers, drivers_hash = parse_drivers('drivers.csv')
````
Parse the generated addresses and drivers from their csv files by removing street numbers and spaces. 
Return a list of parsed destinations and driver names in addition to hashmaps of original names to corresponding parsed names to match up later. 
```python
total_score, assignments = assign_shipments(destinations, drivers)
```
Assigned destinations to drivers to maximize total suitability score by using the [Hungarian algorithm](https://en.wikipedia.org/wiki/Hungarian_algorithm).

Because each destination to driver assignment carries different weights (suitability score) and you are trying to match for the maximum total suitability score, this is an example of a *weighted bipartite assignment problem*. 

Steps implemented for this algorithm include: 
1. Create a 2-D matrix of calculated suitability scores for all possible combinations of destinations to drivers
2. Create a 2-D list of indicies of this matrix to track assignments
3. Loop through list of indicies to track assignments, find the maximum suitabililty score per row and column. 
4. Append maximum destination-driver pairing to assignment list and remove those indicies from the list of indicies
5. Optimize assignment process by stopping early if there are no more assignments for the current shipment loop that would increase total suitabililty score 
6. Continue through steps 3-5 until all possible destinations or drivers are assigned, whichever is lower

Time complexity: $O(n^3)$ - takes $O(n^2)$ time to calculate the 2D array of all possible suitability scores and iterate through indicies, finding the augmenting path through this array adds another *n* time for all the possible assignments, therefore: $O(n^2*n)=O(n^3)$

Space complexity: $O(n^2)$ - due to the storage of all possible suitability scores in a 2-D matrix 

Calculate total suitability score based on the optimal assignments made and return both the score and assignment list. 
```python
create_assignment_file(assignments, destinations_hash, drivers_hash)
```
Create an output file, **assignments.csv**, that shows the optimal destination to driver assignments. Need to input hashmaps as a parameter to display the original destination and driver names instead of the parsed names. 
```python 
print(f'Total SS: {total_score}')
print('Assignments:')
for destination, driver in assignments:
  print(f'{destinations_hash[destination]} -> {drivers_hash[driver]}')
```
Print the resultant maximum total suitability score in addition to the assignments in a text format. 

## Sample Test Case
```
Destinations:
514 East 38th Street
275 Ridge Lane

Drivers: 
Thomas Stansberry
Cora Depner
Joseph Tucker

Result: 
Total SS: 21.0
Assignments:
275 Ridge Lane -> Thomas Stansberry
514 East 38th Street -> Cora Depner
```

Explanation: 
```
ridgelane (length: 9, odd) -> thomasstansberry (length: 16, even; consonants: 12) score = 12
east38thstreet (length: 14, even) -> coradepner (length: 10, even + common factor; vowels: 4) score = 4 * 1.5 = 6 * 1.5 = 9
maximum total suitability score = 21.0 
```




