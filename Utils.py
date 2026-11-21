import json
import re
from datetime import date
from json import JSONDecodeError


def read_json(filepath : str) -> dict:
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            data = json.load(file)
            print(f"Loaded {filepath}")
            file.close()
            return data

    except FileNotFoundError:
        with open(filepath, 'w', encoding='utf-8') as file:
            json.dump({}, file, indent=4, sort_keys=True)
            print(f"Created {filepath}")
            file.close()
        return {}

    except JSONDecodeError as e:
        print("Error: The file contains invalid JSON formatting.")
        print(f"Check line {e.lineno}, column {e.colno}: {e.msg}")

def write_json(filepath : str, data):
    with open(filepath, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, sort_keys=True)
        print("Write Success")
        file.close()

def update_json(filepath : str, data):
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


# The function below this commend is generate by AI
def luhn_check(number: str) -> bool:
    total = 0
    for i, digit in enumerate(reversed(number)):
        d = int(digit)
        if i % 2 == 1:
            d *= 2
            if d > 9:
                d -= 9
        total += d
    return total % 10 == 0


def validate_card_number(card_number: str) -> str | None:
    digits = re.sub(r"[\s-]", "", card_number)
    if not digits.isdigit():
        return "Card number must contain only digits."
    if not 13 <= len(digits) <= 19:
        return "Card number must be 13 to 19 digits long."
    if not luhn_check(digits):
        return "Card number is invalid."
    return None


def validate_cvv(cvv: str, card_number: str = "") -> str | None:
    if not cvv.isdigit():
        return "CVV must contain only digits."
    digits = re.sub(r"[\s-]", "", card_number)
    # American Express cards (starting 34 or 37) use a 4-digit CVV
    expected = 4 if digits.startswith(("34", "37")) else 3
    if len(cvv) != expected:
        return f"CVV must be {expected} digits."
    return None


def validate_expiry(expiry: str, today: date | None = None) -> str | None:
    match = re.fullmatch(r"(\d{2})/(\d{2})", expiry.strip())
    if not match:
        return "Expiry date must be in MM/YY format."
    month = int(match.group(1))
    year = 2000 + int(match.group(2))
    if not 1 <= month <= 12:
        return "Expiry month must be between 01 and 12."
    today = today or date.today()
    # A card is valid through the end of its expiry month
    if (year, month) < (today.year, today.month):
        return "This card has expired."
    return None
