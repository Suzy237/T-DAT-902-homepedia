import os
import json
import urllib.parse
import psycopg2
from pyspark.sql import SparkSession
from pyspark.sql.functions import mean, col, to_date, regexp_replace, current_timestamp, when, broadcast, lpad, substring
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, MapType, DecimalType

# Define the schema for city_data_df
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
    .config("spark.sql.shuffle.partitions", "200") \
    .getOrCreate()

# Function to execute SQL statements
def execute_sql(sql):
    conn = psycopg2.connect(
        dbname=pg_database,
        user=pg_user,
        password=pg_password,
        host=pg_host,
        port=pg_port
    )
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()
    cur.close()
    conn.close()

# Clear PostgreSQL tables before inserting new data
execute_sql("DELETE FROM safety_data")
execute_sql("DELETE FROM cartography")
execute_sql("DELETE FROM real_estate")
execute_sql("DELETE FROM schools")
execute_sql("DELETE FROM departements")

# File paths on HDFS
real_estate_path = 'hdfs://namenode:8020/csv_data/france_total_real_estate_sales_2022.csv'
cartography_path = 'hdfs://namenode:8020/csv_data/france_cartography_data.csv'
schools_path = 'hdfs://namenode:8020/csv_data/france_schools_data.csv'
safety_path = 'hdfs://namenode:8020/csv_data/france_safety_rate_data.csv.gz'
city_data_path = 'hdfs://namenode:8020/csv_data/city_data.json'
departments_path = 'hdfs://namenode:8020/csv_data/france_department_list.csv'

# Read CSV files with specified delimiter
real_estate_df = spark.read.csv(real_estate_path, header=True, inferSchema=True, sep=',')
real_estate_df = real_estate_df.withColumn(
    "Valeur fonciere",
    regexp_replace(col("Valeur fonciere"), ",", ".").cast("double")
)
cartography_df = spark.read.csv(cartography_path, header=True, inferSchema=True, sep=',')
schools_df = spark.read.csv(schools_path, header=True, inferSchema=True, sep=';')
safety_df = spark.read.csv(safety_path, header=True, inferSchema=True, sep=';')
city_data_df = spark.read.option("multiline", "true").schema(city_data_df_schema).json(city_data_path)
departments_df = spark.read.csv(departments_path, header=True, inferSchema=True, sep=',')

# Clean column names to remove any leading/trailing whitespace and replace special characters
def clean_column_names(df):
    for col_name in df.columns:
        new_col_name = col_name.strip().replace('.', '_').replace(' ', '_')
        df = df.withColumnRenamed(col_name, new_col_name)
    return df

safety_df = clean_column_names(safety_df)
cartography_df = clean_column_names(cartography_df)
departments_df = clean_column_names(departments_df)

# Cache DataFrames
cartography_df.cache()

# Broadcast join cartography_df if it's small
safety_df = safety_df.join(broadcast(cartography_df), safety_df['CODGEO_2023'] == cartography_df['code_commune_INSEE'], 'inner')

# Process and transform data
avg_cost_df = real_estate_df.groupBy("Code postal").agg(mean("Valeur fonciere").alias("average_cost"))
safety_rate_df = safety_df.withColumn(
    "tauxpourmille",
    regexp_replace(col("tauxpourmille"), ",", ".").cast(DecimalType(20, 10))
).groupBy("CODGEO_2023").agg(
    mean("tauxpourmille").alias("safety_rate")
)
# Join the average calculations with the cartography data
cartography_df = cartography_df \
    .join(avg_cost_df, cartography_df.code_postal == avg_cost_df["Code postal"], "left") \
    .join(safety_rate_df, cartography_df.code_commune_INSEE == safety_rate_df.CODGEO_2023, "left") \
    .select(
        cartography_df["*"],
        avg_cost_df["average_cost"],
        safety_rate_df["safety_rate"]
    )

# Calculate average costs, average valeur fonciere and safety rates by departments
departments_avg_cost_df = real_estate_df.withColumn("department_code", substring("Code postal", 1, 2)).groupBy("department_code").agg(
    mean("Valeur fonciere").alias("avg_valeur_fonciere")
)
departments_safety_rate_df = safety_df.withColumn("department_code", substring("code_postal", 1, 2)).groupBy("department_code").agg(
    mean("safety_rate").alias("avg_safety_rate")
)
departments_avg_cost_df = departments_avg_cost_df.join(
    real_estate_df.withColumn("department_code", substring("Code postal", 1, 2)).groupBy("department_code").agg(
        mean("average_cost").alias("avg_cost")
    ),
    "department_code"
)

