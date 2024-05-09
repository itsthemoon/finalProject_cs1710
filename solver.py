from z3 import *
import pandas as pd
from data_analysis.mussel_mortality_prediction import predict_mortality_rate

# Define decision variables
copper_conc = Real('copper_conc')
temperature = Real('temperature')
pH = Real('pH')
dissolved_oxygen = Real('dissolved_oxygen')

# Initial bounds for copper concentration
copper_min = 0.001  # Minimal possible concentration
copper_max_ecological = 0.55  # Maximum allowable concentration based on ecological considerations

# Define other constraints
solver = Solver()
# solver.add(temperature >= 0, temperature <= 28.33)  # Celsius
solver.add(temperature >= 10, temperature <= 20)  # Celsius
solver.add(pH >= 6.5, pH <= 9.0)
solver.add(dissolved_oxygen >= 5)  # mg/L

# Binary search to minimize copper concentration
tolerance = 0.01  # Define a tolerance for how precise you want the answer
verified_copper_max = None  # Track the last verified max that met the mortality requirement

while copper_max_ecological - copper_min > tolerance:
    copper_mid = (copper_min + copper_max_ecological) / 2
    print(f"Testing copper concentration: {copper_mid}")
    
    solver.push()  # Save the current state of the solver
    solver.add(copper_conc >= copper_min, copper_conc <= copper_mid)
    
    if solver.check() == sat:
        model = solver.model()
        copper_conc_value = model.eval(copper_conc, model_completion=True).as_decimal(3)
        temperature_value = model.eval(temperature, model_completion=True).as_decimal(1)
        pH_value = model.eval(pH, model_completion=True).as_decimal(2)
        dissolved_oxygen_value = model.eval(dissolved_oxygen, model_completion=True).as_decimal(2)
        
        # Calculate predicted mortality rate using the solution
        predicted_mortality_rate = predict_mortality_rate(
            float(copper_conc_value), float(temperature_value), float(pH_value), float(dissolved_oxygen_value)
        )
        
        print(f"Predicted Mortality Rate: {predicted_mortality_rate} for Copper Concentration: {copper_conc_value} mg/L, Temperature: {temperature_value} C, pH: {pH_value}, Dissolved Oxygen: {dissolved_oxygen_value} mg/L")
        
        if predicted_mortality_rate >= 0.60:
            verified_copper_max = copper_conc_value  # Update the verified max
            copper_max_ecological = float(copper_conc_value)
        else:
            copper_min = float(copper_conc_value) + tolerance
    else:
        copper_min = copper_mid + tolerance
    
    solver.pop()  # Restore the state of the solver to add a new constraint

print(f"Minimum Copper Concentration: {verified_copper_max} that achieves the required mortality rate within ecological constraints.")