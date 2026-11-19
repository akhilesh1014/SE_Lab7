# Lab 7 fuzz testing

```sh
python -m pip install -r requirements-dev.txt
python -m pytest -q test_library_fines.py
python library_fines.py
```

The starter assigns all three functions to `library_fines.py`. The
application accepts a hyphenated alphabetic prefix and decimal member
number, comma-separated nonnegative whole day counts, and titles with two
or more words. Direct calls reject malformed inputs with `ValueError`.
The CLI reports validation errors and moves to the next prompt.

| Example input | Expected result |
| --- | --- |
| `STU-1023` | `('STU', 1023)` |
| `10,20,30` | `44` |
| `The Hobbit` | `TH` |
| `Dune` | Validation error for a single-word title |

The supplied Hypothesis tests exercise valid output properties and invalid
input handling. Hypothesis could not be installed for the recorded runs.
`python verify_seeded_inputs.py` exercises 314 cases with a fixed seed.
The starter failed 107 of those checks and the fixed version passed all 314.
[The evidence PDF](Lab7_Fuzz_Test_Evidence.pdf) records these checks and
the before/after CLI output.