# Merge with departments_df
departments_df = departments_df \
    .join(departments_avg_cost_df, departments_df.num_dep == departments_avg_cost_df.department_code, "left") \
    .join(departments_safety_rate_df, departments_df.num_dep == departments_safety_rate_df.department_code, "left") \
    .select(
        departments_df["*"],
        departments_avg_cost_df["avg_cost"].cast("decimal(15,2)"),
        departments_avg_cost_df["avg_valeur_fonciere"].cast("decimal(15,2)"),
        departments_safety_rate_df["avg_safety_rate"].cast("decimal(20,10)").alias("safety_rate")
    )

# Convert 'Date mutation' column to date type
real_estate_df = real_estate_df.withColumn("Date mutation", to_date(col("Date mutation"), "dd/MM/yyyy"))

# Ensure the real_estate_df columns match the database schema
real_estate_df = real_estate_df.select(
    col("Date mutation").alias("mutation_date"),
    col("Nature mutation").alias("nature_mutation"),
    col("Valeur fonciere").alias("valeur_fonciere").cast("double"),
    col("Code postal").alias("postal_code"),
    col("No voie").alias("address"),
    col("Commune").alias("commune"),
    col("Code departement").alias("department_code"),
    col("Code commune").alias("commune_code"),
    col("Surface reelle bati").alias("surface_reelle_bati"),
    col("Nombre pieces principales").alias("nombre_pieces"),
    col("Surface terrain").alias("surface_terrain"),
)
real_estate_df = real_estate_df.withColumn(
    "postal_code",
    when(col("postal_code").contains("."),
         lpad(regexp_replace(col("postal_code"), "\\.0$", ""), 5, '0')
    ).otherwise(
         lpad(col("postal_code"), 5, '0')
    )
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
    col("nombre_d_eleves").alias("nombre_eleves").cast("int"),
)

# Rename columns in cartography_df to match PostgreSQL table schema
cartography_df = cartography_df.select(
    lpad(col("code_commune_INSEE"), 5, '0').alias("code_commune_INSEE"),
    col("nom_commune_postal"),
    lpad(col("code_postal"), 5, '0').alias("code_postal"),
    col("libelle_acheminement"),
    col("latitude").cast("decimal(10,8)"),
    col("longitude").cast("decimal(11,8)"),
    col("nom_region"),
    col("average_cost").cast("decimal(15,2)"),
    col("safety_rate").cast("decimal(20,10)")
)

# Rename columns in departments_df to match PostgreSQL table schema
departments_df = departments_df.select(
    col("num_dep").alias("num_dep"),
    col("dep_name").alias("dep_name"),
    col("region_name").alias("region_name"),
)

# Fix the tauxpourmille column and ensure it is properly formatted
safety_rate_df = safety_df.withColumn(
    "tauxpourmille",
    regexp_replace(col("tauxpourmille"), ",", ".").cast(DecimalType(20, 10))
).select(
    col("annee").cast("int"),
    col("classe"),
    col("unité_de_compte").alias("unite_de_compte"),
    col("valeur_publiée").alias("valeur_publiee").cast("decimal(15,2)"),
    col("faits").cast("int"),
    col("nom_commune"),
    col("code_postal"),
    col("tauxpourmille"),
)

# Add created_at and updated_at columns
current_timestamp_col = current_timestamp()
safety_rate_df = safety_rate_df.withColumn("created_at", current_timestamp_col).withColumn("updated_at", current_timestamp_col)
cartography_df = cartography_df.withColumn("created_at", current_timestamp_col).withColumn("updated_at", current_timestamp_col)
real_estate_df = real_estate_df.withColumn("created_at", current_timestamp_col).withColumn("updated_at", current_timestamp_col)
schools_df = schools_df.withColumn("created_at", current_timestamp_col).withColumn("updated_at", current_timestamp_col)
departments_df = departments_df.withColumn("created_at", current_timestamp_col).withColumn("updated_at", current_timestamp_col)

# Save to PostgreSQL using append mode
def save_to_postgresql(df, table_name):
    df.write \
        .format("jdbc") \
        .option("url", f"jdbc:postgresql://{pg_host}:{pg_port}/{pg_database}") \
        .option("dbtable", table_name) \
        .option("user", pg_user) \
        .option("password", pg_password) \
        .option("driver", "org.postgresql.Driver") \
        .mode("append") \
        .save()

save_to_postgresql(safety_rate_df, "safety_data")
save_to_postgresql(cartography_df, "cartography")
save_to_postgresql(real_estate_df, "real_estate")
save_to_postgresql(schools_df, "schools")
save_to_postgresql(departments_df, "departements")

# Save to MongoDB
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
