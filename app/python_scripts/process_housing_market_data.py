import os
import json
from pyspark.sql import SparkSession
from pyspark.sql.functions import mean, col, to_date

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

# Initialize Spark session with PostgreSQL JDBC driver
spark = SparkSession.builder \
    .appName("Housing Market Data Processing") \
    .master(os.getenv('SPARK_MASTER')) \
    .config("spark.mongodb.output.uri", f"mongodb://{mongo_user}:{mongo_password}@{mongo_host}:{mongo_port}/{mongo_db}.safety") \
    .config("spark.jars", "/var/www/python_scripts/postgresql-42.7.3.jar") \
    .getOrCreate()

# File paths on HDFS
real_estate_path = 'hdfs://namenode:8020/csv_data/france_total_real_estate_sales_2022.csv'
cartography_path = 'hdfs://namenode:8020/csv_data/france_cartography_data.csv'
schools_path = 'hdfs://namenode:8020/csv_data/france_schools_data.csv'
safety_path = 'hdfs://namenode:8020/csv_data/france_safety_rate_data.csv.gz'

# Read CSV files with specified delimiter
real_estate_df = spark.read.csv(real_estate_path, header=True, inferSchema=True, sep=',')
cartography_df = spark.read.csv(cartography_path, header=True, inferSchema=True, sep=',')
schools_df = spark.read.csv(schools_path, header=True, inferSchema=True, sep=';')
safety_df = spark.read.option("header", "true").csv(safety_path, inferSchema=True, sep=';')

# Print the schema of the safety_df and real_estate_df to verify column names
safety_df.printSchema()
cartography_df.printSchema()
real_estate_df.printSchema()

# Clean column names to remove any leading/trailing whitespace and replace special characters
def clean_column_names(df):
    for col_name in df.columns:
        new_col_name = col_name.strip().replace('.', '_').replace(' ', '_')
        df = df.withColumnRenamed(col_name, new_col_name)
    return df

safety_df = clean_column_names(safety_df)
cartography_df = clean_column_names(cartography_df)

# Verify cleaned column names
safety_df.printSchema()
cartography_df.printSchema()

# Join safety data with cartography data to get 'nom_commune'
safety_df = safety_df.join(cartography_df, safety_df['CODGEO_2023'] == cartography_df['code_commune_INSEE'], 'left')

# Process and transform data
avg_cost_df = real_estate_df.groupBy("Commune").agg(mean("Valeur fonciere").alias("average_cost"))
school_count_df = schools_df.groupBy("nom_commune").count().withColumnRenamed("count", "school_count")
safety_rate_df = safety_df.groupBy("nom_commune").agg(mean("tauxpourmille").alias("safety_rate"))

# Convert 'Date mutation' column to date type
real_estate_df = real_estate_df.withColumn("Date mutation", to_date(col("Date mutation"), "dd/MM/yyyy"))

# Ensure the real_estate_df columns match the database schema
real_estate_df = real_estate_df.select(
    col("Date mutation").alias("mutation_date"),
    col("Nature mutation").alias("nature_mutation"),
    col("Valeur fonciere").alias("valeur_fonciere").cast("double"),
    col("No voie").alias("address"),
    col("Code postal").alias("postal_code").cast("int"),
    col("Commune").alias("commune"),
    col("Code departement").alias("department_code"),
    col("Code commune").alias("commune_code"),
    col("Surface reelle bati").alias("surface_reelle_bati"),
    col("Nombre pieces principales").alias("nombre_pieces"),
    col("Surface terrain").alias("surface_terrain")
)

# Rename columns in schools_df to match PostgreSQL table schema
schools_df = schools_df.select(
    col("identifiant_de_l_etablissement").alias("identifiant"),
    col("nom_etablissement"),
    col("type_etablissement"),
    col("statut_public_prive"),
    col("adresse_1").alias("address"),
    col("code_postal").alias("postal_code"),
    col("nom_commune").alias("commune"),
    col("code_departement").alias("department_code"),
    col("code_region").alias("region_code"),
    col("nombre_d_eleves").alias("nombre_eleves").cast("int")
)

# Rename columns in cartography_df to match PostgreSQL table schema
cartography_df = cartography_df.select(
    col("code_commune_INSEE"),
    col("nom_commune_postal"),
    col("code_postal"),
    col("libelle_acheminement"),
    col("latitude").cast("decimal(10,8)"),
    col("longitude").cast("decimal(11,8)"),
    col("nom_region")
)

# Save to PostgreSQL
real_estate_df.write \
    .format("jdbc") \
    .option("url", f"jdbc:postgresql://{pg_host}:{pg_port}/{pg_database}") \
    .option("dbtable", "real_estate") \
    .option("user", pg_user) \
    .option("password", pg_password) \
    .option("driver", "org.postgresql.Driver") \
    .mode("append") \
    .save()

schools_df.write \
    .format("jdbc") \
    .option("url", f"jdbc:postgresql://{pg_host}:{pg_port}/{pg_database}") \
    .option("dbtable", "schools") \
    .option("user", pg_user) \
    .option("password", pg_password) \
    .option("driver", "org.postgresql.Driver") \
    .mode("append") \
    .save()

cartography_df.write \
    .format("jdbc") \
    .option("url", f"jdbc:postgresql://{pg_host}:{pg_port}/{pg_database}") \
    .option("dbtable", "cartography") \
    .option("user", pg_user) \
    .option("password", pg_password) \
    .option("driver", "org.postgresql.Driver") \
    .mode("append") \
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
