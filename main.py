from datetime import datetime, timedelta
import random

from preprocess_data import preprocess_csv
from person import Person
from pois import POIs
from enter_poi import enter_poi
from leave_poi import leave_poi

def main(file_path, population, start_time, simulation_duration):
    # Process CSV Data
    print("Parsing the CSV file...")
    pois_dict = preprocess_csv(file_path)

    # Create POIs
    pois = POIs(pois_dict)
    print(f"Parsed {len(pois_dict)} POIs.")

    # Create Persons
    hagerstown_pop = population
    people = {person_id: Person() for person_id in range(hagerstown_pop)}
    print(f"Created {hagerstown_pop} Person instances.")

    for hour in range(simulation_duration):
        print(f"Simulating hour {hour + 1}/{simulation_duration}...")
        test = pois.generate_next_poi_distribution_with_tendency(start_time + timedelta(hours=hour), hagerstown_pop)
        print(test)
        # enter_poi(people, pois, start_time + timedelta(hours=hour), hagerstown_pop)


if __name__ == "__main__":
    # Run the main function
    with open('setting.txt', 'r') as f:
        town_name = f.readline().strip()
        population = int(f.readline().strip())
        start_time = f.readline().strip()
        simulation_duration = int(f.readline().strip())
    main(f'./input/{town_name}.csv', population, datetime.fromisoformat(start_time), simulation_duration)
