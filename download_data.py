from __future__ import annotations

from pathlib import Path

import requests
import pandas as pd

PROJECT_DIR = Path(__file__).resolve().parent

SITE_IDS = [
    "08193000",
    "08194000",
    "08194500",
    "08210000",
    "08210100",
    "08206900",
    "08206600",
    "08206700",
    "08205500",
    "08208000",
]


def get_usgs_site_metadata(site_ids: list[str]) -> pd.DataFrame:
    """Download monitoring-location metadata from the USGS OGC API."""

    identifiers = ",".join(f"USGS-{site_id}" for site_id in site_ids)

    url = (
        "https://api.waterdata.usgs.gov/ogcapi/v0/"
        "collections/monitoring-locations/items"
    )

    params = {
        "f": "json",
        "id": identifiers,
        "limit": len(site_ids),
    }

    response = requests.get(url, params=params, timeout=60)
    response.raise_for_status()

    geojson = response.json()

    rows = []
    for feature in geojson.get("features", []):
        properties = feature["properties"]
        longitude, latitude = feature["geometry"]["coordinates"]

        rows.append(
            {
                "site_id": properties.get("monitoring_location_number"),
                "site_name": properties.get("monitoring_location_name"),
                "latitude": latitude,
                "longitude": longitude,
                "site_type": properties.get("site_type"),
                "state": properties.get("state_name"),
                "county": properties.get("county_name"),
                "huc": properties.get("hydrologic_unit_code"),
                "basin_code": properties.get("basin_code"),
                "altitude_ft": properties.get("altitude"),
                "vertical_datum": properties.get("vertical_datum_name"),
                "drainage_area_sqmi": properties.get("drainage_area"),
                "contributing_area_sqmi": properties.get(
                    "contributing_drainage_area"
                ),
                "time_zone": properties.get("time_zone_abbreviation"),
            }
        )

    return pd.DataFrame(rows)


def main() -> None:
    metadata = get_usgs_site_metadata(SITE_IDS)
    print(metadata)
    metadata.to_csv(
        PROJECT_DIR / "usgs_gauge_metadata.csv",
        index=False,
    )


if __name__ == "__main__":
    main()
