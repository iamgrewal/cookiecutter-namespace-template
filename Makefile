BAKE_OPTIONS=--no-input

help:
	@echo bake         "generate project using defaults"
	@echo watch        "generate project using defaults and watch for changes"
	@echo replay       "replay last cookiecutter run and watch for changes"   
	@echo install      "Install the poetry environment"
	@echo check        "Run code quality tools"
	@echo test         "Test the code with pytest"
	@echo build        "Build wheel file using poetry"
	@echo clean-build  "Clean build artifacts"
	@echo publish      "Publish a release to pypi"
	@echo build-and-publish "Build and publish"
	@echo docs-test    "Test if documentation can be built without warnings or errors"
	@echo docs         "Build and serve the documentation"

bake:
	cookiecutter $(BAKE_OPTIONS) . --overwrite-if-exists

.PHONY: watch
watch: bake
	watchmedo shell-command -p '*.*' -c 'make bake -e BAKE_OPTIONS=$(BAKE_OPTIONS)' -W -R -D {{cookiecutter.project_slug}}/

.PHONY: replay
replay: BAKE_OPTIONS=--replay
replay: watch   

install: ## Install the poetry environment
	@echo "🚀 Creating virtual environment using pyenv and poetry"
	@poetry install
	@poetry    shell

check: ## Run code quality tools.
	@echo "🚀 Checking Poetry lock file consistency with 'pyproject.toml': Running poetry check --lock"
	@poetry check --lock
	@echo "🚀 Linting code: Running pre-commit"
	@poetry run pre-commit run -a
	@echo "🚀 Static type checking: Running mypy"
	@poetry run mypy
	@echo "🚀 Checking for obsolete dependencies: Running deptry"
	@poetry run    deptry .

test: ## Test the code with pytest.
	@echo "🚀 Testing code: Running pytest"
	@poetry run pytest --cov --cov-config=pyproject.toml --cov-report=xml tests   

build: clean-build ## Build wheel file using poetry
	@echo "🚀 Creating wheel file"
	@poetry build

clean-build: ## clean build artifacts
	@rm -rf dist

publish: ## publish a release to pypi.
	@echo    "🚀 Publishing: Dry run."
	@poetry config pypi-token.pypi $(PYPI_TOKEN)
	@poetry publish --dry-run
	@echo "🚀 Publishing."
	@poetry publish

build-and-publish: build publish ## Build and publish.   

docs-test: ## Test if documentation can be built without warnings or errors
	@poetry run mkdocs build -s

docs: ## Build and serve the documentation
	@poetry run mkdocs serve   

.DEFAULT_GOAL := help
