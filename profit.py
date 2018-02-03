from numpy import *

past = loadtxt("monthly_sales.csv")
shop_coords = {
	 0: ( 2, 6)
	 1: (10, 6)
	 2: ( 3, 5)
	 3: ( 5, 5)
	 4: ( 8, 5)
	 5: ( 0, 4)
	 6: ( 2, 3)
	 7: ( 6, 3)
	 8: (10, 3)
	 9: (12, 3)
	10: ( 1, 2)
	11: ( 4, 2)
	12: (11, 2)
	13: ( 3, 1)
	14: ( 8, 1)
	15: (10, 1)
	16: ( 2, 0)
	17: ( 4, 0)
	18: ( 7, 0)
	19: (12, 0)
	20: ( 4, 3)
	21: ( 9, 2)
	22: ( 1, 4)
	23: ( 6, 1)
}

def dist_from_shops(a, b):
	return (abs(shop_coords.get(a)[0] - shop_coords.get(b)[0]) +
		abs(shop_coords.get(a)[1] - shop_coords.get(b)[1]))

def total_dist(stops):
	return sum([dist_from_shops(i, i + 1) for i in range(len(stops) - 1)])

def customers():
	return [[[int(round(past[month, 2 * store + product] *
		(0.9 + 0.2 * random.rand()))) for product in range(2)]
		for store in range(20)] for month in range(12)]

def profit(schedule):
	"""
	schedule: A list of routes
	route: A dictionary that represents a delivery route of a truck
		{	"date": int, 
			"stops"; list of tuples representing the number of p1 and p2 the drop off, 
			"path": list of tuples representing the distance and direction 
				(True = EW, False = NS and (0, 0) means stop),
			"starting": starting point of truck	}
		Example: 
		{	"date": 98, 
			"stops": [(3, 5), (-4, 7), (-2, 0)], 
			"path": [(5, False), (0, True), (-3, True), (0, 0)]	
			"starting": (3, 5)	}
	"""
	profits = []

	for i in len(range(100)):
		customers = customers() # (320, 20, 2)
		cost = 0
		revenue = 0
		stock = zeros((22, 2)) # s1 - s20, w1, w2
		route_idx = 0

		for day in range(len(313)):

			for j in range(route_idx, len(schedule)):

				if schedule[j]["day"] == day:
					route = schedule[j]
					route_idx += 1
				else:
				 	break
			
				currx, curry = route["starting"]
				truckp1, truckp1 = (0, 0)
				stop = 0

				for dist, direction in route["path"]:
					if (dist, direction) != (0, 0):
						if direction:
							currx += dist
						else:
							curry += dist 
						cost += dist

					else: 
						number = coord_to_shop(currx, curry)
						if number != -1: # load / unload at a store / warehouse
							stock[number][0] += route["stops"][stop][0]
							stock[number][1] += route["stops"][stop][1]
						# load at a plant
						truckp1 += route["stops"][stop][0]
						truckp2 += route["stops"][stop][1]
						stop += 1

			for j in range(20):
				for k in range(2):
					if customers[day][j][k] <= stock[j][k]:
						revenue += (300 - 200 * k) * customers[day][j][k]
					else:
						revenue += (300 - 200 * k) * stock[j][k]
						for l in range(customers[day][j][k] - stock[j][k]):
							if random.rand() < 0.8 and day != 312:
								customers[day + 1][j][k] += 1

		profit = cost - revenue
		profits.append(profit)

	return profits
