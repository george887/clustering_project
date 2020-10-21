import pandas as pd
import numpy as np
# ENV has credentials needed to access the SQL database. Gitignore should be created before to prevent your info to be compromised
from env import host, user, password
# OS Looks to see if data is stored locally
import os
# allows us to ignore any warnings
import warnings
warnings.filterwarnings("ignore")
# imports the train test split
from sklearn.model_selection import train_test_split
# Scaler
from sklearn.preprocessing import MinMaxScaler, StandardScaler

########################## Establishing connection ###########################
# establish mysql connection
def get_connection(db, user=user, host=host, password=password):
    return f'mysql+pymysql://{user}:{password}@{host}/{db}'

########################## Creating function to get data ######################
def new_zillow_data():
    '''
    This function reads the zillow data from the Codeup db into a df,
    write it to a csv file, and returns the df. 
    '''
    # Selecting all data in the properties_2017 table
    sql_query = '''  select * from properties_2017
                join predictions_2017 using (parcelid)
                left join airconditioningtype using (airconditioningtypeid)
                left join architecturalstyletype using (architecturalstyletypeid)
                left join buildingclasstype using (buildingclasstypeid)
                left join heatingorsystemtype using (heatingorsystemtypeid)
                left join propertylandusetype using (propertylandusetypeid)
                left join storytype using (storytypeid)
                left join typeconstructiontype using (typeconstructiontypeid)
                left join unique_properties using (parcelid)
                where latitude is not null and longitude is not null;
                '''

    # The pandas read_sql function allows us to create a df with the afformentioned sql querry    
    df = pd.read_sql(sql_query, get_connection('zillow'))

    # Converts the df into a csv
    df.to_csv('zillow_df.csv')

    # This prevents any duplicated columns. The ~ allows to return the unique columns. A boolean array is created
    # and only falses are returned
    df = df.loc[:,~df.columns.duplicated()]

    return df

def get_zillow_data(cached=False):
    '''
    This function reads in zillow data from Codeup database if cached == False, a csv is created
    returning the df. If cached == True, the function reads in the zillow df from a csv file & returns df
    '''
    # This runs if there is no csv containing the zillow data
    if cached or os.path.isfile('zillow_df.csv') == False:

        # Converts the df into a csv
        df = new_zillow_data()

    else:

        # If the csv was stored locally, the csv will return the df
        df = pd.read_csv('zillow_df.csv', index_col=0)

    return df

#################### Prepare ##################

def fips_labels(row):
    if row['fips'] == 6037:
        return 'Los Angeles County'
    elif row['fips'] == 6059:
        return 'Orange County'
    elif row['fips'] == 6111:
        return 'Ventura County'
        
def add_fips(df):
    df['fips'] = df.apply(lambda row: fips_labels(row), axis=1)
    return df

def single_unit_properties(df):
    '''This function will filter single unit properties, fillna's, drop unwanted columns, and replace features
    '''
    df = df[df.propertylandusetypeid.isin([260,261,262,279])]
    df = df[(df.bedroomcnt > 0) & (df.bathroomcnt > 0)]
    df = df[(df.bedroomcnt < 6) & (df.bathroomcnt < 5)]
    df = df[df.calculatedfinishedsquarefeet < 7000]
    df.unitcnt = df.unitcnt.fillna(1)
    df = df[df.unitcnt == 1.0]
    df = df.drop(columns=["propertylandusetypeid", "heatingorsystemtypeid", 'propertyzoningdesc', 'calculatedbathnbr', 
                            "id", "id.1", 'parcelid', 'landtaxvaluedollarcnt', 'regionidcounty',
                            'regionidcity', 'regionidzip','finishedsquarefeet12', 'rawcensustractandblock','assessmentyear',
                            'censustractandblock','propertylandusedesc'])
    df['heatingorsystemdesc'].replace(np.nan, 'none', inplace=True)
    df['age'] = 2017 - df.yearbuilt
    df['taxrate'] = df.taxamount/df.taxvaluedollarcnt
    df['acres'] = df.lotsizesquarefeet/43560
    df['price_per_sqft'] = df.taxvaluedollarcnt/df.calculatedfinishedsquarefeet
    df['lotsize_per_sqft'] = df.taxvaluedollarcnt/df.lotsizesquarefeet
    df['bed_bath_ratio'] = df.bedroomcnt/df.bathroomcnt
    # Renaming columns to read easier
    df = df.rename(columns={'calculatedfinishedsquarefeet': 'sqft', 'taxvaluedollarcnt': 'home_value'})
    
    return df

