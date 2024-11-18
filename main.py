<<<<<<< HEAD
from datetime import datetime

from preprocess_data import preprocess_csv
from person import Person
import random
from pois import POIs
=======
import datetime
import random
from preprocess_data import preprocess_csv
from pois import POIs
from person import Person
>>>>>>> origin/leave_distribution

def leaving_poi(person: Person, current_time, pois: POIs, current_occupancy):
    """
    Simulates leaving a certain POI using probabilistic measure based on dwell time and occupancy.
    """
    if person.is_poi:
        poi_id = person.curr_poi
        hour_stayed = person.hour_stayed

        # Get the dwell time CDF for the POI
        dwell_times, dwell_time_cdf = pois.get_dwell_time_cdf(poi_id)

        # Find the index where the dwell time exceeds the person's hour_stayed
        index = 0
        while index < len(dwell_times) and dwell_times[index] < hour_stayed:
            index += 1

        # Probability that the person leaves after hour_stayed
        if index < len(dwell_time_cdf):
            leave_prob = dwell_time_cdf[index]
        else:
            leave_prob = 1.0  # Maximum probability if they've exceeded all dwell times

        # Adjust leave_prob based on occupancy
        
        expected_capacity = pois.get_capacity(poi_id, current_time)
        current_poi_occupancy = current_occupancy.get(poi_id, 0)
        occupancy_ratio = current_poi_occupancy / expected_capacity if expected_capacity > 0 else 0

        # If occupancy is higher than expected, increase leave probability
        if occupancy_ratio > 1:
            leave_prob *= occupancy_ratio
        else:
            leave_prob *= 0.5  # Decrease leave probability if occupancy is low

        # Ensure leave_prob is between 0 and 1
        leave_prob = min(max(leave_prob, 0), 1)

        # Decide if the person leaves
        if random.random() < leave_prob:
            person.leave()
            # Update occupancy
            current_occupancy[poi_id] -= 1
            print("exited!")
        else:
            person.stay()
            print("stayed!")
    return

<<<<<<< HEAD
def main(file_path, start_time, simulation_duration):
    # Process CSV Data
    print("Parsing the CSV file...")
    poi_dict = preprocess_csv(file_path)
    print(f"Parsed {len(poi_dict)} POIs.")
=======

def entering_poi(person, pois, current_time, current_occupancy):
    """
    Simulates entering a certain poi using probabilistic measure.
    """
    if not person.is_poi:
        # Generate a random probability
        enter_prob = random.random()  # Random value between 0 and 1
        print(f"Random probability for entering: {enter_prob:.2f}")
        
        # Check if the person enters based on a threshold
        if enter_prob < 0.3:  # 30% chance of entering
            poi_id = random.choice(list(pois.pois_dict.keys()))  # Randomly pick a POI
            print(f"Person entered POI: {pois.pois_dict[poi_id]['location_name']} (POI ID: {poi_id})")
            person.visit(poi_id)
        else:
            print("Person did not enter any POI.")
    return

def main(file_path):
    # Process CSV Data
    print("Parsing the CSV file...")
    pois_dict = preprocess_csv(file_path)
    pois_names_to_ids = {}  # Assuming you have this mapping
    pois = POIs(pois_dict, pois_names_to_ids)
    print(f"Parsed {len(pois_dict)} POIs.")
>>>>>>> origin/leave_distribution

    # Create population
    hagerstown_pop = 2500
    people = {person_id: Person() for person_id in range(hagerstown_pop)}
    print(f"Created {hagerstown_pop} Person instances.")

    # Initialize current occupancy
    current_occupancy = {poi_id: 0 for poi_id in pois_dict.keys()}

<<<<<<< HEAD
    # Create POIs
    pois = POIs(poi_dict)
    print("Created a POIs instance.")

    for hour in range(simulation_duration):
        print(f"Simulating hour {hour + 1}/{simulation_duration}...")

        capacities = pois.get_capacities_by_time(current_time)

        # Simulate people leaving and entering POIs
        for person_id, person in people.items():
            leaving_poi(person, poi_dict)
            entering_poi(person, poi_dict)
        
        # Update the current time
        current_time = start_time + datetime.timedelta(hours=1)

    # Output the results
=======
    # Main iteration
    days = 30
    for day in range(days):
        for hour in range(24):
            current_time = datetime.datetime(2021, 4, 1) + datetime.timedelta(days=day, hours=hour)
            print(current_time.day, current_time.hour)
            for person_id, person in people.items():
                leaving_poi(person, current_time, pois, current_occupancy)
                entering_poi(person, pois, current_time, current_occupancy)
>>>>>>> origin/leave_distribution


if __name__ == "__main__":
    # Run the main function
    with open('setting.txt', 'r') as f:
        start_time = f.readline().strip()
        simulation_duration = int(f.readline().strip())
    main('./input/hagerstown.csv', datetime.fromisoformat(start_time), simulation_duration)
