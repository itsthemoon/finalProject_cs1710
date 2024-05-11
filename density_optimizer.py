import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import mean_squared_error

# Assume df is your DataFrame loaded with relevant data
# For demonstration, let's create a dummy DataFrame
data = {
    'zebra_density': np.random.randint(0, 301, 100),  # Random zebra densities between 0 and 300
    'water_clarity': np.random.uniform(70, 100, 100)  # Random water clarity values
}
df = pd.DataFrame(data)

# Set a fixed mortality_rate
df['mortality_rate'] = 0.45

# Add a random birth_rate column
np.random.seed(42)  # For reproducibility
df['birth_rate'] = np.random.uniform(0.47, 0.55, size=len(df))

# Selecting features and target variable for the model
X = df[['zebra_density', 'mortality_rate', 'birth_rate']]
y = df['water_clarity']

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialize the Decision Tree Regressor
decision_tree_reg = DecisionTreeRegressor(random_state=42)

# Train the model
decision_tree_reg.fit(X_train, y_train)

# Make predictions
dt_preds = decision_tree_reg.predict(X_test)

# Evaluate the model
dt_mse = mean_squared_error(y_test, dt_preds)

# Finding optimal zebra mussel density within the specified range
# Filter to get densities within the desired range
filtered_indices = X_test[(X_test['zebra_density'] >= 150) & (X_test['zebra_density'] <= 165)].index
filtered_preds = dt_preds[[i in filtered_indices for i in X_test.index]]
filtered_densities = X_test.loc[filtered_indices, 'zebra_density']

if len(filtered_preds) > 0:
    optimal_index = np.argmax(filtered_preds)  # Index of the best predicted water clarity within range
    optimal_zebra_density = filtered_densities.iloc[optimal_index]
    optimal_clarity = filtered_preds[optimal_index]
    print(f"Optimal Zebra Mussel Density: ~ {optimal_zebra_density:.2f} thousand zebra mussels per meters cubed")  # Formats the density to two decimal places
    print(f"Optimal Water Clarity: {optimal_clarity:.2f}")
    if(optimal_clarity <= 75):
        print(f"Sunlight penetration: Low")
    elif(optimal_clarity <= 85):
        print(f"Sunlight penetration: Medium")
    elif(optimal_clarity <= 95):
        print(f"Sunlight penetration: High")
    else:
        print(f"Sunlight penetration: Extreme")
else:
    print("No predictions within the specified zebra mussel density range.")




