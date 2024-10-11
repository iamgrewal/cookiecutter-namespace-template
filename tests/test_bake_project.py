import datetime
import os
import shlex
import subprocess
from contextlib import contextmanager

import pytest
from cookiecutter.utils import rmtree

# Context manager to execute code from inside the specified directory
@contextmanager
def inside_dir(dirpath):
    """
    Execute code from inside the given directory.
    
    :param dirpath: String, path of the directory to change into.
    """
    old_path = os.getcwd()
    try:
        os.chdir(dirpath)
        yield
    finally:
        os.chdir(old_path)

# Context manager for baking the project and cleaning up the temporary directory
@contextmanager
def bake_in_temp_dir(cookies, *args, **kwargs):
    """
    Bake a project using cookiecutter and remove the temporary directory created during tests.
    
    :param cookies: pytest_cookies.Cookies, cookie to be baked.
    """
    result = cookies.bake(*args, **kwargs)
    try:
        yield result
    finally:
        rmtree(str(result.project))

# Function to run a command inside a specific directory and return the exit status
def run_inside_dir(command, dirpath):
    """
    Run a command from inside a given directory, returning the exit status.
    
    :param command: The command that will be executed.
    :param dirpath: String, path of the directory in which to execute the command.
    """
    with inside_dir(dirpath):
        return subprocess.check_call(shlex.split(command))

# Extract project information from the baked result
def project_info(result):
    """
    Extract the top-level directory, project_slug, and package_dir from the baked project.
    
    :param result: The result of the cookiecutter bake.
    :return: Tuple with project_path, project_slug, and package_dir.
    """
    project_path = str(result.project)
    project_slug = os.path.split(project_path)[-1]
    namespace = project_slug.split(".")[0]
    package_name = project_slug.split(".")[1]
    package_dir = os.path.join(project_path, namespace, package_name)
    return project_path, project_slug, package_dir

# Fixture to manage temporary directories and clean up after tests
@pytest.fixture
def baked_project(cookies, *args, **kwargs):
    """
    Pytest fixture to bake the project and clean up after the test completes.
    
    :param cookies: pytest_cookies.Cookies, cookie to be baked.
    """
    result = cookies.bake(*args, **kwargs)
    yield result
    rmtree(str(result.project))

# Test to check that the year is correctly computed in the LICENSE file
def test_year_compute_in_license_file(baked_project):
    license_file_path = baked_project.project.join("LICENSE")
    now = datetime.datetime.now()
    assert str(now.year) in license_file_path.read(), "Year not found in LICENSE file."

# Test for the default project structure when baking a project
def test_bake_with_defaults(baked_project):
    assert baked_project.project.isdir()
    assert baked_project.exit_code == 0
    assert baked_project.exception is None

    found_toplevel_files = [f.basename for f in baked_project.project.listdir()]
    assert "pyproject.toml" in found_toplevel_files
    assert "cusy" in found_toplevel_files
    assert "tox.ini" in found_toplevel_files
    assert "tests" in found_toplevel_files

# Parametrized test for verifying different license types
@pytest.mark.parametrize(
    "license, target_string",
    [
        ("MIT license", "MIT "),
        ("BSD license", "Redistributions of source code must retain the above copyright notice"),
        ("ISC license", "ISC License"),
        ("Apache Software License 2.0", "Licensed under the Apache License"),
        ("GNU General Public License v3", "GNU GENERAL PUBLIC LICENSE")
    ]
)
def test_bake_selecting_license(baked_project, license, target_string):
    assert target_string in baked_project.project.join("LICENSE").read()

# Test to ensure a project is created without a LICENSE file for non-open source licenses
def test_bake_not_open_source(baked_project):
    found_toplevel_files = [f.basename for f in baked_project.project.listdir()]
    assert "LICENSE" not in found_toplevel_files, "LICENSE file should not exist for non-open source projects."
    assert "License" not in baked_project.project.join("README.rst").read()

# Test for CLI generation when no command-line interface is selected
def test_bake_with_no_console_script(baked_project):
    project_path, project_slug, package_dir = project_info(baked_project)
    found_project_files = os.listdir(package_dir)
    assert "cli.py" not in found_project_files, "CLI should not be generated when no command-line interface is selected."

# Test for pytest integration in the generated project
def test_using_pytest(baked_project):
    test_file_path = baked_project.project.join("tests/test_cusy_example.py")
    lines = test_file_path.readlines()
    assert "import pytest" in "".join(lines), "Pytest was not correctly included in the project."
    run_inside_dir("pytest", str(baked_project.project)) == 0

# Test for unittest integration in the generated project
def test_using_unittest(baked_project):
    test_file_path = baked_project.project.join("tests/test_cusy_example.py")
    lines = test_file_path.readlines()
    assert "import unittest" in "".join(lines), "Unittest was not correctly included in the project."
    assert "import pytest" not in "".join(lines)
    run_inside_dir("python -m unittest discover", str(baked_project.project)) == 0

# Test for handling a full name with special characters like double quotes
def test_bake_with_specialchars_and_run_tests(cookies):
    with bake_in_temp_dir(cookies, extra_context={"full_name": 'name "quote" name'}) as result:
        assert result.project.isdir()
        run_inside_dir("pytest", str(result.project)) == 0

# Test for handling a full name with apostrophes
def test_bake_with_apostrophe_and_run_tests(cookies):
    with bake_in_temp_dir(cookies, extra_context={"full_name": "O'connor"}) as result:
        assert result.project.isdir()
        run_inside_dir("pytest", str(result.project)) == 0

# Test for ensuring the project is generated without an AUTHORS file
def test_bake_without_author_file(cookies):
    with bake_in_temp_dir(cookies, extra_context={"create_author_file": "n"}) as result:
        found_toplevel_files = [f.basename for f in result.project.listdir()]
        assert "AUTHORS.rst" not in found_toplevel_files
        doc_files = [f.basename for f in result.project.join("docs").listdir()]
        assert "authors.rst" not in doc_files

        # Check the docs index for consistency
        docs_index_path = result.project.join("docs/index.rst")
        with open(str(docs_index_path)) as index_file:
            assert "contributing\n    history" in index_file.read()

# Test to ensure the 'make help' command works on Unix-like systems
def test_make_help(cookies):
    with bake_in_temp_dir(cookies) as result:
        if sys.platform != "win32":
            output = subprocess.check_output(["make", "help"], cwd=str(result.project))
            assert b"check code coverage quickly with the default Python" in output
