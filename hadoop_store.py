import subprocess

def run_command(command):
    print(f"Exécution de la commande : {command}")
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = process.communicate()
    if process.returncode != 0:
        print(f"Echec de la commande. Erreur : {err.decode('utf-8')}")
        print(f"{out.decode('utf-8')}")
        raise Exception(f"Echec de la commande. Erreur : {err.decode('utf-8')}")
    print(f"{out.decode('utf-8')}")
    return out.decode('utf-8')

# Creation des répertoires dans HDFS
directories = [
    "/data/ecoles",
    "/data/villes",
    "/data/logements",
    #"/data/avis"
]

# Créer le dossier /tmp dans le conteneur docker s'il n'existe pas
run_command("docker exec -it namenode mkdir -p /tmp/data")

for directory in directories:
    run_command(f"docker exec -it namenode hdfs dfs -mkdir -p {directory}")



# Stockage des données brutes dans HDFS
local_file_path= "./data/"
files = [
    ("fr-en-annuaire-education.csv", "/data/ecoles/"),
    ("communes-departement-region.csv", "/data/villes/"),
    ("france_total_real_estate_sales_2022.csv", "/data/logements/")
    #("real_estate_reviews.csv", "/data/avis/")
]

for local_file, hdfs_path in files:
    hdfs_file_path = f"{hdfs_path}{local_file}"
    
    # Copie du fichier local vers le container docker
    run_command(f"docker cp {local_file_path}{local_file} namenode:/tmp/{local_file}")

     # Vérifier que le fichier a été copié correctement
    run_command(f"docker exec -it namenode ls /tmp/")

    # Vérifier si le fichier existe dans HDFS et le supprimer
    check_command = f"docker exec -it namenode hdfs dfs -test -e {hdfs_file_path}"
    try:
        run_command(check_command)
        print(f"File {hdfs_file_path} existe déjà. Pas de chargement.")
        continue
    #    delete_command = f"docker exec -it namenode hdfs dfs -rm -r {hdfs_file_path}"
    #    run_command(delete_command)
    except Exception as e:
        print(f"File {hdfs_file_path} n''existe pas. Chargement.")

    # Copie du container docker vers HDFS
    run_command(f"docker exec -it namenode hdfs dfs -put /tmp/{local_file} {hdfs_path}")

print("Les fichiers ont été chargés avec succès dans HDFS.")