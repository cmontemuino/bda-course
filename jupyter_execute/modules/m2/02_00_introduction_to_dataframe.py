#!/usr/bin/env python
# coding: utf-8

# # Introduction to the DataFrame API
# 
# In this section, we will introduce the [DataFrame and Dataset APIs](https://spark.apache.org/docs/latest/sql-programming-guide.html).
# 
# We will use a small subset from the [Record Linkage Comparison Data Set](https://archive.ics.uci.edu/ml/datasets/record+linkage+comparison+patterns), borrowed from UC Irvine Machine Learning Repository. It consists of several CSV files with match scores for patients in a Germany hospital, but we will use only one of them for the sake of simplicity. Please consult {cite:p}`schmidtmann2009evaluation` and {cite:p}`sariyar2011controlling` for more details regarding the data sets and research. 

# ## Setup
# - Setup a `SparkSession` to work with the Dataset and DataFrame API
# - Unzip the `scores.zip` file located under `data` folder.

# In[1]:


from pyspark import SparkContext, SparkConf

conf = SparkConf().setAppName("intro-to-df").setMaster("local")
sc = SparkContext(conf=conf)
# Avoid polluting the console with warning messages
sc.setLogLevel("ERROR")


# ### Create a SparkSession to work with the DataFrame API

# In[2]:


from pyspark.sql import SparkSession

spark = SparkSession(sc)


# ### Unzip the scores file, if it was not done already

# In[3]:


from os import path
scores_zip = path.join("data", "scores.zip")
scores_csv = path.join("data", "scores.csv")

get_ipython().run_line_magic('set_env', 'SCORES_ZIP=$scores_zip')
get_ipython().run_line_magic('set_env', 'SCORES_CSV=$scores_csv')


# In[4]:


get_ipython().run_cell_magic('bash', '', 'command -v unzip >/dev/null 2>&1 || { echo >&2 "unzip command is not installed. Aborting."; exit 1; }\n[[ -f "$SCORES_CSV" ]] && { echo "file data/$SCORES_CSV already exist. Skipping."; exit 0; }\n\n[[ -f "$SCORES_ZIP" ]] || { echo "file data/$SCORES_ZIP does not exist. Aborting."; exit 1; }\n\necho "Unzip file $SCORES_ZIP"\nunzip "$SCORES_ZIP" -d data')


# In[5]:


get_ipython().system(' head "$SCORES_CSV"')


# ## Loading the Scores CSV file into a DataFrame

# ## References
# 
# ```{bibliography}
# :style: unsrt
# :filter: docname in docnames
# ```
