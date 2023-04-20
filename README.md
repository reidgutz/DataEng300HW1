# DataEng300HW1

How to Run the Code and genrate output?

To run the code in a docker contain run the included bash script 
run.sh in the terminal using the command 

The Dockerfile used to build the container uses an existing python image and then installs additional package requirements located in the requirements.txt file. The requirements.txt, RGHW1.py, Dockerfile, run.sh, and data.csv files should all be in the same directory.

Once the container is built and running, use following command to run the python script
python3 RGHW1.py


Python Script Elements/psuedo code

0. Reading in Data
The data was read in as a pandas dateframe as this is a format that is easy to use and is effective for data cleaning, transformation, visualization, and analysis.

1. Dealing with missing values
To replace missing values in the dataset, we first dropped columns with more than 45% of the data missing. To replace the columns under 45% with missing values, we used the method of mean imputation. Mean imputation works by replacing all missing values in a given column with the mean value of the non missing data in the column. This is an effective method of dealing with missing numerical values and is preferred over methods such as mode imputation since the data is numeric. Mean imputation is effective due to its simplicity, the preservation of the underlying distribution, and the fact that there was enough exisitng data for the mean value we are imputing to be significant.

2. Skewness and transformations

To calculate the skewness we used the Scipy skew function. To transform the non normal numerical data to approximately normal distributions, the boxcox method of transformation was used. When transforming with logs, many of the variables' distributions did not take on a normal shape. Therefore, the boxcox method was used. The boxcox method works by varying an exponential parameter lambda to find an optimal transformation of the distribution. More information on this method can be found here (https://www.statisticshowto.com/probability-and-statistics/normal-distributions/box-cox-transformation/). The variable target did not have a transformation applied to it due to its binary nature. A sample of a transformed distribution for a variable can be seen in Figure 1. 

3. Boxplots

Using the boxplots, outliers were able to be identified. Since most of them appeared to be naturally occuring and did not need to be removed for our analysis, we decided to only remove those that exceeded the 1.5 * IQR limits. This is a very common and effective method of removing outliers. However, for one feature, the count of family members we saw that this method produced 6000+ outliers due to the large amount of 0's that appeared in the data. Therefore, for this feature we only removed outliers above the 1.5*IQR limit and not below. Once the outliers were removed, we plotted boxplots for the income variable and separated by education level. A sample output of this boxplot can be seen in Figure2 . Analyzing and observing this figure, we see that there is overlap in the middle 50% of all 4 levels of education. However, there is an upward trend in the mean income and 75% value as the education level increases. This is an expected result as there are typically higher paying jobs for higher levels of education.

4. Bar Plots

Bar plots were generated to view the relationship between housing type and family status. A sample output of this can be seen in Figure 3. When observing the plots generated, we see that the vast majority of clients have either a house or an apartment. When seperating by family status, we observe that the vast majortiy of these home owners are married. Among all housing types, married is the most commonly listed familty status. However, it is important to note that for the house/apartment housing type, there are still significant contingents of single, widowed, separated, and civil marriage family types.

5. Feature Engineering

To create the new features age, we took the absolute value of the days birth column and divided it by the 365 days in a year and stored it in a new column called age. We then created a new age group column by bucketing the newly created age column using pandas cut function.

We then created a barplot to view the proprtion of applicants across age groups with a target value of 1. Since the data is binary for this column the proportion can be found by just calculating the column mean. Once the data was grouped and plotted, such as in Figure 4, we were able to observe a clear pattern. We observed that as we progressed through the age groups, the proportion of those with a target score of 1 decreased. Therefore, the highest proportion was very young and the lowest was very old. This makes sense as those who are young are more likely to have financial difficulties.

In Figure 5, a more granular version of this analysis can be found as the proportions were separated by gender. In this figure we can see that in all of the groups, men were much more likely to have a target score of 1, which corresponds to a client having payment difficulties. 






