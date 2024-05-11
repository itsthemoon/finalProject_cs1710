from mussel_mortality_prediction import predict_mortality_rate

copper_conc = 0.54  # This is the highest copper concentration observed within the data 
temperature = 8  # Lower end of the temperature range observed within the data 
pH = 7  # Lower end of the pH range observed within the data 
dissolved_oxygen = 5  # Lower end of the dissolved oxygen range observed within the data 

# Predict mortality rate
output = predict_mortality_rate(copper_conc, temperature, pH, dissolved_oxygen, 1)
print(f"Predicted mortality rate: {output}")

