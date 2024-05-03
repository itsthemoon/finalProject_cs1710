from z3 import *
import matplotlib.pyplot as plt

# Define variables
zebra_mussel_population = Int('zebra_mussel_population')
water_clarity = Real('water_clarity')
aquatic_plant_growth = Real('aquatic_plant_growth')
oxygen_level = Real('oxygen_level')

# Define relationships
max_zebra_mussel_population = 1000
max_aquatic_plant_growth = 1
zebra_mussel_growth_rate = 0.1
aquatic_plant_growth_factor = 0.8
water_clarity_threshold = 0.7
oxygen_threshold = 0.6
oxygen_production_factor = 0.5
oxygen_consumption_factor_plants = 0.2
oxygen_consumption_factor_mussels = 0.4

# Set initial conditions
initial_zebra_mussel_population = 100
initial_water_clarity = 0.5
initial_aquatic_plant_growth = 0.3
initial_oxygen_level = 0.8

# Create a solver
solver = Solver()

# Create a list to store the variables for each time step
variables = []

# Simulate the model over time
num_time_steps = 50

for t in range(num_time_steps):
    # Create new variables for each time step
    zebra_mussel_population_t = Int(f'zebra_mussel_population_{t}')
    water_clarity_t = Real(f'water_clarity_{t}')
    aquatic_plant_growth_t = Real(f'aquatic_plant_growth_{t}')
    oxygen_level_t = Real(f'oxygen_level_{t}')

    # Add variables to the list
    variables.append((zebra_mussel_population_t, water_clarity_t, aquatic_plant_growth_t, oxygen_level_t))

    # Zebra mussel population growth with carrying capacity and oxygen level
    if t == 0:
        solver.add(zebra_mussel_population_t == initial_zebra_mussel_population)
    else:
        prev_zebra_mussel_population, _, _, prev_oxygen_level = variables[t-1]
        solver.add(zebra_mussel_population_t == If(
            And(prev_zebra_mussel_population >= max_zebra_mussel_population, prev_oxygen_level >= oxygen_threshold),
            max_zebra_mussel_population,
            If(prev_oxygen_level >= oxygen_threshold,
               prev_zebra_mussel_population + ToInt(prev_zebra_mussel_population * (1 - prev_zebra_mussel_population / max_zebra_mussel_population) * zebra_mussel_growth_rate),
               If(prev_oxygen_level <= 0, 0, prev_zebra_mussel_population - ToInt(prev_zebra_mussel_population * (1 - prev_oxygen_level) * zebra_mussel_growth_rate)))
        ))

    # Water clarity improvement with non-linear relationship
    if t == 0:
        solver.add(water_clarity_t == initial_water_clarity)
    else:
        prev_water_clarity = variables[t-1][1]
        water_clarity_increase = (zebra_mussel_population_t / max_zebra_mussel_population)**0.5
        solver.add(water_clarity_t == If(
            prev_water_clarity + water_clarity_increase >= 1,
            1,
            prev_water_clarity + water_clarity_increase
        ))
        solver.add(water_clarity_t >= prev_water_clarity)
    
    # Aquatic plant growth based on water clarity threshold
    solver.add(aquatic_plant_growth_t == If(
        water_clarity_t >= water_clarity_threshold,
        If(water_clarity_t * aquatic_plant_growth_factor <= max_aquatic_plant_growth,
           water_clarity_t * aquatic_plant_growth_factor,
           max_aquatic_plant_growth),
        If(water_clarity_t < water_clarity_threshold, 
           water_clarity_t * aquatic_plant_growth_factor * 0.5,
           water_clarity_t * aquatic_plant_growth_factor)
    ))

    # Oxygen level based on aquatic plant growth and zebra mussel population
    if t == 0:
        solver.add(oxygen_level_t == initial_oxygen_level)
    else:
        prev_oxygen_level = variables[t-1][3]
        solver.add(oxygen_level_t == If(
            prev_oxygen_level + aquatic_plant_growth_t * oxygen_production_factor - aquatic_plant_growth_t * oxygen_consumption_factor_plants - zebra_mussel_population_t / max_zebra_mussel_population * oxygen_consumption_factor_mussels >= 1,
            1,
            If(prev_oxygen_level + aquatic_plant_growth_t * oxygen_production_factor - aquatic_plant_growth_t * oxygen_consumption_factor_plants - zebra_mussel_population_t / max_zebra_mussel_population * oxygen_consumption_factor_mussels <= 0,
               0,
               prev_oxygen_level + aquatic_plant_growth_t * oxygen_production_factor - aquatic_plant_growth_t * oxygen_consumption_factor_plants - zebra_mussel_population_t / max_zebra_mussel_population * oxygen_consumption_factor_mussels)
        ))

# Check if the constraints are satisfiable
if solver.check() == sat:
    model = solver.model()
    for t in range(num_time_steps):
        zebra_mussel_population_t, water_clarity_t, aquatic_plant_growth_t, oxygen_level_t = variables[t]
        print(f"Time Step {t}:")
        print(f"  Zebra Mussel Population: {model[zebra_mussel_population_t]}")
        print(f"  Water Clarity: {model[water_clarity_t]}")
        print(f"  Aquatic Plant Growth: {model[aquatic_plant_growth_t]}")
        print(f"  Oxygen Level: {model[oxygen_level_t]}")
        print()
else:
    print("No satisfying assignment found.")


if solver.check() == sat:
    model = solver.model()

    # Create lists to store the values for each variable over time
    zebra_mussel_populations = []
    water_clarities = []
    aquatic_plant_growths = []
    oxygen_levels = []

    for t in range(num_time_steps):
        zebra_mussel_population_t, water_clarity_t, aquatic_plant_growth_t, oxygen_level_t = variables[t]
        zebra_mussel_populations.append(model[zebra_mussel_population_t].as_long())
        water_clarities.append(model[water_clarity_t].as_decimal(2))
        aquatic_plant_growths.append(model[aquatic_plant_growth_t].as_decimal(2))
        oxygen_levels.append(model[oxygen_level_t].as_decimal(2))

    # Create a figure with subplots
    fig, axs = plt.subplots(2, 2, figsize=(12, 8))

    # Plot zebra mussel population
    axs[0, 0].plot(zebra_mussel_populations)
    axs[0, 0].set_title("Zebra Mussel Population")
    axs[0, 0].set_xlabel("Time Step")
    axs[0, 0].set_ylabel("Population")

    # Plot water clarity
    axs[0, 1].plot(water_clarities)
    axs[0, 1].set_title("Water Clarity")
    axs[0, 1].set_xlabel("Time Step")
    axs[0, 1].set_ylabel("Clarity")

    # Plot aquatic plant growth
    axs[1, 0].plot(aquatic_plant_growths)
    axs[1, 0].set_title("Aquatic Plant Growth")
    axs[1, 0].set_xlabel("Time Step")
    axs[1, 0].set_ylabel("Growth")

    # Plot oxygen level
    axs[1, 1].plot(oxygen_levels)
    axs[1, 1].set_title("Oxygen Level")
    axs[1, 1].set_xlabel("Time Step")
    axs[1, 1].set_ylabel("Level")

    # Adjust the spacing between subplots
    plt.tight_layout()

    # Display the plot
    plt.show()
else:
    print("No satisfying assignment found.")
    
    
#TODO: 
# add the water clarity improvement so that it can decrease eventually
# add the aquatic plant growth so that it can decrease eventually
# add the oxygen level so that it can decrease eventually

