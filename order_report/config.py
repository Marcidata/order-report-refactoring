from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class ReportConfig:
    """Configuration for the order reporting application."""

    input_file: Path = Path("data/orders.csv")
    output_folder: Path = Path("output")

    overview_filename: str = "overview.csv"
    sales_by_category_filename: str = "sales_by_category.csv"
    sales_by_region_filename: str = "sales_by_region.csv"
    returns_by_category_filename: str = "returns_by_category.csv"