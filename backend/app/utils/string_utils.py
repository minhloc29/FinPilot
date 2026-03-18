import hashlib
import json
import os
import re
import string
from typing import Dict

import json_repair
import re

def make_cache_key(messages):
    serialized = json.dumps(messages, sort_keys=True)
    return "llm_cache:" + hashlib.sha256(serialized.encode()).hexdigest()

def normalize(text: str) -> str:
    return re.sub(r"\s+", "_", re.sub(r"[^\w\s]", "", text.lower()))


def compute_hash(content: str, hash_type="sha256") -> str:
    if hash_type == "md5":
        return hashlib.md5(content.encode("utf-8")).hexdigest()
    elif hash_type == "sha1":
        return hashlib.sha1(content.encode("utf-8")).hexdigest()
    elif hash_type == "sha512":
        return hashlib.sha512(content.encode("utf-8")).hexdigest()
    else:
        return hashlib.sha256(content.encode("utf-8")).hexdigest()


def remove_non_printing_characters(text: str) -> str:
    try:
        return "".join(c for c in text if c.isprintable() or c in {"\r", "\n", "\t"})
    except Exception as e:
        if os.getenv("DEBUG_TOOLKIT", "false").lower() == "true":
            print(f"Error in remove_non_printing_characters({text}): {e}")
        return text


def remove_punctuation(text: str) -> str:
    if not text:
        return ""

    text = text.lower()
    text = re.sub(r"\s+", " ", text).strip()
    text = text.translate(str.maketrans("", "", string.punctuation))

    return text


def check_and_remove_last_occurrence(text: str, subword: str) -> tuple[bool, str]:
    try:
        found = re.search(re.escape(subword), text) is not None
        if found:
            pattern = rf"\S*{re.escape(subword)}\S*"
            matches = list(re.finditer(pattern, text))
            if matches:
                last_match = matches[-1]
                start, end = last_match.span()
                text = text[:start] + text[end:]
                text = re.sub(r"\s+", " ", text).strip()
        return True if found else False, text
    except Exception as e:
        if os.getenv("DEBUG_TOOLKIT", "false").lower() == "true":
            print(f"Error in check_and_remove_last_occurrence({text}, {subword}): {e}")
        return False, text


def remove_numbers_in_parentheses(text: str) -> str:
    try:
        updated_text = re.sub(r"\(\d+\)", "", text)
        return updated_text
    except Exception as e:
        if os.getenv("DEBUG_TOOLKIT", "false").lower() == "true":
            print(f"Error in remove_numbers_in_parentheses({text}): {e}")
        return text


def check_number_in_parentheses(text: str) -> int | None:
    try:
        match = re.search(r"\((\d+)\)", text)
        if match:
            return int(match.group(1))
        return None
    except Exception as e:
        if os.getenv("DEBUG_TOOLKIT", "false").lower() == "true":
            print(f"Error in check_number_in_parentheses({text}): {e}")
        return None


def is_number(s: str) -> bool:
    try:
        float(s)
        return True
    except Exception:
        return False


def is_integer_number(s: str) -> bool:
    try:
        return int(s) == float(s)
    except Exception:
        return False


def extract_integers(text: str) -> list[int]:
    try:
        integers = re.findall(r"\b\d+\b", text)
        return [int(num) for num in integers if is_integer_number(num)]
    except Exception as e:
        if os.getenv("DEBUG_TOOLKIT", "false").lower() == "true":
            print(f"Error in extract_integers({text}): {e}")
        return []


def parse_dict_to_string(dict_obj: dict, kv_str_format: str = "{key}: {value}") -> str:
    try:
        output = []
        for k, v in dict_obj.items():
            output.append(kv_str_format.format(key=k, value=v))
        return "\n".join(output).strip()
    except Exception as e:
        if os.getenv("DEBUG_TOOLKIT", "false").lower() == "true":
            print(f"Error in parse_dict_to_string({dict_obj}, {kv_str_format}): {e}")
        return ""


def slot_filling(
    text: str,
    key_value_mapping: dict | None = None,
    object_dict: dict | None = None,
) -> str:
    try:
        no_change = False
        while not no_change:
            placeholders = re.findall(r"{{(.*?)}}", text)
            old_text = text
            mapping_dict = {}
            for placeholder in placeholders:
                if placeholder in mapping_dict:
                    continue
                if isinstance(object_dict, dict) and placeholder in object_dict:
                    mapping_dict[placeholder] = object_dict[placeholder]["value"]
                elif (
                    isinstance(key_value_mapping, dict)
                    and placeholder in key_value_mapping
                ):
                    mapping_dict[placeholder] = key_value_mapping[placeholder]
            for mapping_key in mapping_dict:
                text = text.replace(
                    "{{" + mapping_key + "}}",
                    str(mapping_dict.get(mapping_key, "{{" + mapping_key + "}}")),
                )
            no_change = text == old_text
        return text
    except Exception as e:
        if os.getenv("DEBUG_TOOLKIT", "false").lower() == "true":
            print(
                f"Error in slot_filling({text}, {key_value_mapping}, {object_dict}): {e}"
            )
        return text


