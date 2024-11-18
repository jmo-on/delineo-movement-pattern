from person import Person
from pois import POIs
import random

def leave_poi(person: Person, current_time, pois: POIs, current_occupancy):
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