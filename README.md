# Zillow Clustering Project

## Goal of Project
The goal of this project was to predict the drivers of logerror using clustering methodologies. Logerror is the difference between sales price and estimated price. We will continue to utilize the 2017 data found on the Codeup SQL server. A jupyter notebook will document all phases of the project including data acquisition, data preparation, exploration and modeling. A README.md will be made to describe and reproduce project. 

## Key Terms
- A [single-unit property](https://help.rentingwell.com/article/multi-unit-vs-single-unit/) is a rental property that is rented as a single entity. A condo, a townhouse, or a vacation rental would typically be single-unit properties. If you’re adding a single-unit property to Renting Well you don’t need to add individual units – the tenant and lease are associated to the property itself.
- [FIPS](https://transition.fcc.gov/oet/info/maps/census/fips/fips.txt#:~:text=FIPS%20codes%20are%20numbers%20which,to%20which%20the%20county%20belongs.) codes are numbers which uniquely identify geographic areas. The number of digits in FIPS codes vary depending on the level of geography. State-level FIPS codes have two digits, county-level FIPS codes have five digits of which the first two are the FIPS code of the state to which the county belongs.

# Project Planning

## Data Preparation
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
- age = 2017 - df.yearbuilt
- taxrate = taxamount / dtaxvaluedollarcnt
- acres = lotsizesquarefeet / 43560
- price_per_sqft = taxvaluedollarcnt / calculatedfinishedsquarefeet
- lotsize_per_sqft =  taxvaluedollarcnt / lotsizesquarefeet
- bed_bath_ratio = bedroomcnt / bathroomcnt

## Wrangle
- Created a wrangle.py 
- File contains functions to acquire and prepare the zillow data from the Codeup SQL server
- Icludes the filters from data prepartion above
- Handles and imputes missing values 
- Data split into train, validate, test, X_train, y_train, X_validate, y_validate, X_test, y_test

## Explore
- Created an explore.py file
- File contains functions to help create plots
- Functions for KMeans, centroids, adding clusters/centroids to data frames and RFE ranker

## Initial Thoughts
1. Is there a relationship between price_per_sqft and logerror?
2. Is there a relationship between bed_bath_ratio and logerror?
3. Is there a relationship between lot size per sqft and logerror?
4. Is there a relationship between lot size per sqft and price per sqft?

## Hypothesis Testing
> H<sub>0</sub>: Means of price_per_sqft_ratio small, medium, large are equal

> H<sub>a</sub>: Means of price_per_sqft_ratio small, medium, large are not equal

> H<sub>0</sub>: Means of bed_bath_ratio small, medium, large are equal

> H<sub>a</sub>: Means of bed_bath_ratio small, medium, large are not equal

## Data Dictionary
| Column | Description | Data Type |
| --- | ---| --- |
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

## Conclusions
- ANNOVA tests were ran on price per square feet and logerror & bed bath ratio and logerror
- Means were differnent in both test so the Ho was rejected
- Clusters were created comparing building quality type id & bed bath ratio, price per sqft & age, and price per sqft and lot size per sqft
- Dummy variables were created with clusters of price per sqft and lot size per sqft
- Modeling was performed with scaled data along with the cluster dummies
- The best model (Lassolars) did out perform the baseline RMSE 0.17374 on train and validate but did not on test 0.18188
- Further testing needs to be done to see how different features can help reduce the RMSE of logerror
- Look further into the relationship of binned bed bath ratio and logerror
- Create dummy variables with price per sqft and age to model

## How to reproduce

- Have access to the Codeup SQL data base
- Have credential in env.py file to establish a connection with the server
- Use wrangle.py file for data acquisition and data preperation
- Use explore.py file to explore
- Look at MVP_walkthru.ipynb to see analysis done

