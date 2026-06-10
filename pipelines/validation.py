from pathlib import Path

from ingestion import EXPECTED_COLUMNS, load_customers


def validate_source_file(path: Path | None = None) -> bool:
    df = load_customers(path) if path else load_customers()
    if list(df.columns) != EXPECTED_COLUMNS:
        raise ValueError("CSV column order or names do not match the expected schema.")
    return True


if __name__ == "__main__":
    validate_source_file()
    print("Source validation: SUCCESS")
