# W8 MAIN PIPELINE
# Goal:
# Run the complete Week 8 machine learning workflow.
#
# Pipeline:
# 1. Train, compare and save the best model
# 2. Generate evaluation visualizations
# 3. Generate prediction


from pathlib import Path
import subprocess
import sys


# Project Directory

PROJECT_DIR = Path(__file__).resolve().parent.parent


# Run Module

def run_module(module_name):
    """
    Execute an individual pipeline module.
    """

    print("\n" + "=" * 60)
    print(f"Running: {module_name}")
    print("=" * 60)

    result = subprocess.run(
        [
            sys.executable,
            "-m",
            module_name,
        ],
        cwd=PROJECT_DIR,
    )

    if result.returncode != 0:
        print(f"\nError while running {module_name}")
        sys.exit(result.returncode)

    print(f"\nCompleted: {module_name}")


# Main Pipeline

def main():
    """
    Execute the complete Week 8 workflow.
    """

    # Train, compare and save the best model
    run_module("src.compare_models")

    # Generate evaluation visualizations
    run_module("src.evaluate")

    # Generate predictions using the best model
    run_module("src.predict")

    print("\n" + "=" * 60)
    print("WEEK 8 PIPELINE COMPLETED SUCCESSFULLY")
    print("=" * 60)


if __name__ == "__main__":
    main()