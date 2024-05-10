from z3 import *
from data_analysis.mussel_mortality_prediction import predict_mortality_rate, data

# Decision variables
copper_conc = Real('copper_conc')
temperature = Real('temperature')
pH = Real('pH')
dissolved_oxygen = Real('dissolved_oxygen')
mortality_rate = Real('mortality_rate')

# Optimization model
opt = Optimize()

# Constraints for environmental factors (adapt based on actual standards)
opt.add(copper_conc >= 0.001, copper_conc <= 0.55)  # Copper concentration range
opt.add(temperature >= 10, temperature <= 20)  # Temperature range
opt.add(pH >= 6.5, pH <= 9.0)  # pH range
opt.add(dissolved_oxygen >= 5)  # Minimum dissolved oxygen in mg/L

# Constraint for the predicted mortality rate
opt.add(mortality_rate >= 0.9)  # Ensure mortality rate is above the desired threshold

# Objective: minimize copper concentration
opt.minimize(copper_conc)

# Solve the optimization problem
if opt.check() == sat:
    model = opt.model()
    copper = model.eval(copper_conc).as_decimal(3)
    temp = model.eval(temperature).as_decimal(1)
    ph = model.eval(pH).as_decimal(2)
    oxygen = model.eval(dissolved_oxygen).as_decimal(2)
    
    # Use the ML model to predict mortality rate based on the Z3 solution
    predicted_mortality_rate = predict_mortality_rate(float(copper), float(temp), float(ph), float(oxygen))
    print(f"Optimal Conditions Found: Copper: {copper} mg/L, Temp: {temp} C, pH: {ph}, Oxygen: {oxygen} mg/L")
    print(f"ML Model Predicted Mortality Rate: {predicted_mortality_rate}")
    
    # Find the closest matching row in the dataset
    closest_row = data.iloc[(data[['Copper', 'Temperature', 'pH', 'Dissolved Oxygen']] - 
                             [float(copper), float(temp), float(ph), float(oxygen)]).abs().sum(axis=1).idxmin()]
    actual_mortality_rate = closest_row['Mortality Rate']
    
    print(f"Actual Mortality Rate (from dataset): {actual_mortality_rate}")
    
    # Calculate the accuracy of the predicted mortality rate
    accuracy = 1 - abs(predicted_mortality_rate - actual_mortality_rate)
    print(f"Accuracy of Predicted Mortality Rate: {accuracy:.4f}")
else:
    print("No feasible solution found.")