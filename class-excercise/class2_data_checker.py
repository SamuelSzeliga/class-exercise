import argparse
import csv
import sys
from pathlib import Path

#Step 1
import logging

def check_data(filename):
    """Read the CSV file and check for missing values."""
    with open(filename, "r") as f:
        reader = csv.reader(f)
        rows = list(reader)

    header = rows[0]
    data = rows[1:]
    missing_rows = []

    for row_number, row in enumerate(data, start=2):
        if any(value == "" for value in row):
            missing_rows.append(row_number)

    return header, data, missing_rows


#Step 2
# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)-8s %(message)s",
    datefmt="%H:%M:%S"
)
# Create a module-level logger
logger = logging.getLogger(__name__)


# TODO 1: Create an ArgumentParser
# Description: "Check the quality of a CSV file."
parser = argparse.ArgumentParser(description="Check the quality of a CSV file")


# TODO 2: Add a named argument (required):
# Long form: --input
# Short form: -i
# Help: "CSV file to check"
parser.add_argument("--input",
    "-i",
    required=True,
    help="CSV file to check")


# TODO 3: Add an named argument (optional):
# Long form: --output
# Short form: -o
# Default: "data_quality.txt"
# Help: "Output report filename"
parser.add_argument("--output",
    "--o",
    default="data_quality.txt",
    help="Output report filename")


# TODO 4: Add a boolean flag:
# Long form: --verbose
# Short form: -v
# Use action="store_true"
# Help: "Show detailed DEBUG messages"
parser.add_argument("--verbose",
    "-v",
    action="store_true",
    help="Show detailed DEBUG messages")


# TODO 5: Parse the command-line arguments
args = parser.parse_args()


#Step 3
if args.verbose:
    logger.setLevel(logging.DEBUG)


#Step 4
#print(f"Arguments parsed; filename={args.input}")
logger.debug(f"Arguments parsed: filename={args.input}")


# Check if the file exists 
#p = Path(args.input)
#if not p.is_file():
    #print(f"File not found: '{args.input}'")
    #sys.exit(1)
#print(f"File validated: '{args.input}'")

#Step 5
p = Path(args.input)
if not p.is_file():
    logger.error(f"File not found: '{args.input}'")
    sys.exit(1)
    
logger.info(f"File validated: '{args.input}'")

#Step 6
logger.debug(f"Loading data from: '{args.input}'")


# Check the data
header, data, missing_rows = check_data(args.input)

#Step 7
logger.info(f"Loaded {len(data)} rows")

for row_number in missing_rows:
    logger.warning(f"Row {row_number} has missing values")

#Step 8
if len(data) == 0:
    logger.error("Input file contains no data; cannot continue")
    sys.exit(1)


# Save the report
with open(args.output, "w") as f:
    f.write(f"Number of rows: {len(data)}\n")
    f.write(f"Number of columns: {len(header)}\n")
    f.write(f"Number of rows with missing values: {len(missing_rows)}\n")

#Step 10
logger.info(f"Report saved to {args.output}")