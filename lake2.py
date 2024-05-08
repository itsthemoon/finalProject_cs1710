from z3 import *
import matplotlib.pyplot as plt
import pandas as pd

# Read and preprocess the data from CSV files
copper_data = pd.read_csv("data/Copper.csv")
water_chemistry_data = pd.read_csv("data/Water Chemistry.csv")
mortality_data = pd.read_csv("data/Mortality.csv")
length_data = pd.read_csv("data/Length.csv")
alkalinity_hardness_data = pd.read_csv("data/Alkalinity and Hardness.csv")

# Define variables
zebra_mussel_population = Int('zebra_mussel_population')
water_clarity = Real('water_clarity')
aquatic_plant_growth = Real('aquatic_plant_growth')
oxygen_level = Real('oxygen_level')
copper_concentration = Real('copper_concentration')
ph = Real('ph')
dissolved_oxygen = Real('dissolved_oxygen')
specific_conductance = Real('specific_conductance')
temperature = Real('temperature')
zebra_mussel_size = Real('zebra_mussel_size')
alkalinity = Real('alkalinity')
hardness = Real('hardness')

# Define relationships and constraints (TODO: Customize these based on the data)
max_zebra_mussel_population = 1000
max_aquatic_plant_growth = 1
zebra_mussel_growth_rate = 0.1
aquatic_plant_growth_factor = 0.8
water_clarity_threshold = 0.7
oxygen_threshold = 0.6
oxygen_production_factor = 0.5
oxygen_consumption_factor_plants = 0.2
oxygen_consumption_factor_mussels = 0.4

# Set initial conditions based on the data 
initial_zebra_mussel_population_control = 50 # we can infer this from the completeness report. From Day 8 onwards, the "Alive" and "Dead" columns in the mortality data sum up to 50 for each tank. This suggests that the initial number of mussels in each tank was likely 50.
initial_zebra_mussel_population_treatment = 50
initial_water_clarity = 0.5 # TODO: adjust this given our data
initial_aquatic_plant_growth = 0.3 # TODO: adjust this given our data
initial_oxygen_level_control = water_chemistry_data[(water_chemistry_data["Day"] == 0) & (water_chemistry_data["Treatment"] == "C")]["Dissolved Oxygen"].mean()
initial_oxygen_level_treatment = water_chemistry_data[(water_chemistry_data["Day"] == 0) & (water_chemistry_data["Treatment"] == "T")]["Dissolved Oxygen"].mean()
initial_copper_concentration_control = copper_data[(copper_data["Day"] == 0) & (copper_data["Treatment"] == "C")]["Copper"].mean()
initial_copper_concentration_treatment = copper_data[(copper_data["Day"] == 0) & (copper_data["Treatment"] == "T")]["Copper"].mean()
initial_ph_control = water_chemistry_data[(water_chemistry_data["Day"] == 0) & (water_chemistry_data["Treatment"] == "C")]["pH"].mean()
initial_ph_treatment = water_chemistry_data[(water_chemistry_data["Day"] == 0) & (water_chemistry_data["Treatment"] == "T")]["pH"].mean()
initial_dissolved_oxygen_control = water_chemistry_data[(water_chemistry_data["Day"] == 0) & (water_chemistry_data["Treatment"] == "C")]["Dissolved Oxygen"].mean()
initial_dissolved_oxygen_treatment = water_chemistry_data[(water_chemistry_data["Day"] == 0) & (water_chemistry_data["Treatment"] == "T")]["Dissolved Oxygen"].mean()
initial_specific_conductance_control = water_chemistry_data[(water_chemistry_data["Day"] == 0) & (water_chemistry_data["Treatment"] == "C")]["Specific Conductance"].mean()
initial_specific_conductance_treatment = water_chemistry_data[(water_chemistry_data["Day"] == 0) & (water_chemistry_data["Treatment"] == "T")]["Specific Conductance"].mean()
initial_temperature_control = water_chemistry_data[(water_chemistry_data["Day"] == 0) & (water_chemistry_data["Treatment"] == "C")]["Temperature"].mean()
initial_temperature_treatment = water_chemistry_data[(water_chemistry_data["Day"] == 0) & (water_chemistry_data["Treatment"] == "T")]["Temperature"].mean()
initial_zebra_mussel_size = length_data["Length"].mean()
initial_alkalinity_control = alkalinity_hardness_data[(alkalinity_hardness_data["Day"] == 0) & (alkalinity_hardness_data["Treatment"] == "C")]["Alkalinity"].mean()
initial_alkalinity_treatment = alkalinity_hardness_data[(alkalinity_hardness_data["Day"] == 0) & (alkalinity_hardness_data["Treatment"] == "T")]["Alkalinity"].mean()
initial_hardness_control = alkalinity_hardness_data[(alkalinity_hardness_data["Day"] == 1) & (alkalinity_hardness_data["Treatment"] == "C")]["Hardness"].mean()
initial_hardness_treatment = alkalinity_hardness_data[(alkalinity_hardness_data["Day"] == 1) & (alkalinity_hardness_data["Treatment"] == "T")]["Hardness"].mean()

