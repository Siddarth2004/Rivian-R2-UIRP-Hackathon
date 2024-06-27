# Rivian-R2-UIRP-Hackathon

Team Members: Alex, Akshat, Sudar, Mayank, Will, Siddarth 

In this project, we utilized two datasets, an EV charger dataset that gives us data on all the EV chargers in the US, and a population density dataset, which allows to visualize population data by county. Using this, we have developed an algorithm that can decide on charger allocation based on availability, accessibility, population density, and proximity to closest EV charger.

The EV Charger Dataset contains a list of all chargers in the US, sorted by location, and by type of station (Gas, Electric, etc), and we correlated the location data from this dataset and mapped it onto the world map by converting the location into its latitudinal and longitudinal coordinates. The population density data had split the land masses of the US into small "hexagons" and using the population data of this particular hexagon and existing EV chargers, we were able to decide whether that hexagon needs a charger and if it does, where exactly does it need to be located.

For example, let's say a person lives in a rural area of Illinois and they own an EV car. According to our analysis, they may have to travel a long distance just to charge their vehicle. This, obviously, is not favourable. Similarly, what we have noticed, particularly in a city like Chicago, is that the EV chargers arr localised to the downtown area. However, a significant proportion of the population lives in the suburbs, making it hard for them to access high speed electric chargers. Thus, they are forced to use level 1 chargers, which are typically slow and not reliable, and are not suggested for use by car manufacturers. While level 2 chargers take 1-1.5 hours to charge completely, a level 1 charger takes 8-10 hours for a typical ModelX/Y Tesla or Rivian R1S.

Our algorithm works as such: Within a particular hexagonal radius, it takes into account the number of chargers within, and the relative position of each charger. After taking the weighted average of the chargers, it decides where to place a new charger (if needed). If the population density is justified by the number of EV chargers in the area, there is no need to add another one. However, if needed, we will add another EV charger. For example, if in a hexagon, there is a large concentration of EV chargers on the right hand side, we would mirror the weighted average of the positions and place the new EV charger on the left hand side.

Thus, we hope that our project can be utilized by large scale car manufacturers in order to decide where to allocate the next EV charger. In order to prepare for the future, and work towards sustainability, it is of prime importance to open more EV chargers in the right places, ensuring an accessible charger for every EV owner.

EV Charger Dataset: https://www.kaggle.com/datasets/saketpradhan/electric-and-alternative-fuel-charging-stations?select=Electric+and+Alternative+Fuel+Charging+Stations.csv

Population Density Dataset: https://data.humdata.org/dataset/kontur-population-dataset-3km
