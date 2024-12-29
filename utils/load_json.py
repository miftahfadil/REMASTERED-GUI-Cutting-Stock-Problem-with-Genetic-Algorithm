import json
from typing import Dict
from typing import Any

def load_json_data(path) -> Dict[str, Any] | None:
    metadata = None
    if path:
        with open(path, "r") as json_file:
            metadata = json.load(json_file)
    
    return metadata
