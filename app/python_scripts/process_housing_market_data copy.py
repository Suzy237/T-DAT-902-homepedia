import os
import json
import urllib.parse
from pyspark.sql import SparkSession
from pyspark.sql.functions import mean, col, to_date
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, DoubleType, MapType

from pyspark.sql.types import StructType, StructField, StringType, IntegerType, MapType

city_data_df_schema = StructType([
    StructField("geocoordinates", StructType([
        StructField("latitude", StringType(), True),
        StructField("longitude", StringType(), True)
    ]), True),
    StructField("departement", StringType(), True),
    StructField("nom_ville", StringType(), True),
    StructField("stat_population", StructType([
        StructField("Nombre d'habitants", StringType(), True),
        StructField("Age moyen", StringType(), True),
        StructField("Pop active", StringType(), True),
        StructField("Taux chômage", StringType(), True),
        StructField("Pop densité", StringType(), True),
        StructField("Revenu moyen", StringType(), True)
    ]), True),
    StructField("evolution_pop", StructType([
        StructField("chart_evolution", MapType(StringType(), IntegerType()), True)
    ]), True),
    StructField("chart", StructType([
        StructField("chart_age", MapType(StringType(), StringType()), True),
        StructField("chart_metier", MapType(StringType(), StringType()), True),
        StructField("chart_diplome", MapType(StringType(), StringType()), True),
        StructField("chart_menage", MapType(StringType(), StringType()), True)
    ]), True),
    StructField("secu", StructType([
        StructField("Agressions physiques / sexuelles", StringType(), True),
        StructField("Cambriolages", StringType(), True),
        StructField("Vols / dégradations", StringType(), True),
        StructField("Stupéfiants", StringType(), True)
    ]), True),
    StructField("secu_chart", StructType([
        StructField("Agressions", MapType(StringType(), IntegerType()), True),
        StructField("Cambriolages", MapType(StringType(), IntegerType()), True),
        StructField("Vols", MapType(StringType(), IntegerType()), True),
        StructField("Stupéfiants", MapType(StringType(), IntegerType()), True)
    ]), True),
    StructField("immobilier", StructType([
        StructField("Maison", StructType([
            StructField("Prix moyen", StringType(), True),
            StructField("Prix moyen au m²", StringType(), True)
        ]), True),
        StructField("Appartement", StructType([
            StructField("Prix moyen", StringType(), True),
            StructField("Prix moyen au m²", StringType(), True)
        ]), True)
    ]), True),
    StructField("immo_chart", StructType([
        StructField("data-appartement", MapType(StringType(), IntegerType()), True),
        StructField("data-maison", MapType(StringType(), IntegerType()), True)
    ]), True),
    StructField("services", StructType([
        StructField("Commerce", StructType([
            StructField("Hypermarché(2km)", StringType(), True),
            StructField("Supermarché", StringType(), True),
            StructField("Boulangerie", StringType(), True),
            StructField("Boucherie", StringType(), True),
            StructField("Station-service", StringType(), True),
            StructField("Banque", StringType(), True),
            StructField("LaPoste", StringType(), True),
            StructField("Coiffeur", StringType(), True),
            StructField("Vétérinaire", StringType(), True),
            StructField("Restaurant", StringType(), True)
        ]), True),
        StructField("Santé", StructType([
            StructField("Médecin", StringType(), True),
            StructField("Dentiste", StringType(), True),
            StructField("Pharmacie", StringType(), True)
        ]), True),
        StructField("Éducation", StructType([
            StructField("Maternelle", StringType(), True),
            StructField("Primaire", StringType(), True),
            StructField("Collège", StringType(), True),
            StructField("Lycée", StringType(), True)
        ]), True)
    ]), True),
    StructField("politique", StructType([
        StructField("tour1", MapType(StringType(), StringType()), True),
        StructField("tour2", StructType([
            StructField("Emmanuel MACRON", StringType(), True),
            StructField("Marine LE PEN", StringType(), True)
        ]), True)
    ]), True)
])



