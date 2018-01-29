
# coding: utf-8

# # Capstone 2: Biodiversity Project

# # Introduction
# You are a biodiversity analyst working for the National Parks Service.  You're going to help them analyze some data about species at various national parks.
# 
# Note: The data that you'll be working with for this project is *inspired* by real data, but is mostly fictional.

# # Step 1
# Import the modules that you'll be using in this assignment:
# - `from matplotlib import pyplot as plt`
# - `import pandas as pd`

# In[64]:


# import statements
from matplotlib import pyplot as plt
import pandas as pd


# # Step 2
# You have been given two CSV files. `species_info.csv` with data about different species in our National Parks, including:
# - The scientific name of each species
# - The common names of each species
# - The species conservation status
# 
# Load the dataset and inspect it:
# - Load `species_info.csv` into a DataFrame called `species`

# In[65]:


#load data from csv file into a pandas dataframe.
species = pd.read_csv('species_info.csv')


# Inspect each DataFrame using `.head()`.

# In[66]:


#inspect the species dataframe to find out column names and data types.
species.head(10)


# # Step 3
# Let's start by learning a bit more about our data.  Answer each of the following questions.

# How many different species are in the `species` DataFrame?

# In[67]:


# Find the number of unique scientific names.
species['scientific_name'].nunique()


# In[68]:


# Find the number of unique category names.
species['category'].nunique()


# In[69]:


# Find the number of unique common names.
species['common_names'].nunique()


# In[70]:


# Find the number of unique conservation status levels.
species['conservation_status'].nunique()


# What are the different values of `category` in `species`?

# In[71]:


# Find the different values for the category column.
species['category'].unique()


# What are the different values of `conservation_status`?

# In[72]:


# Find the different conservation levels.
species['conservation_status'].unique()


# In[73]:


# Count the number of species at each conservation level.
# Notice that we do not get a count of nan values.
species.groupby('conservation_status').scientific_name.count().reset_index()


# In[74]:


# Check the values in above table.
endangered_count = len(species[species.conservation_status == 'Endangered'])
print 'endangered', endangered_count
in_recovery_count = len(species[species.conservation_status == 'In Recovery'])
print 'in recovery', in_recovery_count
species_of_concern_count = len(species[species.conservation_status == 'Species of Concern'])
print 'species of concern', species_of_concern_count
threatened_count = len(species[species.conservation_status == 'Threatened'])
print 'threatened', threatened_count
isnot_null = endangered_count + in_recovery_count + species_of_concern_count + threatened_count
print 'count of protected species', isnot_null

nan_count = len(species[species.conservation_status == 'None'])
print 'no intervention (nan)', nan_count


# In[75]:


# get information regarding the species dataframe.
species.info()


# As we saw before, there are far more than 200 species in the `species` table.  Clearly, only a small number of them are categorized as needing some sort of protection.  The rest have `conservation_status` equal to `None`.  Because `groupby` does not include `None`, we will need to fill in the null values.  We can do this using `.fillna`.  We pass in however we want to fill in our `None` values as an argument.
# 
# Paste the following code and run it to see replace `None` with `No Intervention`:
# ```python
# species.fillna('No Intervention', inplace=True)
# ```

# In[76]:


# Use the .fillna method to replace the null values in the conservation status to 'No Intervention'.
species.fillna('No Intervention', inplace=True)


# Great! Now run the same `groupby` as before to see how many species require `No Protection`.

# In[77]:


# After replacing the null values using .fillna('No Intervention', inplace=True)
# we get a count of null values.
species.groupby('conservation_status').scientific_name.count().reset_index()


# In[78]:


# instead of using .count(), we are repeating the count using .nunique 
# because some scientific names are repeated.
species.groupby('conservation_status').scientific_name.nunique().reset_index()


# Let's use `plt.bar` to create a bar chart.  First, let's sort the columns by how many species are in each categories.  We can do this using `.sort_values`.  We use the the keyword `by` to indicate which column we want to sort by.
# 
# Paste the following code and run it to create a new DataFrame called `protection_counts`, which is sorted by `scientific_name`:
# ```python
# protection_counts = species.groupby('conservation_status')\
#     .scientific_name.count().reset_index()\
#     .sort_values(by='scientific_name')
# ```

# In[79]:


# We sort our list in ascending order with the largest value at the bottom of the list.
# To sort, we use .sort_values(by='columnName')
# We use .count() not .nunique()

