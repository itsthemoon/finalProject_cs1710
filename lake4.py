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

# Define the target zebra mussel population for Rhode Island
target_population_percentage = 0.2  # 20% of the initial population

# Calculate the target population based on the initial population
target_population_control = int(initial_zebra_mussel_population_control * target_population_percentage)
target_population_treatment = int(initial_zebra_mussel_population_treatment * target_population_percentage)

# Define a variable for the number of days
num_days_control = Int('num_days_control')
num_days_treatment = Int('num_days_treatment')

# Add constraints for the number of days
solver_control.add(num_days_control >= 0)
solver_treatment.add(num_days_treatment >= 0)

# Define our variables
zebra_mussel_population_t_control = Int('zebra_mussel_population_control')
water_clarity_t_control = Real('water_clarity_control')
aquatic_plant_growth_t_control = Real('aquatic_plant_growth_control')
oxygen_level_t_control = Real('oxygen_level_control')
copper_concentration_t_control = Real('copper_concentration_control')
ph_t_control = Real('ph_control')
dissolved_oxygen_t_control = Real('dissolved_oxygen_control')
specific_conductance_t_control = Real('specific_conductance_control')
temperature_t_control = Real('temperature_control')
zebra_mussel_size_t_control = Real('zebra_mussel_size_control')
alkalinity_t_control = Real('alkalinity_control')
hardness_t_control = Real('hardness_control')

zebra_mussel_population_t_treatment = Int('zebra_mussel_population_treatment')
water_clarity_t_treatment = Real('water_clarity_treatment')
aquatic_plant_growth_t_treatment = Real('aquatic_plant_growth_treatment')
oxygen_level_t_treatment = Real('oxygen_level_treatment')
copper_concentration_t_treatment = Real('copper_concentration_treatment')
ph_t_treatment = Real('ph_treatment')
dissolved_oxygen_t_treatment = Real('dissolved_oxygen_treatment')
specific_conductance_t_treatment = Real('specific_conductance_treatment')
temperature_t_treatment = Real('temperature_treatment')
zebra_mussel_size_t_treatment = Real('zebra_mussel_size_treatment')
alkalinity_t_treatment = Real('alkalinity_treatment')
hardness_t_treatment = Real('hardness_treatment')

# Add variables to the lists
variables_control.append((zebra_mussel_population_t_control, water_clarity_t_control, aquatic_plant_growth_t_control, oxygen_level_t_control,
                          copper_concentration_t_control, ph_t_control, dissolved_oxygen_t_control, specific_conductance_t_control, temperature_t_control,
                          zebra_mussel_size_t_control, alkalinity_t_control, hardness_t_control))

variables_treatment.append((zebra_mussel_population_t_treatment, water_clarity_t_treatment, aquatic_plant_growth_t_treatment, oxygen_level_t_treatment,
                            copper_concentration_t_treatment, ph_t_treatment, dissolved_oxygen_t_treatment, specific_conductance_t_treatment, temperature_t_treatment,
                            zebra_mussel_size_t_treatment, alkalinity_t_treatment, hardness_t_treatment))

# Add the target population constraint
solver_control.add(zebra_mussel_population_t_control <= target_population_control)
solver_treatment.add(zebra_mussel_population_t_treatment <= target_population_treatment)

control_result = solver_control.check()
treatment_result = solver_treatment.check()

if control_result == sat:
    print("The target zebra mussel population can be achieved under control conditions in Rhode Island.")
    model_control = solver_control.model()
    print(f"Number of days required (control): {model_control[num_days_control]}")
else:
    print("The target zebra mussel population cannot be achieved under control conditions in Rhode Island.")
if treatment_result == sat:
    print("The target zebra mussel population can be achieved under treatment conditions in Rhode Island.")
    model_treatment = solver_treatment.model()
    print(f"Number of days required (treatment): {model_treatment[num_days_treatment]}")
else:
    print("The target zebra mussel population cannot be achieved under treatment conditions in Rhode Island.")

