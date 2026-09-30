import pandas as pd

from order_report.processing import (
    apply_missing_value_defaults,
    calculate_order_values,
    prepare_orders,
)


def test_prepare_orders_normalizes_text_and_returned():
    data = pd.DataFrame(
        {
            "region": [" north "],
            "product_category": [" electronics "],
            "quantity": ["2"],
            "unit_price": ["100"],
            "discount": ["0.1"],
            "returned": ["YES"],
        }
    )

    result = prepare_orders(data)

    assert result.loc[0, "region"] == "North"
    assert result.loc[0, "product_category"] == "Electronics"
    assert result.loc[0, "quantity"] == 2
    assert result.loc[0, "unit_price"] == 100
    assert result.loc[0, "discount"] == 0.1
    assert bool(result.loc[0, "returned"]) is True


def test_apply_missing_value_defaults():
    data = pd.DataFrame(
        {
            "quantity": [2, None],
            "unit_price": [100, None],
            "discount": [0.1, None],
        }
    )

    result = apply_missing_value_defaults(data)

    assert result.loc[1, "quantity"] == 1
    assert result.loc[1, "unit_price"] == 100
    assert result.loc[1, "discount"] == 0


def test_calculate_order_values():
    data = pd.DataFrame(
        {
            "quantity": [2],
            "unit_price": [100],
            "discount": [0.1],
        }
    )

    result = calculate_order_values(data)

    assert result.loc[0, "order_value"] == 200
    assert result.loc[0, "discounted_value"] == 180