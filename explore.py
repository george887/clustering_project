import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import scipy.stats
import os
from sklearn.cluster import KMeans

# Plots a pairgrid, distplot and regplot
def plot_variable_pairs(df):
    g = sns.PairGrid(df) 
    g.map_diag(sns.distplot)
    g.map_offdiag(sns.regplot)

# Plots boxplot, violinplot, and swarmplot
def plot_categorical_and_continuous_vars(cat_var, cont_var, df):
    '''This function takes in both categorical and continuous variables along with the corresponding df to create plots
    '''
    plt.rc('font', size=13)
    plt.rc('figure', figsize=(13, 7))
    sns.boxplot(data=df, y=cont_var, x=cat_var)
    plt.show()   
    sns.violinplot(data=df, y=cont_var, x=cat_var)
    plt.show()
    sns.swarmplot(data=df, y=cont_var, x=cat_var)
    plt.show()

def elbow_plot(X_train_scaled, cluster_vars):
    ''' This function will create an elbow plow to see what k value we should have in our Kmeans algo
    '''
    # elbow method to identify good k for us
    ks = range(2,20)
    
    # empty list to hold inertia (sum of squares)
    sse = []

    # loop through each k, fit kmeans, get inertia
    for k in ks:
        kmeans = KMeans(n_clusters=k)
        kmeans.fit(X_train_scaled[cluster_vars])
        # inertia
        sse.append(kmeans.inertia_)

    print(pd.DataFrame(dict(k=ks, sse=sse)))

    # plot k with inertia
    plt.plot(ks, sse, 'bx-')
    plt.xlabel('k')
    plt.ylabel('SSE')
    plt.title('Elbow method to find optimal k')
    plt.show()

#area_vars = ['latitude', 'longitude', 'age']
#elbow_plot(X_train_scaled, cluster_vars = area_vars) 

def run_kmeans(X_train_scaled, X_train, cluster_vars, k, cluster_col_name):
    ''' This function will run the kmeans algo
    '''
    # create kmeans object
    kmeans = KMeans(n_clusters = k, random_state = 13)
    # Fit the object
    kmeans.fit(X_train_scaled[cluster_vars])
    # predict and create a dataframe with cluster per observation
    train_clusters = \
        pd.DataFrame(kmeans.predict(X_train_scaled[cluster_vars]),
                              columns=[cluster_col_name],
                              index=X_train.index)
    
    return train_clusters, kmeans

# How to run
# train_clusters, kmeans = kmeans(X_train_scaled, X_train, k, cluster_vars, cluster_col_name)

def get_centroids(kmeans, cluster_vars, cluster_col_name):
    '''Gives us the centroid column names and creates a centroid df
    '''
    centroid_col_names = ['centroid_' + i for i in cluster_vars]

    centroids = pd.DataFrame(kmeans.cluster_centers_, 
             columns=centroid_col_names).reset_index().rename(columns={'index': cluster_col_name})
    
    return centroids

# How to run. cluster_vars = area_vars
# centroids = get_centroids(kmeans, cluster_vars, cluster_col_name)

def add_to_train(X_train, train_clusters, X_train_scaled, centroids, cluster_col_name):
    '''Adds the 
    '''
    # concatenate cluster id
    X_train = pd.concat([X_train, train_clusters], axis=1)

    # join on clusterid to get centroids
    X_train = X_train.merge(centroids, how='left', 
                            on=cluster_col_name).\
                        set_index(X_train.index)
    
    # concatenate cluster id
    X_train_scaled = pd.concat([X_train_scaled, train_clusters], 
                               axis=1)

    # join on clusterid to get centroids
    X_train_scaled = X_train_scaled.merge(centroids, how='left', 
                                          on=cluster_col_name).\
                            set_index(X_train.index)
    
    return X_train, X_train_scaled

def rfe_ranker(train):
    '''
    Uses Recursive Feature Elimination (RFE) to rank the given features in order of their usefulness in
    predicting logerror with a linear regression model.
    '''
    # creating linear regression object
    lm = LinearRegression()

    # fitting linear regression model to features 
    lm.fit(train.drop(columns=['bathroomcnt','fullbathcnt','bedroomcnt','unitcnt','taxrate', 'logerror','propertycountylandusecode','heatingorsystemdesc', 'binned_price_per_sqft', 'binned_bed_bath_ratio', 'transactiondate']), train['logerror'])

    # creating recursive feature elimination object and specifying to rank 5 of the best features
    rfe = RFE(lm, 5)

    # using rfe object to transform features 
    x_rfe = rfe.fit_transform(train.drop(columns=['bathroomcnt','fullbathcnt','bedroomcnt','unitcnt','taxrate', 'logerror','propertycountylandusecode','heatingorsystemdesc', 'binned_price_per_sqft', 'binned_bed_bath_ratio','transactiondate']), train['logerror'])

    feature_mask = rfe.support_

    # creating train df for rfe object 
    rfe_train = train.drop(columns=['bathroomcnt','fullbathcnt','bedroomcnt','unitcnt','taxrate', 'logerror','propertycountylandusecode','heatingorsystemdesc', 'binned_price_per_sqft', 'binned_bed_bath_ratio', 'transactiondate'])

    # creating list of the top features per rfe
    rfe_features = rfe_train.loc[:,feature_mask].columns.tolist()

    # creating ranked list 
    feature_ranks = rfe.ranking_

    # creating list of feature names
    feature_names = rfe_train.columns.tolist()

    # create df that contains all features and their ranks
    rfe_ranks_df = pd.DataFrame({'Feature': feature_names, 'Rank': feature_ranks})

    # return df sorted by rank
    return rfe_ranks_df.sort_values('Rank')

    def kmeans_transform(X_scaled, kmeans, cluster_vars, cluster_col_name):
    kmeans.transform(X_scaled[cluster_vars])
    trans_clusters = \
        pd.DataFrame(kmeans.predict(X_scaled[cluster_vars]),
                              columns=[cluster_col_name],
                              index=X_scaled.index)
    
    return trans_clusters
