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

- create a mortality function that can calculate the decline of zebra mussels (with the copper stuff added)
- using this function we can extrapolate to many more mussels and see how long it would take (if we keep using the treatment)
  for them to reach a low population, or if it is even possible

TODO:

- finish the mortality function analysis (claude)
- starting from 1000 mussels track the population over time if we 
