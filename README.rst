#Cookiecutter Namespace Template

This Cookiecutter template provides a foundation for creating Python namespace packages, enhanced with additional setup and automation features.

## Features

* **Namespace package structure:** Sets up a well-organized structure for your Python namespace package.
* **Conda environment:** Includes an `environment.yml` file to create a Conda environment with all the necessary dependencies.
* **Automated setup:** Provides a `setup_project.sh` script that automates:
    * Conda environment creation
    * User authentication with Git
    * Project customization by updating `cookiecutter.json`
    * Running Cookiecutter to generate the project
* **Testing:** Includes testing setup with `unittest` or `pytest` and `tox` for testing across different Python versions.
* **Documentation:** Sphinx setup for generating documentation.
* **Version bumping:** `bump2version` for easy version management.
* **Licensing:** Options for different open-source licenses.
* **CI/CD:** GitHub Actions workflows for testing and optional PyPI release.

## Quickstart

1.  **Install Cookiecutter and cruft:**

    ```bash
    python -m pip install -U cookiecutter cruft
    ```

2.  **Generate a project:**

    ```bash
    python -m cruft create [https://github.com/iamgrewal/cookiecutter-namespace-template.git](https://github.com/iamgrewal/cookiecutter-namespace-template.git)
    ```

3.  **Run the setup script:**

    ```bash
    bash setup_project.sh
    ```

    This script will guide you through:
    * Creating the Conda environment
    * Entering your GitHub credentials
    * Providing project details (name, description, etc.)

4.  **Customize (if needed):**
    * Modify any generated files to further tailor the project to your needs.

## Contributing

If you have improvements or suggestions for this template, feel free to fork the repository and submit a pull request.

## License


**Key changes**

*   Updated description:  Reflects the focus on namespace packages and the added features.
*   Conda environment:  Highlights the inclusion of the `environment.yml` file.
*   Automated setup:  Explains the role of the `setup_project.sh` script.
*   Clearer quickstart:  Provides step-by-step instructions on how to use the template, including running the setup script.
*   Contributing section:  Encourages contributions and pull requests.
*   License:  Reminds you to add the appropriate license information.

 
