# Web Automation Framework

This web automation framework uses Selenium and pytest, following industry standards. It includes setup configuration, logging, detailed reports and screenshots, data-driven testing, and useful tools. It also offers improvements like better configuration management, enhanced logging, improved reporting, a structured Page Object Model (POM), integration with Continuous Integration (CI), and support for different environments.

## Project Structure

    selenium_web_automation_framework/
    │
    ├── config/
    │   ├── config.yaml
    │   └── config_reader.py
    │
    ├── logs/
    │   └── test.log
    │
    ├── reports/
    │   └── report.html
    │
    ├── screenshots/
    │
    ├── src/
    │   ├── __init__.py
    │   ├── base/
    │   │   └── base_driver.py
    │   ├── pages/
    │   │   ├── __init__.py
    │   │   └── example_page.py
    │   └── utilities/
    │       ├── __init__.py
    │       ├── logger.py
    │       ├── read_data.py
    │       └── capture_screenshot.py
    │
    ├── test_cases/
    │   ├── __init__.py
    │   └── test_example.py
    │
    ├── TestData/
    │   └── data.xlsx
    │
    ├── ci/
    │   └── ci_config.yml
    │
    ├── pytest.ini
    ├── requirements.txt
    └── README.md

## Setup

1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Run tests:
   ```
   pytest
   ```

## Configuration

The `config/config.yaml` file contains environment-specific configurations.

## Logging

Logs are configured in `src/utilities/logger.py` and can be found in the `logs/test.log` file.

## Reports

Test reports are generated in the `reports/report.html` file.

## Continuous Integration

The CI configuration is in the `ci/ci_config.yml` file. It is set up to run tests on push and upload test reports if any tests fail.

## Pytest Configuration

The `pytest.ini` file configures pytest settings, including:
- HTML report generation
- Live logging
- Custom markers for test categorization

## Running Tests

To run the code and execute the tests in the specified environment, follow these steps:

### Prerequisites

1. **Python and Pip**: Ensure Python and pip are installed on your system.
2. **WebDrivers**: Download the appropriate WebDriver for your browser (e.g., ChromeDriver for Chrome, GeckoDriver for Firefox) and place them in a directory included in your system's PATH.
3. **Dependencies**: Install the required dependencies from the `requirements.txt` file.

### Steps

   1. **Clone the Repository**: If you haven't already, clone the repository to your local machine.
      ```sh
      git clone https://your-repo-url.git
      cd project_name
      ```

2. **Install Dependencies**: Install the required Python packages.
   ```sh
   pip install -r requirements.txt
   ```

3. **Running Tests**: Use the `pytest` command with the `--env` option to specify the environment. You can run tests in either the test or staging environment.

   - **Run Tests in the Test Environment**:
     ```sh
     pytest --env test
     ```

   - **Run Tests in the Staging Environment**:
     ```sh
     pytest --env staging
     ```

Assuming the repository is cloned and you're in the root directory of the project:

1. **Install Dependencies**:
   ```sh
   pip install -r requirements.txt
   ```

2. **Run Tests in the Test Environment**:
   ```sh
   pytest --env test
   ```

   3. **Run Tests in the Staging Environment**:
      ```
      pytest --env staging
      ```

### Pytest Options

You can also use various pytest options to customize the test run. Some useful options include:

- `-m <marker>`: Run tests with the specified marker (e.g., smoke, regression).
  - `-v`: Increase verbosity.
  - `-s`: Show print statements.
  - `--maxfail=<num>`: Stop after a specified number of failures.

### Example with Options

   - **Run Smoke Tests in the Test Environment with Increased Verbosity**:
     ```sh
     pytest -m smoke --env test -v
     ```
   
     - **Run Regression Tests in the Staging Environment and Stop After 1 Failure**:
       ```sh
       pytest -m regression --env staging --maxfail=1
       ```

### CI Configuration

In CI pipeline (e.g., GitHub Actions), the configuration will automatically use the specified environment matrix to run the tests in both environments.

```


This setup will ensure that tests are executed in both the test and staging environments on each push, providing comprehensive coverage across different environments.
