# Health Automation

A Python-based log simulation and analysis tool designed to mimic service health monitoring workflows. This project generates synthetic service logs, analyzes key performance metrics, and is integrated with GitHub Actions for continuous testing.

## Features

- **Log Simulation**: Generates logs with timestamps, job IDs, latency, and status (success or failure).
- **Log Analysis**: Parses logs to extract:
  - Total number of jobs
  - Percentage of success/failure
  - Average latency
  - Most common error reason
- **Test Coverage**: Includes unit tests for log parsing and metric calculation.
- **CI/CD**: Automatically runs tests and analysis on every push via GitHub Actions.

## File Structure

```
health-automation/
├── logs/                 # Generated log files
├── src/
│   ├── simulate.py       # Generates log data
│   └── analyze.py        # Parses logs and summarizes metrics
├── tests/
│   └── test\_analyze.py   # Unit tests for analysis
├── .github/workflows/
│   └── ci.yml            # GitHub Actions workflow
├── requirements.txt      # Python dependencies
└── README.md             # Project documentation
```

## How to Run

1. Clone the repository:
   ```bash
   git clone https://github.com/stevenarbo3/health-automation.git
   cd health-automation
   ```


3. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

4. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

5. Generate logs:

   ```bash
   python src/simulate.py --count 100
   ```

6. Analyze logs:

   ```bash
   python src/analyze.py
   ```

7. Run tests:

   ```bash
   pytest
   ```

## GitHub Actions Workflow

This project includes a CI workflow that:

* Checks out the repo
* Installs dependencies
* Runs the simulator
* Analyzes logs
* Executes all unit tests

Workflow is defined in `.github/workflows/ci.yml` and is triggered on every push or pull request.

## License

This project is open-source and free to use.
