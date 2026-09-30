import pandas as pd
import pytest

from order_report.validation import validate_orders


def create_valid_data():
    return pd.DataFrame(
        {
            "order_id": ["O001", "O002"],
            "order_date": ["2026-01-01", "2026-01-02"],
            "customer_id": ["C001", "C002"],
            "region": ["North", "South"],
            "product_category": ["Books", "Electronics"],
            "quantity": [2, 1],
            "unit_price": [100.0, 200.0],
            "discount": [0.1, 0.2],
            "returned": ["false", "true"],
        }
    )


def test_valid_orders_pass_validation():
    data = create_valid_data()

    validate_orders(data)


def test_empty_data_is_rejected():
    data = pd.DataFrame()

    with pytest.raises(ValueError, match="empty"):
        validate_orders(data)


def test_missing_required_column_is_rejected():
    data = create_valid_data()
    data = data.drop(columns=["discount"])

    with pytest.raises(ValueError, match="Missing required columns"):
        validate_orders(data)


def test_invalid_numeric_value_is_rejected():
    data = create_valid_data()
    data["discount"] = data["discount"].astype(object)
    data.loc[0, "discount"] = "not-a-number"

    with pytest.raises(ValueError, match="invalid numeric values"):
        validate_orders(data)


def test_negative_quantity_is_rejected():
    data = create_valid_data()
    data.loc[0, "quantity"] = -1

    with pytest.raises(ValueError, match="greater than 0"):
        validate_orders(data)


def test_negative_unit_price_is_rejected():
    data = create_valid_data()
    data.loc[0, "unit_price"] = -10

    with pytest.raises(ValueError, match="cannot be negative"):
        validate_orders(data)


def test_discount_above_one_is_rejected():
    data = create_valid_data()
    data.loc[0, "discount"] = 1.5

    with pytest.raises(ValueError, match="between 0 and 1"):
        validate_orders(data)