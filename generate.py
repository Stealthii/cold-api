"""
Cold API data exporter
======================

Fetches API data and generates JSON for use with Jekyll site.

"""

import json
from pathlib import Path
import sys

import httpx

API_PATH = "https://storage.googleapis.com/cold-api/"
DATA_PATH = Path("data")
SITE_PATH = Path("public")

NAMES = [
    "artifacts_config",
    "contracts",
    "contributors",
    "live_config",
    "mission_reward_count",
    "notation",
    "roles",
]


def data_gen() -> None:
    """Generates data for Cold API."""

    client = httpx.Client(base_url=API_PATH)

    for name in NAMES:
        if Path(DATA_PATH / f"{name}.json").is_file():
            # Load local data
            print(f"Loading {name} from local data...")
            with Path(DATA_PATH / f"{name}.json").open("r", encoding="UTF-8") as fh:
                data = json.load(fh)
        else:
            # Fetch data from Cold API
            try:
                print(f"Fetching {name} from Cold API...")
                data = client.get(f"{name}.json").json()
            except httpx.HTTPError as err:
                print(f"Failed to retrieve {name} from {API_PATH}")
                sys.exit(1)
            except json.JSONDecodeError as err:
                print(f"Could not decode JSON from {name} at {API_PATH}")
                sys.exit(1)

        with Path(SITE_PATH / f"{name}.json").open("w", encoding="UTF-8") as fh:
            json.dump(data, fh)
        with Path(SITE_PATH / f"{name}.pretty.json").open("w", encoding="UTF-8") as fh:
            json.dump(data, fh, indent=2, ensure_ascii=False)

        print(f"Generated data for {name} successfully!")


if __name__ == "__main__":
    data_gen()
