from pyspark.sql import SparkSession
from pyspark.sql.functions import count, sum as spark_sum

spark = SparkSession.builder \
    .appName("HealthcarePatientAnalytics") \
    .getOrCreate()

# Complete HDFS URI
input_path = "hdfs://localhost:9000/healthcare/input/healthcare_visits.csv"
output_path = "hdfs://localhost:9000/healthcare/analytics/patient_analytics"

# Read healthcare data from HDFS
df = spark.read \
    .option("header", "true") \
    .option("inferSchema", "true") \
    .csv(input_path)

print("Healthcare Data:")
df.show()

# Patient-level analytics
patient_analytics = df.groupBy("Patient_ID") \
    .agg(
        count("Visit_ID").alias("Visit_Count"),
        spark_sum("Amount").alias("Total_Amount")
    ) \
    .orderBy("Patient_ID")

print("Patient Analytics:")
patient_analytics.show()

# Write analytics result back to HDFS
patient_analytics.write \
    .mode("overwrite") \
    .option("header", "true") \
    .csv(output_path)

spark.stop()