protection_counts = species.groupby('conservation_status')    .scientific_name.count().reset_index()    .sort_values(by='scientific_name')
protection_counts


# Now let's create a bar chart!
# 1. Start by creating a wide figure with `figsize=(10, 4)`
# 1. Start by creating an axes object called `ax` using `plt.subplot`.
# 2. Create a bar chart whose heights are equal to `scientific_name` column of `protection_counts`.
# 3. Create an x-tick for each of the bars.
# 4. Label each x-tick with the label from `conservation_status` in `protection_counts`
# 5. Label the y-axis `Number of Species`
# 6. Title the graph `Conservation Status by Species`
# 7. Plot the grap using `plt.show()`

# In[80]:


# Use matplotlib to create a bar chart indicating the number of species
# at each intervention level.
plt.close('all')
plt.figure()
plt.figure(figsize=(10,4))
plt.ylabel('Number of Species')
plt.title('Conservation Status by Species')
ax = plt.subplot()
plt.bar(range(len(protection_counts)),       protection_counts.scientific_name.values)
ax.set_xticks(range(len(protection_counts)))
ax.set_xticklabels(protection_counts.conservation_status.values)
ax.set_yticks([0, 1000, 2000, 3000, 4000, 5000, 6000, 7000])
ax.set_yticklabels(['0', '1000', '2000', '3000', '4000', '5000', '6000', '7000'])
plt.show()


# # Step 4
# Are certain types of species more likely to be endangered?

# Let's create a new column in `species` called `is_protected`, which is `True` if `conservation_status` is not equal to `No Intervention`, and `False` otherwise.

# In[81]:


# create a new column in the species dataframe.
species['is_protected'] = species.conservation_status.apply(lambda x: True if x != 'No Intervention' else False)


# In[82]:


species.info()


# Let's group by *both* `category` and `is_protected`.  Save your results to `category_counts`.

# In[83]:


# create a new dataframe from data in the species dataframe.
category_count = species.groupby(['category', 'is_protected']).scientific_name.nunique().reset_index()


# In[84]:


category_count.info()


# Examine `category_count` using `head()`.

# In[85]:


# View the new category_count dataframe.
category_count


# It's going to be easier to view this data if we pivot it.  Using `pivot`, rearange `category_counts` so that:
# - `columns` is `conservation_status`
# - `index` is `category`
# - `values` is `scientific_name`
# 
# Save your pivoted data to `category_pivot`. Remember to `reset_index()` at the end.

# In[86]:


# create a pivot table from the category_count dataframe.
category_pivot = category_count.pivot(columns='is_protected', index='category', values='scientific_name').reset_index()


# Examine `category_pivot`.

# In[87]:


# view the pivot table.
category_pivot


# In[88]:


# rename the columns of the pivot table.
category_pivot.columns = ['category', 'not_protected', 'protected']


# In[89]:


# view the category_pivot table.
category_pivot


# In[90]:


# create a new column for the category_pivot table which 
# adds the values in the protected and not protected columns.
category_pivot['totals'] = category_pivot['not_protected'] + category_pivot['protected']
category_pivot


# In[91]:


# create a new column which presents the percent of species protected for each category.
category_pivot['percent_protected'] = category_pivot['protected'] / (category_pivot['not_protected'] + category_pivot['protected'])


# In[92]:


# View the category pivot table with the new columns totals and percent protected.
category_pivot


# In[93]:


# sort category_pivot by percent protected in ascending order.
sorted_category_pivot = category_pivot.sort_values(by='percent_protected')
sorted_category_pivot


# In[94]:


# check the numbers in the total column.
# discrepancies may be a result of same name being used multiple times.
vascular_plant_count = len(species[species.category == 'Vascular Plant'])
print 'vascular plant count', vascular_plant_count
nonvascular_plant_count = len(species[species.category == 'Nonvascular Plant'])
print 'nonvascular plant count', nonvascular_plant_count
mammal_count = len(species[species.category == 'Mammal'])
print 'mammal count', mammal_count
bird_count = len(species[species.category == 'Bird'])
print 'bird count', bird_count
reptile_count = len(species[species.category == 'Reptile'])
print 'reptile count', reptile_count
amphibian_count = len(species[species.category == 'Amphibian'])
print 'amphibian count', amphibian_count
fish_count = len(species[species.category == 'Fish'])
print 'fish count', fish_count


