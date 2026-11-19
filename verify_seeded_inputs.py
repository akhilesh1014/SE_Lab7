"""Independent, deterministic checks for the valid and invalid data contracts."""
import importlib.util
from pathlib import Path
from random import Random
import string
import sys

path = Path("library_fines.py").resolve()
spec = importlib.util.spec_from_file_location("library_fines", path)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

random = Random(42)

def word():
    return "".join(random.choices(string.ascii_letters, k=random.randint(1, 12)))

def valid_id():
    prefix, number = word(), random.randint(0, 10**12)
    return f" {prefix}-00{number} ", (prefix.upper(), number)

def valid_csv():
    values = [random.randrange(500) for _ in range(random.randint(1, 12))]
    return ", ".join(map(str, values)), sum((n - 14) * 2 for n in values if n > 14)

def valid_title():
    words = [word() for _ in range(random.randint(2, 5))]
    return " ".join(words), (words[0][0] + words[1][0]).upper()

cases = (
    (module.parse_member_id, valid_id, [None, "", "STU", "STU-abc", "STU--1"]),
    (module.total_fine, valid_csv, [None, "", "1,,3", "14,-1", "10,1.5"]),
    (module.shelf_code, valid_title, [None, "", " ", "Dune"]),
)

failures = []
checks = 0
for function, generate, invalid in cases:
    for _ in range(100):
        value, expected = generate()
        actual = function(value)
        checks += 1
        if actual != expected:
            failures.append(f"{function.__name__}({value!r}) returned {actual!r}")
    for value in invalid:
        checks += 1
        try:
            actual = function(value)
        except ValueError:
            continue
        except (TypeError, AttributeError, IndexError) as error:
            failures.append(f"{function.__name__}({value!r}): {type(error).__name__}")
        else:
            failures.append(f"{function.__name__}({value!r}) accepted: {actual!r}")

for failure in failures:
    print("FAIL", failure)
print(f"{checks - len(failures)} passed, {len(failures)} failed ({checks} checks, seed 42)")
sys.exit(bool(failures))
