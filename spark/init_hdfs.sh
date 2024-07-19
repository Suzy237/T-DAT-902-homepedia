#!/bin/bash

# HDFS Namenode host and port
HDFS_NAMENODE="namenode"
HDFS_PORT="9870"
HDFS_USER="hadoop"

# Function to check HDFS readiness
check_hdfs_ready() {
  until curl -L -s "http://${HDFS_NAMENODE}:${HDFS_PORT}/webhdfs/v1/?op=GETHOMEDIRECTORY&user.name=${HDFS_USER}" | grep -q "/user/${HDFS_USER}"; do
    echo "Waiting for HDFS to be ready..."
    echo "http://${HDFS_NAMENODE}:${HDFS_PORT}/webhdfs/v1/?op=GETHOMEDIRECTORY&user.name=${HDFS_USER}"
    sleep 5
  done
}

# Function to create HDFS directory
create_hdfs_directory() {
  local dir=$1
  curl -L -i -X PUT "http://${HDFS_NAMENODE}:${HDFS_PORT}/webhdfs/v1/${dir}?op=MKDIRS&user.name=${HDFS_USER}"
  echo "http://${HDFS_NAMENODE}:${HDFS_PORT}/webhdfs/v1/${dir}?op=MKDIRS&user.name=${HDFS_USER}"
}

# Function to upload files to HDFS
upload_to_hdfs() {
  local dir=$1
  for file in /opt/python_scripts/*; do
    local filename=$(basename "$file")
    curl -L -i -X PUT -T "$file" "http://${HDFS_NAMENODE}:${HDFS_PORT}/webhdfs/v1/${dir}/${filename}?op=CREATE&user.name=${HDFS_USER}&overwrite=true"
    echo "http://${HDFS_NAMENODE}:${HDFS_PORT}/webhdfs/v1/${dir}/${filename}?op=CREATE&user.name=${HDFS_USER}&overwrite=true"
  done
}

# Main script execution
check_hdfs_ready
create_hdfs_directory "python_scripts"
upload_to_hdfs "python_scripts"

echo "Python scripts uploaded to HDFS."

# Execute the original command passed to the container
exec "$@"
