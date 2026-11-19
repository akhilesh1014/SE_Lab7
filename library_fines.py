"""Validate library records and calculate fines for overdue books."""

import re


def parse_member_id(member_id):
    """Return an uppercase alphabetic prefix and a nonnegative ID number."""
    if not isinstance(member_id, str):
        raise ValueError("member ID must be text")
    match = re.fullmatch(r"([A-Za-z]+)-([0-9]+)", member_id.strip())
    if match is None:
        raise ValueError("member ID must contain letters, a hyphen, and digits")
    member_type, number = match.groups()
    return member_type.upper(), int(number)


def total_fine(days_csv):
    """Return two units per day past 14 for each nonnegative day count."""
    if not isinstance(days_csv, str):
        raise ValueError("days kept must be comma-separated text")
    fields = [field.strip() for field in days_csv.split(",")]
    if any(re.fullmatch(r"[0-9]+", field) is None for field in fields):
        raise ValueError("enter one or more nonnegative whole day counts")
    return sum(2 * max(int(field) - 14, 0) for field in fields)


def shelf_code(title):
    """Return the initials of the first two words in uppercase."""
    if not isinstance(title, str):
        raise ValueError("title must be text")
    words = title.split()
    if len(words) < 2:
        raise ValueError("title must contain at least two words")
    return (words[0][0] + words[1][0]).upper()


def main():
    """Prompt for each operation and report invalid input at the prompt."""
    prompts = (
        (
            parse_member_id,
            "Enter a member ID (e.g. STU-1023): ",
            "Member Type and Number",
        ),
        (
            total_fine,
            "Enter days kept for each book as CSV (e.g. 10,20,30): ",
            "Total Fine",
        ),
        (
            shelf_code,
            "Enter a book title with at least two words: ",
            "Shelf Code",
        ),
    )
    for operation, prompt, label in prompts:
        print(f"==== Running {operation.__name__} ====")
        try:
            print(f"{label}: {operation(input(prompt))}")
        except ValueError as error:
            print(f"Invalid input: {error}")
        except EOFError:
            print("Input ended.")
            break
        print()


if __name__ == "__main__":
    main()