# Create solvers for control and treatment scenarios
solver_control = Solver()
solver_treatment = Solver()

# Create lists to store the variables for each time step
variables_control = []
variables_treatment = []

# Simulate the model over time for control and treatment scenarios
num_time_steps = 10

for t in range(num_time_steps):
    # Create new variables for each time step
    zebra_mussel_population_t_control = Int(f'zebra_mussel_population_control_{t}')
    zebra_mussel_population_t_treatment = Int(f'zebra_mussel_population_treatment_{t}')
    water_clarity_t_control = Real(f'water_clarity_control_{t}')
    water_clarity_t_treatment = Real(f'water_clarity_treatment_{t}')
    aquatic_plant_growth_t_control = Real(f'aquatic_plant_growth_control_{t}')
    aquatic_plant_growth_t_treatment = Real(f'aquatic_plant_growth_treatment_{t}')
    oxygen_level_t_control = Real(f'oxygen_level_control_{t}')
    oxygen_level_t_treatment = Real(f'oxygen_level_treatment_{t}')
    copper_concentration_t_control = Real(f'copper_concentration_control_{t}')
    copper_concentration_t_treatment = Real(f'copper_concentration_treatment_{t}')
    ph_t_control = Real(f'ph_control_{t}')
    ph_t_treatment = Real(f'ph_treatment_{t}')
    dissolved_oxygen_t_control = Real(f'dissolved_oxygen_control_{t}')
    dissolved_oxygen_t_treatment = Real(f'dissolved_oxygen_treatment_{t}')
    specific_conductance_t_control = Real(f'specific_conductance_control_{t}')
    specific_conductance_t_treatment = Real(f'specific_conductance_treatment_{t}')
    temperature_t_control = Real(f'temperature_control_{t}')
    temperature_t_treatment = Real(f'temperature_treatment_{t}')
    zebra_mussel_size_t_control = Real(f'zebra_mussel_size_control_{t}')
    zebra_mussel_size_t_treatment = Real(f'zebra_mussel_size_treatment_{t}')
    alkalinity_t_control = Real(f'alkalinity_control_{t}')
    alkalinity_t_treatment = Real(f'alkalinity_treatment_{t}')
    hardness_t_control = Real(f'hardness_control_{t}')
    hardness_t_treatment = Real(f'hardness_treatment_{t}')

    # Add variables to the lists 
    variables_control.append((zebra_mussel_population_t_control, water_clarity_t_control, aquatic_plant_growth_t_control, oxygen_level_t_control,
                              copper_concentration_t_control, ph_t_control, dissolved_oxygen_t_control, specific_conductance_t_control, temperature_t_control,
                              zebra_mussel_size_t_control, alkalinity_t_control, hardness_t_control))
    variables_treatment.append((zebra_mussel_population_t_treatment, water_clarity_t_treatment, aquatic_plant_growth_t_treatment, oxygen_level_t_treatment,
                                copper_concentration_t_treatment, ph_t_treatment, dissolved_oxygen_t_treatment, specific_conductance_t_treatment, temperature_t_treatment,
                                zebra_mussel_size_t_treatment, alkalinity_t_treatment, hardness_t_treatment))

    # Zebra mussel population growth with carrying capacity, oxygen level, and copper concentration
    if t == 0:
        solver_control.add(zebra_mussel_population_t_control == int(initial_zebra_mussel_population_control))
        solver_treatment.add(zebra_mussel_population_t_treatment == int(initial_zebra_mussel_population_treatment))
    else:
        prev_zebra_mussel_population_control, _, _, prev_oxygen_level_control, prev_copper_concentration_control, _, _, _, _, _, _, _ = variables_control[t-1]
        prev_zebra_mussel_population_treatment, _, _, prev_oxygen_level_treatment, prev_copper_concentration_treatment, _, _, _, _, _, _, _ = variables_treatment[t-1]   
        
        # TODO: Adjust this to be in accordance with the data     
        mortality_factor_control = If(prev_copper_concentration_control >= 0.5, 0.99, If(prev_copper_concentration_control >= 0.2, 0.85, 0))
        mortality_factor_treatment = If(prev_copper_concentration_treatment >= 0.5, 0.99, If(prev_copper_concentration_treatment >= 0.2, 0.85, 0))
        
        solver_control.add(zebra_mussel_population_t_control == If(
            And(prev_zebra_mussel_population_control >= max_zebra_mussel_population, prev_oxygen_level_control >= oxygen_threshold),
            max_zebra_mussel_population,
            If(prev_oxygen_level_control >= oxygen_threshold,
               ToInt(prev_zebra_mussel_population_control * (1 - mortality_factor_control) * (1 - prev_zebra_mussel_population_control / max_zebra_mussel_population) * zebra_mussel_growth_rate),
               If(prev_oxygen_level_control <= 0, 0, ToInt(prev_zebra_mussel_population_control * (1 - mortality_factor_control) * (1 - prev_oxygen_level_control) * zebra_mussel_growth_rate)))
        ))
        solver_treatment.add(zebra_mussel_population_t_treatment == If(
            And(prev_zebra_mussel_population_treatment >= max_zebra_mussel_population, prev_oxygen_level_treatment >= oxygen_threshold),
            max_zebra_mussel_population,
            If(prev_oxygen_level_treatment >= oxygen_threshold,
               ToInt(prev_zebra_mussel_population_treatment * (1 - mortality_factor_treatment) * (1 - prev_zebra_mussel_population_treatment / max_zebra_mussel_population) * zebra_mussel_growth_rate),
               If(prev_oxygen_level_treatment <= 0, 0, ToInt(prev_zebra_mussel_population_treatment * (1 - mortality_factor_treatment) * (1 - prev_oxygen_level_treatment) * zebra_mussel_growth_rate)))
        ))

    # Water clarity improvement with non-linear relationship
    if t == 0:
        solver_control.add(water_clarity_t_control == initial_water_clarity)
        solver_treatment.add(water_clarity_t_treatment == initial_water_clarity)
    else:
        prev_water_clarity_control, _, _, _, _, _, _, _, _, _, _, _ = variables_control[t-1]
        prev_water_clarity_treatment, _, _, _, _, _, _, _, _, _, _, _ = variables_treatment[t-1]
        
        # TODO: Adjust the relationship between zebra mussel population and water clarity using data to back us up
        water_clarity_increase_control = (zebra_mussel_population_t_control / max_zebra_mussel_population)**0.5
        water_clarity_increase_treatment = (zebra_mussel_population_t_treatment / max_zebra_mussel_population)**0.5
        
        solver_control.add(water_clarity_t_control == If(
            prev_water_clarity_control + water_clarity_increase_control >= 1,
            1,
            prev_water_clarity_control + water_clarity_increase_control
        ))
        solver_treatment.add(water_clarity_t_treatment == If(
            prev_water_clarity_treatment + water_clarity_increase_treatment >= 1,
            1,
            prev_water_clarity_treatment + water_clarity_increase_treatment
        ))
        
        # TODO: Determine if we need these constraints (Essentially, they ensure that water clarity should always be greater than or equal to the previous day's water clarity)
        solver_control.add(water_clarity_t_control >= prev_water_clarity_control)
        solver_treatment.add(water_clarity_t_treatment >= prev_water_clarity_treatment)
    
    # Aquatic plant growth based on water clarity threshold
    # TODO: Adjust the relationship between aquatic plant growth and water clarity using data to back us up
    solver_control.add(aquatic_plant_growth_t_control == If(
        water_clarity_t_control >= water_clarity_threshold,
        If(water_clarity_t_control * aquatic_plant_growth_factor <= max_aquatic_plant_growth,
        water_clarity_t_control * aquatic_plant_growth_factor,
        max_aquatic_plant_growth),
        If(water_clarity_t_control < water_clarity_threshold, 
        water_clarity_t_control * aquatic_plant_growth_factor * 0.5,
        water_clarity_t_control * aquatic_plant_growth_factor)
    ))
    solver_treatment.add(aquatic_plant_growth_t_treatment == If(
        water_clarity_t_treatment >= water_clarity_threshold,
        If(water_clarity_t_treatment * aquatic_plant_growth_factor <= max_aquatic_plant_growth,
        water_clarity_t_treatment * aquatic_plant_growth_factor,
        max_aquatic_plant_growth),
        If(water_clarity_t_treatment < water_clarity_threshold, 
        water_clarity_t_treatment * aquatic_plant_growth_factor * 0.5,
        water_clarity_t_treatment * aquatic_plant_growth_factor)
    ))

    # Oxygen level based on aquatic plant growth, zebra mussel population, and water chemistry
    # TODO: Adjust the relationship between oxygen level and aquatic plant growth, zebra mussel population, and water chemistry using data to back us up
    if t == 0:
        solver_control.add(oxygen_level_t_control == initial_oxygen_level_control)
        solver_treatment.add(oxygen_level_t_treatment == initial_oxygen_level_treatment)
    else:
        prev_oxygen_level_control, _, _, _, _, prev_ph, prev_dissolved_oxygen, prev_specific_conductance, prev_temperature, _, _, _ = variables_control[t-1]
        prev_oxygen_level_treatment, _, _, _, _, _, _, _, _, _, _, _ = variables_treatment[t-1]
        
        solver_control.add(oxygen_level_t_control == If(
            prev_oxygen_level_control + aquatic_plant_growth_t_control * oxygen_production_factor - aquatic_plant_growth_t_control * oxygen_consumption_factor_plants - zebra_mussel_population_t_control / max_zebra_mussel_population * oxygen_consumption_factor_mussels >= 1,
            1,
            If(prev_oxygen_level_control + aquatic_plant_growth_t_control * oxygen_production_factor - aquatic_plant_growth_t_control * oxygen_consumption_factor_plants - zebra_mussel_population_t_control / max_zebra_mussel_population * oxygen_consumption_factor_mussels <= 0,
            0,
            prev_oxygen_level_control + aquatic_plant_growth_t_control * oxygen_production_factor - aquatic_plant_growth_t_control * oxygen_consumption_factor_plants - zebra_mussel_population_t_control / max_zebra_mussel_population * oxygen_consumption_factor_mussels)
        ))
        
        solver_treatment.add(oxygen_level_t_treatment == If(
            prev_oxygen_level_treatment + aquatic_plant_growth_t_treatment * oxygen_production_factor - aquatic_plant_growth_t_treatment * oxygen_consumption_factor_plants - zebra_mussel_population_t_treatment / max_zebra_mussel_population * oxygen_consumption_factor_mussels >= 1,
            1,
            If(prev_oxygen_level_treatment + aquatic_plant_growth_t_treatment * oxygen_production_factor - aquatic_plant_growth_t_treatment * oxygen_consumption_factor_plants - zebra_mussel_population_t_treatment / max_zebra_mussel_population * oxygen_consumption_factor_mussels <= 0,
            0,
            prev_oxygen_level_treatment + aquatic_plant_growth_t_treatment * oxygen_production_factor - aquatic_plant_growth_t_treatment * oxygen_consumption_factor_plants - zebra_mussel_population_t_treatment / max_zebra_mussel_population * oxygen_consumption_factor_mussels)
        ))

    # Copper concentration based on treatment data
    if t == 0:
        solver_control.add(copper_concentration_t_control == initial_copper_concentration_control)
        solver_treatment.add(copper_concentration_t_treatment == initial_copper_concentration_treatment)
    else:
        # Get the mean copper concentration for the current day or use the previous day's value if missing
        copper_concentration_control_today = copper_data[(copper_data["Day"] == t) & (copper_data["Treatment"] == "C")]["Copper"].mean()
        copper_concentration_treatment_today = copper_data[(copper_data["Day"] == t) & (copper_data["Treatment"] == "T")]["Copper"].mean()

        # If data for the current day is missing (resulting in NaN), use the previous day's data
        if pd.isna(copper_concentration_control_today):
            copper_concentration_control_today = copper_data[(copper_data["Day"] == t-1) & (copper_data["Treatment"] == "C")]["Copper"].mean()
        if pd.isna(copper_concentration_treatment_today):
            copper_concentration_treatment_today = copper_data[(copper_data["Day"] == t-1) & (copper_data["Treatment"] == "T")]["Copper"].mean()

        solver_control.add(copper_concentration_t_control == copper_concentration_control_today)
        solver_treatment.add(copper_concentration_t_treatment == copper_concentration_treatment_today)
        
    # pH based on water chemistry data
    if t == 0:
        solver_control.add(ph_t_control == initial_ph_control)
        solver_treatment.add(ph_t_treatment == initial_ph_treatment)
    else:
        solver_control.add(ph_t_control == water_chemistry_data[(water_chemistry_data["Day"] == t) & (water_chemistry_data["Treatment"] == "C")]["pH"].mean())
        solver_treatment.add(ph_t_treatment == water_chemistry_data[(water_chemistry_data["Day"] == t) & (water_chemistry_data["Treatment"] == "T")]["pH"].mean())
    
    # Dissolved oxygen based on water chemistry data
    if t == 0:
        solver_control.add(dissolved_oxygen_t_control == initial_dissolved_oxygen_control)
        solver_treatment.add(dissolved_oxygen_t_treatment == initial_dissolved_oxygen_treatment)
    else:
        solver_control.add(dissolved_oxygen_t_control == water_chemistry_data[(water_chemistry_data["Day"] == t) & (water_chemistry_data["Treatment"] == "C")]["Dissolved Oxygen"].mean())
        solver_treatment.add(dissolved_oxygen_t_treatment == water_chemistry_data[(water_chemistry_data["Day"] == t) & (water_chemistry_data["Treatment"] == "T")]["Dissolved Oxygen"].mean())
    
    # Specific conductance based on water chemistry data
    if t == 0:
        solver_control.add(specific_conductance_t_control == initial_specific_conductance_control)
        solver_treatment.add(specific_conductance_t_treatment == initial_specific_conductance_treatment)
    else:
        solver_control.add(specific_conductance_t_control == water_chemistry_data[(water_chemistry_data["Day"] == t) & (water_chemistry_data["Treatment"] == "C")]["Specific Conductance"].mean())
        solver_treatment.add(specific_conductance_t_treatment == water_chemistry_data[(water_chemistry_data["Day"] == t) & (water_chemistry_data["Treatment"] == "T")]["Specific Conductance"].mean())
        
    # Temperature based on water chemistry data
    if t == 0:
        solver_control.add(temperature_t_control == initial_temperature_control)
        solver_treatment.add(temperature_t_treatment == initial_temperature_treatment)
    else:
        solver_control.add(temperature_t_control == water_chemistry_data[(water_chemistry_data["Day"] == t) & (water_chemistry_data["Treatment"] == "C")]["Temperature"].mean())
        solver_treatment.add(temperature_t_treatment == water_chemistry_data[(water_chemistry_data["Day"] == t) & (water_chemistry_data["Treatment"] == "T")]["Temperature"].mean())
    
    # Zebra mussel size based on length data
    # TODO: Possibly adjust this to use a different control/treatment variable
    if t == 0:
        solver_control.add(zebra_mussel_size_t_control == initial_zebra_mussel_size)
        solver_treatment.add(zebra_mussel_size_t_treatment == initial_zebra_mussel_size)
    else:
        # Keep the mussel size constant over time as it does not change day by day
        solver_control.add(zebra_mussel_size_t_control == initial_zebra_mussel_size)
        solver_treatment.add(zebra_mussel_size_t_treatment == initial_zebra_mussel_size)
        
    # Alkalinity based on alkalinity and hardness data
    if t == 0:
        solver_control.add(alkalinity_t_control == initial_alkalinity_control)
        solver_treatment.add(alkalinity_t_treatment == initial_alkalinity_treatment)
    else:
        solver_control.add(alkalinity_t_control == alkalinity_hardness_data[(alkalinity_hardness_data["Day"] == t) & (alkalinity_hardness_data["Treatment"] == "C")]["Alkalinity"].mean())
        solver_treatment.add(alkalinity_t_treatment == alkalinity_hardness_data[(alkalinity_hardness_data["Day"] == t) & (alkalinity_hardness_data["Treatment"] == "T")]["Alkalinity"].mean())

    # Hardness based on alkalinity and hardness data
    if t == 0:
        solver_control.add(hardness_t_control == initial_hardness_control)
        solver_treatment.add(hardness_t_treatment == initial_hardness_treatment)
    else:
        solver_control.add(hardness_t_control == alkalinity_hardness_data[(alkalinity_hardness_data["Day"] == t) & (alkalinity_hardness_data["Treatment"] == "C")]["Hardness"].mean())
        solver_treatment.add(hardness_t_treatment == alkalinity_hardness_data[(alkalinity_hardness_data["Day"] == t) & (alkalinity_hardness_data["Treatment"] == "T")]["Hardness"].mean())
        
    # Add constraints for realistic ranges
    solver_control.add(zebra_mussel_population_t_control >= 0)
    solver_treatment.add(zebra_mussel_population_t_treatment >= 0)
    solver_control.add(water_clarity_t_control >= 0, water_clarity_t_control <= 1)
    solver_treatment.add(water_clarity_t_treatment >= 0, water_clarity_t_treatment <= 1)
    solver_control.add(aquatic_plant_growth_t_control >= 0, aquatic_plant_growth_t_control <= max_aquatic_plant_growth)
    solver_treatment.add(aquatic_plant_growth_t_treatment >= 0, aquatic_plant_growth_t_treatment <= max_aquatic_plant_growth)
    solver_control.add(oxygen_level_t_control >= 0, oxygen_level_t_control <= 1)
    solver_treatment.add(oxygen_level_t_treatment >= 0, oxygen_level_t_treatment <= 1)
    solver_control.add(copper_concentration_t_control >= 0)
    solver_treatment.add(copper_concentration_t_treatment >= 0)
    solver_control.add(ph_t_control >= 0, ph_t_control <= 14)
    solver_treatment.add(ph_t_treatment >= 0, ph_t_treatment <= 14)
    solver_control.add(dissolved_oxygen_t_control >= 0)
    solver_treatment.add(dissolved_oxygen_t_treatment >= 0)
    solver_control.add(specific_conductance_t_control >= 0)
    solver_treatment.add(specific_conductance_t_treatment >= 0)
    solver_control.add(temperature_t_control >= 0)
    solver_treatment.add(temperature_t_treatment >= 0)
    solver_control.add(zebra_mussel_size_t_control >= 0)
    solver_treatment.add(zebra_mussel_size_t_treatment >= 0)
    solver_control.add(alkalinity_t_control >= 0)
    solver_treatment.add(alkalinity_t_treatment >= 0)
    solver_control.add(hardness_t_control >= 0)
    solver_treatment.add(hardness_t_treatment >= 0)

    # Add constraints for relationships between variables
    # TODO: Adjust the thresholds based on our data
    solver_control.add(Implies(zebra_mussel_population_t_control >= max_zebra_mussel_population * 0.8, water_clarity_t_control >= 0.9))
    solver_treatment.add(Implies(zebra_mussel_population_t_treatment >= max_zebra_mussel_population * 0.8, water_clarity_t_treatment >= 0.9))
    solver_control.add(Implies(water_clarity_t_control < water_clarity_threshold, aquatic_plant_growth_t_control < 0.5 * max_aquatic_plant_growth))
    solver_treatment.add(Implies(water_clarity_t_treatment < water_clarity_threshold, aquatic_plant_growth_t_treatment < 0.5 * max_aquatic_plant_growth))
    solver_control.add(Implies(copper_concentration_t_control >= 0.5, zebra_mussel_population_t_control <= 0.01 * initial_zebra_mussel_population_control))
    solver_treatment.add(Implies(copper_concentration_t_treatment >= 0.5, zebra_mussel_population_t_treatment <= 0.01 * initial_zebra_mussel_population_treatment))
    solver_control.add(Implies(copper_concentration_t_control >= 0.2, zebra_mussel_population_t_control <= 0.15 * initial_zebra_mussel_population_control))
    solver_treatment.add(Implies(copper_concentration_t_treatment >= 0.2, zebra_mussel_population_t_treatment <= 0.15 * initial_zebra_mussel_population_treatment))
  