import json
import logging
from pathlib import Path

import pandas as pd
import yaml
import os
from dotenv import load_dotenv

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)-8s %(message)s",
    datefmt="%H:%M:%S"
)
logger = logging.getLogger(__name__)


def inspect_csv(filepath):
    """Read a CSV file and display basic information."""
    # TODO:
    # 1. Read the file using pd.read_csv().
    data = pd.read_csv(filepath)

    # 2. Log the filepath at INFO.
    logger.info(f"Inspecting CSV:{filepath.name}")
    
    # 3. Print the first three rows (e.g. DataFrame.head(3))
    print(data.head(3))


def inspect_json(filepath):
    """Read a JSON file and display basic information."""
    # TODO:
    # 1. Open the file and read it using json.load().
    with open(filepath, "r") as f:
        data = json.load(f)

    # 2. Log the filepath at INFO.
    logger.info(f"Inspecting {filepath.suffix}:{filepath.name}")

    # 3. Print the contents.
    print(data)


def inspect_yaml(filepath):
    """Read a YAML file and display basic information."""
    # TODO:
    # 1. Open the file and read it using yaml.safe_load().
    with open(filepath, "r") as f:
        config = yaml.safe_load(f)

    # 2. Log the filepath at INFO.
    logger.info(f"Inspecting {filepath.suffix}:{filepath.name}")

    # 3. Print the contents.
    print(config)


def inspect_env():
    """Read a .env file and display basic information."""
    load_dotenv()

    keys = [
        key for key in ["USERNAME", "PASSWORD"]
        if os.getenv(key) is not None
    ]

    logger.info(f"Inspecting {filepath.suffix}:{filepath.name}")
    print(keys)

    # TODO:
    # 1. Log at INFO that .env was loaded.
    # 2. Print keys.
    # Do not print passwords, API keys, or other secret values.


def main():
    # TODO:
    # 1. Create a Path object for the data directory.
    # 2. Use the / operator to build the CSV, JSON, and YAML paths.
    # 3. Call each inspection function using the matching path.
    # 4. Call inspect_env() without an argument.
    data_dir = Path("data")
    filepath_csv = data_dir / "sample.csv"
    filepath_json = data_dir / "sample.json"
    filepath_yaml = data_dir / "sample.yaml"

    inspect_csv("data/sample.csv")
    inspect_json(filepath_json)
    inspect_yaml(filepath_yaml)
    inspect_env()

if __name__ == "__main__":
    main()