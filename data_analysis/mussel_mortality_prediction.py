# Zebra Mussel Mortality Prediction Model
# This script loads a dataset of zebra mussel mortality rates, pre-processes it, and applies machine learning models to predict mortality rates based on water quality measurements and treatment types.
# Steps:
# 1. Load the dataset: The dataset containing information on zebra mussels from Day 2 onwards is loaded from a CSV file.
# 2. Data Preprocessing:
#    - Filters data to include records from Day 2 onwards due to the start of mortality assessments post-treatment.
#    - Sorts data by 'Tank', 'Treatment', and 'Day' to maintain chronological order.
#    - Calculates cumulative deaths for each group by summing up the 'Dead' count cumulatively within each 'Tank' and 'Treatment' group from Day 2.
#    - Computes the mortality rate as the ratio of cumulative deaths to the total number of mussels (alive + dead).
#    - Encodes the 'Treatment' categorical variable into binary variables to differentiate between control (C) and treatment (T) groups.
# 3. Feature Selection: Selects features relevant for prediction, including copper concentration, water temperature, pH, dissolved oxygen levels, and treatment type.
# 4. Model Training and Evaluation:
#    - Splits the data into training (80%) and testing (20%) sets to validate the model's performance.
#    - Trains three different regression models: Linear Regression, Decision Tree Regressor, and Random Forest Regressor.
#    - Evaluates each model's performance using Mean Squared Error (MSE), Root Mean Squared Error (RMSE), and R-squared (R²) metrics to assess the accuracy and reliability of predictions.
# 5. Outputs performance metrics for each model to compare their effectiveness in predicting the mortality rate based on the selected features.

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor, export_text
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import MinMaxScaler
from sklearn.tree import DecisionTreeRegressor
from z3 import *
from sklearn.metrics import mean_squared_error, r2_score
import numpy as np
import math
import matplotlib.pyplot as plt

data = pd.read_csv('./data/Final_Merged_Dataset.csv')

# Filter data to start from Day 2
data = data[data['Day'] >= 2]

# Initialize cumulative deaths and adjust for days >= 7
data['Cumulative Deaths'] = data['Dead']  # Start with current day's deaths
data.sort_values(by=['Tank', 'Treatment', 'Day'], inplace=True)  # Sort data to ensure correct cumulative sum

# Apply a groupby on 'Tank' and 'Treatment' to handle multiple tanks and treatments correctly
data['Cumulative Deaths'] = data.groupby(['Tank', 'Treatment'])['Cumulative Deaths'].cumsum()

# Calculate mortality rate using cumulative deaths post-Day 7
data['Mortality Rate'] = data['Cumulative Deaths'] / (data['Alive'] + data['Cumulative Deaths'])

# Encode categorical data
data = pd.get_dummies(data, columns=['Treatment'])

features = data[['Copper', 'Temperature', 'pH', 'Dissolved Oxygen', 'Treatment_C', 'Treatment_T']]
target = data['Mortality Rate'].fillna(0)  # Handling any NaN by replacing them with 0

# Normalize the features
scaler = MinMaxScaler()
scaled_features = scaler.fit_transform(features)

# Update the feature names
scaled_feature_names = ['Scaled_' + col for col in features.columns]

# Create a new DataFrame with the scaled features
scaled_features_df = pd.DataFrame(scaled_features, columns=scaled_feature_names, index=features.index)

# Update the features DataFrame
features = scaled_features_df

X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.2, random_state=42)

linear_reg = LinearRegression()
decision_tree_reg = DecisionTreeRegressor()
random_forest_reg = RandomForestRegressor()

def evaluate_model(model, X_train, y_train, X_test, y_test):
    model.fit(X_train, y_train)
    predictions = model.predict(X_test)
    mse = mean_squared_error(y_test, predictions)
    rmse = math.sqrt(mse)
    r2 = r2_score(y_test, predictions)
    return mse, rmse, r2

# Evaluate models
linear_reg_metrics = evaluate_model(linear_reg, X_train, y_train, X_test, y_test)
decision_tree_reg_metrics = evaluate_model(decision_tree_reg, X_train, y_train, X_test, y_test)
random_forest_reg_metrics = evaluate_model(random_forest_reg, X_train, y_train, X_test, y_test)

# print("Linear Regression:", linear_reg_metrics)
# print("Decision Tree Regressor:", decision_tree_reg_metrics)
# print("Random Forest Regressor:", random_forest_reg_metrics)

# Select Random Forest Regressor as the final model
final_model = RandomForestRegressor()
final_model.fit(features, target)

def predict_mortality_rate(copper_conc, temperature, pH, dissolved_oxygen, treatment_t):
    # Normalize the input values using the same scaling used in the machine learning model
    scaled_copper, scaled_temperature, scaled_pH, scaled_dissolved_oxygen, scaled_treatment_t = normalize_inputs_numeric(copper_conc, temperature, pH, dissolved_oxygen, treatment_t)
    
    # Create a DataFrame with the normalized input parameters
    input_data = pd.DataFrame({
        'Scaled_Copper': [scaled_copper],
        'Scaled_Temperature': [scaled_temperature],
        'Scaled_pH': [scaled_pH],
        'Scaled_Dissolved Oxygen': [scaled_dissolved_oxygen],
        'Scaled_Treatment_C': [1 - scaled_treatment_t],
        'Scaled_Treatment_T': [scaled_treatment_t]
    })
    
    # Use the trained model to make predictions
    predicted_mortality_rate = final_model.predict(input_data)[0]
    return predicted_mortality_rate

