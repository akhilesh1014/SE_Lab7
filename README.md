# Lab 7 — Fuzz Testing

This lab tests input validation in the [library fines application](library_fines.py). The program parses a member ID, calculates fines from comma-separated loan durations, and generates a shelf code from a book title.

## Run the demo and tests

```sh
python -m pip install -r requirements-dev.txt
python library_fines.py
python -m pytest -q test_library_fines.py
python verify_seeded_inputs.py
```

| Example input | Expected result |
| --- | --- |
| `STU-1023` | Member type `STU`, number `1023` |
| `10,20,30` | Total fine of `44` |
| `The Hobbit` | Shelf code `TH` |
| `Dune` | Validation error because the title has only one word |

## Results

The starter failed 107 of the 314 seeded checks. The fixed implementation passed all 314. The [evidence PDF](Lab7_Fuzz_Test_Evidence.pdf) records those checks and the before-and-after CLI output. The [Hypothesis suite](test_library_fines.py) is included and was unavailable for the recorded run.
