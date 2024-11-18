import random

def enter_poi(people, pois, current_time, hagerstown_pop):
    for person_id, person in people.items():
        if person.is_poi:
            next_poi_id = pois.get_next_poi_with_tendency(current_time, hagerstown_pop, person.curr_poi)
        else:
            next_poi_id = pois.get_next_poi(current_time, hagerstown_pop)
        print(f"Person {person_id} is moving from {person.curr_poi} to {next_poi_id}")
        