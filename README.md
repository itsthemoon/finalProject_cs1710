# Modeling Zebra Mussel Populations and Impacts on Freshwater Ecosystems

## Overview

In this project, we aimed to model the complex relationships between zebra mussel populations, water quality parameters, and the broader impacts on freshwater ecosystems over time, specifically within Rhode Island. Zebra mussels are an invasive species found in Rhode Island,and elsewhere, that can rapidly proliferate and substantially alter the ecosystems they invade.

We initially attempted to model these dynamics using the Forge modeling language. However, we found that the complex interplay between factors like zebra mussel density, sunlight penetration depth, dissolved oxygen, pH, and more was difficult to capture in Forge. We then pivoted to using Z3, which provided more powerful mathematical and logical modeling capabilities.

## Approach

### Zebra Mussel Mortality Model

Using a dataset on the impacts of copper-based molluscicide treatment on zebra mussel mortality, we trained a small machine learning model to predict the percentage of zebra mussels that would die over a 10-day treatment period based on factors like copper concentration, pH, dissolved oxygen, and temperature.

To integrate this predictive model into Z3, we converted it into a depth-5 decision tree, which we could then express using Z3 syntax and constraints. We used water quality regulations from the Rhode Island EPA to set bounds on acceptable ranges for the relevant water quality parameters. This allowed us to use Z3 to prove whether it was possible to achieve >50% zebra mussel mortality with a copper treatment while keeping water quality within legal limits. Additionally, once Z3 found a soultion, we were able to test this solution on our actual ml model to confirm what Z3 solved.

### Zebra Mussel Ecosystem Impacts Model

Zebra mussels are effective filter feeders that can substantially increase water clarity, which in turn allows sunlight to penetrate deeper into the water (increased light attenuation). This can lead to excessive growth of aquatic plants and destabilize the ecosystem.

To model this, we created decision trees (based on our best judgment and review of scientific literature) to approximate 1) the relationship between zebra mussel density and water clarity, and 2) the relationship between water clarity and light attenuation. We integrated these decision trees into a Z3 model along with a simulated zebra mussel reproduction rate, natural death rate, and an assumed 50% 10-day mortality from copper treatment (based on the results of our first Z3 model).

This model allowed us to assess how zebra mussel populations would change over time with copper-based molluscicide treatments and how this would impact the light attenuation depth in the lake ecosystem, while still adhering to water quality regulations.

## Results

We were able to use Z3 to prove that it is possible to achieve >50% zebra mussel mortality over a 10-day copper treatment while staying within the water quality bounds set by the RI EPA.

Our ecosystem model demonstrated that with this treatment regimen, we could keep zebra mussel populations low enough to prevent light attenuation from increasing to concerning levels that would lead to excessive plant growth and ecosystem disruption.

## Limitations and Future Work

The main limitations of our models were the lack of large real-world datasets to train and validate our models and the need to make many simplifying assumptions about the complex ecosystem dynamics. Ideally, we would collaborate with environmental scientists and lake managers to refine the models with more expert knowledge and real-world data.

Potential extensions could include modeling the impacts on other parts of the ecosystem (native mussels, fish populations, etc.), incorporating variable treatment schedules, and adding economic considerations around treatment costs vs. ecosystem services. A more advanced approach could involve learning the structure of the models themselves from data.

## References

- [Zebra Mussels Q&A - New York Sea Grant](https://seagrant.sunysb.edu/ais/pdfs/ZmusselQ-A.pdf)
- [Zebra Mussels in Rhode Island - RI Department of Environmental Management](https://dem.ri.gov/sites/g/files/xkgbur861/files/programs/benviron/water/quality/surfwq/pdfs/lakes012.pdf)
- [Bioassay Verification of a Zebra Mussel (Dreissena polymorpha) Eradication Treatment: Data](https://www.sciencebase.gov/catalog/file/get/5b85b224e4b05f6e321d4056?f=__disk__3e%2Fba%2F51%2F3eba51b77f68a7b2fcdf0ae9aef84948878b3c08&transform=1&allowOpen=true)
- [RI Water Quality Regulations](https://www.epa.gov/sites/default/files/2014-12/documents/riwqs.pdf)
- [Light Attenuation Kd490](https://catalog.data.gov/dataset/light-attenuation-kd490)

## Collaborators

- Jackson Davis
- Yonas Amha

## Note
The demo video can be found in this github repo, titled: "1710demovid.mp4"
