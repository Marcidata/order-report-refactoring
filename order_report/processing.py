import pandas as pd


def prepare_orders(data: pd.DataFrame) -> pd.DataFrame:
    """Prepare order data after validation."""

    prepared = data.copy()

    prepared["region"] = (
        prepared["region"]
        .fillna("Unknown")
        .astype(str)
        .str.strip()
        .str.title()
    )

    prepared["product_category"] = (
        prepared["product_category"]
        .fillna("Unknown")
        .astype(str)
        .str.strip()
        .str.title()
    )

    prepared["quantity"] = pd.to_numeric(
        prepared["quantity"],
        errors="coerce",
    )

    prepared["unit_price"] = pd.to_numeric(
        prepared["unit_price"],
        errors="coerce",
    )

    prepared["discount"] = pd.to_numeric(
        prepared["discount"],
        errors="coerce",
    )

    prepared["returned"] = (
        prepared["returned"]
        .fillna("false")
        .astype(str)
        .str.strip()
        .str.lower()
        .isin(["true", "yes", "1", "ja"])
    )

    return prepared


def apply_missing_value_defaults(data: pd.DataFrame) -> pd.DataFrame:
    """Apply the defaults used by the original application."""

    prepared = data.copy()

    prepared["quantity"] = prepared["quantity"].fillna(1)

    prepared["unit_price"] = prepared["unit_price"].fillna(
        prepared["unit_price"].median()
    )

    prepared["discount"] = prepared["discount"].fillna(0)

    return prepared


def calculate_order_values(data: pd.DataFrame) -> pd.DataFrame:
    """Calculate order value and discounted order value."""

    calculated = data.copy()

    calculated["order_value"] = (
        calculated["quantity"] * calculated["unit_price"]
    )

    calculated["discounted_value"] = (
        calculated["order_value"]
        * (1 - calculated["discount"])
    )

    return calculated
