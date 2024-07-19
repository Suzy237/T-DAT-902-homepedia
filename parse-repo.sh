#!/bin/bash

output_file="repo_contents.txt"
> "$output_file"

git ls-files | while IFS= read -r file; do
    # Skip binary files
    if file "$file" | grep -q "binary"; then
        continue
    fi

    # Skip .DS_Store files
    if [[ "$file" == *".DS_Store" ]]; then
        continue
    fi

    # Write a compact file delimiter
    echo "FILE:$file" >> "$output_file"
    
    # Efficiently append non-empty lines from the file
    sed '/^\s*$/d' "$file" >> "$output_file"
done

echo "Repository contents have been written to $output_file"