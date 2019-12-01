#!/usr/bin/env python
# coding: utf-8

# # Imports

# In[1]:


import random

import pandas as pd

import numpy as np

from collections import defaultdict

import matplotlib

import matplotlib.pyplot as plt


# # Functions created for implementing the kMeans 

# #### Create the Euclidean distance 

# In[3]:


def distance_2(vec1, vec2):
    
    if len(vec1) == len(vec2):
        
        if len(vec1) > 1:
            
            add = 0
            
            for i in range(len(vec1)):
                
                add = add + (vec1[i] - vec2[i])**2
                
            return add**(1/2)
        
        else:
            
            return abs(vec1 - vec2)
        
    else:
        
        return "Wrong Input"
    


# #### We will now check the dissimilarity of our clusters. To do that we need to define the variability of every cluster. Meaning the sum of the distances of every element in the cluster from the mean(centroid). 

# In[4]:


def dissimilarity(cluster):
    
    def kmeansreduce(centroid, dictionary):
        
        a = dictionary[centroid] 
    
        if len(a) > 0 :
        
            vector = a[0]
        
            for i in range(1,len(a)):
            
                vector = np.add(vector, a[i])
                        
            return vector
        
        else:
            
            pass
    
    var = []
    
    add = 0
    
    for i in range(len(cluster.keys())):
        
        if len(cluster[i]) > 0:
            
            m = kmeansreduce(i, cluster) / len(cluster[i])
        
            for j in range(len(cluster[i])):
            
                add = add + distance_2(m, cluster[i][j])
            
    return(add)


# #### Compute the sum of the squared distance between data points and all centroids (distance_2).  
# #### Assign each data point to the closest cluster (clusters dictionary).
# #### Compute the centroids for the clusters by taking the average of the all data points that belong to each cluster.(initial centroids)
# #### We define also two functions to show that this algorithm can be done by MapReduce method

# In[5]:


def kmeans(data, k):
    
    def kmeansmap(information, num_centroids, centroids):
        
        clusters = defaultdict(list)
        
        for i in range(num_centroids):
            
            clusters[i] = []

        classes = defaultdict(list)
        
        for i in range(information.shape[0]): 
            
            d = []
            
            for j in range(num_centroids):
                
                d.append(distance_2(information[i,], centroids[j]))
                
            clusters[np.argmin(d,axis=0)].append(information[i,])
            
            classes[i].append(np.argmin(d,axis=0))
            
        return [clusters, classes]
        
        
    def kmeansreduce(centroid, dictionary):
        
        a = dictionary[centroid] 
    
        if len(a) > 0 :
        
            vector = a[0]
        
            for i in range(1,len(a)):
            
                vector = np.add(vector, a[i])
                        
            return vector
        
        else:
            
            pass

            
        # ===================================================================================
        
    initial_centroids = random.sample(list(data), k)

    while True:
        
        dict1 = kmeansmap(data, k, initial_centroids)[0]
        
        dict2 = kmeansmap(data, k, initial_centroids)[1]
        
        dict3 = defaultdict(list)
        
        for i in range(k):
            
            dict3[i] = []
                        
        old_clusters = initial_centroids
        
        for i in range(k):
            
            dict3[i] = kmeansreduce(i, dict1)
            
            if len(dict3[i]) > 0:
                
                initial_centroids[i] =  dict3[i]/len(dict3[i])                       
                
        if old_clusters == initial_centroids:
            
            break
            
    return [dict1, dict2]
    


# # Now we will implement the algorithms and functions to the data
# #### To implement the algorithms we will clean a bit the data

# In[53]:


url = r"C:\Users\HP\Documents\ADM\HW 4\wine.data"

header = ["Class", "Alcohol", "Malic acid", "Ash","Alcalinity of ash", "Magnesium", "Total phenols", "Flavanoids", "Nonflavanoid phenols", 
          "Proanthocyanins", "Color intensity", "Hue", "OD280/OD315 of diluted wines", "Proline"]

data = pd.read_table(url, delimiter = ",", names = header )

data.head(3)


# #### We normalize the values of the DataFrame, so we can measure the distance
# 
# #### Some columns are not saved as floats , so we will have an error normalizing them, so we make them floats and then normalize them

# In[54]:


for col in data.columns[1:]:
    
    if data[col].dtype == 'int64':
        
        data[col] = data[col].astype("float64")
        
for col in data.columns[1:]:
    
    r = (max(data[col]) - min(data[col]))
    
    minimum = min(data[col])
    
    for i in range(len(data[col])):
        
        data[col][i] = (float(data[col][i]) - minimum)/r
        
data.head(3)


# #### We will not test the variable class, since this is the classification we target. So we are going to save it in a file called target and work with the other variables.

# In[55]:


target = data["Class"]

data = data.drop(columns = ["Class"])

data = data.to_numpy()

data


# #### This way the elements of each row are to be taken as a vector

# In[56]:


data[1,]


# #### Now we will implement the kmeans algorithm, with an unknown number of clusters. We will use the elbow method to figure whats the best number of clusters for our data.  We will run the method for up to k = 10 clusters

# In[57]:


elbow = {}

for k in range(1, 11):
    
    best = kmeans(data, k)
    
    for t in range(100):
        
        C = kmeans(data, k)
        
        if dissimilarity(C[0]) < dissimilarity(best[0]):
            
            best = C
            
    elbow[k] = dissimilarity(best[0])


# In[58]:


plt.plot(list(elbow.keys()), list(elbow.values()))


