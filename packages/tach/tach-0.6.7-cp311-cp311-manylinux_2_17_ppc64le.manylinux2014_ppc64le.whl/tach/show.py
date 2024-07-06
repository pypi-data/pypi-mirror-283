from __future__ import annotations

import json
from json.decoder import JSONDecodeError
from typing import TYPE_CHECKING
from urllib import error, request

if TYPE_CHECKING:
    from tach.core import ProjectConfig

TACH_SHOW_URL = "https://show.gauge.sh"


def generate_show_url(project_config: ProjectConfig) -> str | None:
    json_data = project_config.model_dump_json()
    json_bytes = json_data.encode("utf-8")
    req = request.Request(
        f"{TACH_SHOW_URL}/api/core/0.6.5/graph/",
        data=json_bytes,
        headers={"Content-Type": "application/json"},
    )

    try:
        # Send the request and read the response
        with request.urlopen(req) as response:
            response_data = response.read().decode("utf-8")
            response_json = json.loads(response_data)
            url = response_json.get("uid")
            return f"{TACH_SHOW_URL}?uid={url}"
    except (UnicodeDecodeError, JSONDecodeError, error.URLError) as e:
        print(f"Error: {e}")
        return None


__all__ = ["generate_show_url"]
