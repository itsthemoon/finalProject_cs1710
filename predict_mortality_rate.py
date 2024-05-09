from data_analysis.mussel_mortality_prediction import predict_mortality_rate

# Define input values
copper_conc = 0.54  # Highest copper concentration observed in the data
temperature = 8  # Lower end of the temperature range in the data
pH = 6.5  # Lower end of the pH range in the data
dissolved_oxygen = 5  # Lower end of the dissolved oxygen range in the data

# Predict mortality rate
output = predict_mortality_rate(copper_conc, temperature, pH, dissolved_oxygen)
print(f"Predicted mortality rate: {output}")

