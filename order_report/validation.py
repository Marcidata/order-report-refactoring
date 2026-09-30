import logging

import pandas as pd


logger = logging.getLogger(__name__)

REQUIRED_COLUMNS = {
    "order_id",
    "order_date",
    "customer_id",
    "region",
    "product_category",
    "quantity",
    "unit_price",
    "discount",
    "returned",
}

KNOWN_MISSING_MARKERS = {"unknown"}


def validate_orders(data: pd.DataFrame) -> None:
    """Validate the structure and values of raw order data."""
    if data.empty:
        raise ValueError("Order data is empty.")

    missing_columns = REQUIRED_COLUMNS - set(data.columns)

    if missing_columns:
        missing = ", ".join(sorted(missing_columns))
        raise ValueError(f"Missing required columns: {missing}")

    numeric_values = validate_numeric_columns(data)
    validate_numeric_ranges(numeric_values)


def validate_numeric_columns(
    data: pd.DataFrame,
) -> dict[str, pd.Series]:
    """Validate numeric columns and handle known missing-value markers."""
    numeric_values = {}

    for column in ["quantity", "unit_price", "discount"]:
        text_values = (
            data[column]
            .astype("string")
            .str.strip()
            .str.lower()
        )

        known_missing = text_values.isin(KNOWN_MISSING_MARKERS)

        if known_missing.any():
            count = int(known_missing.sum())
            logger.warning(
                "Column '%s' contains %d known missing-value marker(s). "
                "They will be treated as missing.",
                column,
                count,
            )

        converted = pd.to_numeric(data[column], errors="coerce")

        invalid_values = (
            data[column].notna()
            & converted.isna()
            & ~known_missing
        )

        if invalid_values.any():
            raise ValueError(
                f"Column '{column}' contains invalid numeric values."
            )

        converted = converted.mask(known_missing)
        numeric_values[column] = converted

    return numeric_values


def validate_numeric_ranges(
    numeric_values: dict[str, pd.Series],
) -> None:
    """Validate that numeric values are within reasonable ranges."""
    quantity = numeric_values["quantity"]
    unit_price = numeric_values["unit_price"]
    discount = numeric_values["discount"]

    if (quantity.dropna() <= 0).any():
        raise ValueError("Quantity must be greater than 0.")

    if (unit_price.dropna() < 0).any():
        raise ValueError("Unit price cannot be negative.")

    if ((discount.dropna() < 0) | (discount.dropna() > 1)).any():
        raise ValueError("Discount must be between 0 and 1.")