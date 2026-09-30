from pathlib import Path

import pandas as pd


def load_orders(input_file: Path) -> pd.DataFrame:
    """Load order data from a CSV file."""

    try:
        return pd.read_csv(input_file)

    except FileNotFoundError as error:
        raise FileNotFoundError(
            f"Input file not found: {input_file}"
        ) from error

    except pd.errors.EmptyDataError as error:
        raise ValueError(
            f"Input file is empty: {input_file}"
        ) from error

    except pd.errors.ParserError as error:
        raise ValueError(
            f"Could not parse CSV file: {input_file}"
        ) from error