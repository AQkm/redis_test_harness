# General
The goal of this project is to enable testing for Redis based on scenarios written in the Gherkin language and to create conditions for further development.

## Installation
To set up the project, you'll need to install the following dependencies:

- Python 3
- pip

Once you have Python and pip installed, run:

```bash
pip install -r requirements.txt
```

## Running Tests
To run tests locally, we recommend using a Python virtual environment:

```bash
python -m venv venv
```
```bash
venv\Scripts\activate
```
or
```bash
source venv/bin/activate
```
```bash
behave --format html --outfile reports/behave-report.html
```

## Structure

#### Redis service
The Redis service under test runs in a Docker container. All functions related to managing the Redis container are stored in `./service_under_test/redis_docker.py`.

#### Gherkin Scenarios
Behave is used to create and execute the Gherkin scenarios. Feature files and step definitions can be found in the following directories:
 - `./features/` – Contains the Gherkin feature files.
 - `./features/steps/` – Contains the step implementations.
The `./features/environments.py` file contains hooks for executing actions before and after scenarios.

#### Reporting
After running the tests, an HTML report is generated and saved in the ./reports directory. The report contains a summary of the test results, which helps in tracking the success or failure of the executed scenarios.

The report can be found at the path: `./reports/behave-report.html`











