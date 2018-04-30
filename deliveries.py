from numpy import *

past = loadtxt("monthly_sales.csv").reshape((12, 20, 2))
capacity = [15, 15, 20, 20, 15, 20, 30, 30, 35, 25, 30, 30, 30, 35, 30, 40, 25, 20, 15,
	20, 650, 650, 1000000000, 1000000000]
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
shop_to_p = [0, 1, 0, 0, 1, 0, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1]
w1_shops = [5, 6, 10, 0, 11, 2, 17, 13, 3, 16]
w2_shops = [7, 14, 18, 15, 4, 8, 12, 19, 9, 1]
indices = [3, 9, 5, 8, 4, 0, 1, 0, 5, 8, 2, 4, 6, 7, 1, 3, 9, 6, 2, 7]
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

def worst_schedule(max_day):
	schedule = []

	for day in range(max_day):
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
				schedule.append(route)

		# fill up stores (0 - 19)
		shop_capacity = [[15, 15, 20, 20, 15, 20, 30, 30, 35, 25, 30, 30, 30, 35,
			30, 40, 25, 20, 15, 20], [15, 15, 20, 20, 15, 20, 30, 30, 35, 25,
			30, 30, 30, 35, 30, 40, 25, 20, 15, 20]]
	
		for store in range(20):
			if store in w1_shops:
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
					p1 = min(int((20 - 0.4 * p2) / 0.8),
						shop_capacity[0][store])
					shop_capacity[0][store] -= p1
				warehouse_capacity[warehouse - 20][0] += p1
				warehouse_capacity[warehouse - 20][1] += p2
				route = {
					"date": day,
					"stops": asarray([[warehouse, p1, p2],
						[store, -p1, -p2],
						[warehouse, 0, 0]])
				}
				schedule.append(route)

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
				schedule.append(route)

	return schedule

def execute_route(route, stock):
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
			truck[k] = max(stop[k + 1], 0)
			old_truck[k] += min(stop[k + 1], 0)

		# throw away extra
		if 2 * truck[0] + truck[1] > 50:
			if truck[0] <= 25:
				truck[1] = (50 - 2 * truck[0])
			else:
				truck = [25, 0]
		else:
			truck[0] += min(old_truck[0], (50 - 2 *
				truck[0] - truck[1]) // 2)
			truck[1] += min(old_truck[1], 50 - 2 *
				truck[0] - truck[1])
	return stock

def month_from_day(day):
	return searchsorted(sums, day + 1) - 1

def profit(schedule, extra_route_function):
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
	
	ITER = 1000

	for i in range(ITER):
		customers = generate_customers() # (313, 20, 2)
		cost = 0
		revenue = 0
		stock = array([[0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0],
			[0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0],
			[0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0],
			[1000000000, 1000000000], [1000000000, 1000000000]])
		extra_customers = zeros((20, 2))
		# s1 - s20, w1, w2, p1, p2

		for day in range(313):
			routes = []

			for j in range(len(schedule)):
				if schedule[j]["date"] == day:
					routes.append(schedule[j]["stops"])
			for route in routes:
				cost += total_dist(route[:, 0])
				stock = execute_route(route, stock)
			
			month = month_from_day(day)
			added_routes = extra_route_function(month, day, -ones((20, 2)) if
				day == sums[month] else mean(customers[sums[month]:day],
				axis = 0), stock)

			for added_route in added_routes:
				cost += 1.2 * total_dist(added_route[:, 0])
				stock = execute_route(added_route, stock)

			for j in range(20):
				for k in range(2):
					total_customers = int(customers[day, j, k] +
						extra_customers[j, k])
					extra_customers[j, k] = 0
					old_stock = stock[j, k]
					stock[j, k] = max(stock[j, k] -
						total_customers, 0)
					revenue += ((300 - 200 * k) *
						(old_stock - stock[j, k]))
					for l in range(total_customers - old_stock):
						if random.rand() < 0.8:
							extra_customers[j, k] += 1

		profits.append([revenue - cost, revenue, cost])
		print(len(profits), mean(profits, axis = 0), std(profits, axis = 0))

	return mean(array(profits)[:, 0])

def extra_routes(month, day, mean_this_month, stock):
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
	shop_capacity = [capacity] * 2 - stock.T

	a = 0.5 #expected from historical data
	b = 0.5 #expected from this month so far

	warehouse_capacity = [650, 650] - stock[20:22]
	w_trips = []
	for w in range(2):
		while warehouse_capacity[w].dot([2, 1]) >= 50:
			p1 = min(25, warehouse_capacity[w][0])
			p2 = min(50 - 2 * p1, warehouse_capacity[w][1])
			warehouse_capacity[w] -= [p1, p2]
			w_trips.append([w, p1, p2])

	s_trips = []
	for store in range(20):
		for product in [1, 0]:
			# expected = avg of the same month last year and 
			# the number of customers so far this month
			expected = (a * past[month, store, product] / days[month] +
				b * mean_this_month[store, product])
			if day_of_month == 0:
				expected = ((a + b) * past[month, store, product] /
					days[month])

			# If k times expected customers is greater than the stocks
			while (1.2 * expected >= capacity[store] -
				shop_capacity[product][store] and
				shop_capacity[product][store] > 0):
				p1, p2 = 0, 0
				if product == 0:
					p1 = min(25, shop_capacity[0][store])
					p2 = min(50 - 2 * p1, shop_capacity[1][store])
				else:
					p2 = shop_capacity[1][store]
					p1 = min((50 - p2) // 2, shop_capacity[0][store])
				shop_capacity[0][store] -= p1
				shop_capacity[1][store] -= p2
				if p1 + p2 > 0:
					s_trips.append([store, p1, p2])
	while len(w_trips) > 0:
		w, p1, p2 = w_trips[0]
		shops = w1_shops if w == 0 else w2_shops
		best_trip, bti, mind = 0, -1, 10
		for i, trip in enumerate(s_trips):
			if trip[0] in shops and indices[trip[0]] < mind:
				mind = indices[trip[0]]
				best_trip = trip
				bti = i
		if bti == -1:
			extra.append(array([[w + 20, 0, 0], [w + 22, p1, p2],
				[w + 20, -p1, -p2]]))
		else:
			extra.append(array([[w + 20, best_trip[1], best_trip[2]],
				[best_trip[0], -best_trip[1], -best_trip[2]],
				[w + 22, p1, p2], [w + 20, -p1, -p2]]))
			s_trips = delete(s_trips, bti, axis = 0)
		w_trips = delete(w_trips, 0, axis = 0)
	while len(s_trips) > 0:
		s, p1, p2 = s_trips[0]
		w = 20 if s in w1_shops else 21
		extra.append(array([[w, p1, p2], [s, -p1, -p2], [w, 0, 0]]))
		s_trips = delete(s_trips, 0, axis = 0)
	return extra

print(profit(worst_schedule(1), extra_routes))
