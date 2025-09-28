# sanity string json and convert to dict
import json
def str_to_dict(s: str) -> dict:
    try:
        # Attempt to parse the string as JSON
        return json.loads(s)
    except json.JSONDecodeError as e:
        # If parsing fails, return an empty dictionary or handle the error as needed
        return e