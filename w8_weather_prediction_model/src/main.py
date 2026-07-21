# W8 MAIN PIPELINE
# Goal:
# Run the complete Week 8 workflow.

from pathlib import Path
import subprocess
import sys


SCRIPT_DIR = Path(__file__).resolve().parent


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


def main():

    run_script("compare_models.py")
    run_script("evaluate.py")
    run_script("predict.py")

    print("\n" + "=" * 60)
    print("WEEK 8 PIPELINE COMPLETED SUCCESSFULLY")
    print("=" * 60)


if __name__ == "__main__":
    main()