from preprocess_data import preprocess_csv
from person import Person
import random

def leaving_poi(person: Person):
    """
    Simulates leaving a certain poi using probabilistic measure
    """
    if person.is_poi:
        if random.random() < 0.2:
            person.leave()
    return

def entering_poi(person: Person, poi_dict):
    """
    Simulates entering a certain poi using probabilistic measure
    """
    if not person.is_poi:
        if random.random() < 0.3: 
            poi_id = random.choice(list(poi_dict.keys()))  
            person.visit(poi_id)
    return

def main(file_path):
    # Process CSV Data
    print("Parsing the CSV file...")
    poi_dict = preprocess_csv(file_path)
    print(f"Parsed {len(poi_dict)} POIs.")

    # Create population
    hagerstown_pop = 43000
    people = {person_id: Person() for person_id in range(hagerstown_pop)}
    print("Created a Person instance.")

    # Main iteration
    month = 720
    
    for hour in range(month):
        print(f"Simulating hour {hour + 1}/720...")
        for person_id, person in people.items():
            leaving_poi(person, poi_dict)
            entering_poi(person, poi_dict)

    # Output the results


if __name__ == "__main__":
    # Run the main function
    main('./input/hagerstown.csv')

