"""Analyze actual-versus-budget financial results using a CSV file.

This is a small educational tool with no third-party dependencies.
"""
import argparse
import csv
from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import Dict, List


REQUIRED_COLUMNS = {"category", "actual", "budget", "type"}
VALID_TYPES = {"revenue", "expense"}


def parse_amount(value: str, row_number: int, column: str) -> Decimal:
    """Parse a numeric CSV value and provide a helpful error if invalid."""
    try:
        return Decimal(value.strip())
    except (InvalidOperation, AttributeError):
        raise ValueError(
            f"Row {row_number}: {column!r} must be a valid number; got {value!r}."
        )


def analyze_row(row: Dict[str, str], row_number: int = 2) -> Dict[str, str]:
    """Calculate variance, variance percentage, and business-friendly status."""
    category = (row.get("category") or "").strip()
    line_type = (row.get("type") or "").strip().lower()

    if not category:
        raise ValueError(f"Row {row_number}: category cannot be empty.")
    if line_type not in VALID_TYPES:
        raise ValueError(
            f"Row {row_number}: type must be 'revenue' or 'expense'; got {line_type!r}."
        )

    actual = parse_amount(row.get("actual", ""), row_number, "actual")
    budget = parse_amount(row.get("budget", ""), row_number, "budget")
    variance = actual - budget

    if budget == 0:
        variance_pct = ""
    else:
        variance_pct = str((variance / abs(budget) * Decimal("100")).quantize(Decimal("0.01")))

    if variance == 0:
        status = "On budget"
    else:
        favourable = (variance > 0) if line_type == "revenue" else (variance < 0)
        status = "Favourable" if favourable else "Unfavourable"

    return {
        "category": category,
        "type": line_type,
        "actual": str(actual.quantize(Decimal("0.01"))),
        "budget": str(budget.quantize(Decimal("0.01"))),
        "variance": str(variance.quantize(Decimal("0.01"))),
        "variance_pct": variance_pct,
        "status": status,
    }


def analyze_file(input_path: Path) -> List[Dict[str, str]]:
    """Read and validate the input CSV, then return analyzed rows."""
    with input_path.open("r", newline="", encoding="utf-8-sig") as file:
        reader = csv.DictReader(file)
        if not reader.fieldnames:
            raise ValueError("The input CSV is empty or has no header row.")

        missing = REQUIRED_COLUMNS - set(reader.fieldnames)
        if missing:
            raise ValueError("Missing required CSV columns: " + ", ".join(sorted(missing)))

        results = []
        for row_number, row in enumerate(reader, start=2):
            if not any((value or "").strip() for value in row.values()):
                continue
            results.append(analyze_row(row, row_number))
        return results


def write_report(results: List[Dict[str, str]], output_path: Path) -> None:
    """Write analyzed results to a CSV file."""
    columns = [
        "category", "type", "actual", "budget",
        "variance", "variance_pct", "status"
    ]
    with output_path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=columns)
        writer.writeheader()
        writer.writerows(results)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Compare actual financial results with budget using a CSV file."
    )
    parser.add_argument("input", type=Path, help="Path to input financial CSV")
    parser.add_argument(
        "--output", type=Path, default=Path("variance_report.csv"),
        help="Output CSV path (default: variance_report.csv)"
    )
    args = parser.parse_args()

    try:
        results = analyze_file(args.input)
        write_report(results, args.output)
    except (OSError, ValueError) as error:
        parser.error(str(error))

    print(f"Analyzed {len(results)} line(s). Report saved to: {args.output}")
    if results:
        favourable = sum(row["status"] == "Favourable" for row in results)
        unfavourable = sum(row["status"] == "Unfavourable" for row in results)
        on_budget = sum(row["status"] == "On budget" for row in results)
        print(
            f"Summary: {favourable} favourable, {unfavourable} unfavourable, "
            f"{on_budget} on budget."
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
