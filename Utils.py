import json
from json import JSONDecodeError


def read_json(filepath : str):
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            data = json.load(file)
            print("Loaded" % filepath)
            file.close()
            return data

    except FileNotFoundError:
        print(f"Error: The file '{filepath}' could not be found.")

    except JSONDecodeError as e:
        print(f"Error: The file contains invalid JSON formatting.")
        print(f"Check line {e.lineno}, column {e.colno}: {e.msg}")

def write_json(filepath : str, data):
    with open(filepath, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, sort_keys=True)
        print("Write Success")
        file.close()

def get_all_dict(data) -> dict:
    datas = {}

    for key, value in data.items():
        datas[key] = value
    return datas

def get_all_list(data) -> list:
    datas = []

    for item in data:
        print(datas[item])
    return datas

