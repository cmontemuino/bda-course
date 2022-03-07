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


# In[3]:


help(SparkSession)


# ### Unzip the scores file, if it was not done already

# In[4]:


from os import path
scores_zip = path.join("data", "scores.zip")
scores_csv = path.join("data", "scores.csv")

get_ipython().run_line_magic('set_env', 'SCORES_ZIP=$scores_zip')
get_ipython().run_line_magic('set_env', 'SCORES_CSV=$scores_csv')


# In[5]:


get_ipython().run_cell_magic('bash', '', 'command -v unzip >/dev/null 2>&1 || { echo >&2 "unzip command is not installed. Aborting."; exit 1; }\n[[ -f "$SCORES_CSV" ]] && { echo "file data/$SCORES_CSV already exist. Skipping."; exit 0; }\n\n[[ -f "$SCORES_ZIP" ]] || { echo "file data/$SCORES_ZIP does not exist. Aborting."; exit 1; }\n\necho "Unzip file $SCORES_ZIP"\nunzip "$SCORES_ZIP" -d data')


# In[6]:


get_ipython().system(' head "$SCORES_CSV"')


# ## Loading the Scores CSV file into a DataFrame

# We are going to use the Reader API

# In[7]:


help(spark.read)


# In[8]:


help(spark.read.csv)


# In[9]:


scores = spark.read.csv(scores_csv)


# In[10]:


scores


# In[11]:


help(scores.show)


# We can look at the head of the DataFrame calling the `show` method.

# scores.show()

# **Can anyone spot what's wrong with the above data?**
# 
# - Question marks
# - Column names
# - `Float` and `Int` in the same column
# 
# Let's check the schema of our DataFrame

# In[12]:


help(scores.printSchema)


# In[13]:


scores.printSchema()


# **Why everythin is a `String`?**

# ### Managing Schema and Null Values

# In[14]:


scores_df = (
    spark.read
        .option("header", "true")
        .option("nullValue", "?")
        .option("inferSchema", "true")
        .csv(scores_csv)
)


# In[15]:


scores_df.printSchema()


# In[16]:


scores_df.show(5)


# ## Transformations and Actions
# 
# Creating a DataFrame does not cause any distributed computation in the cluster. **A DataFrame is un data set representing an intermediate step in a computation**.
# 
# For operatring data (in a distributed manner), we have two type of operations: **transformations** and **actions**:
# 
# - Transformations: lazy evaluation. They're not computed immediately, but they are recorded as a **lineage** for query play optimization.
# - Actions: distributed computation occurs after invoking an action

# In[17]:


# how many?
scores_df.count()


# We can use the `collect` action to return `Array` with all the `Row` objects in our DataFrame.

# In[18]:


scores_df.collect()


# **The `Array` will reside in local memory!!**

# ## Write to Disk
# 
# We are going to save the DataFrame into a different format: Parquet

# In[19]:


scores_df.write.format("parquet").save("data/scores-parquet")


# In[20]:


get_ipython().system(' ls data/scores-parquet')


# In[21]:


scores_parquet = spark.read.parquet("data/scores-parquet")


# In[22]:


scores_parquet.printSchema()


# In[23]:


scores_parquet.show(5)


# ## Analyzing Data
# 
# All good for now, but we don't load data for the sake of i, we do it because we want to run some analysis.
# 
# - First two column are Integer IDs. There represent the patients that were matched in the record.
# - The next nine column are numeric values (int and double). They represnt match scores on different fields, such name, sex, birthday, and locations.
# - The last column is a boolean value indicating whether or not the pair of patient records represented by the line was a match.
# 
# **We could use this dataset to build a simple classifier that allows us to predict whether a record will be a match based on the values of the match scores for patient records.**

# ### Caching
# 
# Each time we process data (e.g., calling the `collect` method), Spark re-opens the file, parsea the rows, and then execute the requested action. It does not matter if we have filtered the data and created a smaller set of record.
# 
# We can use the `cache` method to indicate to store the DataFrame in memory.

# In[24]:


help(scores_df.cache)


# **Spark is in-memory only. Myth or misconception?**
# 
# "Spill"
# Storage levels:
# - `MEMORY_AND_DISK`
# - `MEMORY`
# - `MEMORY_SER`

# In[25]:


scores_cached = scores_df.cache()


# In[26]:


scores_cached.count()


# In[27]:


scores_cached.take(10)


# ### Query Plan

# In[28]:


scores_cached.explain()


# ### GroupBy + OrderBy

# In[29]:


from pyspark.sql.functions import col

scores_cached.groupBy("is_match").count().orderBy(col("count").desc()).show()


# ## Aggregation Functions
# 
# In addition to `count`, we can also compute more complex aggregation like sums, mins, maxes, means, and standard deviation. How? we use `agg` method of the DataFrame API.

# In[30]:


from pyspark.sql.functions import avg, stddev


# In[31]:


aggregated = scores_cached.agg(avg("cmp_sex"), stddev("cmp_sex"))


# In[32]:


aggregated.explain()


# In[33]:


aggregated.show()


# ## SQL
# 
# ANSI 2003-compliant version or HiveQL.

# In[34]:


scores_df.createOrReplaceTempView("scores")


# In[35]:


# scores_cached.groupBy("is_match").count().orderBy(col("count").desc()).show()
spark.sql("""
    SELECT is_match, COUNT(*) cnt
    FROM scores
    GROUP BY is_match
    ORDER BY cnt DESC
""").show()


# In[36]:


spark.sql("""
    SELECT is_match, COUNT(*) cnt
    FROM scores
    GROUP BY is_match
    ORDER BY cnt DESC
""").explain()


# In[37]:


scores_cached.groupBy("is_match").count().orderBy(col("count").desc()).explain()


# ### Should I use Spark SQL or the DataFrame API
# 
# Depends on the query. 

# ## Pandas is my friend!
# 
# required packages: `pandas` and `numpy`
# - poetry add pandas numpy
# - pip install pandas numpy

# In[38]:


scores_pandas = scores_df.toPandas()


# In[39]:


scores_pandas.head()


# In[40]:


scores_pandas.shape


# In[ ]:





# In[ ]:





# ## References
# 
# ```{bibliography}
# :style: unsrt
# :filter: docname in docnames
# ```
