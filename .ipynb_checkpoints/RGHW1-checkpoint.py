#!/usr/bin/env python
# coding: utf-8

# Import the necessary packages


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import skew
from scipy.stats import boxcox

plt.rcParams.update(**{'figure.dpi':150})
plt.style.use('ggplot') # can skip this - plots are more visually appealing with this style


# Read in data as a dataframe using pandas


client_data = pd.read_csv("data.csv")
client_data.head()


# Find percentage of Missing Data in original dataframe


client_missing = (client_data.isnull().sum()/client_data.shape[0]).round(2)
client_missing


# Drop columns with a high proportion of missing data


client_data = client_data.drop(['TOTALAREA_MODE','HOUSETYPE_MODE','EXT_SOURCE_1'], axis = 1)


# Mean Imputation for the numerical values with missing data


amt_req_credit = client_data['AMT_REQ_CREDIT_BUREAU_YEAR'].mean(skipna = True)
client_data['AMT_REQ_CREDIT_BUREAU_YEAR'].fillna(amt_req_credit, inplace=True)
client_missing = (client_data.isnull().sum()/client_data.shape[0])
client_missing


mode_ext_source3 = client_data['EXT_SOURCE_3'].mean(skipna = True)
client_data['EXT_SOURCE_3'].fillna(mode_ext_source3, inplace=True)

mode_ext_source2 = client_data['EXT_SOURCE_2'].mean(skipna = True)
client_data['EXT_SOURCE_2'].fillna(mode_ext_source2, inplace=True)


# Confirm there is no more missing data
client_missing = (client_data.isnull().sum()/client_data.shape[0])


#Calculate Skew for numerical columns



numerical_columns = client_data.select_dtypes(include=['float64','int64'])
skews = numerical_columns.skew()
skews


# Create histograms of numerical columns

for col in numerical_columns:
    plt.hist(client_data[col], bins=10)
    plt.title(col)
    plt.show()

plt.close()

# Transform columns to be more normal

transformationdf = client_data.copy()
for col in numerical_columns:
    if col != 'TARGET':
        fig, ax = plt.subplots()
        transformed,lambda_value = boxcox(abs((client_data[col]+ 1)))
        plt.hist(transformed)
        plt.title(col)
        transformationdf[col] = transformed
        transformationdf[col].skew()
plt.close()

# Calculate skew of transformed numerical columns


numerical_columns = transformationdf.select_dtypes(include=['float64','int64'])
numerical_columns.skew()


# Create boxplots


for col in numerical_columns.columns:
    if col != 'TARGET':
        plt.boxplot(transformationdf[col])
        plt.title(col)
        plt.show()

plt.close()
# Remove outliers using the 1.5*IQR method


for col in numerical_columns.columns:
    if col != 'TARGET':
        q1 = transformationdf[col].quantile(0.25)
        q3 = transformationdf[col].quantile(0.75)
        iqr = q3 - q1
        lower_bound = q1 - 1.5 * iqr
        upper_bound = q3 + 1.5 * iqr
        transformationdf = transformationdf[(transformationdf[col] >= lower_bound) & (transformationdf[col] <= upper_bound)]


# Replot boxplots


for col in numerical_columns.columns:
    if col != 'TARGET':
        plt.boxplot(transformationdf[col])
        plt.title(col)
        plt.show()


# Plot boxplots separated by target


for col in numerical_columns.columns:
    if col != 'TARGET':
        fig, axs = plt.subplots(ncols=2, figsize=(10,5))
        axs[0].boxplot(transformationdf[col][transformationdf['TARGET']==1])
        axs[0].set_title('Boxplot 1 ' + col)
        axs[1].boxplot(transformationdf[col][transformationdf['TARGET']==0])
        axs[1].set_title('Boxplot 0 '+ col)
        plt.show()


# Plot boxplots based on Education type


values = transformationdf['NAME_EDUCATION_TYPE'].values.tolist()
values = list(set(values))
for col in numerical_columns.columns:
    if col == 'AMT_INCOME_TOTAL':
        fig, axs = plt.subplots(ncols=4, figsize=(10,5))
        axs[0].boxplot(transformationdf[col][transformationdf['NAME_EDUCATION_TYPE']== "Lower secondary"])
        axs[0].set_title("Lower secondary")
        axs[1].boxplot(transformationdf[col][transformationdf['NAME_EDUCATION_TYPE']== "Secondary / secondary special"])
        axs[1].set_title("Secondary")
        axs[2].boxplot(transformationdf[col][transformationdf['NAME_EDUCATION_TYPE']==  "Incomplete higher"])
        axs[2].set_title("Incomplete higher")
        axs[3].boxplot(transformationdf[col][transformationdf['NAME_EDUCATION_TYPE']== "Higher education"])
        axs[3].set_title("Higher education")                                     
        plt.show()

plt.close()
# Bar plot based on housing type


counts = client_data['NAME_HOUSING_TYPE'].value_counts()
fig,ax = plt.subplots(figsize = (12,6))
ax.bar(counts.index, counts.values)
ax.set_xlabel('Types')
ax.set_ylabel('Frequency')
plt.show()


# Bar plot based on Housing Type and Family Status


grouped = client_data.groupby(['NAME_FAMILY_STATUS','NAME_HOUSING_TYPE'])['NAME_HOUSING_TYPE'].count().unstack('NAME_FAMILY_STATUS')
fig,ax = plt.subplots(figsize = (12,6))
grouped.plot(kind = "bar", ax=ax)
ax.set_xlabel('Types')
ax.set_title('Housing Type Frequency by Family Status')
ax.set_ylabel('Frequency')
ax.legend(title = 'Family Status')
plt.show()


# Create age and age group columns


client_data['AGE'] = abs(client_data['DAYS_BIRTH']/365)
client_data.head()
bins = [0, 25, 35,60,200] 
labels = ["Very_Young","Young", "Middle_Age","Senior_Citizen"]
client_data['AGE_GROUP'] = pd.cut(client_data['AGE'], bins=bins, labels=labels)


# Plot proportion of age groups with target 1


props = client_data.groupby('AGE_GROUP')['TARGET'].mean()
props.plot.bar()
plt.xlabel("Age Group")
plt.ylabel("Proportion")
plt.title("Proportion of Applicants with Target = 1")


# Plot proportion of age groups with target 1 by gender


props = client_data.groupby(['AGE_GROUP','CODE_GENDER'])['TARGET'].mean().unstack()
props.plot.bar()
plt.xlabel("Age Group")
plt.ylabel("Proportion")
plt.title("Proportion of Applicants with Target = 1")




