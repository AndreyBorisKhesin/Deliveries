from numpy import *

past = loadtxt("monthly_sales.csv").reshape((12, 20, 2))
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
days = [27, 24, 27, 25, 27, 26, 26, 27, 25, 27, 26, 26]
sums = [0, 27, 51, 78, 103, 130, 156, 182, 209, 234, 261, 287, 313]

def dist_from_shops(a, b):
	return (abs(shop_coords[a][0] - shop_coords[b][0]) +
		abs(shop_coords[a][1] - shop_coords[b][1]))

def total_dist(stops):
	return sum([dist_from_shops(stops[i], stops[i + 1])
		for i in range(len(stops) - 1)])

def generate_customers():
	customers = zeros((313, 20, 2))
	monthly = asarray([[[int(round(past[month, store, product] *
		(0.9 + 0.2 * random.rand()))) for product in range(2)]
		for store in range(20)] for month in range(12)])
	for i in range(12):
		for j in range(20):
			for k in range(2):
				for l in range(monthly[i, j, k]):
					customers[int(sums[i] + days[i] *
						random.rand()), j, k] += 1
	return customers.astype(int)

def worst_schedule():
	schedule = []

	for day in range(313):
		warehouse_capacity = [[650, 650], [650, 650]]
		for w in range(2):
			while max(warehouse_capacity[w]) > 0:
				p1, p2 = 0, 0
				if warehouse_capacity[w][0] > 0:
					p1 = 25
					warehouse_capacity[w][0] -= p1
				if warehouse_capacity[w][1] > 0:
					p2 = int((20 - 0.8 * p1) / 0.4)
					warehouse_capacity[w][1] -= p2
				route = {
					"date": day,
					"stops": asarray([[w + 20, 0, 0],
						[w + 22, p1, p2],
						[w + 20, - p1, - p2]])
				}
				schedule = append(schedule, [route])

		# fill up stores (0 - 19)
		shop_capacity = [[15, 15, 20, 20, 15, 20, 30, 30, 35, 25, 30, 30, 30, 35,
			30, 40, 25, 20, 15, 20], [15, 15, 20, 20, 15, 20, 30, 30, 35, 25,
			30, 30, 30, 35, 30, 40, 25, 20, 15, 20]]
	
		for store in range(20):
			if store in [0, 2, 3, 5, 6, 10, 11, 13, 16, 17]:
				warehouse = 20
			else:
				warehouse = 21
			while max(shop_capacity[0][store],
				shop_capacity[1][store]) > 0:
				p1, p2 = 0, 0
				if shop_capacity[1][store] > 0:
					p2 = shop_capacity[1][store]
					shop_capacity[1][store] = 0
				if shop_capacity[0][store] > 0:
					p1 = int((20 - 0.4 * p2) / 0.8)
					shop_capacity[0][store] -= p1
				route = {
					"date": day,
					"stops": asarray([[warehouse, p1, p2],
						[store, -p1, -p2],
						[warehouse, 0, 0]])
				}
				schedule = append(schedule, [route])

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
	
	ITER = 1

	for i in range(ITER):
		customers = generate_customers() # (313, 20, 2)
		cost = 0
		revenue = 0
		stock = array([[0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0],
			[0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0],
			[0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0],
			[1000000000, 1000000000], [1000000000, 1000000000]])
		# s1 - s20, w1, w2, p1, p2
		capacity = [15, 15, 20, 20, 15, 20, 30, 30, 35, 25, 30, 30, 30, 35, 30,
			40, 25, 20, 15, 20, 650, 650, 1000000000, 1000000000]

		for day in range(313):
			routes = []

			for j in range(len(schedule)):
				if schedule[j]["date"] == day:
					routes = (append(routes, [schedule[j]["stops"]],
						axis = 0) if not routes == [] else
						[schedule[j]["stops"]])
			for route in routes:
				cost += total_dist(route[:, 0])
				
				truck = [0, 0]

				for stop in route:
					old_truck = copy(truck)

					for k in range(2):
						stop[k + 1] = max(min(stop[k + 1],
							stock[stop[0], k]), - truck[k])
						stock[stop[0], k] = min(max(
							stock[stop[0], k] - stop[k + 1],
							0), capacity[stop[0]])

						# load / unload truck
						truck[k] = max(stop[k], 0)
						old_truck[k] += min(stop[k], 0)

					# throw away extra
					if 2 * truck[0] + truck[1] > 50:
						if 2 * truck[0] <= 50:
							truck[1] = (50 - 2 * truck[0])
						else:
							truck = [25, 0]
					else:
						truck[0] += min(old_truck[0], (50 - 2 *
							truck[0] - truck[1]) // 2)
						truck[1] += min(old_truck[1], 50 - 2 *
							truck[0] - truck[1])

			for j in range(20):
				for k in range(2):
					old_stock = stock[j, k]
					stock[j, k] = max(stock[j, k] -
						customers[day, j, k], 0)
					revenue += ((300 - 200 * k) *
						(old_stock - stock[j, k]))
					for l in range(customers[day, j, k] - old_stock):
						if (random.rand() < 0.8 and day != 312):
							customers[day + 1, j, k] += 1

		profit = revenue - cost
		profits.append((revenue, cost))

	return profits

def extra_routes(month, day, cust_this_month, stock):
	"""
	Input:
		day: day of the year
		cust_this_month: (20, 2)
		stock: (24, 2)
	Return:
		Routes of extra trucks to send out with 1.2 times penalty
	"""
	extra = []
	day_of_month = day - sums[month]

	for store in range(20):
		p = [0, 0]
		for product in range(2):
			# expected = avg of the same month last year and 
			# the number of customers so far this month
			expected = 0.5 * (past[month, store, product] / days[month]) + \
				0.5 * (cust_this_month[store, product] / (day_of_month - 1))

			k = 1
			# If k times expected customers is greater than the stocks
			if expected * k > stock[store, product]:
				p[products] = capacity[store] - stock[store, product]

		route = {
			"date": day,
			"stops": array([[warehouse, p[0], p[1]],
				[store, -p[0], -p[1]],
				[warehouse, 0, 0]])
		}
		extra.append(route)
	return extra

#c = generate_customers()
#print([[[c[i,j,k] for k in range(2)] for j in range(20)] for i in range(313)])
print(profit(worst_schedule()))