# #### From the previous plot we can figure out what's the best k for me... We will implement the kmeans algorithm for the specific k

# In[60]:


best = kmeans(data, 3)

for t in range(100):
    
    C = kmeans(data, 3)
    
    if dissimilarity(C[0]) < dissimilarity(best[0]):
        
        best = C
        
outcome = []

for i in range(data.shape[0]):
    
    outcome.append(best[1][i][0] + 1)
    


# #### We did the following commands for all the columns, and we observed that two columns/features have a big effect on the clustering of the other features. Here we will show the distribution of the features, when plotted with Magnesium and  Total Phenols

# In[63]:


f, axes = plt.subplots(4,3,figsize=(20,20))

axes[0][0].scatter(data[:, 5], data[:, 1], c=outcome, cmap=matplotlib.colors.ListedColormap(["purple", "blue", "red"]))
axes[0][0].set_xlabel(header[1])

axes[0][1].scatter(data[:, 5], data[:, 2], c=outcome, cmap=matplotlib.colors.ListedColormap(["purple", "blue", "red"]))
axes[0][1].set_xlabel(header[2])

axes[0][2].scatter(data[:, 5], data[:, 3], c=outcome, cmap=matplotlib.colors.ListedColormap(["purple", "blue", "red"]))
axes[0][2].set_xlabel(header[3])

axes[1][0].scatter(data[:, 5], data[:, 4], c=outcome, cmap=matplotlib.colors.ListedColormap(["purple", "blue", "red"]))
axes[1][0].set_xlabel(header[4])

axes[1][1].scatter(data[:, 5], data[:, 6], c=outcome, cmap=matplotlib.colors.ListedColormap(["purple", "blue", "red"]))
axes[1][1].set_xlabel(header[6])

axes[1][2].scatter(data[:, 5], data[:, 7], c=outcome, cmap=matplotlib.colors.ListedColormap(["purple", "blue", "red"]))
axes[1][2].set_xlabel(header[7])

axes[2][0].scatter(data[:, 5], data[:, 8], c=outcome, cmap=matplotlib.colors.ListedColormap(["purple", "blue", "red"]))
axes[2][0].set_xlabel(header[8])

axes[2][1].scatter(data[:, 5], data[:, 9], c=outcome, cmap=matplotlib.colors.ListedColormap(["purple", "blue", "red"]))
axes[2][1].set_xlabel(header[9])

axes[2][2].scatter(data[:, 5], data[:, 10], c=outcome, cmap=matplotlib.colors.ListedColormap(["purple", "blue", "red"]))
axes[2][2].set_xlabel(header[10])

axes[3][0].scatter(data[:, 5], data[:, 11], c=outcome, cmap=matplotlib.colors.ListedColormap(["purple", "blue", "red"]))
axes[3][0].set_xlabel(header[11])

axes[3][1].scatter(data[:, 5], data[:, 12], c=outcome, cmap=matplotlib.colors.ListedColormap(["purple", "blue", "red"]))
axes[3][1].set_xlabel(header[12])

plt.suptitle(header[5])

plt.show()


# In[65]:


f, axes = plt.subplots(4,3,figsize=(20,20))

axes[0][0].scatter(data[:, 6], data[:, 1], c=outcome, cmap=matplotlib.colors.ListedColormap(["purple", "blue", "red"]))
axes[0][0].set_xlabel(header[1])

axes[0][1].scatter(data[:, 6], data[:, 2], c=outcome, cmap=matplotlib.colors.ListedColormap(["purple", "blue", "red"]))
axes[0][1].set_xlabel(header[2])

axes[0][2].scatter(data[:, 6], data[:, 3], c=outcome, cmap=matplotlib.colors.ListedColormap(["purple", "blue", "red"]))
axes[0][2].set_xlabel(header[3])

axes[1][0].scatter(data[:, 6], data[:, 4], c=outcome, cmap=matplotlib.colors.ListedColormap(["purple", "blue", "red"]))
axes[1][0].set_xlabel(header[4])

axes[1][1].scatter(data[:, 6], data[:, 5], c=outcome, cmap=matplotlib.colors.ListedColormap(["purple", "blue", "red"]))
axes[1][1].set_xlabel(header[5])

axes[1][2].scatter(data[:, 6], data[:, 7], c=outcome, cmap=matplotlib.colors.ListedColormap(["purple", "blue", "red"]))
axes[1][2].set_xlabel(header[7])

axes[2][0].scatter(data[:, 6], data[:, 8], c=outcome, cmap=matplotlib.colors.ListedColormap(["purple", "blue", "red"]))
axes[2][0].set_xlabel(header[8])

axes[2][1].scatter(data[:, 6], data[:, 9], c=outcome, cmap=matplotlib.colors.ListedColormap(["purple", "blue", "red"]))
axes[2][1].set_xlabel(header[9])

axes[2][2].scatter(data[:, 6], data[:, 10], c=outcome, cmap=matplotlib.colors.ListedColormap(["purple", "blue", "red"]))
axes[2][2].set_xlabel(header[10])

axes[3][0].scatter(data[:, 6], data[:, 11], c=outcome, cmap=matplotlib.colors.ListedColormap(["purple", "blue", "red"]))
axes[3][0].set_xlabel(header[11])

axes[3][1].scatter(data[:, 6], data[:, 12], c=outcome, cmap=matplotlib.colors.ListedColormap(["purple", "blue", "red"]))
axes[3][1].set_xlabel(header[12])

plt.suptitle(header[6])

plt.show()

