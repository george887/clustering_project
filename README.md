# Zillow Clustering Project

## Goal of Project
The goal of this project is to predict what is causing more and less logerror using clustering methodologies. We will continue to utilize the 2017 data found on the Codeup SQL server. A jupyter notebook will document all phases of the project including data acquisition, data preparation, exploration and modeling. A README.md will be made to describe and reproduce project. 

## Key Terms
- A [single-unit property](https://help.rentingwell.com/article/multi-unit-vs-single-unit/) is a rental property that is rented as a single entity. A condo, a townhouse, or a vacation rental would typically be single-unit properties. If you’re adding a single-unit property to Renting Well you don’t need to add individual units – the tenant and lease are associated to the property itself.
- [FIPS](https://transition.fcc.gov/oet/info/maps/census/fips/fips.txt#:~:text=FIPS%20codes%20are%20numbers%20which,to%20which%20the%20county%20belongs.) codes are numbers which uniquely identify geographic areas. The number of digits in FIPS codes vary depending on the level of geography. State-level FIPS codes have two digits, county-level FIPS codes have five digits of which the first two are the FIPS code of the state to which the county belongs.

## Data preparation
For this project some filters were applied to help limit for only single unit properties, outliers and null values. 
- Propertylandusetypeid = [260,261,262,279]
- Bedroomcnt > 0 and < 6
- Bathroomcnt > 0 and < 5
- Sqft < 7000
- Unitcnt nulls == 1
- Heatingorsystemdesc nulls replaced as “none”
- Required columns and rows set at 60%. Anything below was dropped
- Categorical variables with an acceptable amount of nulls missing replaced with the mode
- Continuous variables with an acceptable amount of nulls missing replaced with the median

## Data Dictionary
| Column | Description | Data Type |
| --- | ---|
| bathroomcnt | Number of bathrooms including fractional bathrooms | float64 |
| bedroomcnt | Number of bedrooms | float64 |
| buildingqualitytypeid | Assessment of condition of home from best (lowest) to worst (highest) | float64 |
| sqft | Total squarefeet of home | float64 |
| fips | Federal Information Processing System codes - unique geographical areas | float64 |
| fullbathcnt | Number of full bathrooms | float64 |
| latitude | Latitude of the property | float64 |
| longitude | Longitude of the property | float64
| lotsizesquarefeet| Size of the lot in square feet | float64 |
| propertycountylandusecode | County land use code AKA zoning at the county level | object |
| roomcnt | Number of rooms in the property | float64 |
| unitcnt | Number of property units on the property | float 64 |
| yearbuilt | The year the property was built | float 64 |
| structuretaxvaluedollarcnt | The tax assessed value of the property structure | float64 |
| home_value | The tax accessed value of the property | float64 |
| taxamount | Property tax assessed for that year | float 64 |
| logerror | Zillow's Zestimate model. Difference in sale price and estimated price | float64 |
| transactiondate | Date of property purchase | object |
| heatingorsystemdesc | Type of heating system in home | object |
| county | Fips value converted to actual county | | object |
| age | Age of property | float64 | 
