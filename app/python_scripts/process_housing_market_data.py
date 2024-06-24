import os
import json
from pyspark.sql import SparkSession
from pyspark.sql.functions import mean

# Read environment variables
pg_host = os.getenv('DB_HOST')
pg_port = os.getenv('DB_PORT')
pg_database = os.getenv('DB_DATABASE')
pg_user = os.getenv('DB_USERNAME')
pg_password = os.getenv('DB_PASSWORD')
mongo_host = os.getenv('MONGO_HOST')
mongo_port = os.getenv('MONGO_PORT')
mongo_db = os.getenv('MONGO_DB')
mongo_user = os.getenv('MONGO_USER')
mongo_password = os.getenv('MONGO_PASSWORD')

# Initialize Spark session
spark = SparkSession.builder \
    .appName("Housing Market Data Processing") \
    .master(os.getenv('SPARK_MASTER')) \
    .config("spark.mongodb.output.uri", f"mongodb://{mongo_user}:{mongo_password}@{mongo_host}:{mongo_port}/{mongo_db}.safety") \
    .getOrCreate()

# File paths on HDFS
real_estate_path = 'hdfs://namenode:8020/csv_data/france_total_real_estate_sales_2022.csv'
cartography_path = 'hdfs://namenode:8020/csv_data/france_cartography_data.csv'
schools_path = 'hdfs://namenode:8020/csv_data/france_school_data.csv'
safety_path = 'hdfs://namenode:8020/csv_data/france_safety_rate_data.csv'

# Read CSV files
real_estate_df = spark.read.csv(real_estate_path, header=True, inferSchema=True)
cartography_df = spark.read.csv(cartography_path, header=True, inferSchema=True)
schools_df = spark.read.csv(schools_path, header=True, inferSchema=True)
safety_df = spark.read.csv(safety_path, header=True, inferSchema=True)

# Process and transform data
avg_cost_df = real_estate_df.groupBy("Commune").agg(mean("Valeur fonciere").alias("average_cost"))
school_count_df = schools_df.groupBy("nom_commune").count().withColumnRenamed("count", "school_count")
safety_rate_df = safety_df.groupBy("nom_commune").agg(mean("tauxpourmille").alias("safety_rate"))

# Save to PostgreSQL
real_estate_df.write \
    .format("jdbc") \
    .option("url", f"jdbc:postgresql://{pg_host}:{pg_port}/{pg_database}") \
    .option("dbtable", "real_estate") \
    .option("user", pg_user) \
    .option("password", pg_password) \
    .save()

schools_df.write \
    .format("jdbc") \
    .option("url", f"jdbc:postgresql://{pg_host}:{pg_port}/{pg_database}") \
    .option("dbtable", "schools") \
    .option("user", pg_user) \
    .option("password", pg_password) \
    .save()

cartography_df.write \
    .format("jdbc") \
    .option("url", f"jdbc:postgresql://{pg_host}:{pg_port}/{pg_database}") \
    .option("dbtable", "cartography") \
    .option("user", pg_user) \
    .option("password", pg_password) \
    .save()

# Save to MongoDB
safety_df.write \
    .format("mongo") \
    .mode("overwrite") \
    .option("database", mongo_db) \
    .option("collection", "safety") \
    .save()

# Print JSON output
print(json.dumps({
    "status": "success",
    "message": "Data processing completed successfully."
}))

spark.stop()
