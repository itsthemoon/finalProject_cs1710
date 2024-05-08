import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import pearsonr
import statsmodels.api as sm
from statsmodels.stats.outliers_influence import variance_inflation_factor
import numpy as np

class Analysis:
    def __init__(self, mortality_file, copper_file, water_chemistry_file):
        self.df_mortality = pd.read_csv(mortality_file)
        self.df_copper = pd.read_csv(copper_file)
        self.df_chemistry = pd.read_csv(water_chemistry_file)  # Assuming you have a single file for water chemistry
        self.df_combined = pd.merge(self.df_mortality, self.df_copper, on=['Tank', 'Day', 'Treatment'])
        self.df_combined = pd.merge(self.df_combined, self.df_chemistry, on=['Tank', 'Day', 'Treatment'], how='left')

    def get_treatment_data(self):
        return self.df_combined[self.df_combined['Treatment'] == 'T']

    def get_control_data(self):
        return self.df_combined[self.df_combined['Treatment'] == 'C']

    def calculate_vif(self, X):
        """ Calculate VIF for each variable in the given DataFrame X """
        # Adding a constant for intercept
        X = sm.add_constant(X)
        vif_data = pd.DataFrame()
        vif_data['Variable'] = X.columns
        vif_data['VIF'] = [variance_inflation_factor(X.values, i) for i in range(X.shape[1])]
        return vif_data

    def analyze(self, df_treatment, df_control):
        df_treatment.loc[:, 'Total'] = df_treatment['Alive'] + df_treatment['Dead']
        df_treatment.loc[:, 'Mortality Rate'] = df_treatment['Dead'] / df_treatment['Total']
        df_control.loc[:, 'Total'] = df_control['Alive'] + df_control['Dead']
        df_control.loc[:, 'Mortality Rate'] = df_control['Dead'] / df_control['Total']

        df_diff = pd.merge(df_treatment, df_control, on='Day', suffixes=('_treatment', '_control'))
        df_diff['Mortality Rate Difference'] = df_diff['Mortality Rate_treatment'] - df_diff['Mortality Rate_control']

        # Define the predictors and the response variable
        X_columns = ['Copper_treatment', 'pH_treatment', 'Dissolved Oxygen_treatment', 'Specific Conductance_treatment', 'Temperature_treatment']
        X = df_diff[X_columns]
        X = sm.add_constant(X)  # Make sure to add a constant to the model
        y = df_diff['Mortality Rate Difference']

        # Fit the model
        model = sm.OLS(y, X).fit()
        print(model.summary())

        # Set up the plot
        plt.figure(figsize=(10, 5))
        plt.scatter(df_diff['Copper_treatment'], df_diff['Mortality Rate Difference'], alpha=0.5)

        # Generating data for predictions
        copper_range = np.linspace(df_diff['Copper_treatment'].min(), df_diff['Copper_treatment'].max(), 100)
        plot_df = pd.DataFrame({
            'Copper_treatment': copper_range,
            'pH_treatment': np.repeat(np.mean(df_diff['pH_treatment']), 100),
            'Dissolved Oxygen_treatment': np.repeat(np.mean(df_diff['Dissolved Oxygen_treatment']), 100),
            'Specific Conductance_treatment': np.repeat(np.mean(df_diff['Specific Conductance_treatment']), 100),
            'Temperature_treatment': np.repeat(np.mean(df_diff['Temperature_treatment']), 100),
        })

        plot_df = sm.add_constant(plot_df)  # add constant for intercept
        predictions = model.predict(plot_df)  # Ensure this DataFrame matches the model

        plt.plot(copper_range, predictions, 'r', linewidth=2)
        plt.xlabel('Copper Concentration (mg/L)')
        plt.ylabel('Adjusted Mortality Rate Difference')
        plt.title('Regression Line: Adjusted Mortality Rate vs. Copper Concentration')
        plt.show()


if __name__ == "__main__":
    analysis = Analysis("data/Mortality.csv", "data/Copper.csv", "data/Water Chemistry.csv")
    df_treatment = analysis.get_treatment_data()
    df_control = analysis.get_control_data()
    analysis.analyze(df_treatment, df_control)
