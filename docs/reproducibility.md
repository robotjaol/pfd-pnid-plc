# Reproducibility Guide

## Environment

Use Python 3.10 or newer. A clean virtual environment is recommended.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
make reproduce
```

## Determinism

The reference scenario sets a NumPy seed. Configuration, software version, command, and generated output should be retained together. Floating-point results can vary slightly across platforms, so regression thresholds should use tolerances rather than byte equality.

## Expected artifacts

- `results/reference-run.csv`: time-series evidence for PID operation.
- `results/benchmark.json`: fixed-speed versus PID metrics.
- test output: safety and model property evidence.

## Proposal build

Install a TeX distribution with `IEEEtran`, then run `make proposal`. The bibliography is stored locally and the first-page preview is regenerated with Poppler.

