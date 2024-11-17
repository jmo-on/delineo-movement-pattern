class POIs:
    def __init__(self, pois_dict, pois_names_to_ids):
        self.pois_dict = pois_dict
        self.pois_names_to_ids = pois_names_to_ids

        # capacities = [{poi_id: capacity} for 30 days]
        self.capacities = [{poi_id: poi_dict['visits_by_day'][i] for poi_id, poi_dict in self.pois_dict.items()} for i in range(30)]
        # probabilities = [{poi_id: probability} for 24 hours]
        self.probabilities = [{poi_id: poi_dict['probability_by_hour'][i] for poi_id, poi_dict in self.pois_dict.items()} for i in range(24)]
        # {prev_poi_id: {after_poi_id: tendency}}
        self.tendency_probabilities = {poi_id: poi_dict['tendency_probabilities'] for poi_id, poi_dict in self.pois_dict.items()}

    def get_capacities(self, current_time):
        return self.capacities[current_time.day]

    def get_probabilities(self, current_time):
        return self.probabilities[current_time.hour]
    
    def get_capacity(self, poi_id, current_time):
        return self.capacities[current_time.day][poi_id]

    def get_probability(self, poi_id, current_time):
        return self.probabilities[current_time.hour][poi_id]
    
    def get_after_tendency(self, prev_poi_id, after_poi_id):
        return self.tendency_probabilities[prev_poi_id][after_poi_id] if after_poi_id in self.tendency_probabilities[prev_poi_id] else 0