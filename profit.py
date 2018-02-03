from numpy import *

past = loadtxt("monthly_sales.csv")			

def coord_to_shop(x, y):
	return {
		20:  0,
		76:  1,
		26:  2,
		40:  3,
		61:  4,
		 4:  5,
		17:  6,
		45:  7,
		73:  8,
		87:  9,
		 9: 10,
		30: 11,
		79: 12,
		22: 13,
		57: 14,
		71: 15,
		14: 16,
		28: 17,
		49: 18,
		84: 19,
		31: 20,
		65: 21
	}.get(7 * x + y, -1)

def customers():
	return [[[int(round(past[month, 2 * store + product] *
		(0.9 + 0.2 * random.rand()))) for product in range(2)]
		for store in range(20)] for month in range(12)]

def profit(schedule):
	"""
	schedule: A list of routes
	route: A dictionary that represents a delivery route of a truck
		{	"date": int, 
			"stops"; list of triples representing the point 
			(store / warehouse / plant), number of p1 and p2 the drop off, 
			"starting": starting point of truck	}
		Example: 
		{	"date": 98, 
			"stops": [(20, 3, 5), (13, -4, 7), (15, -2, 0)], 	
			"starting": (3, 5)	}
	"""
	profits = []

	for i in len(range(100)):

		customers = customers() # (320, 20, 2)
		cost = 0
		revenue = 0
		stock = zeros((22, 2)) # s1 - s20, w1, w2
		route_idx = 0
		shop_capacity = [15, 15, 20, 20, 15, 20, 30, 30, 35, 25, 
						30, 30, 30, 35, 30, 40, 25, 20, 15, 20]
		warehouse_capacity = [[650, 650], [650, 650]]

		for day in range(len(313)):

			for j in range(route_idx, len(schedule)):

				truck_capacity = 

				if schedule[j]["day"] == day:
					route = schedule[j]
					route_idx += 1
				else:
				 	break
			
				currx, curry = route["starting"]
				stop = 0



			for stop in range(len(route["stops"])):
				number = coord_to_shop(currx, curry)
				if number != -1: # load / unload at a store / warehouse
					for k in range(2):
						if route["stops"][stop][k] + stock[numb] <= shop_capacity[k][number]:
							shop_capacity[k][number] -= stock[number][k]
						else:
							shop_capacity[k][number] = 0
						stock[number][k] -= route["stops"][stop][k]

					stock[number][1] += route["stops"][stop][1]
				# load at a plant
				truckp1 += route["stops"][stop][0]
				truckp2 += route["stops"][stop][1]

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
