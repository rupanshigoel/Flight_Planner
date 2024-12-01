from flight import Flight
from planner import Planner


def check_path_validity(path, start_city, end_city):
    """Checks if the given path is valid (all flights connect correctly)."""
    if not path or path[0].start_city != start_city or path[-1].end_city != end_city:
        print(f"Path validation failed: Path is empty or does not start at {start_city} or end at {end_city}.")
        return False
    for i in range(1, len(path)):
        if path[i].start_city != path[i-1].end_city:
            print(f"Path validation failed: Flight at index {i} does not connect correctly (from {path[i-1].end_city} to {path[i].start_city}).")
            return False
    return True

def compare_steps_and_time(actual_path, expected_criteria):
    """Compares path based on the number of steps (flights) and total time."""
    if len(actual_path) != expected_criteria["num_flights"]:
        print(f"Comparison failed: Expected {expected_criteria['num_flights']} flights but got {len(actual_path)}.")
        return False
    if actual_path[-1].arrival_time != expected_criteria["total_time"]:
        print(f"Comparison failed: Expected arrival time {expected_criteria['total_time']} but got {actual_path[-1].arrival_time}.")
        return False
    return True

def compare_fare(actual_path, expected_criteria):
    """Compares path based on total fare."""
    total_fare = sum(flight.fare for flight in actual_path)
    if total_fare != expected_criteria["total_fare"]:
        print(f"Comparison failed: Expected total fare {expected_criteria['total_fare']} but got {total_fare}.")
        return False
    return True

def compare_steps_and_fare(actual_path, expected_criteria):
    """Compares path based on the number of steps (flights) and total fare."""
    if len(actual_path) != expected_criteria["num_flights"]:
        print(f"Comparison failed: Expected {expected_criteria['num_flights']} flights but got {len(actual_path)}.")
        return False
    total_fare = sum(flight.fare for flight in actual_path)
    if total_fare != expected_criteria["total_fare"]:
        print(f"Comparison failed: Expected total fare {expected_criteria['total_fare']} but got {total_fare}.")
        return False
    return True

def validate_and_compare(actual_path, expected_criteria, start_city, end_city, t1, t2, check_type):
    """Validates path and compares it against the expected criteria, including time constraints for certain checks."""
    if not check_path_validity(actual_path, start_city, end_city):
        return False
    if check_type == "steps_and_time":
        if not (t1 <= actual_path[0].departure_time and actual_path[-1].arrival_time <= t2):
            print(f"Time constraint failed: Path departure time {actual_path[0].departure_time} or arrival time {actual_path[-1].arrival_time} is not within the range [{t1}, {t2}].")
            return False
        return compare_steps_and_time(actual_path, expected_criteria)
    elif check_type == "fare":
        return compare_fare(actual_path, expected_criteria)
    elif check_type == "steps_and_fare":
        return compare_steps_and_fare(actual_path, expected_criteria)
    else:
        print(f"Unknown check type: {check_type}")
        return False


