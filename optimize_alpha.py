import numpy as np
from accuracy import calculate_metrics
from pois import POIs
from main import main
from datetime import datetime
import os

def optimize_alpha(simulation_function, alpha_range=(0.001, 1.0), tolerance=1e-4, max_iterations=50):
    """
    Optimize alpha using binary search to minimize MSE.
    
    Args:
        simulation_function: Function that runs simulation with given alpha
        alpha_range: Tuple of (min_alpha, max_alpha)
        tolerance: Convergence tolerance
        max_iterations: Maximum number of binary search iterations
    """
    left, right = alpha_range
    best_alpha = None
    best_mse = float('inf')
    
    for iteration in range(max_iterations):
        # Test three points: left third, middle, right third
        alpha1 = left + (right - left) / 3
        alpha2 = left + 2 * (right - left) / 3
        
        # Run simulations with both alpha values
        mse1 = simulation_function(alpha1)
        mse2 = simulation_function(alpha2)
        
        # Update best result
        if mse1 < best_mse:
            best_mse = mse1
            best_alpha = alpha1
        if mse2 < best_mse:
            best_mse = mse2
            best_alpha = alpha2
            
        # Update search range
        if mse1 < mse2:
            right = alpha2
        else:
            left = alpha1
            
        # Check convergence
        if abs(right - left) < tolerance:
            break
            
    return best_alpha, best_mse

def run_simulation_with_alpha(alpha):
    """
    Run simulation with a specific alpha value and return MSE.
    """
    # Clear previous output files
    if os.path.exists('output/capacity_occupancy.csv'):
        os.remove('output/capacity_occupancy.csv')
    
    # Read settings
    with open('setting.txt', 'r') as f:
        town_name = f.readline().strip()
        population = int(f.readline().strip())
        alpha = float(f.readline().strip())
        start_time = f.readline().strip()
        simulation_duration = int(f.readline().strip())
    
    # Run simulation with current alpha
    main(
        f'./input/{town_name}.csv',
        population,
        datetime.fromisoformat(start_time),
        simulation_duration,
        alpha
    )
    
    # Calculate metrics
    metrics = calculate_metrics('output/capacity_occupancy.csv')
    return metrics['mean_squared_error']

if __name__ == "__main__":
    # Find optimal alpha
    optimal_alpha, best_mse = optimize_alpha(
        run_simulation_with_alpha,
        alpha_range=(0.001, 1.0),
        tolerance=1e-3,
        max_iterations=10  # Reduced for faster testing
    )
    
    print(f"Optimization Results:")
    print(f"Optimal alpha: {optimal_alpha:.6f}")
    print(f"Best MSE: {best_mse:.6f}") 