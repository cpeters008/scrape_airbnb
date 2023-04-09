#!/bin/bash

if [ -z "$VIRTUAL_ENV" ]; then
    echo "Error: Not running in a virtual environment."
    exit 1
fi

script_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
requirements_file="${script_dir}/requirements.txt"

if [ ! -f "$requirements_file" ]; then
    echo "Error: $requirements_file not found."
    exit 1
fi

if ! pip install -r "$requirements_file"; then
    echo "Error: Failed to install packages from $requirements_file."
    exit 1
fi

echo "Successfully installed packages from $requirements_file"