# Create a simplified decision tree with depth constraints
simplified_model = DecisionTreeRegressor(max_depth=5)
simplified_model.fit(features, target)

# Extract the decision tree rules
tree_rules = export_text(simplified_model, feature_names=features.columns.tolist())
# print("Decision Tree Rules:")
# print(tree_rules)

def normalize_inputs_numeric(copper_conc, temperature, pH, dissolved_oxygen, treatment_t):
    # Normalize the input values using the same scaling used in the machine learning model
    scaled_copper = (copper_conc - features['Scaled_Copper'].min()) / (features['Scaled_Copper'].max() - features['Scaled_Copper'].min())
    scaled_temperature = (temperature - features['Scaled_Temperature'].min()) / (features['Scaled_Temperature'].max() - features['Scaled_Temperature'].min())
    scaled_pH = (pH - features['Scaled_pH'].min()) / (features['Scaled_pH'].max() - features['Scaled_pH'].min())
    scaled_dissolved_oxygen = (dissolved_oxygen - features['Scaled_Dissolved Oxygen'].min()) / (features['Scaled_Dissolved Oxygen'].max() - features['Scaled_Dissolved Oxygen'].min())
    scaled_treatment_t = 1 if treatment_t == 1 else 0
    
    return scaled_copper, scaled_temperature, scaled_pH, scaled_dissolved_oxygen, scaled_treatment_t

def normalize_inputs(copper_conc, temperature, pH, dissolved_oxygen, treatment_t):
    # Normalize the input values using the same scaling used in the machine learning model
    scaled_copper = (copper_conc - features['Scaled_Copper'].min()) / (features['Scaled_Copper'].max() - features['Scaled_Copper'].min())
    scaled_temperature = (temperature - features['Scaled_Temperature'].min()) / (features['Scaled_Temperature'].max() - features['Scaled_Temperature'].min())
    scaled_pH = (pH - features['Scaled_pH'].min()) / (features['Scaled_pH'].max() - features['Scaled_pH'].min())
    scaled_dissolved_oxygen = (dissolved_oxygen - features['Scaled_Dissolved Oxygen'].min()) / (features['Scaled_Dissolved Oxygen'].max() - features['Scaled_Dissolved Oxygen'].min())
    scaled_treatment_t = If(treatment_t == 1, 1, 0)

    return scaled_copper, scaled_temperature, scaled_pH, scaled_dissolved_oxygen, scaled_treatment_t

def predict_mortality_rate_simplified(copper_conc, temperature, pH, dissolved_oxygen, treatment_t):
    # Normalize the input values
    scaled_copper, scaled_temperature, scaled_pH, scaled_dissolved_oxygen, scaled_treatment_t = normalize_inputs(copper_conc, temperature, pH, dissolved_oxygen, treatment_t)

    # Translate the decision tree rules into Z3's If conditions
    return If(scaled_temperature <= 0.25,
              If(scaled_pH <= 0.46,
                 If(scaled_dissolved_oxygen <= 0.40,
                    If(scaled_copper <= 0.42,
                       If(scaled_copper <= 0.29,
                          0.95,
                          0.98),
                       If(scaled_dissolved_oxygen <= 0.16,
                          0.99,
                          1.00)),
                    If(scaled_copper <= 0.45,
                       If(scaled_pH <= 0.40,
                          0.92,
                          0.99),
                       If(scaled_dissolved_oxygen <= 0.47,
                          0.78,
                          0.88))),
                 If(scaled_dissolved_oxygen <= 0.52,
                    If(scaled_temperature <= 0.06,
                       0.90,
                       If(scaled_dissolved_oxygen <= 0.43,
                          0.82,
                          0.79)),
                    If(scaled_copper <= 0.87,
                       If(scaled_dissolved_oxygen <= 0.61,
                          0.99,
                          0.95),
                       If(scaled_dissolved_oxygen <= 0.60,
                          0.92,
                          0.88)))),
              If(scaled_copper <= 0.51,
                 If(scaled_treatment_t <= 0.50,
                    0.00,
                    If(scaled_copper <= 0.37,
                       If(scaled_dissolved_oxygen <= 0.94,
                          0.28,
                          0.31),
                       If(scaled_pH <= 0.97,
                          0.20,
                          0.24))),
                 If(scaled_pH <= 0.52,
                    If(scaled_pH <= 0.50,
                       0.62,
                       If(scaled_copper <= 0.67,
                          0.70,
                          0.62)),
                    If(scaled_dissolved_oxygen <= 0.52,
                       0.53,
                       0.60))))
    
# Model Selection Summary:
# After evaluating three regression models (Linear Regression, Decision Tree Regressor, and Random Forest Regressor) 
# on their ability to predict zebra mussel mortality rates, the Random Forest Regressor was chosen as the final model. 
# This decision was based on its superior performance metrics: it achieved the lowest Mean Squared Error (MSE) of 0.00340, 
# the lowest Root Mean Squared Error (RMSE) of 0.05833, and the highest R-squared (R²) value of 0.9774. 
# These statistics indicate the highest accuracy and best fit among the models tested. 
# The Random Forest Regressor's ability to effectively handle complex interactions and non-linear relationships in the data 
# makes it the most suitable model for predicting mortality rates with high reliability and precision.
