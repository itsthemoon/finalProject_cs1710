# finalProject_cs1710

# Setup

pip install -r requirements.txt

# Info

Dissolved oxygen (DO) measures the amount of oxygen that is mixed in water and available to aquatic organisms. It is typically reported in milligrams per liter (mg/L). The presence of dissolved oxygen is critical for the survival of fish, invertebrates, bacteria, and other aquatic life. It is measured using luminescent sensors that detect the oxygen levels based on luminescence emitted by a special material in the sensor that reacts to oxygen. High levels of dissolved oxygen are generally indicative of a healthy water environment, whereas low levels can be a sign of pollution or overpopulation of organisms consuming the oxygen.

# Information About Our Tests

- Scenario 1 (99% zebra mussel mortality and high water clarity):
  This scenario checks if it's possible to achieve a 99% reduction in the zebra mussel population compared to the initial population (variables_control[-1][0] <= 0.01 initial_zebra_mussel_population_control and variables_treatment[-1][0] <= 0.01 initial_zebra_mussel_population_treatment) while maintaining a high water clarity of at least 0.95 (variables_control[-1][1] >= 0.95 and variables_treatment[-1][1] >= 0.95) at the end of the simulation period.
- if Scenario 1 is feasible for the treatment condition but not for the control condition, it suggests that the copper treatment can effectively achieve high zebra mussel mortality and maintain high water clarity, while the control condition may not be able to reach those outcomes.

- Scenario 2 (Low water clarity):
  This scenario checks if it's possible for the water clarity to be below 0.4 (variables_control[-1][1] < 0.4 and variables_treatment[-1][1] < 0.4) at the end of the simulation period.
- if Scenario 2 is feasible for the control condition but not for the treatment condition, it indicates that low water clarity is possible in the absence of treatment, but the copper treatment helps prevent such an outcome.

- Future Test
  - Define a target zebra mussel population that is considered manageable or acceptable for Rhode Island based on the local ecosystem and stakeholder input. Create a scenario that checks if the model can achieve this target population under both control and treatment conditions. This test will help determine if the copper treatment can effectively control the zebra mussel population to the desired level in Rhode Island.
  - Further research can check for long term affects on the overall ecosystem

Difficulties:

- trying to make the data useful and developing a mortality function that is accurate given our data

PLAN:

Step 1: Data Preparation
First, you'll need to preprocess and clean the provided datasets. This includes:

Handling missing values (e.g., removing rows with missing data or imputing values)
Ensuring consistent data types and units across all variables
Merging the datasets based on common columns (e.g., Tank, Treatment, Day) to create a single unified dataset
Exploring the relationships between variables using scatter plots, correlation matrices, etc.

Step 2: Build Mortality Rate Model
Next, you'll build a model to predict zebra mussel mortality rate based on copper concentration and other water quality parameters.

Select relevant features (e.g., copper concentration, temperature, pH, dissolved oxygen) as independent variables and mortality rate as the dependent variable
Split the data into training and testing sets
Try different modeling approaches (e.g., logistic regression, decision trees, random forests) and evaluate their performance using metrics like accuracy, precision, recall, and F1 score
Choose the best-performing model and interpret its coefficients to understand the impact of each variable on mortality rate

Step 3: Research Rhode Island Water Quality Standards (we used: https://www.epa.gov/sites/default/files/2014-12/documents/riwqs.pdf)
To set up the constraints for your Z3 optimization, you need to know the acceptable ranges for water quality parameters in Rhode Island.

Review Rhode Island's environmental regulations and water quality standards
Identify the minimum and maximum allowable values for key parameters like temperature, pH, dissolved oxygen, etc.
Consult with local experts if needed to clarify any ambiguities or get guidance on appropriate ranges

Step 4: Determine Target Mortality Rate
Work with Rhode Island environmental agencies or experts to determine an appropriate target mortality rate for effective zebra mussel control.

Consider factors like the current extent of infestation, ecological impacts, and long-term management goals
Set a specific numerical target (e.g., 90% mortality) to use as the objective in your Z3 problem

Step 5: Formulate Z3 Optimization Problem
Now you can set up your Z3 optimization problem:

Define the decision variable as the copper concentration
Set the objective function to minimize the copper concentration
Add constraints for:

Achieving the target mortality rate based on your predictive model
Maintaining water quality parameters within Rhode Island's acceptable ranges

Write the Z3 code to solve the optimization problem and find the optimal copper concentration

Step 6: Analyze and Interpret Results
Finally, interpret the Z3 results in the context of Rhode Island's zebra mussel management:

Discuss the optimal copper concentration found and its predicted impact on mortality rate and water quality
Consider the practical feasibility and cost of applying this treatment strategy
Assess potential limitations of the approach and suggest areas for further research or field validation
Highlight the broader applicability of this optimization approach for invasive species management in other regions

Sources:

- zebra mussels are more commonly found in warm water: https://seagrant.sunysb.edu/ais/pdfs/ZmusselQ-A.pdf
- zebra mussels are more commonly found in fresh water: https://dem.ri.gov/sites/g/files/xkgbur861/files/programs/benviron/water/quality/surfwq/pdfs/lakes012.pdf
