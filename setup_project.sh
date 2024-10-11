#!/bin/bash

# --- Project Setup ---

# Get additional project details
read -r -p "Enter your current location where the project is installed: " PROJECT_PATH
read -r -p "Enter the project name: " PROJECT_NAME
read -r -p "Enter the project short description: " PROJECT_SHORT_DES
read -r -p "Enter the project long description: " PROJECT_LONG_DES

# --- Create Conda environment ---

# Create the environment from the provided environment.yml
conda env create -f environment.yml

# Activate the newly created environment
conda activate "${PROJECT_NAME}_env"

# --- User Authentication ---

# Use git credential helper for secure storage of credentials
git config --global credential.helper store

echo "Please enter your GitHub credentials:"
read -r -p "Enter your full name: " YOURNAME
read -r -p "Enter your GitHub email: " YOUREMAIL
read -r -p "Enter your GitHub username: " USERNAME
read -r -s -p "Enter your GitHub personal access token: " TOKEN
echo ""  # Print a newline after the password input

# Store credentials securely using the credential helper
git credential approve <<< "protocol=https
host=github.com
username=$USERNAME
password=$TOKEN"

# Set global Git config for user.name and user.email
git config --global user.name "${YOURNAME}"
git config --global user.email "${YOUREMAIL}"

# --- Update cookiecutter.json ---

# Inline the cookiecutter.json content
cookiecutter_json='
{
  "full_name": "'"$YOURNAME"'",
  "email": "'"$YOUREMAIL"'",
  "github_username": "'"$USERNAME"'",
  "project_name": "'"$PROJECT_NAME"'", 
  "project_slug": "{{ cookiecutter.project_name.lower().replace(' ', '_').replace('-', '_') }}",
  "namespace": "{{ cookiecutter.project_slug.split('.')[0] }}",
  "package_name": "{{ cookiecutter.project_slug.split('.')[1] }}",
  "project_short_description": "Python Namespace Package contains all you need to create a Python namespace package.",
  "pypi_username": "iamgrewal",
  "use_pytest": "y",
  "use_black": "y",
  "command_line_interface": ["Typer", "Click", "Argparse", "No command-line interface"],
  "version": "0.1.0",
  "create_author_file": "y",
  "license": ["MIT", "BSD-2-Clause", "BSD-3-Clause", "Apache-2.0", "GPL-3.0-only", "GPL-3.0-or-later", "Other/Proprietary License"],
  "_copy_without_render": [".github/workflows/pre-commit.yml"],
  "include_github_actions": ["y", "n"],
  "publish_to": ["pypi", "artifactory", "none"],
  "typechecking": ["mypy", "pyright"],
  "deptry": ["y", "n"],
  "mkdocs": ["y", "n"],
  "codecov": ["y", "n"],
  "dockerfile": ["y", "n"],
  "devcontainer": ["y", "n"],
  "open_source_license": [
    "MIT license",
    "BSD license",
    "ISC license",
    "Apache Software License 2.0",
    "GNU General Public License v3",
    "Not open source"
  ]
}
'

# Create a temporary file to store the updated JSON
TEMP_FILE=$(mktemp)

# Use jq to update the values in cookiecutter.json (no need for --arg here)
echo "$cookiecutter_json" > "$TEMP_FILE" 

# Replace the original cookiecutter.json with the updated one
mv "$TEMP_FILE" cookiecutter.json

# --- Run cookiecutter ---
cookiecutter .

echo "Project setup complete!"
