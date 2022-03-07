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
# ```{note}
# This course relies on [Poetry](https://python-poetry.org) as package manager. Commands below can might
# slightly differ if you are using a different strategy (e.g., [Pipenv](https://pipenv.pypa.io/en/latest/) or [Conda](https://docs.conda.io/en/latest/), just to mention a few).
# ```
# 
# ```
# poetry shell
# ipython kernel install --name "bda-labs" --user
# ```
# 
# <details>
# The output from above command is a JSON file located under your Jupyter installation. For example: `/path_to_jupyter_installation/kernels/bda-labs/kernel.json`
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
# </details>
# 
# ### Initialize Spark
# 
# We need to do some preparation first. In the next snippet, we will import the [SparkContext](https://spark.apache.org/docs/latest/api/python/reference/api/pyspark.SparkContext.html#pyspark.SparkContext) and [SparkConf](https://spark.apache.org/docs/latest/api/python/reference/api/pyspark.SparkConf.html#pyspark.SparkConf) classes.
# 
# Now we we proceed to create the **configuration** for our application and a **context** which tells Spark how to access the execution environment (local or a cluster). 

# In[1]:


from pyspark import SparkContext, SparkConf

# we use "local" to indicate we're running in local mode
conf = SparkConf().setAppName("intro-to-rdd").setMaster("local")
sc = SparkContext(conf=conf)


# #### SparkConf
#     
# We triggered a couple of actions with the above code. To start with, we created a `SparkConfig` object and chained two important configurations:
#     - The Spark application name.
#     - The URL where the `master node` can be located. **Setting it to `"local"` is a special configuration to indicate we are running on the same host where this code is being executed.**
#     
# **Note**: it is important to notice that Spark runs on a JVM. When a `SparkConf` is created, it will load values from `spark.*` Java system properties. If we make such properties available to the process running Spark, then they would be picked up.
# 
# Let's inspect a couple of common Spark configuration properties:

# In[2]:


print(f"spark.app.name: {conf.get('spark.app.name')}")
print(f"spark.master: {conf.get('spark.master')}")
print(f"spark.home: {conf.get('spark.home')}")


# So far so good. We get the same value we chained to the `SparkConf` object before.
# 
# **Homework/self-research**:
# 
# - Why don't we have a value for `spark.home`?
# - Should we care?
# 
# Should we want to know all the properties available, then the following snippet might help.

# In[3]:


for p in sorted(conf.getAll(), key=lambda p: p[0]):
    print(p)


# #### SparkContext
# 
# `SparkContext` is at the hearth of Spark. It is the main entry point for Spark that representes the connection of the "driver program" to a Spark cluster. **You must get familiarized with it**.
# 
# We can pass several parameters to it, from which two of them are mandatory: `master` and `appName`. In our case, we passed such information wrapped into a `SparkConf` object.
# 
# ```{attention}
# 
# - `SparkContext` is **always** created on the driver and **it is not serialized**. Thus, it cannot be shipped to workers.
# - We can have one `SparkContext` per application at most. Try to run the cell where we created the `SparkContext` and see what happens!
# ```
# 
# 
# ```{note}
# Actually, only one `SparkContext` can be active per JVM. If we want to create a new one, we must call the `stop()` method to our existing `SparkContext` object first.
# ```
# 
# Another consequence of passing a `SparkConf` object to the `SparkContext` constructor is **immutable configuration**. The `SparkConf` object is cloned and can no longer be modified. Let's see it in action:

# In[4]:


# Is our SparkConf object the same we get from SparkContext?
print(f"conf == sc.getConf() --> {conf == sc.getConf()}")


# 
# ### Define an RDD
# 
# Let's start by defining a very simple RDD. We can think of it as data points indicating the recovery days for a certain disease.

# In[5]:


recovery_days_per_disease = [("disease_1", [3, 6, 9, 10]), ("disease_2", [11, 11, 10, 9])]
rdd = sc.parallelize(recovery_days_per_disease)


# Now we can operate on it. For example, we can compute the average.

# In[6]:


rdd.mapValues(lambda x: sum(x) / len(x)).collect()


# ## References
# 
# ```{bibliography}
# :style: unsrt
# :filter: docname in docnames
# ```

# 
