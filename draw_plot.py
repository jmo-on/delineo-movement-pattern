import matplotlib.pyplot as plt

def draw_plot(df, location_names):
    # Create plot
    plt.figure(figsize=(20, 10))  # Made figure wider to accommodate legend
    
    # Create the plot
    for location in location_names:
        plt.plot(df.index, df[location], label=location)
    
    plt.xlabel('Hour')
    plt.ylabel('Occupancy')
    plt.title('POI Occupancy Over Time')
    
    # Add legend with multiple columns to make it more compact
    plt.legend(bbox_to_anchor=(1.02, 0.5),
              loc='center left',
              borderaxespad=0.,
              bbox_transform=plt.gca().transAxes,
              ncol=4,  # Use 4 columns for legend
              fontsize='small',
              title="Locations")
    
    # Adjust layout
    plt.subplots_adjust(right=0.75)  # Adjust right margin to fit legend
    
    plt.savefig('output/occupancy_plot.png', bbox_inches='tight', dpi=300)
    plt.close()