# Read environment variables
pg_host = os.getenv('DB_HOST')
pg_port = os.getenv('DB_PORT')
pg_database = os.getenv('DB_DATABASE')
pg_user = os.getenv('DB_USERNAME')
pg_password = os.getenv('DB_PASSWORD')
mongo_host = os.getenv('MONGO_HOST')
mongo_port = os.getenv('MONGO_PORT')
mongo_db = os.getenv('MONGO_DB')
mongo_user = os.getenv('MONGO_USERNAME')
mongo_password = urllib.parse.quote_plus(os.getenv('MONGO_PASSWORD'))

# Initialize Spark session with PostgreSQL JDBC driver and MongoDB Spark Connector
spark = SparkSession.builder \
    .appName("Housing Market Data Processing") \
    .master(os.getenv('SPARK_MASTER')) \
    .config("spark.mongodb.input.uri", f"mongodb://{mongo_user}:{mongo_password}@{mongo_host}:{mongo_port}/{mongo_db}.safety") \
    .config("spark.mongodb.output.uri", f"mongodb://{mongo_user}:{mongo_password}@{mongo_host}:{mongo_port}/{mongo_db}.safety") \
    .config("spark.jars", "/var/www/downloads/postgresql-42.7.3.jar,/var/www/downloads/mongo-spark-connector_2.12-10.3.0-all.jar") \
    .getOrCreate()

# File paths on HDFS
real_estate_path = 'hdfs://namenode:8020/csv_data/france_total_real_estate_sales_2022.csv'
cartography_path = 'hdfs://namenode:8020/csv_data/france_cartography_data.csv'
schools_path = 'hdfs://namenode:8020/csv_data/france_schools_data.csv'
safety_path = 'hdfs://namenode:8020/csv_data/france_safety_rate_data.csv.gz'
city_data_path = 'hdfs://namenode:8020/csv_data/city_data.json'

# Read CSV files with specified delimiter
real_estate_df = spark.read.csv(real_estate_path, header=True, inferSchema=True, sep=',')
cartography_df = spark.read.csv(cartography_path, header=True, inferSchema=True, sep=',')
schools_df = spark.read.csv(schools_path, header=True, inferSchema=True, sep=';')
safety_df = spark.read.option("header", "true").csv(safety_path, inferSchema=True, sep=';')
city_data_df = spark.read.option("multiline", "true").schema(city_data_df_schema).json(city_data_path)

# Print the schema of the safety_df and real_estate_df to verify column names
safety_df.printSchema()
cartography_df.printSchema()
real_estate_df.printSchema()
city_data_df.printSchema()

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
safety_df = safety_df.join(cartography_df, safety_df['CODGEO_2023'] == cartography_df['code_commune_INSEE'], 'inner')

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
    .mode("overwrite") \
    .save()

schools_df.write \
    .format("jdbc") \
    .option("url", f"jdbc:postgresql://{pg_host}:{pg_port}/{pg_database}") \
    .option("dbtable", "schools") \
    .option("user", pg_user) \
    .option("password", pg_password) \
    .option("driver", "org.postgresql.Driver") \
    .mode("overwrite") \
    .save()

cartography_df.write \
    .format("jdbc") \
    .option("url", f"jdbc:postgresql://{pg_host}:{pg_port}/{pg_database}") \
    .option("dbtable", "cartography") \
    .option("user", pg_user) \
    .option("password", pg_password) \
    .option("driver", "org.postgresql.Driver") \
    .mode("overwrite") \
    .save()

# Save to MongoDB
safety_df.write \
    .format("mongodb") \
    .mode("overwrite") \
    .option("connection.uri", f"mongodb://{mongo_user}:{mongo_password}@{mongo_host}:{mongo_port}") \
    .option("database", mongo_db) \
    .option("collection", "safety") \
    .save()

city_data_df.write \
    .format("mongodb") \
    .mode("overwrite") \
    .option("connection.uri", f"mongodb://{mongo_user}:{mongo_password}@{mongo_host}:{mongo_port}") \
    .option("database", mongo_db) \
    .option("collection", "cityData") \
    .save()

# Print JSON output
print(json.dumps({
    "status": "success",
    "message": "Data processing completed successfully."
}))

spark.stop()