# How to call function df= single_unit_properties(df)

def handle_missing_values(df, prop_required_column = .60, prop_required_row = .60):
    ''' This function will drop na's when the required thresh is not met'''
    threshold = int(round(prop_required_column*len(df.index),0))
    df.dropna(axis=1, thresh=threshold, inplace=True)
    threshold = int(round(prop_required_row*len(df.columns),0))
    df.dropna(axis=0, thresh=threshold, inplace=True)
    return df

# How to call function df=handle_missing_values(df, prop_required_column = .60, prop_required_row = .60)

def impute_missing_values(df):
    '''This function will split the data into train, validate and test data frames. I imputed the missing values of 
    the list of features (Categorical/Discrete) using the mode or most common
    '''

    train_and_validate, test = train_test_split(df, test_size=.2, random_state=123)
    train, validate = train_test_split(train_and_validate, test_size=.3, random_state=123)
    
    cols1 = [
    "buildingqualitytypeid",
    "yearbuilt",
    "age"
    ]

# filling in nulls with the most frequent
    for col in cols1:
        mode = int(train[col].mode()) 
        train[col].fillna(value=mode, inplace=True)
        validate[col].fillna(value=mode, inplace=True)
        test[col].fillna(value=mode, inplace=True)

    return train, validate, test

# How to call function train, validate, test =impute_missing_values(df)

def impute_missing_values_1(train, validate, test):
    '''This function will imputed the missing values of 
    the list of features (Continuous columns) using the median
    '''

    cols = [
        "structuretaxvaluedollarcnt",
        "taxamount",
        "home_value",
        "structuretaxvaluedollarcnt",
        "sqft",
        "fullbathcnt", 
        "lotsizesquarefeet",
        "lotsize_per_sqft",
        "taxrate",
        "acres",
        "price_per_sqft"
    ]

    for col in cols:
        median = train[col].median()
        train[col].fillna(median, inplace=True)
        validate[col].fillna(median, inplace=True)
        test[col].fillna(median, inplace=True)
        
    return train, validate, test

# How to call function train, validate, test = impute_missing_values_1(train, validate, test)

def X_train_select(train, validate, test, target_var):
    '''This function will create an X_train, X_validate, X_test and Y_train etc. for modeling
    '''
    # create X_train by dropping the target variable 
    X_train = train.drop(columns=[target_var])
    
    # create y_train by keeping only the target variable.
    y_train = train[[target_var]]

    # create X_validate by dropping the target variable 
    X_validate = validate.drop(columns=[target_var])
    # create y_validate by keeping only the target variable.
    y_validate = validate[[target_var]]

    # create X_test by dropping the target variable 
    X_test = test.drop(columns=[target_var])
    # create y_test by keeping only the target variable.
    y_test = test[[target_var]]
    
    return X_train, y_train, X_validate, y_validate, X_test, y_test    

    # How to call function X_train, y_train, X_validate, y_validate, X_test, y_test = X_train_select(train, validate, test, target_var = 'logerror')

def add_scaled_columns(X_train, X_validate, X_test, scaler, columns_to_scale):
    """This function will add scaled columns to X_train_scaled, X_validate_scaled, and X_test_scaled"""
    new_column_names = [c + '_scaled' for c in columns_to_scale]
    scaler.fit(X_train[columns_to_scale])

    X_train_scaled = pd.concat([
        X_train,
        pd.DataFrame(scaler.transform(X_train[columns_to_scale]), columns=new_column_names, index=X_train.index),
    ], axis=1)
    X_validate_scaled = pd.concat([
        X_validate,
        pd.DataFrame(scaler.transform(X_validate[columns_to_scale]), columns=new_column_names, index=X_validate.index),
    ], axis=1)
    X_test_scaled = pd.concat([
        X_test,
        pd.DataFrame(scaler.transform(X_test[columns_to_scale]), columns=new_column_names, index=X_test.index),
    ], axis=1)
    
    return X_train_scaled, X_validate_scaled, X_test_scaled

    # How to call function
    # scaler = StandardScaler() or whatever scaler wanting to use. 
    # columns_to_scale = train.drop(columns=["logerror",'propertycountylandusecode','transactiondate','heatingorsystemdesc']).columns.tolist()
    # X_train_scaled, X_validate_scaled, X_test_scaled = add_scaled_columns(X_train, X_validate, X_test, scaler, columns_to_scale)