# It looks like species in category `Mammal` are more likely to be endangered than species in `Bird`.  We're going to do a significance test to see if this statement is true.  Before you do the significance test, consider the following questions:
# - Is the data numerical or categorical?
# - How many pieces of data are you comparing?

# Based on those answers, you should choose to do a *chi squared test*.  In order to run a chi squared test, we'll need to create a contingency table.  Our contingency table should look like this:
# 
# ||protected|not protected|
# |-|-|-|
# |Mammal|?|?|
# |Bird|?|?|
# 
# Create a table called `contingency` and fill it in with the correct numbers

# In[95]:


# Mammal and bird contingency table.
contingency = [[30, 146], [75, 413]]


# In order to perform our chi square test, we'll need to import the correct function from scipy.  Past the following code and run it:
# ```py
# from scipy.stats import chi2_contingency
# ```

# In[96]:


# import statement.
from scipy.stats import chi2_contingency


# Now run `chi2_contingency` with `contingency`.

# In[97]:


# run the chi2_contingency test using the mammal and bird contingency table.
chi2_contingency(contingency)


# It looks like this difference isn't significant!
# 
# Let's test another.  Is the difference between `Reptile` and `Mammal` significant?

# In[98]:


# reptile and mammal contingency table.
rep_mam_contingency = [[5, 73], [30, 146]]


# In[99]:


# run the chi2_contingency test using the reptile and mammal contingency table.
chi2_contingency(rep_mam_contingency)


# Yes! It looks like there is a significant difference between `Reptile` and `Mammal`!

# In[100]:


# create and run chi2 _contingency test
# contingency table uses the protected, not protected numbers for members of Group A:
# Vascular Plants
# Nonvascular Plants
# Reptiles
groupA_contingency = [[46, 4216], [5, 328], [5, 73]]
chi_GroupA, pVal_GroupA, dof_GroupA, expected_GroupA = chi2_contingency(groupA_contingency)
print 'p-value Group A', pVal_GroupA
if pVal_GroupA < 0.05:
    print 'The pvalue is less than 0.05 We have to reject the Null Hypothesis.'
    print 'Variation in protection rates is statistically significant.'
else:
    print 'The pvalue is greater than 0.05. We have to accept the Null Hypothesis.'
    print 'The variation in protection rates is due to random chance.'


# In[101]:


# create a contingency table and run chi2_contingency test
#Group B: Amphibian, Fish, Bird, Mammal
groupB_contingency = [[7, 72], [11, 115], [75, 413], [30, 146]]
chi_GroupB, pVal_GroupB, dof_GroupB, expected_GroupB = chi2_contingency(groupB_contingency)
print 'The p-value for Group B is : ', pVal_GroupB
if pVal_GroupB < 0.05:
    print 'Since the p-value for this test is less than 0.05, we have to reject the Null Hypothesis.'
    print 'Variation in protection rates is statistically significant.'
else:
    print 'The pvalue is greater than 0.05. We have to accept the Null Hypothesis.'
    print 'The variation in protection rates is due to random chance.'


# In[102]:


# Run a chi2_contingency test on all the members of Group A and Group B.
combined = [[7, 72], [11, 115], [75, 413], [30, 146], [46, 4216], [5, 328], [5, 73]]
combined_chi, combined_pval, combined_dof, combined_expected = chi2_contingency(combined)
print 'the p-value is ', combined_pval
if combined_pval < 0.05:
    print 'Since the p-value for this test is less than 0.05, we have to reject the Null Hypothesis.'
    print 'Variation in protection rates is statistically significant.'
else:
    print 'The pvalue is greater than 0.05. We have to accept the Null Hypothesis.'
    print 'The variation in protection rates is due to random chance.'


# In[103]:


# Run a chi2_contingency test on members of Group B.
fish_bird = [[11, 115], [75, 413]]
chi2_contingency(fish_bird)


# In[104]:


# Run chi2_contingency on members of Group A
vascular_nonvascular = [ [46, 4216], [5, 328]]
chi2_contingency(vascular_nonvascular)


# In[105]:


# Run chi2_contingecy on members of Group A.
nonvascular_reptile = [ [5, 328], [5, 73]]
chi2_contingency(nonvascular_reptile)


# # Step 5

