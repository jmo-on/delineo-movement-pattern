from datetime import datetime

from preprocess_data import preprocess_csv
from person import Person
import random
from pois import POIs

def leaving_poi(person: Person):
    """
    Simulates leaving a certain poi using probabilistic measure
    """
    if person.is_poi:
        if random.random() < 0.2:
            person.leave()
    return

def main(file_path, start_time, simulation_duration):
    # Process CSV Data
    print("Parsing the CSV file...")
    poi_dict = preprocess_csv(file_path)
    print(f"Parsed {len(poi_dict)} POIs.")

    # Create population
    hagerstown_pop = 43000
    people = {person_id: Person() for person_id in range(hagerstown_pop)}
    print("Created a Person instance.")

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


if __name__ == "__main__":
    # Run the main function
    with open('setting.txt', 'r') as f:
        start_time = f.readline().strip()
        simulation_duration = int(f.readline().strip())
    main('./input/hagerstown.csv', datetime.fromisoformat(start_time), simulation_duration)
