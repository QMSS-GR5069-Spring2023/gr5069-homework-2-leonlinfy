#!/usr/bin/env python
# coding: utf-8

import numpy as np
import pandas as pd

from google.colab import drive
drive.mount('/content/gdrive')
import os
os.chdir('/content/gdrive/MyDrive')


peaks = pd.read_csv("peaks.csv")
expeditions = pd.read_csv("expeditions.csv")
members = pd.read_csv("members.csv")


# ### 1. Peaks
# Answer the following questions using the peaks data only :
# 
# a) What proportion of peaks is still unclimbed? 
# 
# b) What is the average height of the climbed peaks vs. unclimbed peaks?


peaks.head()

unclimbed = peaks[peaks['climbing_status'] == 'Unclimbed']
proportion_of_unclimbed = len(unclimbed) / len (peaks)
print ('a. The proportion is', proportion_of_unclimbed)

climbed = peaks[peaks['climbing_status'] == 'Climbed']
climbed_avg = climbed['height_metres'].mean()
unclimbed_avg = unclimbed['height_metres'].mean()
print ('b. The average height of climbed is', climbed_avg, ', while the unclimbed is', unclimbed_avg)


# ### 2. Sherpas
# Using the members data only, select a subset of all persons who have a Nepalese citizenship.
# 
# a) What proportion of them was hired for the expedition? 
# 
# b) What are their minimum, maximum, and average ages?

members.head()


Nepal = members[members['citizenship'] == 'Nepal']
hire = Nepal [Nepal ['hired'] == True]
proportion_of_hire = len (hire) / len (Nepal)
print ('a. The porportion is', proportion_of_hire)


oldest = hire ['age'].max()
youngest = hire ['age'].min()
average_age = hire ['age'].mean()
print('b. The minimum is', youngest, ', the maximum is', oldest, 'and the average age is', average_age)


# ### 3. Gender
# 
# Now use all three data sets and join them on the provided ID variables. For this question, limit yourself to the subset of non-hired participants.
# 
# a) What is the first record of a woman summitting a peak? Which peak (name and height in meters) was that?
# 
# b) Provide a single cross-tab table of the sex of an expedition participant and
# - the proportion of success in summitting a main peak or sub-peak
# - the proportion of participants using oxygen support - the proportion of participants who died.
# 
# That is, sex should be displayed as the rows of the output and the three requested proportions as its columns.

join1 = pd.merge(peaks, expeditions,
                how = 'left')


join2 = pd.merge(join1, members,
                how = 'left')
join = join2 [join2 ['hired'] == False]
join_female = join[join['sex'] == 'F']


join_female.info()


female_peak = join_female.loc[join_female['year'] == join_female['year'].min(), ['member_id', 'peak_name', 'height_metres']]
print('a. The first record is \n', female_peak)


sex_prop = join.loc[:, ['sex','success','oxygen_used','died']]
print('b. the cross_table is:\n', sex_prop.groupby('sex').mean())


# ### 4.Accidents
# For this question, use the expeditions data only.
# 
# a) Aggregate the data by decade and count the number of expeditions, the total number of expedition members, and the average rates of death for members and 
# hired staff. Briefly describe what you found.
# 
# b) Calculate the length_of_expedition as the time between the basecamp_date and the termination_date in days. Now, standardize these length_of_expedition values to z-values grouped by each peak (that is you need to standardize with the mean and standard deviation of expeditions for the same peak only). Are longer expeditions more or less likely to be associated with death? (no statistical test necessary)

expeditions.head() 

s1900 = expeditions[(expeditions['year'] >= 1900) & (expeditions['year'] < 1910)]
s1910 = expeditions[(expeditions['year'] >= 1910) & (expeditions['year'] < 1920)]
s1920 = expeditions[(expeditions['year'] >= 1920) & (expeditions['year'] < 1930)]
s1930 = expeditions[(expeditions['year'] >= 1930) & (expeditions['year'] < 1940)]
s1940 = expeditions[(expeditions['year'] >= 1940) & (expeditions['year'] < 1950)]
s1950 = expeditions[(expeditions['year'] >= 1950) & (expeditions['year'] < 1960)]
s1960 = expeditions[(expeditions['year'] >= 1960) & (expeditions['year'] < 1970)]
s1970 = expeditions[(expeditions['year'] >= 1970) & (expeditions['year'] < 1980)]
s1980 = expeditions[(expeditions['year'] >= 1980) & (expeditions['year'] < 1990)]
s1990 = expeditions[(expeditions['year'] >= 1990) & (expeditions['year'] < 2000)]
s2000 = expeditions[(expeditions['year'] >= 2000) & (expeditions['year'] < 2010)]
s2010 = expeditions[(expeditions['year'] >= 2010) & (expeditions['year'] < 2020)]


decades = [s1900, s1910, s1920, s1930, s1940, s1950, s1960, s1970, s1980, s1990, s2000, s2010]


s1980.head()

print('a.')
j = 1900
for i in decades:
  
  i_total = len(i)
  print ('For the decades of', j)
  print ('The number of expeditions in', 'is', i_total)
  i_members_sum = i['members'].sum()
  print ('The number of members is', i_members_sum)
  i_members_death = i['member_deaths'].sum() / i_members_sum #question : should the denominator be total pop or just member?
  print ('The average of members_death is', i_members_death)
  i_hired_sum = i['hired_staff'].sum()
  i_hired_death = i['hired_staff_deaths'].sum() / i_hired_sum
  print ('The average of hired_staff_death is', i_hired_death)  #same question as above
  print('\n')
  j=j+10 # move forward the decades

expeditions['termination_date'] = pd.to_datetime(expeditions['termination_date'], errors='coerce')
expeditions['basecamp_date'] = pd.to_datetime(expeditions['basecamp_date'], errors='coerce')


expeditions['length_of_expedition'] = (expeditions['termination_date'] - expeditions['basecamp_date']).dt.days
expeditions_extract = expeditions[['peak_name', 'length_of_expedition']].dropna() # for this question, i cannot find a way to deal with Nan except dropping. I am looking for an auto-fill.
expeditions_extract

expeditions_extract['z_score_length'] = expeditions_extract.groupby('peak_name').transform(lambda x: (x - x.mean()) / x.std())
print('b. the final answer is \n', expeditions_extract)


# Longer expeditions are more likely to be associated with death.