def load_json_string(json_string: str) -> dict | list | None:
    try:
        parsed_json = json_repair.loads(json_string)
        if not isinstance(parsed_json, (dict, list)):
            return None
        return parsed_json
    except json.JSONDecodeError:
        return None


def fix_json_string(json_string: str) -> str:
    return json_repair.repair_json(json_string)


def extract_json_from_text(
    text: str, extract_all: bool = False
) -> dict | list[dict | list]:
    try:
        json_objects = []
        used_positions = set()

        text = re.sub(r'\\(?!["\\/bfnrtu])', r"\\\\", text)

        json_code_blocks = re.finditer(r"```json(.*?)```", text, re.DOTALL)
        for match in json_code_blocks:
            json_text = match.group(1).strip()
            try:
                parsed = json_repair.loads(json_text)
                if isinstance(parsed, (dict, list)):
                    json_objects.append(parsed)
                    used_positions.update(range(match.start(), match.end()))
            except json.JSONDecodeError:
                pass

        first_brace_pos = text.find("{")
        last_brace_pos = text.rfind("}")
        if (
            first_brace_pos != -1
            and last_brace_pos != -1
            and first_brace_pos < last_brace_pos
            and not any(
                pos in used_positions
                for pos in range(first_brace_pos, last_brace_pos + 1)
            )
        ):
            json_text = text[first_brace_pos : last_brace_pos + 1]
            try:
                parsed = json_repair.loads(json_text)
                if isinstance(parsed, (dict, list)):
                    json_objects.append(parsed)
                    used_positions.update(range(first_brace_pos, last_brace_pos + 1))
            except json.JSONDecodeError:
                pass

        first_bracket_pos = text.find("[")
        last_bracket_pos = text.rfind("]")
        if (
            first_bracket_pos != -1
            and last_bracket_pos != -1
            and first_bracket_pos < last_bracket_pos
            and not any(
                pos in used_positions
                for pos in range(first_bracket_pos, last_bracket_pos + 1)
            )
        ):
            json_text = text[first_bracket_pos : last_bracket_pos + 1]
            try:
                parsed = json_repair.loads(json_text)
                if isinstance(parsed, (dict, list)):
                    json_objects.append(parsed)
                    used_positions.update(
                        range(first_bracket_pos, last_bracket_pos + 1)
                    )
            except json.JSONDecodeError:
                pass

        all_candidates = []

        for match in re.finditer(r"\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}", text, re.DOTALL):
            if not any(
                pos in used_positions for pos in range(match.start(), match.end())
            ):
                all_candidates.append((match.start(), match.end(), match.group()))

        for match in re.finditer(
            r"\[[^\[\]]*(?:\[[^\[\]]*\][^\[\]]*)*\]", text, re.DOTALL
        ):
            if not any(
                pos in used_positions for pos in range(match.start(), match.end())
            ):
                all_candidates.append((match.start(), match.end(), match.group()))

        all_candidates.sort(key=lambda x: (x[0], -x[1]))

        for start, end, json_text in all_candidates:
            if any(pos in used_positions for pos in range(start, end)):
                continue

            try:
                parsed = json_repair.loads(json_text)
                if isinstance(parsed, (dict, list)):
                    json_objects.append(parsed)
                    used_positions.update(range(start, end))
            except json.JSONDecodeError:
                pass

        if extract_all:
            return json_objects
        else:
            return json_objects[0] if json_objects else None
    except Exception as e:
        if os.getenv("DEBUG_TOOLKIT", "false").lower() == "true":
            print(f"Error in extract_json_from_text({text}, {extract_all}): {e}")
        return None



def extract_integer_numbers_from_text(text: str) -> Dict[str, int]:
    try:
        number_strings = re.findall(
            r"[-+]?\d{1,3}(?:\.\d{3})+|[-+]?\d{1,3}(?:,\d{3})+|[-+]?\d+", text
        )
        numbers = {}
        for num_str in number_strings:
            try:
                clean_num = re.sub(r"[.,]", "", num_str)
                numbers[num_str] = int(clean_num)
            except ValueError:
                continue
        return numbers
    except Exception as e:
        if os.getenv("DEBUG_TOOLKIT", "false").lower() == "true":
            print(f"Error in extract_integer_numbers_from_text({text}): {e}")
        return {}

def resolve_symbol(message: str, symbol_db):
    tokens = re.findall(r"[A-Z]{2,4}", message.upper())

    for token in tokens:
        # if symbol_db.has_symbol(token):
        return token

    return None