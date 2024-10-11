#!/usr/bin/env python
import os

project_path = os.path.realpath(os.path.curdir)
project_slug = os.path.split(project_path)[1]
namespace = project_slug.split(".")[0]
package_name = project_slug.split(".")[1]
package_path = os.path.join(project_path, namespace, package_name)

def remove_file(filepath):   
    """Removes a file if it exists."""
    if os.path.exists(filepath):
        os.remove(filepath)

if __name__ == "__main__":
    if "{{ cookiecutter.create_author_file }}" != "y":
        remove_file(os.path.join(project_path, "AUTHORS.rst"))
        remove_file(os.path.join(project_path, "docs/authors.rst"))

    if "{{ cookiecutter.use_pytest }}" == "y":
        remove_file(os.path.join(project_path, "tests", "__init__.py"))

    if "no" in "{{ cookiecutter.command_line_interface|lower }}":
        remove_file(os.path.join(package_path, "cli.py"))

    if "Other/Proprietary License" == "{{ cookiecutter.license }}":
        remove_file(os.path.join(project_path, "LICENSE"))

    # Additional cleanup (optional):
    # You can add more cleanup tasks here if needed, for example:
    # - Remove specific files based on other cookiecutter variables
    # - Rename files
    # - Create new directories
