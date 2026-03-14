import glob
import json
import os

import jsonlines


def read_txt_lines(path: str) -> list[str]:
    try:
        with open(path, encoding="utf-8", mode="r") as reader:
            lines = reader.readlines()
        return lines
    except Exception as e:
        if os.getenv("DEBUG_TOOLKIT", "false").lower() == "true":
            print(f"Error in read_txt_lines({path}): {e}")
        return []


def write_txt_lines(lines: list[str], path: str, mode: str = "w") -> None:
    try:
        create_parent_directory_from_path(path)
        with open(path, mode=mode, encoding="utf-8") as writer:
            for line in lines:
                writer.write(line)
                writer.write("\n")
    except Exception as e:
        if os.getenv("DEBUG_TOOLKIT", "false").lower() == "true":
            print(f"Error in write_txt_lines({lines}, {path}, {mode}): {e}")


def read_txt(path: str) -> str:
    try:
        lines = read_txt_lines(path)
        txt = "".join(lines)
        return txt
    except Exception as e:
        if os.getenv("DEBUG_TOOLKIT", "false").lower() == "true":
            print(f"Error in read_txt({path}): {e}")
        return ""


def write_txt(path: str, data: str) -> None:
    try:
        create_parent_directory_from_path(path)
        with open(path, mode="w", encoding="utf-8") as f:
            f.write(data)
    except Exception as e:
        if os.getenv("DEBUG_TOOLKIT", "false").lower() == "true":
            print(f"Error in write_txt({path}, {data}): {e}")


def read_json(path: str) -> dict:
    try:
        with open(path, encoding="utf-8") as fi:
            data = json.load(fi)
        return data
    except Exception as e:
        if os.getenv("DEBUG_TOOLKIT", "false").lower() == "true":
            print(f"Error in read_json({path}): {e}")
        return {}


def write_json(
    path: str, data: list | dict, intent: int = 2, merge_if_exist: bool = False
) -> None:
    try:
        create_parent_directory_from_path(path)
        if merge_if_exist and os.path.exists(path):
            if os.getenv("DEBUG_TOOLKIT", "false").lower() == "true":
                print(f"Merging data into existing JSON file: {path}")

            write_data = read_json(path)
            if isinstance(write_data, list):
                write_data.extend(data)
            elif isinstance(write_data, dict):
                write_data.update(data)
        else:
            write_data = data

        with open(path, "w", encoding="utf-8") as f:
            json.dump(write_data, f, indent=intent, ensure_ascii=False)
    except Exception as e:
        if os.getenv("DEBUG_TOOLKIT", "false").lower() == "true":
            print(
                f"Error in write_json({path}, {data}, {intent}, {merge_if_exist}): {e}"
            )


def read_jsonlines(path: str) -> list[dict]:
    try:
        lines = []
        with jsonlines.open(path) as reader:
            for line in reader:
                lines.append(line)
        return lines
    except Exception as e:
        if os.getenv("DEBUG_TOOLKIT", "false").lower() == "true":
            print(f"Error in read_jsonlines({path}): {e}")
        return []


def write_jsonlines(path: str, lines: list[dict], mode: str = "w") -> None:
    try:
        create_parent_directory_from_path(path)
        with jsonlines.open(path, mode=mode) as writer:
            for line in lines:
                writer.write(line)
    except Exception as e:
        if os.getenv("DEBUG_TOOLKIT", "false").lower() == "true":
            print(f"Error in write_jsonlines({path}, {lines}, {mode}): {e}")


def create_parent_directory_from_path(path: str) -> None:
    try:
        dir_name = os.path.dirname(path)
        if dir_name and not os.path.exists(dir_name):
            os.makedirs(dir_name)
    except Exception as e:
        if os.getenv("DEBUG_TOOLKIT", "false").lower() == "true":
            print(f"Error in create_parent_directory_from_path({path}): {e}")


def get_list_files(dir: str, ignore_file_list: list[str]) -> list[str]:
    try:
        files = []
        for file in glob.glob(os.path.join(dir, "*")):
            file_name = os.path.basename(file)
            if file_name not in ignore_file_list:
                files.append(file_name)
        return files
    except Exception as e:
        if os.getenv("DEBUG_TOOLKIT", "false").lower() == "true":
            print(f"Error in get_list_files({dir}, {ignore_file_list}): {e}")
        return []
