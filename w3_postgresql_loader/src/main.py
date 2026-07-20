from create_tables import create_table
from load_data import load_data
from validate_load import validate_load


def run_pipeline():
    """
    Run the complete Week 3 PostgreSQL loading pipeline.
    """

    print("\n===== W3 PostgreSQL Loader =====\n")

    create_table()

    load_data()

    validate_load()

    print("\n===== W3 Pipeline Completed Successfully =====")


if __name__ == "__main__":
    run_pipeline()