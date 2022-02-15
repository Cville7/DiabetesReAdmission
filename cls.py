#!/usr/bin/env python
# coding: utf-8

# In[23]:


from sklearn.linear_model import LogisticRegression
import pandas as pd


# In[53]:


data = pd.read_csv('output.csv')
dataDF = pd.DataFrame(data)

attributes = dataDF[dataDF.columns[:43]]
labels = dataDF[dataDF.columns[43]]

lr = LogisticRegression(solver = "sag")
lr.fit(attributes, labels)
probs = lr.predict_proba(attributes)
coefs = lr.coef_


# In[54]:


print(coefs) #Model seems to place significant importance an age range.
            #Increasing age seems to have a net gain towards likelihood of being re-admitted.


# In[50]:


#Averaging Age, removing min/max columns, no cito, no exam.
dataAGE = pd.read_csv('output_nce_age_avg.csv')
dataAGE = pd.DataFrame(dataAGE)

attributesAGE = dataAGE[dataAGE.columns[:42]]
labelsAGE = dataAGE[dataAGE.columns[42]]

lrAGE = LogisticRegression(solver = "sag")
lrAGE.fit(attributesAGE, labelsAGE)
probsAGE = lrAGE.predict_proba(attributesAGE)
coefsAGE = lrAGE.coef_


# In[56]:


print(coefsAGE) #Averaging the age, the model seems to think the range of age is way too important.
                #Model still concludes that an increase in age leads to an increase in readmittance.


# In[59]:


#Removal of all demographical data, no cito, no exam, no race, no gender.
dataND = pd.read_csv('output_no_demos.csv')
dataND = pd.DataFrame(dataND)

attributesND = dataND[dataND.columns[:39]]
labelsND = dataND[dataND.columns[39]]

lrND = LogisticRegression(solver = "sag")
lrND.fit(attributesND, labelsND)
probsND = lrND.predict_proba(attributesND)
coefsND = lrND.coef_


# In[61]:


print(coefsND)


# In[ ]:




