import pandas as pd
import pytest

from order_report.data_loader import load_orders


def test_load_orders_reads_csv(tmp_path):
    csv_file = tmp_path / "orders.csv"

    data = pd.DataFrame(
        {
            "order_id": ["O1"],
            "quantity": [2],
            "unit_price": [100],
        }
    )

    data.to_csv(csv_file, index=False)

    result = load_orders(csv_file)

    assert len(result) == 1
    assert list(result.columns) == [
        "order_id",
        "quantity",
        "unit_price",
    ]


def test_load_orders_missing_file_is_rejected(tmp_path):
    csv_file = tmp_path / "missing.csv"

    with pytest.raises(
        FileNotFoundError,
        match="Input file not found",
    ):
        load_orders(csv_file)


def test_load_orders_empty_file_is_rejected(tmp_path):
    csv_file = tmp_path / "empty.csv"
    csv_file.write_text("")

    with pytest.raises(
        ValueError,
        match="Input file is empty",
    ):
        load_orders(csv_file)


def test_load_orders_invalid_csv_is_rejected(tmp_path):
    csv_file = tmp_path / "broken.csv"

    csv_file.write_text(
        "order_id,quantity\n"
        '"O1,2\n'
    )

    with pytest.raises(
        ValueError,
        match="Could not parse CSV file",
    ):
        load_orders(csv_file)