def find_optimized_paths(flights, start_city, end_city, t1, t2):
    """
    Finds and returns optimized paths from start_city to end_city based on:
    - Least flights and earliest arrival
    - Least flights and cheapest fare
    - Overall cheapest route
    
    Args:
        flights (List[Flight]): List of available flights.
        start_city (int): Starting city.
        end_city (int): Destination city.
        t1 (int): Earliest departure time.
        t2 (int): Latest arrival time.
    
    Returns:
        Dict: A dictionary containing paths for the specified optimization criteria.
    """
    all_paths = []  # To store all valid paths

    def dfs(current_city, current_path, current_arrival_time, total_fare, flights_taken, prev_flight):
        # If we reached the end city, store the current path details
        if current_city == end_city:
            all_paths.append({
                "path": current_path[:],
                "total_time": current_arrival_time if prev_flight else 0,  # Overall time to reach end city
                "total_fare": total_fare,
                "num_flights": flights_taken
            })
            return

        # Explore all flights starting from the current city
        for flight in flights:
            # Consider only flights originating from the current city
            if flight.start_city != current_city:
                continue

            # Check departure constraint for the first flight
            if prev_flight is None and flight.departure_time < t1:
                continue
            
            # Ensure layover time of at least 20 minutes between flights
            if prev_flight is not None and flight.departure_time < prev_flight.arrival_time + 20:
                continue
            
            # Check if the flight's arrival is within the allowed time window
            if flight.arrival_time > t2:
                continue

            # Calculate new path details
            new_fare = total_fare + flight.fare
            new_flights_taken = flights_taken + 1

            # Recur to explore further paths
            current_path.append(flight)
            dfs(flight.end_city, current_path, flight.arrival_time, new_fare, new_flights_taken, flight)
            current_path.pop()  # Backtrack

    # Start DFS from the start city
    dfs(start_city, [], 0, 0, 0, None)

    # Variables to store the optimized paths
    least_flights_least_time = None
    least_flights_cheapest_fare = None
    overall_cheapest = None

    min_flights = float('inf')
    min_cost = float('inf')
    min_arrival_time = float('inf')  # Track the earliest arrival time

    for path_info in all_paths:
        last_flight = path_info["path"][-1] if path_info["path"] else None
        
        if path_info["num_flights"] < min_flights:
            min_flights = path_info["num_flights"]
            least_flights_least_time = path_info
            least_flights_cheapest_fare = path_info
            min_arrival_time = last_flight.arrival_time if last_flight else float('inf')
        elif path_info["num_flights"] == min_flights:
            # Update least flights and cheapest fare path if fare is lower
            if path_info["total_fare"] < least_flights_cheapest_fare["total_fare"]:
                least_flights_cheapest_fare = path_info
            # Update least flights and least time if arrival time is earlier
            if last_flight and last_flight.arrival_time < min_arrival_time:
                least_flights_least_time = path_info
                min_arrival_time = last_flight.arrival_time

        # Overall cheapest path (regardless of flights taken)
        if path_info["total_fare"] < min_cost:
            min_cost = path_info["total_fare"]
            overall_cheapest = path_info

    # Create result dictionary to hold the paths
    result = {
        "least_flights_least_time": least_flights_least_time,
        "least_flights_cheapest_fare": least_flights_cheapest_fare,
        "overall_cheapest": overall_cheapest
    }

    # Write paths to a file
    with open('optimized_paths.txt', 'w') as file:
        for key, path_info in result.items():
            if path_info:
                file.write(f"{key.replace('_', ' ').capitalize()}:\n")
                for flight in path_info["path"]:
                    file.write(f"  Flight No: {flight.flight_no}, From: {flight.start_city} To: {flight.end_city}, "
                               f"Departure: {flight.departure_time}, Arrival: {flight.arrival_time}, Fare: {flight.fare}\n")
                file.write(f"  Total Time: {path_info['total_time']} (arrival time)\n")
                file.write(f"  Total Fare: {path_info['total_fare']}\n")
                file.write(f"  Number of Flights: {path_info['num_flights']}\n\n")
            else:
                file.write(f"{key.replace('_', ' ').capitalize()}: No valid path found.\n\n")

    return result


