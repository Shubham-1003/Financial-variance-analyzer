# Open-Source Financial Variance Analyzer

A small, beginner-friendly Python tool that compares actual financial results with budget or forecast values and produces a CSV variance report.

## What it does

- Calculates dollar variance (`actual - budget`).
- Calculates variance percentage against budget.
- Labels each line as **Favourable**, **Unfavourable**, or **On budget** using a configurable rule.
- Includes a sample dataset with fictional data.
- Exports results to a CSV file.
- Includes basic automated tests.

> **Important:** This is an educational starter project, not accounting, tax, or investment advice. The sample data is fictional. Do not upload employer, customer, or other confidential data.

## Requirements

- Python 3.9 or newer
- No third-party packages are required.

## Run it

1. Download or clone this repository.
2. Open a terminal in the project folder.
3. Run:

   ```bash
   python analyzer.py sample_data/financials.csv --output variance_report.csv
   ```

4. Open `variance_report.csv` in Excel or another spreadsheet program.

On some systems, use `python3` instead of `python`.

## Input CSV format

The input file must include these columns:

- `category`: Name of the financial line, such as Revenue or Labour.
- `actual`: Actual value.
- `budget`: Budget or forecast value.
- `type`: Either `revenue` or `expense`.

Example:

```csv
category,actual,budget,type
Revenue,10500,10000,revenue
Food Cost,4200,4000,expense
Labour,3100,3300,expense
```

For revenue, actual above budget is favourable. For expenses, actual below budget is favourable.

## Example output

The tool adds:

- `variance`: Actual minus budget.
- `variance_pct`: Variance as a percentage of budget.
- `status`: Favourable, Unfavourable, or On budget.

Variance percentage is left blank when the budget is zero to avoid division-by-zero errors.

## Run tests

```bash
python -m unittest discover -s tests -v
```

## Roadmap / ideas for contributors

Potential improvements include:
- Add Excel (`.xlsx`) export.
- Add configurable materiality thresholds.
- Add a summary section by category.
- Add a simple web interface.
- Add support for multiple reporting periods.

Contributions are welcome. Please open an issue to discuss substantial changes before submitting a pull request.

## Project status

This is an initial community project. If you use it, please report bugs or suggest improvements through GitHub Issues.
