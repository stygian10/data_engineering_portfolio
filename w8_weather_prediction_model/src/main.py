# W8 MAIN PIPELINE
# Goal:
# Run the complete Week 8 machine learning workflow.
#
# Pipeline:
# 1. Train, compare and save the best model
# 2. Generate evaluation visualizations
# 3. Generate prediction dataset


from pathlib import Path
import subprocess
import sys


# PROJECT DIRECTORY


SCRIPT_DIR = Path(__file__).resolve().parent


# RUN SCRIPT
# Execute an individual pipeline script.


def run_script(script_name):

    print("\n" + "=" * 60)
    print(f"Running: {script_name}")
    print("=" * 60)

    result = subprocess.run(
        [sys.executable, script_name],
        cwd=SCRIPT_DIR
    )

    if result.returncode != 0:

        print(f"\nError while running {script_name}")

        sys.exit(result.returncode)

    print(f"\nCompleted: {script_name}")


# MAIN PIPELINE
# Execute the complete Week 8 workflow.


def main():

    # Train, compare and save the best model
    run_script(
        "compare_models.py"
    )

    # Generate evaluation visualizations
    run_script(
        "evaluate.py"
    )

    # Generate predictions using the best model
    run_script(
        "predict.py"
    )

    print("\n" + "=" * 60)
    print("WEEK 8 PIPELINE COMPLETED SUCCESSFULLY")
    print("=" * 60)


if __name__ == "__main__":
    main()