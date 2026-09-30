import pandas as pd

from order_report.reports import (
    create_overview,
    create_returns_by_category,
    create_sales_report,
    save_report,
)


def create_test_data() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "order_id": ["O1", "O2", "O3"],
            "region": ["North", "South", "North"],
            "product_category": ["Books", "Books", "Sports"],
            "discounted_value": [180.0, 200.0, 120.0],
            "returned": [False, True, False],
        }
    )


def test_create_overview():
    data = create_test_data()

    result = create_overview(data)

    assert result.loc[0, "metric"] == "total_sales"
    assert result.loc[0, "value"] == 500.0

    assert result.loc[1, "metric"] == "order_count"
    assert result.loc[1, "value"] == 3

    assert result.loc[2, "metric"] == "return_count"
    assert result.loc[2, "value"] == 1


def test_create_sales_report_by_category():
    data = create_test_data()

    result = create_sales_report(data, "product_category")

    books = result[result["product_category"] == "Books"].iloc[0]

    assert books["order_count"] == 2
    assert books["total_sales"] == 380.0
    assert books["returns"] == 1
    assert books["return_rate"] == 0.5


def test_create_sales_report_by_region():
    data = create_test_data()

    result = create_sales_report(data, "region")

    north = result[result["region"] == "North"].iloc[0]

    assert north["order_count"] == 2
    assert north["total_sales"] == 300.0
    assert north["returns"] == 0
    assert north["return_rate"] == 0.0


def test_create_returns_by_category():
    data = create_test_data()

    result = create_returns_by_category(data)

    books = result[result["product_category"] == "Books"].iloc[0]

    assert books["order_count"] == 2
    assert books["returns"] == 1
    assert books["return_rate"] == 0.5


def test_save_report(tmp_path):
    data = create_test_data()

    output_folder = tmp_path / "output"

    save_report(
        data,
        output_folder,
        "test_report.csv",
    )

    output_file = output_folder / "test_report.csv"

    assert output_file.exists()

    saved_data = pd.read_csv(output_file)

    assert len(saved_data) == 3
    assert list(saved_data.columns) == list(data.columns)