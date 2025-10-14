# Pentagi Taxonomy GitHub Installation Test

This directory contains a test suite that validates the GitHub installation instructions from the main README.

## Quick Run

```bash
# Run all tests
bash run_tests.sh
```

This will:
1. Create/activate a virtual environment
2. Install v1 from GitHub and run tests
3. Uninstall v1
4. Install v2 from GitHub and run tests
5. Display results

## Files

- `test_venv/` - Python virtual environment
- `test_v1.py` - Test script for version 1
- `test_v2.py` - Test script for version 2
- `run_tests.sh` - Main test runner
- `TEST_RESULTS.md` - Detailed test results and findings

## What Gets Tested

### Version 1
- Target and Port entities
- HAS_PORT and DISCOVERED edges
- Field validation (IP regex, port ranges, enums)
- JSON serialization

### Version 2
- Target, Port, and Vulnerability entities
- HAS_PORT, DISCOVERED, and AFFECTS edges
- New fields (discovered_at timestamps)
- Extended enums and validation

## Installation Commands Tested

```bash
# v1
pip install "git+https://github.com/zavgorodnii/pentagi-taxonomy.git#subdirectory=v1/python"

# v2
pip install "git+https://github.com/zavgorodnii/pentagi-taxonomy.git#subdirectory=v2/python"
```

Both commands work as documented in the main README!

