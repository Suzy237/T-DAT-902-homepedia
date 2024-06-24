import os
import requests
import json
import sys
from concurrent.futures import ThreadPoolExecutor

# Directory to store the downloaded CSV files
csv_dir = '/tmp/downloads/'
os.makedirs(csv_dir, exist_ok=True)

# Example CSV file URLs with redirections
urls = [
    ("https://www.data.gouv.fr/fr/datasets/r/dbe8a621-a9c4-4bc3-9cae-be1699c5ff25", "france_cartography_data.csv"),
    ("https://www.data.gouv.fr/fr/datasets/r/b22f04bf-64a8-495d-b8bb-d84dbc4c7983", "france_schools_data.csv"),
    ("https://www.data.gouv.fr/fr/datasets/r/3f51212c-f7d2-4aec-b899-06be6cdd1030", "france_safety_rate_data.csv")
]

namenode_host = "namenode"
webhdfs_port = 9870
webhdfs_url = f"http://{namenode_host}:{webhdfs_port}/webhdfs/v1"
user = "hadoop"

def create_hdfs_directory(path):
    url = f"{webhdfs_url}{path}?op=MKDIRS&user.name={user}"
    response = requests.put(url)
    response.raise_for_status()

def upload_to_hdfs(local_path, hdfs_path):
    # Step 1: Open for write
    url = f"{webhdfs_url}{hdfs_path}?op=CREATE&overwrite=true&user.name={user}"
    response = requests.put(url, allow_redirects=False)
    response.raise_for_status()
    
    # Step 2: Follow redirect to upload
    upload_url = response.headers['Location']
    with open(local_path, 'rb') as f:
        response = requests.put(upload_url, data=f)
        response.raise_for_status()

def download_file(url, output_filename):
    response = requests.get(url, allow_redirects=True)
    response.raise_for_status()  # Raise HTTPError for bad responses
    filename = os.path.join(csv_dir, output_filename)
    
    # Write the CSV file
    with open(filename, 'wb') as file:
        file.write(response.content)

# Collect all messages and statuses
results = []

try:
    # Download each file using ThreadPoolExecutor for parallel downloading
    with ThreadPoolExecutor() as executor:
        futures = [executor.submit(download_file, url, output_filename) for url, output_filename in urls]
        for future in futures:
            future.result()

    results.append({"status": "success", "message": "Files have been downloaded successfully."})
except requests.exceptions.RequestException as e:
    results.append({"status": "error", "message": f"Error downloading files: {e}"})

try:
    # Create HDFS directory
    create_hdfs_directory("/csv_data")

    # Upload files to HDFS using ThreadPoolExecutor for parallel uploading
    with ThreadPoolExecutor() as executor:
        futures = [executor.submit(upload_to_hdfs, os.path.join(csv_dir, filename), f"/csv_data/{filename}") for _, filename in urls]
        for future in futures:
            future.result()

    results.append({"status": "success", "message": "Files have been uploaded to HDFS successfully."})

    # Verify files in HDFS
    response = requests.get(f"{webhdfs_url}/csv_data?op=LISTSTATUS&user.name={user}")
    response.raise_for_status()
    files = response.json()
    results.append({"status": "success", "message": "Verification successful.", "files": files})
except Exception as e:
    results.append({"status": "error", "message": f"Error uploading files to HDFS: {e}"})

# Ensure the overall status is included in the final JSON output
overall_status = "success" if all(result["status"] == "success" for result in results) else "error"
final_output = {"status": overall_status, "results": results}
print(json.dumps(final_output))