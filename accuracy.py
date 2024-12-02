import csv
import math

def calculate_metrics(file_path):
    total_capacity = 0
    total_occupancy = 0
    total_difference = 0
    
    # For error calculations
    squared_errors = 0
    absolute_errors = 0
    n = 0  # number of non-zero capacity locations
    
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            if len(row) >= 3:  # Ensure row has enough columns
                try:
                    capacity = float(row[1])
                    difference = float(row[2])
                    occupancy = float(row[3])
                    
                    if capacity > 0:  # Only count locations with non-zero capacity
                        n += 1
                        total_capacity += capacity
                        total_occupancy += occupancy
                        total_difference += difference
                        
                        # Calculate errors
                        error = difference
                        squared_errors += error ** 2
                        absolute_errors += abs(error)
                        
                except (ValueError, IndexError):
                    continue  # Skip rows with invalid data
    
    # Calculate error metrics
    mse = squared_errors / n if n > 0 else 0  # Mean Squared Error
    rmse = math.sqrt(mse)  # Root Mean Squared Error
    mae = absolute_errors / n if n > 0 else 0  # Mean Absolute Error
    
    # Calculate accuracy (as percentage)
    average_error_rate = mae / (total_capacity / n) if n > 0 and total_capacity > 0 else 1.0
    accuracy = max(0.0, min(1.0, 1.0 - average_error_rate)) * 100  # Convert to percentage and clamp between 0-100
    
    return {
        'total_capacity': total_capacity,
        'total_occupancy': total_occupancy,
        'total_difference': total_difference,
        'number_of_locations': n,
        'mean_squared_error': mse,  # Now returns raw MSE instead of normalized
        'root_mean_squared_error': rmse,
        'mean_absolute_error': mae,
        'accuracy': accuracy  # New accuracy metric
    }

# Usage
metrics = calculate_metrics('output/capacity_occupancy.csv')

print(f"Analysis Results:")
print(f"Number of locations with capacity: {metrics['number_of_locations']}")
print(f"Total Capacity: {metrics['total_capacity']:.2f}")
print(f"Total Occupancy: {metrics['total_occupancy']:.2f}")
print(f"Total Difference: {metrics['total_difference']:.2f}")
print(f"\nError Metrics:")
print(f"Mean Squared Error: {metrics['mean_squared_error']:.4f}")
print(f"Root Mean Squared Error: {metrics['root_mean_squared_error']:.4f}")
print(f"Mean Absolute Error: {metrics['mean_absolute_error']:.4f}")
print(f"Accuracy: {metrics['accuracy']:.2f}%")  # Add accuracy to output