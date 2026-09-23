import argparse

parser = argparse.ArgumentParser(description="Analyze a data file")

parser.add_argument("--input",
    "-i",
    required=True,
    help="Path to input CSV file")

parser.add_argument("--output",
    "--o",
    default="results.txt",
    help="Output file path")

parser.add_argument("--verbose",
                    "-v",
                    action="store_true",
                    help="Print detailed information")

args = parser.parse_args()