# Conservationists have been recording sightings of different species at several national parks for the past 7 days.  They've saved sent you their observations in a file called `observations.csv`.  Load `observations.csv` into a variable called `observations`, then use `head` to view the data.

# In[106]:


# create and load data from a csv file into a pandas dataframe.
observations = pd.read_csv('observations.csv')


# In[107]:


# inspect the observations dataframe.
observations.head()


# Some scientists are studying the number of sheep sightings at different national parks.  There are several different scientific names for different types of sheep.  We'd like to know which rows of `species` are referring to sheep.  Notice that the following code will tell us whether or not a word occurs in a string:

# In[108]:


# get information regarding the observations dataframe.
observations.info()


# In[109]:


# Does "Sheep" occur in this string?
str1 = 'This string contains Sheep'
'Sheep' in str1


# In[110]:


# Does "Sheep" occur in this string?
str2 = 'This string contains Cows'
'Sheep' in str2


# Use `apply` and a `lambda` function to create a new column in `species` called `is_sheep` which is `True` if the `common_names` contains `'Sheep'`, and `False` otherwise.

# In[111]:


# create a new column in the species dataframe
species['is_sheep'] = species.common_names.apply(lambda commonName: True if 'Sheep' in commonName else False)


# Select the rows of `species` where `is_sheep` is `True` and examine the results.

# In[112]:


# selects all records from the species dataframe where the column 'is_sheep' has a true value. 
# not useful because plant names which have sheep in it are also included.
species[species.is_sheep == True]


# Many of the results are actually plants.  Select the rows of `species` where `is_sheep` is `True` and `category` is `Mammal`.  Save the results to the variable `sheep_species`.

# In[113]:


# create a new datafram called sheep_species which pull records from the species 
# dataframe where two conditions have to be met:
# the is_sheep column must be true and the category column has to be mammal.
sheep_species = species[(species.is_sheep == True) & (species.category == 'Mammal') ]


# Now merge `sheep_species` with `observations` to get a DataFrame with observations of sheep.  Save this DataFrame as `sheep_observations`.

# In[114]:


# view the sheep species dataframe to find the names of all
# sheep species in the national parks.
sheep_species


# In[115]:


# view the species dataframe.
species


# In[116]:


# create a new sheep_observations dataframe which merges sheep_species with observations.
sheep_observations = pd.merge(sheep_species, observations)
sheep_observations


# How many total sheep observations (across all three species) were made at each national park?  Use `groupby` to get the `sum` of `observations` for each `park_name`.  Save your answer to `obs_by_park`.
# 
# This is the total number of sheep observed in each park over the past 7 days.

# In[117]:


# create a dataframe which lists observation counts by sheep species and national park.
obs_by_park = sheep_observations.groupby(['park_name', 'scientific_name']).observations.sum().reset_index()
obs_by_park


# In[118]:


# create a pivot table which organizes sheep count by sheep species (column) and park name (rows).
park_obs_pivot = obs_by_park.pivot(columns='scientific_name', index='park_name', values='observations')
park_obs_pivot


# In[119]:


# adds a totals column to the park_obs_pivot table.
park_obs_pivot['totals'] = park_obs_pivot['Ovis aries'] + park_obs_pivot['Ovis canadensis'] + park_obs_pivot['Ovis canadensis sierrae']
park_obs_pivot


# In[120]:


# create a bar chart using matplotlib
# captures sheep population totals at each national park.

plt.close('all')
plt.figure()
plt.figure(figsize=(16, 6))
plt.title('Sheep Counts at Parks')
plt.ylabel('Number of Sheep')
plt.xlabel('Parks')
parks = ['Bryce National Park', 'Great Smoky Mountains National Park', 'Yellowstone National Park', 'Yosemite National Park']
sheep_totals = park_obs_pivot.totals.values
ax = plt.subplot()
plt.bar(range(len(parks)), sheep_totals)
ax.set_xticks(range(len(parks)))
ax.set_xticklabels(parks)
ax.set_yticks([0, 100, 200, 300, 400, 500, 600, 700])
ax.set_yticklabels(['0', '100', '200', '300', '400', '500', '600', '700'])
plt.show()


