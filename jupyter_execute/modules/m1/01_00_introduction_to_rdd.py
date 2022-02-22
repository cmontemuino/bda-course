#!/usr/bin/env python
# coding: utf-8

# # Introduction to RDD
# 
# In this first session, we will introduce what is a [Resilient Distributed Dataset (RDD)](https://databricks.com/glossary/what-is-rdd). Please refer to the original paper for in-depth details
# {cite:p}`zaharia2012resilient`.
# 
# To understand how Spark works, we need to understand the essence of RDD. Long story short, an RDD **represents a fault-tolerant collection of elements partitioned across the nodes of a cluster that can be operated in parallel**. We will chop the last sentence into pieces now.

# ## Processing Logic Expressed as RDD Operations
# 
# We use RDDs to express a certain processic logic we want to apply to a dataset. For example, finding the average number of days required to recover from a certain disease.
# 
# Then, Spark makes its magic to **schedule** and **execute** our data processing logic on a distributed fashion.
# 
# If we look behind the scenes, the Spark runtime requires to determine the order of execution of RDDs, and make sure the execution is fault-tolerant. It uses the following pieces of information for the aforementioned purposes: 
# 
# - Lineage
#   - Dependencies on parent RDDs
# - Fault-tolerance
#   - The partitions that makes the whole dataset: used to execute in **parallel** to speed up the computation with **executors**.
#   - The function for computing all the rows in the dataset: provided by users (i.e., "you"). Each **executor** in the cluster execute this function against each row in each partition.
# 
# With the above information, Spark can reproduce the RDD in case of failure scenarios.

# ## Quick Demo
# 
# ### Prepare a Jupyter Kernel
# 
# You will need to prepare a Jupyter kernel in order to run this notebook on your local environment.
# 
# ```{note} This course relies on [Poetry](https://python-poetry.org) as package manager. Commands below can might
# slightly differ if you are using a different strategy (e.g., [Pipenv](https://pipenv.pypa.io/en/latest/) or [Conda](https://docs.conda.io/en/latest/), just to mention a few).
# ```
# 
# ```
# poetry shell
# ipython kernel install --name "bda-labs" --user
# ```
# 
# The output from above command is a JSON file located under your Jupyter installation. For example: `/path_to_jupyter_installtion/kernels/bda-labs/kernel.json`
# 
# It's content will be similar to the following:
# 
# ```json
# {
#  "argv": [
#   "<some_path_here>/bda-course/.venv/bin/python",
#   "-m",
#   "ipykernel_launcher",
#   "-f",
#   "{connection_file}"
#  ],
#  "display_name": "bda-labs",
#  "language": "python",
#  "metadata": {
#   "debugger": true
#  }
# }
# ```
# 
# ### Initialize Spark
# 
# We need to do some preparation first. In the next snippet, we will import the [SparkContext](https://spark.apache.org/docs/latest/api/python/reference/api/pyspark.SparkContext.html#pyspark.SparkContext) and [SparkConf](https://spark.apache.org/docs/latest/api/python/reference/api/pyspark.SparkConf.html#pyspark.SparkConf) classes.

# In[1]:


from pyspark import SparkContext, SparkConf


# Now we we proceed to create the **configuration** for our application and a **context** which tells Spark how to access the execution environment (local or a cluster). 

# In[2]:


# we use "local" to indicate we're running in local mode
conf = SparkConf().setAppName("into-to-rdd").setMaster("local")
sc = SparkContext(conf=conf)


# ### Define an RDD
# 
# Let's start by defining a very simple RDD. We can think of it as data points indicating the recovery days for a certain disease.

# In[3]:


recovery_days_per_disease = [("disease_1", [3, 6, 9, 10]), ("disease_2", [11, 11, 10, 9])]
rdd = sc.parallelize(recovery_days_per_disease)


# Now we can operate on it. For example, we can compute the average.

# In[4]:


rdd.mapValues(lambda x: sum(x) / len(x)).collect()


# ## References
# 
# ```{bibliography}
# :style: unsrt
# :filter: docname in docnames
# ```

# 
