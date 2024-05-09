from z3 import *
from data_analysis.mussel_mortality_prediction import predict_mortality_rate


# Decision variables
copper_conc = Real('copper_conc')
temperature = Real('temperature')
pH = Real('pH')
dissolved_oxygen = Real('dissolved_oxygen')
mortality_rate = Real('mortality_rate')

# Optimization model
opt = Optimize()

# Constraints for copper concentration and estimated mortality rate
opt.add(If(copper_conc < 0.1, mortality_rate == 0.0,
           If(And(copper_conc >= 0.1, copper_conc < 0.2), mortality_rate == 0.668,
              If(And(copper_conc >= 0.2, copper_conc < 0.3), mortality_rate == 0.812,
                 If(And(copper_conc >= 0.3, copper_conc < 0.4), mortality_rate == 0.775,
                    If(And(copper_conc >= 0.4, copper_conc < 0.5), mortality_rate == 0.943,
                       mortality_rate == 0.969))))))

# Constraints for other environmental factors (these ranges should be adapted based on actual standards)
opt.add(temperature >= 10, temperature <= 20)  # Temperature range
opt.add(pH >= 6.5, pH <= 9.0)  # pH range
opt.add(dissolved_oxygen >= 5)  # Minimum dissolved oxygen in mg/L

# Ensure the mortality rate is above the threshold needed to control zebra mussels effectively
opt.add(mortality_rate >= 0.9)

# Objective: minimize copper concentration
opt.minimize(copper_conc)

# Solve the optimization problem
if opt.check() == sat:
    model = opt.model()
    copper = model.eval(copper_conc).as_decimal(3)
    temp = model.eval(temperature).as_decimal(1)
    ph = model.eval(pH).as_decimal(2)
    oxygen = model.eval(dissolved_oxygen).as_decimal(2)
    mort_rate = model.eval(mortality_rate).as_decimal(2)
    print(f"Optimal Conditions Found: Copper: {copper} mg/L, Temp: {temp} C, pH: {ph}, Oxygen: {oxygen} mg/L")
    print(f"Predicted Mortality Rate (from model): {mort_rate}")
    
    # Use the ML model to predict mortality rate based on the Z3 solution
    predicted_mortality_rate = predict_mortality_rate(float(copper), float(temp), float(ph), float(oxygen))
    print(f"ML Model Predicted Mortality Rate: {predicted_mortality_rate}")
else:
    print("No feasible solution found.")
