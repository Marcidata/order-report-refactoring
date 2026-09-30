import logging

import pandas as pd

from order_report.config import ReportConfig
from order_report.data_loader import load_orders
from order_report.processing import (
    apply_missing_value_defaults,
    calculate_order_values,
    prepare_orders,
)
from order_report.reports import (
    create_overview,
    create_returns_by_category,
    create_sales_report,
    save_report,
)
from order_report.validation import validate_orders


logger = logging.getLogger(__name__)


def configure_logging() -> None:
    """Configure application logging."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(levelname)s: %(message)s",
    )


def main() -> int:
    """Run the order reporting application."""

    configure_logging()

    config = ReportConfig()

    try:
        logger.info("Starting order report")

        data = load_orders(config.input_file)

        logger.info("Loaded %d rows", len(data))

        validate_orders(data)
        logger.info("Validation completed")

        data = prepare_orders(data)
        data = apply_missing_value_defaults(data)
        data = calculate_order_values(data)

        overview = create_overview(data)
        save_report(
            overview,
            config.output_folder,
            config.overview_filename,
        )

        sales_by_category = create_sales_report(
            data,
            "product_category",
        )
        save_report(
            sales_by_category,
            config.output_folder,
            config.sales_by_category_filename,
        )

        sales_by_region = create_sales_report(
            data,
            "region",
        )
        save_report(
            sales_by_region,
            config.output_folder,
            config.sales_by_region_filename,
        )

        returns_by_category = create_returns_by_category(data)
        save_report(
            returns_by_category,
            config.output_folder,
            config.returns_by_category_filename,
        )

        logger.info("Reports created successfully")
        logger.info("Reports saved to %s", config.output_folder)
        logger.info("Order report completed successfully")

        return 0

    except (
        FileNotFoundError,
        ValueError,
        pd.errors.ParserError,
    ) as error:
        logger.error("Order report failed: %s", error)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())