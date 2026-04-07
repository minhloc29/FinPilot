import json
import os
import re

import json_repair


def load_json_string(json_string: str) -> dict | list | None:
    try:
        parsed = json_repair.loads(json_string)
        if not isinstance(parsed, (dict, list)):
            return None
        return parsed
    except json.JSONDecodeError:
        return None


def fix_json_string(json_string: str) -> str:
    return json_repair.repair_json(json_string)


def extract_json_from_text(text: str, extract_all: bool = False) -> dict | list[dict | list]:
    try:
        json_objects = []
        used_positions = set()

        text = re.sub(r'\\(?![\"\\/bfnrtu])', r'\\\\', text)

        for match in re.finditer(r"```json(.*?)```", text, re.DOTALL):
            json_text = match.group(1).strip()
            try:
                parsed = json_repair.loads(json_text)
                if isinstance(parsed, (dict, list)):
                    json_objects.append(parsed)
                    used_positions.update(range(match.start(), match.end()))
            except json.JSONDecodeError:
                pass

        first_brace = text.find("{")
        last_brace = text.rfind("}")
        if (
            first_brace != -1
            and last_brace != -1
            and first_brace < last_brace
            and not any(pos in used_positions for pos in range(first_brace, last_brace + 1))
        ):
            try:
                parsed = json_repair.loads(text[first_brace: last_brace + 1])
                if isinstance(parsed, (dict, list)):
                    json_objects.append(parsed)
                    used_positions.update(range(first_brace, last_brace + 1))
            except json.JSONDecodeError:
                pass

        first_bracket = text.find("[")
        last_bracket = text.rfind("]")
        if (
            first_bracket != -1
            and last_bracket != -1
            and first_bracket < last_bracket
            and not any(pos in used_positions for pos in range(first_bracket, last_bracket + 1))
        ):
            try:
                parsed = json_repair.loads(text[first_bracket: last_bracket + 1])
                if isinstance(parsed, (dict, list)):
                    json_objects.append(parsed)
            except json.JSONDecodeError:
                pass

        if extract_all:
            return json_objects
        return json_objects[0] if json_objects else None

    except Exception:
        return None