def main():
    flights = [ Flight(0,0,10,1,30,10),
                Flight(1,0,10,2,20,50),  
                Flight(2,1,50,2,70,10),  
                Flight(3,1,40,3,60,40),  
                Flight(4,1,90,4,140,40),  
                Flight(5,2,40,3,50,30),  
                Flight(6,2,90,3,110,10),  
                Flight(7,2,20,4,40,20),  
                Flight(8,3,130,4,150,10),  
                Flight(9,3,70,5,80,20),  
                Flight(10,4,180,5,200,10),  
               ]
    flights3 = [
                Flight(0,0,300,1,330,100),
                Flight(1,0,360,1,390,10),
                Flight(2,1,350,2,400,10),
                Flight(3,1,410,2,420,1000),
    ]
    flights2 = [    Flight(0, 0, 5, 1, 25, 15),
    Flight(1, 0, 10, 2, 30, 40),
    Flight(2, 0, 15, 3, 40, 20),
    Flight(3, 1, 35, 2, 55, 25),
    Flight(4, 1, 50, 3, 70, 30),
    Flight(5, 1, 55, 4, 100, 50),
    Flight(6, 2, 60, 3, 90, 15),
    Flight(7, 2, 70, 4, 95, 35),
    Flight(8, 3, 80, 4, 100, 25),
    Flight(9, 3, 90, 5, 120, 45),
    Flight(10, 4, 110, 5, 130, 20),
    Flight(11, 4, 140, 6, 180, 60),
    Flight(12, 5, 150, 6, 200, 30),
    Flight(13, 6, 160, 7, 210, 70),
    Flight(14, 6, 180, 8, 230, 50),
    Flight(15, 7, 200, 8, 240, 40),
    Flight(16, 7, 220, 9, 260, 80),
    Flight(17, 8, 250, 9, 290, 35),
    Flight(18, 9, 280, 10, 310, 60),
    Flight(19, 9, 300, 10, 340, 20)  
               ]
    flights4 = [
        Flight(0,0,1,1,20,20),
        Flight(1,0,1,2,10,10),
        Flight(2,1,40,3,50,40),
        Flight(3,1,40,3,41,50),
        Flight(4,2,30,3,42,70),
        Flight(5,2,30,3,50,40),
        Flight(6,3,65,4,100,2),
        Flight(7,3,75,4,100,20),
    ]
    flight_planner1 = Planner(flights3)
    flight_planner2 = Planner(flights)
    flight_planner3 = Planner(flights4)

    # Test case 1
    params = (0, 2, 0, 1000)  # start, end, t1, t2
    route1 = flight_planner1.least_flights_earliest_route(*params)
    route2 = flight_planner1.cheapest_route(*params)
    route3 = flight_planner1.least_flights_cheapest_route(*params)
    paths = find_optimized_paths(flights3, *params)

    # Model expected paths
    expected_route1 = paths['least_flights_least_time']
    expected_route2 = paths["overall_cheapest"]
    expected_route3 = paths['least_flights_cheapest_fare']

    if validate_and_compare(route1, expected_route1, *params,'steps_and_time'):
        print("Task 1 PASSED")
    else:
        print("Task 1 FAILED")

    if validate_and_compare(route2, expected_route2, *params, 'fare'):
        print("Task 2 PASSED")
    else:
        print("Task 2 FAILED")

    if validate_and_compare(route3, expected_route3, *params, 'steps_and_fare'):
        print("Task 3 PASSED")
    else:
        print("Task 3 FAILED")
        print(route3)

    params = (0, 5, 0, 1000)  # start, end, t1, t2
    route1 = flight_planner2.least_flights_earliest_route(*params)
    route2 = flight_planner2.cheapest_route(*params)
    route3 = flight_planner2.least_flights_cheapest_route(*params)
    paths = find_optimized_paths(flights, *params)

    expected_route1 = paths['least_flights_least_time']
    expected_route2 = paths["overall_cheapest"]
    expected_route3 = paths['least_flights_cheapest_fare']

    if validate_and_compare(route1, expected_route1, *params,'steps_and_time'):
        print("Task 4 PASSED")
    else:
        print("Task 4 FAILED")

    if validate_and_compare(route2, expected_route2, *params, 'fare'):
        print("Task 5 PASSED")
    else:
        print("Task 5 FAILED")

    if validate_and_compare(route3, expected_route3, *params, 'steps_and_fare'):
        print("Task 6 PASSED")
    else:
        print("Task 6 FAILED")
        print(route3)

    params = (0, 4, 0, 1000)  # start, end, t1, t2
    route1 = flight_planner3.least_flights_earliest_route(*params)
    route2 = flight_planner3.cheapest_route(*params)
    route3 = flight_planner3.least_flights_cheapest_route(*params)
    paths = find_optimized_paths(flights4, *params)

    expected_route1 = paths['least_flights_least_time']
    expected_route2 = paths["overall_cheapest"]
    expected_route3 = paths['least_flights_cheapest_fare']
    if validate_and_compare(route1, expected_route1, *params,'steps_and_time'):
        print("Task 7 PASSED")
    else:
        print("Task 7 FAILED")

    if validate_and_compare(route2, expected_route2, *params, 'fare'):
        print("Task 8 PASSED")
    else:
        print("Task 8 FAILED")

    if validate_and_compare(route3, expected_route3, *params, 'steps_and_fare'):
        print("Task 9 PASSED")
    else:
        print("Task 9 FAILED")
   

if __name__ == "__main__":
    main()
