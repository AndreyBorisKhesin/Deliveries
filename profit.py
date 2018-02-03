from numpy import *

past = loadtxt("monthly_sales.csv")
shop_coords = {
	 0: ( 2, 6),
	 1: (10, 6),
	 2: ( 3, 5),
	 3: ( 5, 5),
	 4: ( 8, 5),
	 5: ( 0, 4),
	 6: ( 2, 3),
	 7: ( 6, 3),
	 8: (10, 3),
	 9: (12, 3),
	10: ( 1, 2),
	11: ( 4, 2),
	12: (11, 2),
	13: ( 3, 1),
	14: ( 8, 1),
	15: (10, 1),
	16: ( 2, 0),
	17: ( 4, 0),
	18: ( 7, 0),
	19: (12, 0),
	20: ( 4, 3),
	21: ( 9, 2),
	22: ( 1, 4),
	23: ( 6, 1)
}

def dist_from_shops(a, b):
	return (abs(shop_coords[a, 0] - shop_coords[b, 0]) +
		abs(shop_coords[a, 1] - shop_coords[b, 1]))

def total_dist(stops):
	return sum([dist_from_shops(i, i + 1) for i in range(len(stops) - 1)])

def customers():
	return [[[int(round(past[month, 2 * store + product] *
		(0.9 + 0.2 * random.rand()))) for product in range(2)]
		for store in range(20)] for month in range(12)]

def schedule():
	schedule = []

	for day in range(1):
		warehouse_capacity = [[560, 560], [560, 560]]
		for w in range(2):
			while warehouse_capacity[w][0] > 0 or warehouse_capacity[w][1] > 0:
				p1, p2 = 0, 0
				if warehouse_capacity[w][0] > 0:
					p1 = 20 / 0.4
					warehouse_capacity[w][0] -= p1
				if warehouse_capacity[w][1] > 0:
					p2 = (20 - 0.4 * p1) // 0.8
					warehouse_capacity[w][1] -= p2
				route = {"date": day, 
						"stops": [[w+20, p1, p2], [w+22, -p1, -p2], [w+20, 0, 0]]}
				schedule.append(route)

		# fill up stores (0 - 19)
		shop_capacity = [[15, 15, 20, 20, 15, 20, 30, 30, 35, 25, 
						30, 30, 30, 35, 30, 40, 25, 20, 15, 20],
						[15, 15, 20, 20, 15, 20, 30, 30, 35, 25, 
						30, 30, 30, 35, 30, 40, 25, 20, 15, 20]]
	
		for store in range(20):
			if store in [0, 2, 3, 5, 6, 10, 11, 13, 16, 17]:
				warehouse = 20
			else:
				warehouse = 21
			while shop_capacity[0][store] > 0 or shop_capacity[1][store] > 0:
				p1, p2 = 0, 0
				if shop_capacity[0][store] > 0:
					p1 = shop_capacity[0][store]
					shop_capacity[0][store] = 0
				if shop_capacity[1][store] > 0:
					p2 = (20 - 0.4 * p1) // 0.8
					shop_capacity[1][store] -= p2
				route = {"date": day, 
						"stops": [[warehouse, p1, p2], [store, -p1, -p2], [warehouse, 0, 0]]}
				schedule.append(route)

	return schedule

def profit(schedule):
	"""
	schedule: A list of routes
	route: A dictionary that represents a delivery route of a truck
		{	"date": int, 
			"stops"; list of triples representing the point 
				(store / warehouse / plant), number of p1 and
				p2 to pick up / drop off
		}
		Example: 
		{	
			"date": 98, 
			"stops": [[20, 3, 5], [13, -4, 7], [15, -2, 0]]
		}
	"""
	profits = []
	
	const ITER = 100

	for i in len(range(ITER)):

		customers = customers() # (320, 20, 2)
		cost = 0
		revenue = 0
		stock = [[0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0],
			[0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0],
			[0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0],
			[0, 0], [0, 0], [0, 0], [0, 0],
			[1000000000, 1000000000], [1000000000, 1000000000]]
		# s1 - s20, w1, w2, p1, p2
		route_idx = 0
		capacity = [15, 15, 20, 20, 15, 20, 30, 30, 35, 25, 30, 30,
			30, 35, 30, 40, 25, 20, 15, 20, 650, 650, 1000000000,
			1000000000]

		for day in range(313):

			routes = []

			for j in range(route_idx, len(schedule)):

				truck_capacity = [0, 0]
				
				if schedule[j, "date"] == day:
					routes.add(schedule[j, "stops"])
					route_idx += 1
				else:
				 	break
			
			for route in routes:
				cost += total_dist([route[i, 0] for i in
					range(len(route))])
				
				truck = [0, 0]

				for stop in route:
					old_truck_values = truck[:]

					for k in range(2):
						stop[k + 1] = max(min(
							stop[k + 1],
							stock[stop[0], k])
							- truck[k])
						stock[stop[0], k] = min(max(
							stock[stop[0], k] +
							stop[k + 1], 0),
							capacity[stop[0]])

						# load / unload truck
						truck[k] = max(stop[k], 0)
						old_truck[k] += min(stop[k],
							0)

					# throw away extra
					if 2 * truck[0] + truck[1] > 50:
						if 2 * truck[0] <= 50:
							truck[1] = (50 - 2 *
								truck[0])
						else:
							truck = [25, 0]
					else:
						truck[0] += min(old_truck[0],
							(50 - 2 * truck[0] -
							truck[1]) // 2)
						truck[1] += min(old_truck[1],
							50 - 2 * truck[0] -
							truck[1])

			for j in range(20):
				for k in range(2):
					old_stock = stock[j, k]
					stock[j, k] = max(
						customers[day, j, k] -
						stock[j, k], 0)
					if (customers[day, j, k] <=
						stock[j, k]):
					revenue += ((300 - 200 * k) *
						old_stock - stock[j, k])
					for l in range(customers[day, j, k] -
						stock[j, k]):
						if (random.rand() < 0.8 and
							day != 312):
							customers[day + 1, j,
								k] += 1

		profit = cost - revenue
		profits.append(profit)

	return profits
