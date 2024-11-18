import csv
import json

def parse_json_field(field):
    if not field:
        return {}
    try:
        return json.loads(field)
    except json.JSONDecodeError:
        return {}
    
def create_pois_names_to_ids(file_path):
    pois_names_to_ids = {}
    with open(file_path, mode='r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            pois_names_to_ids[row['location_name']] = row['safegraph_place_id']
    return pois_names_to_ids

def preprocess_csv(file_path):
    pois_dict = {}
    pois_names_to_ids = create_pois_names_to_ids(file_path)
    with open(file_path, mode='r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            safegraph_place_id = row['safegraph_place_id']

            if not safegraph_place_id:
                continue  

            sum_popularity = sum(parse_json_field(row['popularity_by_hour']))
            probability_by_hour = [p/sum_popularity for p in parse_json_field(row['popularity_by_hour'])]

            bucketed_dwell_times = parse_json_field(row['bucketed_dwell_times'])

            # related_same_month_brand = {pois_names_to_ids[poi_name]: tendency for poi_name, tendency in parse_json_field(row['related_same_month_brand'])}

            related_same_month_brand = {}
            for poi_name, tendency in parse_json_field(row['related_same_month_brand']).items():
                if poi_name in pois_names_to_ids:
                    related_same_month_brand[pois_names_to_ids[poi_name]] = tendency

            sum_tendency = sum(related_same_month_brand.values())
            tendency_probabilities = {poi_id: tendency / sum_tendency for poi_id, tendency in related_same_month_brand.items()}

            # Construct the inner dictionary for poi_dict
            pois_dict[safegraph_place_id] = {
                'location_name': row['location_name'],
                'raw_visit_counts': int(row['raw_visit_counts']),
                'raw_visitor_counts': int(row['raw_visitor_counts']),
                'visits_by_day': parse_json_field(row['visits_by_day']),
                'probability_by_hour': probability_by_hour,
                'bucketed_dwell_times': bucketed_dwell_times,
                'related_same_day_brand': parse_json_field(row['related_same_day_brand']),
                'tendency_probabilities': tendency_probabilities
            } 

    return pois_dict

if __name__ == "__main__":
    pois_dict = preprocess_csv('input/hagerstown.csv')
    import yaml

    # Write the processed data to YAML file
    with open('output/parsed_hagerstown.yaml', 'w') as yaml_file:
        yaml.dump(pois_dict, yaml_file, default_flow_style=False)