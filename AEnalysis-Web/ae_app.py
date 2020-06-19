#!/bin/env python

# All data processing libraries
import numpy as np
import pandas as pd
from scipy import stats

# All graphing libraries
import altair as alt
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.font_manager

# All machine learning libraries
from sklearn import metrics
from sklearn import model_selection
from sklearn import preprocessing
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor

import streamlit as st
from pyArango.connection import *

'''
# AliExpress Product Analytics

This is a tool to view item data that was mined from all AliExpress categories.
The list of categories are available on the left and can be used to select the product category you would like to see.
'''
colls = {'Name': ["Appliances", "Automobiles & Motorcycles", "Bags", "Beauty & Health", "Computer", "Consumer Electronics", "Hair", "Home Improvement", "Home", "Jewelry", "Kids & Babies", "Men's Fashion", "Office", "Outdoor, Fun & Sports", "Pet", "Phones & Telecommunications", "Security", "Shoes", "Tools", "Toys", "Watches", "Women's Fashion"],
         'Coll': ["Appliances", "Automobiles_n_Motorcycles", "Bags", "Beauty_n_Health", "Computer", "Consumer_Electronics", "Hair", "Home_Improvement", "Home", "Jewelry", "Kids_n_Babies", "Mens_Fashion",  "Office", "Outdoor_Fun_n_Sports",  "Pet", "Phones_n_Telecommunications", "Security", "Shoes", "Tools", "Toys", "Watches", "Womens_Fashion"]}

df_coll = pd.DataFrame(colls)
# Import e-commerce data
option_df = st.sidebar.selectbox(
    'Choose the product category', df_coll['Name'])


def read_collection(user, passwd, dbname, collname):
    conn = Connection(username=user, password=passwd)
    d_server = conn[dbname]  # ["raw-data"]
    # extracting the Records
    aql_val = "FOR x IN " + collname + " RETURN x"
    valueResult = d_server.AQLQuery(aql_val, rawResults=True, batchSize=4000)
    col_value = {}
    ind_val = 0

    for value in valueResult:
        col_value[ind_val] = value
        ind_val += 1

    return d_server[collname], col_value


df_to_load = df_coll[df_coll['Name'] == option_df]['Coll'].values[0]

db_coll, c_dict = read_collection(
    "admin", "password", "AE_Items", df_to_load)

df = pd.DataFrame.from_dict(c_dict, orient='index')
df.drop(['_key', '_id', '_rev'], axis=1, inplace=True)

# Remove all non-latin characters from the label
df['Title'] = df['Title'].str.replace(r"[^a-zA-Z0-9_\s]+", " ").str.strip()

'''
# Rating prediction tool

This is a tool to perform training and testing of the selected product category.
Once the training has been completed, the accuracy score will be shown.
You could then input your own data to see the rating that would predicted if you had an item in this product category.

'''


def predict(df):
    # Perform normalization of the data
    df_ln = df.copy()

    # Prepare the data for learning by removing variables with non-numerical values
    df_ln.drop(['Title'], axis=1, inplace=True)
    df_ln.drop(['Store'], axis=1, inplace=True)
    df_ln.drop(['URL'], axis=1, inplace=True)
    # Get a data description of the normalized data set
    # st.table(df_ln.describe())

    # Break down the variables into X and Y, with Y being the expected outcome
    normalize = pd.DataFrame(preprocessing.normalize(df_ln))
    X = normalize.iloc[:, [0, 1, 2, 4]].values
    y = normalize.iloc[:, [3]].values

    # Divide the data into 80% for training and 20% for testing
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=0)

    # Initialize the random forrest regressor for training
    rnd_f = RandomForestRegressor(n_estimators=200, random_state=0)

    # Fit the training data into the model for training
    rnd_f.fit(X_train, y_train.ravel())
    # We then perform the prediction using the test data
    pred_y = rnd_f.predict(X_test)

    # Print the prediction score or accuracy
    st.write("Prediction accuracy: " +
             str(round(metrics.r2_score(y_test, pred_y) * 100, 4)) + '%')

    sprice_value = st.text_input('Minimum Price (US $)', 10)
    bprice_value = st.text_input('Maximum Price (US $)', 50)
    sold_value = st.text_input('Items Sold', 100)
    ship_value = st.text_input('Shipping Costs (US $)', 1)

    sample = {'PriceMin': [sprice_value],
              'PriceMax': [bprice_value],
              'Sold': [sold_value],
              'Shipping': [ship_value]}
    df_u = pd.DataFrame(sample)
    pred_u = rnd_f.predict(pd.DataFrame(preprocessing.normalize(df_u)))
    npv = (1 - pred_u[0]) * 5
    st.text("Rating estimate: " + str(round(npv, 2)))


