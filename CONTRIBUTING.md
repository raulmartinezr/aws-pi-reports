# Contributing to pg-stats-tools

Contributions are welcome! You can contribute to this project by:

* Reporting a bug
* Submitting a fix
* Discussing the current state of the code
* Proposing new features

If you want to start developing this project, please take a look at the `Getting started` section.

## Getting started

Ready to contribute? Here's how to set up cortex for local development. Before you start you will need:

* [Python](https://www.python.org/): 3.10
* [pip](https://pip.pypa.io/en/stable/): 23.1.2+
* [tox](https://pypi.org/project/tox/): 1.6.1+
* [git](https://git-scm.com/) or [mercurial](https://www.mercurial-scm.org/)
* [GNU make](https://www.gnu.org/software/make/): 4.3+

Please take a look at the documentation of your OS or distribution on how to install these software dependencies.

Once you have everything ready, you can start contributing to the project. Before doing do, please make sure you understand what code style you should follow, conventions, branching strategy, merge request requirements, etc. In case of doubt, contact any of the maintainers of the project. You can use the following basic workflow:

1. Clone this repository on your development machine and `cd` into the newly created folder.
1.1. Install dependencies

    python3.10 python3.10-dev ppython3-pip python3.10-venv



2. Create a development virtual environment: `make env-switch-310`. This will create and activate dev environment
3. Install precommit hooks: `make precommit-install`.
4. (Optional) Manage required dependencies in `pyproject.toml` file
5. Make your changes!
6. Make sure the code complies with code style conventions (PEP8) and looks correct (pylint): `make code-style` and `make lint`.
9. Check the code for security vulnerabilities: `make security` and `make check-dependencies`
10. Inspect the code metrics to assess that there is no unneeded complexity (refactor): `make code-metrics`
11. Update the documentation and generate it with: `make docs`
12. Update the `CHANGELOG.md`
13. If the package is ready to be released, bump the version number with: `make tag-bump PART=minor` (where `PART` can be `major`, `minor` or `patch`)
14. Push your changes!
15. Check that the CI pipeline runs all steps successfully

For a more comprehensive list of scripted operations, please take a look at the following section.


## About the `Makefile`

Almost all the needed operations required to develop this project are scripted in the `Makefile` for your convenience. It is recommended that you familiarize yourself with this file and the features it provides. Below is a complete list of the available targets (operations):

| Target                    | Parameters                                                                                                                  | Description                                                                                                                                                      |
|---------------------------|-----------------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `help`                    |                                                                                                                             | Prints all the available targets with a brief explanation of each of them                                                                                        |
| `env-create`              |                                                                                                                             | Creates a development virtual environment using `tox` (the name is the same as the project slug)                                                                 |
| `env-compile`  | | Compiles the `requirements.txt` and `requirements-dev.txt` files by pinning the dependencies found on `requirements.in`/`requirements-dev.in`  |
| `env-sync` |  | Synchronizes the requirements with the current environment |
| `env-add-package`         | `PACKAGE`: for example `requests`                                                                                           | Adds a new package to `requirements.in`                                                                                                                          |
| `env-add-dev-package`     | `PACKAGE`: for example `responses`                                                                                          | Adds a new development package to `requirements-dev.in`                                                                                                          |
| `env-upgrade-package`     | `PACKAGE`: for example `requests`                                                                                           | Upgrades a package in `requirements.in`                                                                                                                          |
| `env-upgrade-dev-package` | `PACKAGE`: for example `responses`                                                                                          | Upgrades a development package in `requirements-dev.in`                                                                                                          |
| `env-upgrade-all`         |                                                                                                                             | Upgrades all packages in `requirements.in`/`requirements-dev.in`                                                                                                 |
| `install`                 |                                                                                                                             | Installs this package using `pip` (not really required during development)                                                                                       |
| `uninstall`               |                                                                                                                             | Uninstalls this package using `pip`                                                                                                                              |
| `develop`                 |                                                                                                                             | Installs this package in development mode (not really required during development)                                                                               |
| `fmt`                     |                                                                                                                             | Formats the code according to the [PEP8 guidelines](https://www.python.org/dev/peps/pep-0008/) using [black](https://pypi.org/project/black/)                    |
| `lint`                    |                                                                                                                             | Lints the code using [pylint](https://www.pylint.org/)                                                                                                           |
| `lint-tests`              |                                                                                                                             | Lints the tests using [pylint](https://www.pylint.org/)                                                                                                          |
| `test`                    |                                                                                                                             | Runs the tests using [pytest](https://docs.pytest.org/en/latest/)                                                                                                |
| `test-report`             | `REPORT_NAME`: (default `pytest`)                                                                                           | Runs the tests and generates HTML and XML Junit reports on `docs/_build/test-reports/<REPORT_NAME>`                                                              |
| `coverage`                |                                                                                                                             | Checks code coverage using [coverage](https://pypi.org/project/coverage/)                                                                                        |
| `coverage-report`         |                                                                                                                             | Checks code coverage using [coverage](https://pypi.org/project/coverage/) and generates an HTML report (at `docs/_build/coverage`)                               |
| `security`                |                                                                                                                             | Runs a static security analysis on the code using [bandit](https://pypi.org/project/bandit/)                                                                     |
| `security-report`         |                                                                                                                             | Runs a static security analysis on the code using [bandit](https://pypi.org/project/bandit/) and generates an HTML report (at `docs/_build/security`)            |
| `check-dependencies`      |                                                                                                                             | Checks dependencies for vulnerabilities using [safety](https://pypi.org/project/safety/)                                                                         |
| `docs`                    |                                                                                                                             | Generates package documentation using [sphinx](https://www.sphinx-doc.org/en/master/) (saved at `docs/_build/sphinx`)                                            |
| `version`                 |                                                                                                                             | Gets the current package version (found on the `__version__` variable at `cortex/_meta.py`)                                               |
| `tag-bump` | `PART`: the part of version to bump. One of X.Y.Z (major, minor, patch) | Calculates which version to go, checks if there is an entry in CHANGELOG.md, increases version, tags the version and commits. |
| `tag-push` | `PART`: the part of version to bump One of X.Y.Z (major, minor, patch) | Pushes the current version's tag to remote origin |
| `tag-delete` | `TAG`: the **tag** to delete | Deletes the given `TAG` in local and in remote origin  |
| `dist`                    |                                                                                                                             | Builds a binary distribution (wheel) compiled with [cython](https://cython.org/)                                                                                 |
| `dist-dev`                |                                                                                                                             | Builds a non-compiled binary distribution (wheel)                                                                                                                |
| `sdist`                   |                                                                                                                             | Builds a source code distribution                                                                                                                                |
| `publish`                 |                                                                                                                             | Publishes all wheels found on the `dist` folder to our private PyPi repository (Artifactory)                                                                     |
| `publish-docs`            | `SOURCE`: source folder, `BUILD_ID`: the build identifier (free-form text), `TARGET`: the destination folder on Artifactory | Publishes docs found on the `SOURCE` folder to Artifactory                                                                                                       |
| `docker-run`              | `TARGET`: make target to run inside Docker                                                                                  | Runs the specified `TARGET` inside a Docker container (configured on `docker/dev/docker-compose.yml`). Useful if the package requires system-level dependencies. |
| `docker-shell`            |                                                                                                                             | Runs a shell inside the Docker container configured on `docker/dev/docker-compose.yml`                                                                           |
| `docker-lint`             |                                                                                                                             | Lints the `Dockerfile` at `docker/prod` using [hadolint](https://github.com/hadolint/hadolint)                                                                   |
| `docker-build`            | `REVISION` (optional): current commit SHA (will be added as a `LABEL`)                                                      | Builds the production docker image (the name will be the project slug)                                                                                           |
| `docker-tag`              | `IMAGE_NAME` (optional): new name of the image                                                                              | Tags the production docker image (the name will be `$IMAGE_NAME:<current_version>`)                                                                              |
| `docker-push`             | `IMAGE_NAME`: name of the image to push                                                                                     | Pushes the production docker image                                                                                                                               |
| `docker-security`         | `IMAGE_NAME`: name of the image to scan (default is the project slug)                                                       | Scans the production docker image for security vulnerabilities using [trivy](https://github.com/aquasecurity/trivy)                                              |
| `ci-all`                  |                                                                                                                             | Simulate the complete CI pipeline by running all the `ci-*` targets                                                                                              |
| `ci-prepare`              |                                                                                                                             | Creates the virtual environment for every support Python version using `tox` (used on CI).                                                                       |
| `ci-lint`                 |                                                                                                                             | Lints code and tests (used on CI)                                                                                                                                |
| `ci-code-style`           |                                                                                                                             | Checks code style against [PEP8 guidelines](https://www.python.org/dev/peps/pep-0008/) (used on CI). Equivalent to `make code-style`                             |
| `ci-code-metrics`         |                                                                                                                             | Check cyclomatic complexity, print LOCs and calculate maintainability index using [radon](https://pypi.org/project/radon/) (used on CI)                          |
| `ci-security`             |                                                                                                                             | Runs a static security analysis on the code using [bandit](https://pypi.org/project/bandit/) (used on CI). Equivalent to `make security-report`                  |
| `ci-check-dependencies`   |                                                                                                                             | Checks dependencies for vulnerabilities using [safety](https://pypi.org/project/safety/) (used on CI)                                                            |
| `ci-test`                 |                                                                                                                             | Runs tests on every supported Python version. Equivalent to `make test-report` (used on CI). Reports are saved on `docs/_build/test_reports/py<version_number>`  |
| `ci-coverage`             |                                                                                                                             | Checks code coverage using [coverage](https://pypi.org/project/coverage/) (used on CI). Equivalent to `make coverage-report`                                     |
| `ci-docs`                 |                                                                                                                             | Generates package documentation using [sphinx](https://www.sphinx-doc.org/en/master/) (used on CI). Equivalent to `make docs`                                    |
| `ci-version-set`          | `VERSION`: semantic version number                                                                                          | Sets the package version to the one provided in the `VERSION` parameter (used on CI)                                                                             |
| `ci-dist`                 |                                                                                                                             | Builds binary distributions (wheel) for each supported Python version (used on CI). Equivalent to `make dist`.                                                   |
| `ci-dist-dev`             |                                                                                                                             | Builds development (non-binary) distributions (wheel) for each supported Python version (used on CI). Equivalent to `make dist-dev`.                             |
| `ci-publish`              |                                                                                                                             | Publishes all wheels found on the `dist` folder to our private PyPi repository (used on CI). Equivalent to `make publish`                                        |
| `ci-publish-docs`         |                                                                                                                             | Publishes project documentation (used on CI). Equivalent to `make publish-docs`                                                                                  |
| `ci-release`              |                                                                                                                             | Builds and publishes binary distributions (wheel) for each supported Python version (used on CI). Equivalent to `make dist`.                                     |
| `ci-release-dev`          |                                                                                                                             | Builds and publishes development (non-binary) distributions (wheel) for each supported Python version (used on CI). Equivalent to `make dist-dev`.               |
| `ci-docker-dist`          | `IMAGE_NAME`: name of the image to build (should be the URL of GitLab's docker repository)                                  | Lints, builds, publishes to GitLab's repository and scans the production image for vulnerabilities (used on CI)                                                  |
| `ci-docker-publish`       | `IMAGE_NAME`: name of the image to push (should be the URL of the remote docker repository)                                 | Publishes the docker image to a remote repository (used on CI)                                                                                                   |
| `ci-clean`                |                                                                                                                             | Cleans build artifacts and tox environments (used on CI)                                                                                                         |
| `clean`                   |                                                                                                                             | Removes build artifacts, test artifacts, docs, etc.                                                                                                              |
| `clean-docs`              |                                                                                                                             | Removes built documentation (`docs/_build)`)                                                                                                                     |
| `clean-build`             |                                                                                                                             | Removes build artifacts                                                                                                                                          |
| `clean-dist`              |                                                                                                                             | Removes package builds found on `dist/`                                                                                                                          |
| `clean-pyc`               |                                                                                                                             | Removes python cache artifacts                                                                                                                                   |
| `clean-test`              |                                                                                                                             | Removes pytest and coverage artifacts                                                                                                                            |
| `clean-env`               |                                                                                                                             | Removes tox virtual environments (`.tox`)                                                                                                                        |
| `clean-docker`            |                                                                                                                             | Removes docker containers, networks, etc.                                                                                                                        |
