#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd


# In[2]:


from google.colab import drive
drive.mount('/content/gdrive')
import os
os.chdir('/content/gdrive/MyDrive')


# In[3]:


peaks = pd.read_csv("peaks.csv")
expeditions = pd.read_csv("expeditions.csv")
members = pd.read_csv("members.csv")


# ### 1. Peaks
# Answer the following questions using the peaks data only :
# 
# a) What proportion of peaks is still unclimbed? 
# 
# b) What is the average height of the climbed peaks vs. unclimbed peaks?

# In[ ]:


peaks.head()


# In[ ]:


unclimbed = peaks[peaks['climbing_status'] == 'Unclimbed']
proportion_of_unclimbed = len(unclimbed) / len (peaks)
print ('a. The proportion is', proportion_of_unclimbed)


# In[ ]:


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

# In[ ]:


members.head()


# In[ ]:


Nepal = members[members['citizenship'] == 'Nepal']
hire = Nepal [Nepal ['hired'] == True]
proportion_of_hire = len (hire) / len (Nepal)
print ('a. The porportion is', proportion_of_hire)


# In[ ]:


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

# In[10]:


join1 = pd.merge(peaks, expeditions,
                how = 'left')


join2 = pd.merge(join1, members,
                how = 'left')
join = join2 [join2 ['hired'] == False]
join_female = join[join['sex'] == 'F']


join_female.info()


# In[11]:


female_peak = join_female.loc[join_female['year'] == join_female['year'].min(), ['member_id', 'peak_name', 'height_metres']]
print('a. The first record is \n', female_peak)


# In[12]:


sex_prop = join.loc[:, ['sex','success','oxygen_used','died']]
print('b. the cross_table is:\n', sex_prop.groupby('sex').mean())


# ### 4.Accidents
# For this question, use the expeditions data only.
# 
# a) Aggregate the data by decade and count the number of expeditions, the total number of expedition members, and the average rates of death for members and 
# hired staff. Briefly describe what you found.
# 
# b) Calculate the length_of_expedition as the time between the basecamp_date and the termination_date in days. Now, standardize these length_of_expedition values to z-values grouped by each peak (that is you need to standardize with the mean and standard deviation of expeditions for the same peak only). Are longer expeditions more or less likely to be associated with death? (no statistical test necessary)

# In[ ]:


expeditions.head() 


# In[ ]:

# creating new function to avoid using same code over and over
# technically this should be at the top of this file or in another file to pull in
# I can't figure out how to do that without merge conflicts
def split_df_by_year(df, col, year1, year2):
  new_df = df[(df[col] >= year1) & (df[col] < year2)]
  return new_df

# creating empty list to fill with dataframes
decades = []

# creating dictionary to iterate through with decade definitions
years = {'decade1':[1900,1910],
        'decade2':[1910,1920],
        'decade3':[1920,1930],
        'decade4':[1920,1930],
        'decade5':[1930,1940],
        'decade6':[1940,1950],
        'decade7':[1950,1960],
        'decade8':[1960,1970],
        'decade9':[1970,1980],
        'decade10':[1980,1990],
        'decade11':[1990,2000],
        'decade12':[2000,2010],
        'decade13':[2010,2020]}

# iterating through decade dictionary and appending to empty list
for key,value in years.iteritems():
  decade_df = split_df_by_year(expeditions,year,value[0],value[1])
  decades.append(decade_df)


# In[ ]:


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
  


# In[ ]:


expeditions['termination_date'] = pd.to_datetime(expeditions['termination_date'], errors='coerce')
expeditions['basecamp_date'] = pd.to_datetime(expeditions['basecamp_date'], errors='coerce')


# In[ ]:


expeditions['length_of_expedition'] = (expeditions['termination_date'] - expeditions['basecamp_date']).dt.days
expeditions_extract = expeditions[['peak_name', 'length_of_expedition']].dropna() # for this question, i cannot find a way to deal with Nan except dropping. I am looking for an auto-fill.
expeditions_extract


# In[ ]:


expeditions_extract['z_score_length'] = expeditions_extract.groupby('peak_name').transform(lambda x: (x - x.mean()) / x.std())
print('b. the final answer is \n', expeditions_extract)


# Longer expeditions are more likely to be associated with death.
