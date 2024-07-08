# Pyinfusion
---
- Pyinfusion calculates aggregated information about the Infusion and Active Time of Infusion Pumps. It is still under development and is undergoing experimentation. 
- The input to the algorithm is a Spark DataFrame.
- Algorithm output is also a Spark DataFrame.



## How To Use
---

```python
from pyspark.sql import SparkSession
from pyinfuse import infusion_desc

# create spark instance
spark = SparkSession.builder.appName('sample_app').getOrCreate()

# read in the data
data = spark.read.csv(filepath)

# initilaze the package
infusion_inform = infusion_desc(data)

# obtain the infusion time
infusion_time_ = infusion_inform.infusion_time()

```