from scipy.optimize import minimize
from data_analysis.mussel_mortality_prediction import predict_mortality_rate

def objective_function(x):
    copper_conc, temperature, pH, dissolved_oxygen, treatment_t = x
    return -predict_mortality_rate(copper_conc, temperature, pH, dissolved_oxygen, treatment_t)

# Define the bounds for each variable
bounds = [
    (0.001, 0.55),  # Copper concentration range
    (10, 20),       # Temperature range
    (6.5, 9.0),     # pH range
    (5, 10),        # Dissolved oxygen range
    (1,1)          # Treatment type (0 or 1)
]

# Define the initial guess for the variables
initial_guess = [0.1, 15, 7.5, 8, 1]

# Perform the optimization
result = minimize(objective_function, initial_guess, bounds=bounds)

# Extract the optimal values
optimal_copper_conc, optimal_temperature, optimal_pH, optimal_dissolved_oxygen, optimal_treatment_t = result.x

# Calculate the maximum predicted mortality rate
max_predicted_mortality_rate = predict_mortality_rate(optimal_copper_conc, optimal_temperature, optimal_pH, optimal_dissolved_oxygen, optimal_treatment_t)

print("Optimal values:")
print("Copper concentration:", optimal_copper_conc)
print("Temperature:", optimal_temperature)
print("pH:", optimal_pH)
print("Dissolved oxygen:", optimal_dissolved_oxygen)
print("Treatment type:", optimal_treatment_t)
print("Maximum predicted mortality rate:", max_predicted_mortality_rate)