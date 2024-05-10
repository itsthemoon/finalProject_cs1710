from z3 import *
from data_analysis.mussel_mortality_prediction import data, predict_mortality_rate_simplified, predict_mortality_rate

# Decision variables
copper_conc = Real('copper_conc')
temperature = Real('temperature')
pH = Real('pH')
dissolved_oxygen = Real('dissolved_oxygen')
treatment_t = Real('treatment_t')

# Optimization model
opt = Optimize()

# Constraints for environmental factors (adapt based on actual standards)
opt.add(copper_conc >= 0.001, copper_conc <= 0.55)  # Copper concentration range
opt.add(temperature >= 5, temperature <= 20)  # Temperature range
opt.add(pH >= 6.5, pH <= 9.0)  # pH range
opt.add(dissolved_oxygen >= 5)  # Minimum dissolved oxygen in mg/L
opt.add(treatment_t == 1)  # Assuming treatment_t is always 1 for the simplified model

# Constraint for the simplified function's output
opt.add(predict_mortality_rate_simplified(copper_conc, temperature, pH, dissolved_oxygen, treatment_t) > 0.5)

# Objective: minimize copper concentration
opt.minimize(copper_conc)

# Solve the optimization problem
if opt.check() == sat:
    model = opt.model()
    copper = model.eval(copper_conc).as_decimal(3)
    temp = model.eval(temperature).as_decimal(1)
    ph = model.eval(pH).as_decimal(2)
    oxygen = model.eval(dissolved_oxygen).as_decimal(2)
    
    print(f"Optimal Conditions Found: Copper: {copper} mg/L, Temp: {temp} C, pH: {ph}, Oxygen: {oxygen} mg/L")
    
    #Compare the predicted mortality rate to the actual mortality rate from our ml model
    actual_mortality_rate = predict_mortality_rate(float(copper), float(temp), float(ph), float(oxygen), 1)
    print(f"Actual Mortality Rate: {actual_mortality_rate}")
else:
    print("No feasible solution found.")