# Create a bar chart showing the different number of observations per week at each park.
# 
# 1. Start by creating a wide figure with `figsize=(16, 4)`
# 1. Start by creating an axes object called `ax` using `plt.subplot`.
# 2. Create a bar chart whose heights are equal to `observations` column of `obs_by_park`.
# 3. Create an x-tick for each of the bars.
# 4. Label each x-tick with the label from `park_name` in `obs_by_park`
# 5. Label the y-axis `Number of Observations`
# 6. Title the graph `Observations of Sheep per Week`
# 7. Plot the grap using `plt.show()`

# In[121]:


# play with different x-tick values to create grouped bars bar chart.
xtick_values = [3 * x + 2 * 0.80 for x in range(4)]
xtick_values


# In[122]:


# Create a grouped bars bar chart to document sheep populations by 
# species at each national park.


# t = total number of bars in each set -- here we have three species of sheep we are studying - ie 3 datasets
# w = width of bar
# n = number of bar in set of bars, series of bars at each location
# d = number of parks
def create_x(t, w, n, d):
    return [t*x + w*n for x in range(d)]


parks = ['Bryce National Park', 'Great Smoky Mountains National Park', 'Yellowstone National Park', 'Yosemite National Park']
ovis_aries = [119, 76, 221, 126]
ovis_canadensis = [109, 48, 219, 117]
ovis_canadensis_sierrae = [22, 25, 67, 39]

ovis_aries_xvalues = create_x(3, 0.80, 1, 4)
ovis_canadensis_xvalues = create_x(3, 0.80, 2, 4)
ovis_canadensis_sierrae_xvalues = create_x(3, 0.80, 3, 4)

xtick_values = [3 * x + 2 * 0.80 for x in range(4)]

plt.close('all')
plt.figure()
plt.figure(figsize=(16, 6))
ax = plt.subplot()
plt.title('Sheep Species Counts at Parks')
plt.ylabel('Number of Sheep')
plt.xlabel('Parks')
plt.bar(ovis_aries_xvalues, ovis_aries, label='Ovis aries', align='center')
plt.bar(ovis_canadensis_xvalues, ovis_canadensis, label='Ovis canadensis', align='center')
plt.bar(ovis_canadensis_sierrae_xvalues, ovis_canadensis_sierrae, label='Ovis canadensis sierrae', align='center')
plt.legend()
ax.set_xticks(xtick_values)
ax.set_xticklabels(parks)
ax.set_yticks([0, 50, 100, 150, 200, 250, 300])
ax.set_yticklabels(['0', '50', '100', '150', '200', '250', '300'])



plt.show()


# Our scientists know that 15% of sheep at Bryce National Park have foot and mouth disease.  Park rangers at Yellowstone National Park have been running a program to reduce the rate of foot and mouth disease at that park.  The scientists want to test whether or not this program is working.  They want to be able to detect reductions of at least 5 percentage point.  For instance, if 10% of sheep in Yellowstone have foot and mouth disease, they'd like to be able to know this, with confidence.
# 
# Use the sample size calculator at <a href="https://www.optimizely.com/sample-size-calculator/">Optimizely</a> to calculate the number of sheep that they would need to observe from each park.  Use the default level of significance (90%).
# 
# Remember that "Minimum Detectable Effect" is a percent of the baseline.

# In[123]:


# current baseline conversion is 15%
current_baseline = 15 
# desired conversion is 10%
desired_conversion = 10
# we wish to use a statistical significance of 90%
statistical_significance = 90
# lift = 100 * (new - old) / old
# lift = 100 * (.10 - .15) / .15
# lift = -33.33333% we want a negative lift -- we want to see a reduction 
# lift is 33.33333% rounded to 33%
lift_1 = 33 
lift_2 = 33.3333
sample_size_33 = 520
sample_size_33_3 = 510


# How many weeks would you need to observe sheep at Bryce National Park in order to observe enough sheep?  How many weeks would you need to observe at Yellowstone National Park to observe enough sheep?

# In[124]:


# There are 507 sheep at Yellowstone National Park.
# We require a sample of 520
# 520 / 507 = 1.02
# 510 / 507 = 1.00
# We need approximately 1 week to complete the observation at Yellowstone National Park.
yellowstone_survey = 1
# There are 250 sheep at Yellowstone National Park.
# We require a sample of 520 with lift 33%
# 520 / 250 = 2.08
# We need a sample of 510 with lift 33.33%
# 510 / 250 = 2.04
# We need approximately 2 weeks to complete the observation at Bryce National Park.
bryce_survey = 2

