import numpy as np

class POIs:
    def __init__(self, pois_dict):
        # pois = [poi_id, ...]
        self.pois = list(pois_dict.keys())
        self.raw_visit_counts = {poi_id: poi_data['raw_visit_counts'] for poi_id, poi_data in pois_dict.items()}
        self.raw_visitor_counts = {poi_id: poi_data['raw_visitor_counts'] for poi_id, poi_data in pois_dict.items()}
        
        # capacities = [{poi_id: capacity} for 30 days]
        self.capacities = [{poi_id: pois_dict[poi_id]['visits_by_day'][i] for poi_id in pois_dict} for i in range(30)]
        # probabilities = [{poi_id: probability} for 24 hours]
        self.probabilities = [{poi_id: pois_dict[poi_id]['probability_by_hour'][i] for poi_id in pois_dict} for i in range(24)]
        # {prev_poi_id: {after_poi_id: tendency}}
        self.tendency_probabilities = {poi_id: pois_dict[poi_id]['related_same_month_brand_probabilities'] for poi_id in pois_dict}
        # {poi_id: occupancy}
        self.occupancies = {poi_id: 0 for poi_id in pois_dict}
        # Dwell times and CDFs
        self.dwell_times = {poi_id: poi_dict['dwell_times'] for poi_id, poi_dict in self.pois_dict.items()}
        self.dwell_time_cdfs = {poi_id: poi_dict['dwell_time_cdf'] for poi_id, poi_dict in self.pois_dict.items()}

    def get_capacities_by_day(self, current_time):
        return self.capacities[current_time.day]

    def get_probabilities_by_time(self, current_time):
        return self.probabilities[current_time.hour]
    
    def get_capacities_by_time(self, current_time):
        return {poi_id: self.capacities[current_time.day][poi_id] * self.probabilities[current_time.hour][poi_id] for poi_id in self.capacities[current_time.day]}
    
    def get_after_tendencies(self, prev_poi_id):
        return {after_poi_id: self.tendency_probabilities[prev_poi_id].get(after_poi_id, 0) for after_poi_id in self.pois}
    
    def get_dwell_time_cdf(self, poi_id):
        return self.dwell_times[poi_id], self.dwell_time_cdfs[poi_id]

    
    def generate_next_poi_distribution(self, current_time, population):
        C = np.array(list(self.get_capacities_by_time(current_time).values()))
        O = np.array(list(self.occupancies.values()))
        A = np.array([list(self.get_after_tendencies(poi_id).values()) for poi_id in self.pois])
        alpha = 0.1
        return ((A * alpha) + (C - O)[:, np.newaxis]) / population
    
    def leave(self, poi_id):
        self.occupancies[poi_id] -= 1

    def enter(self, poi_id):
        self.occupancies[poi_id] += 1
    