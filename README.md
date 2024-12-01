# Flight_Planner
The task involves designing a flight planner using a set of available flights,
characterized by departure and arrival cities, times, flight numbers, and fares.
Given that multiple flights may exist between any two cities, the planner must
efficiently choose the best itinerary based on three key objectives: minimizing
the number of flights, reducing costs, or balancing both factors.<br/>
# Constraints:
A person may take multiple flights to reach their
destination. However, after deboarding flight F at city A, the next
connecting flight must depart from city A atleast 20 min after
the arrival time of flight F, to ensure that the person is able to fulfill
all formalities of a connecting flight.<br/>
Given parameters start city, end city, t1, t2, find a route (i.e.,
a list of flights) such that you can reach end city from start city by departing
after or at t1 and reaching before or at t2<br/>
# Route 1 - Fewest Flights and Earliest: 
Identify a route between two
given cities A and B that uses the minimum number of flights. If
multiple options meet this criterion, choose the route that arrives at city
B the earliest.<br/>
# Route 2 - Cheapest Trip: 
Find a route between cities A and B with
the lowest total fare, regardless of the number of flights involved.<br/>
# Route 3 - Fewest Flights and Cheapest:
Identify a route between
two given cities A and B that uses the minimum number of flights. If
multiple options meet this criterion, choose the route that is the cheapest.
