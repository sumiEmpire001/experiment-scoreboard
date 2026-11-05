# Experiment Scoreboard

A Python standard-library CLI for comparing conversion outcomes across A/B test variants. Reads a CSV, aggregates repeated rows per variant, calculates observed conversion rates and Wilson 95% confidence intervals, and identifies the highest **observed** conversion rate.

## Usage

```bash
python scoreboard.py examples/experiment.csv
python scoreboard.py examples/experiment.csv --output report.json
```

CSV columns: `variant,visitors,conversions`. Visitors must be positive integers and conversions must be between zero and visitors.

## Tests

```bash
python -m unittest discover -s tests -v
```

Eight tests run in GitHub Actions on Python 3.10, 3.12, and 3.13.

## Interpretation

The best observed variant is **not necessarily a statistically significant winner**. Wilson intervals summarize binomial uncertainty, but this tool does not perform hypothesis testing, correct for repeated peeking or multiple comparisons, or assess experiment randomization. Do not use it alone to declare experiment success.
