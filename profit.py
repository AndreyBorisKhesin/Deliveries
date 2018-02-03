from numpy import *

past = loadtxt("monthly_sales.csv")

def customers():
	return [[[round(past[month, 2 * store + product] *
		(0.9 + 0.2 * random.rand()) for product in range(2)]
		for store in range(20)] for month in range(12)]

def profit(schedule):
	"""
	schedule: A list of routes
	route: A dictionary that represents an annual delivery schedule
		{	"date": int, 
			"stops"; list of tuples representing the number of p1 and p2 the drop off, 
			"path": list of tuples representing the distance and direction 
				(True = EW, False = NS and (0, 0) means stop),
			"starting": starting point of truck	}
		Example: 
		{	"date": 98, 
			"stops": [(3, 5), (-4, 7), (-2, 0)], 
			"path": [(5, False), (0, True), (-3, True), (0, 0)]	
			"starting": (3, 5)}
	"""
	cost = 0
	revenue = 0

	for route in schedule:
		
		currx, curry = route["starting"]
		for dist, direction in route["path"]:
			if (x, y) != (0, 0):


	profit = cost - revenue
	return profit