predict(df)

'''
# Product attributes analysis

This section provides typical analysis of the features for the data provided by this category.
We do some basic exploration of the data to view key statistics of the data series, including number of non-missing values, mean, standard deviation, min, max, and quantiles.
'''

if st.checkbox('Show data description'):
    '''
    View the first 10 rows of this dataset.
    '''
    st.write(df.head(10))
    '''
    Get a data description of the dataset for this category.
    '''
    st.write(df.describe())
    '''
    Identify attributes that contain null values
    '''
    st.text(df.isnull().sum())

# Remove the URL field, since we do not need it
df.drop(['URL'], axis=1, inplace=True)

# Correlation analysis between attributes in the data set
df_corr = df.corr().stack().reset_index().rename(
    columns={0: 'correlation', 'level_0': 'Y', 'level_1': 'X'})
df_corr['correlation_label'] = df_corr['correlation'].map('{:.3f}'.format)

if st.checkbox('Show correlation sample'):
    '''
    The pairwise correlation of all attributes in the data set.
    '''
    st.table(df_corr.head())

# Visualize the correlation using a heat map
base = alt.Chart(df_corr).encode(
    x='X:O',
    y='Y:O'
)

# Text layer with correlation labels
# Colors are for easier readability
text = base.mark_text().encode(
    text='correlation_label',
    color=alt.condition(
        alt.datum.correlation > 0.5,
        alt.value('white'),
        alt.value('black')
    )
)

'''
Visualization of the correlation of features using a heat map. The magnitude of correlation between the attributes are strong.
'''
# The correlation heatmap itself
cor_plot = base.mark_rect().encode(
    color='correlation:Q'
)

# The '+' means overlaying the text and rect layer
st.altair_chart(cor_plot + text, use_container_width=True)

'''
Plots showing the distribution of data for each variable.
'''
# Histogram plots of all variables
hist = alt.Chart(df).mark_bar().encode(
    alt.X("Sold:Q", bin=True),
    y='count()',
)
st.altair_chart(hist, use_container_width=True)
hist = alt.Chart(df).mark_bar().encode(
    alt.X("Shipping:Q", bin=True),
    y='count()',
)
st.altair_chart(hist, use_container_width=True)
hist = alt.Chart(df).mark_bar().encode(
    alt.X("Rating:Q", bin=True),
    y='count()',
)
st.altair_chart(hist, use_container_width=True)
hist = alt.Chart(df).mark_bar().encode(
    alt.X("PriceMin:Q", bin=True),
    y='count()',
)
st.altair_chart(hist, use_container_width=True)
hist = alt.Chart(df).mark_bar().encode(
    alt.X("PriceMax:Q", bin=True),
    y='count()',
)
st.altair_chart(hist, use_container_width=True)

'''
Plots showing the density of data for each variable.
'''
# Create a selection that chooses the nearest point & selects based on x-value
density = alt.Chart(df).transform_density(
    'PriceMin',
    as_=['PriceMin', 'density']
).mark_area(
    color='blue'
).encode(
    x="PriceMin:Q",
    y='density:Q',
)
st.altair_chart(density, use_container_width=True)

density = alt.Chart(df).transform_density(
    'PriceMax',
    as_=['PriceMax', 'density']
).mark_area(
    color='orange'
).encode(
    x="PriceMax:Q",
    y='density:Q',
)
st.altair_chart(density, use_container_width=True)

density = alt.Chart(df).transform_density(
    'Sold',
    as_=['Sold', 'density']
).mark_area(
    color='green'
).encode(
    x="Sold:Q",
    y='density:Q',
)
st.altair_chart(density, use_container_width=True)

density = alt.Chart(df).transform_density(
    'Rating',
    as_=['Rating', 'density']
).mark_area(
    color='red'
).encode(
    x="Rating:Q",
    y='density:Q',
)
st.altair_chart(density, use_container_width=True)

density = alt.Chart(df).transform_density(
    'Shipping',
    as_=['Shipping', 'density']
).mark_area(
    color='purple'
).encode(
    x="Shipping:Q",
    y='density:Q',
)
st.altair_chart(density, use_container_width=True)

'''
Lastly, the box plots of the variables to see the outliers (extreme values) and concentration of the data.
'''
# Box plots of all variables
df.plot(kind='box', subplots=True, layout=(3, 2),
        sharex=False, sharey=False, figsize=(10, 10))
st.pyplot()
