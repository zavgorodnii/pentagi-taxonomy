# GitHub Installation Test Results

## Summary

✅ **All tests passed successfully!**

This test validates the README instructions for installing `pentagi-taxonomy` packages directly from GitHub.

## Test Environment

- **Location**: `/Users/aozav/pentagi-taxonomy/tmp/py/`
- **Virtual Environment**: `test_venv/`
- **Python Version**: 3.13
- **Repository**: `github.com/zavgorodnii/pentagi-taxonomy`

## What Was Tested

### Version 1 (v1)
- ✅ Installation from GitHub using: `pip install "git+https://github.com/zavgorodnii/pentagi-taxonomy.git#subdirectory=v1/python"`
- ✅ Successfully imported `pentagi_taxonomy` module (version 1)
- ✅ Created and validated **Target** entity with all fields
- ✅ Created and validated **Port** entity
- ✅ Created and validated **HAS_PORT** edge relationship
- ✅ Created and validated **DISCOVERED** edge relationship
- ✅ JSON serialization works correctly

### Version 2 (v2)
- ✅ Installation from GitHub using: `pip install "git+https://github.com/zavgorodnii/pentagi-taxonomy.git#subdirectory=v2/python"`
- ✅ Successfully imported `pentagi_taxonomy` module (version 2)
- ✅ Created and validated **Target** entity (with new `discovered_at` field)
- ✅ Created and validated **Port** entity (with new `discovered_at` field)
- ✅ Created and validated **Vulnerability** entity (NEW in v2)
- ✅ Created and validated **HAS_PORT** edge relationship
- ✅ Created and validated **AFFECTS** edge relationship (NEW in v2)
- ✅ Created and validated **DISCOVERED** edge relationship
- ✅ JSON serialization works correctly

## Key Differences Between Versions

### v1 Features
- 2 node types: Target, Port
- 2 edge types: HAS_PORT, DISCOVERED
- Status enum: `[active, inactive]`
- Target type enum: `[host, web_service, api]`

### v2 Features (Additions)
- **NEW**: Vulnerability node type
- **NEW**: AFFECTS edge type
- **NEW**: `discovered_at` timestamp fields on Target and Port
- Extended status enum: `[active, inactive, scanning]`
- Extended target type enum: `[host, web_service, api, domain]`

## Validation Tests

All entities were tested with:
1. **Type safety**: Pydantic models enforce correct types
2. **Field constraints**: 
   - IP address regex validation
   - Port number range (1-65535)
   - CVSS score range (0.0-10.0)
   - Risk score range (0.0-10.0)
   - Confidence range (0.0-1.0)
   - Enum validations (status, severity, impact, etc.)
3. **JSON serialization**: Models correctly serialize to JSON

## Installation Command Verification

The following commands from the README work correctly:

```bash
# Install v1 from GitHub
pip install "git+https://github.com/zavgorodnii/pentagi-taxonomy.git#subdirectory=v1/python"

# Install v2 from GitHub
pip install "git+https://github.com/zavgorodnii/pentagi-taxonomy.git#subdirectory=v2/python"
```

## Test Files

- `test_v1.py` - Comprehensive test for version 1
- `test_v2.py` - Comprehensive test for version 2
- `run_tests.sh` - Automated test runner for both versions

## Conclusion

The GitHub installation instructions in the README are **accurate and working correctly**. Users can successfully install and use the pentagi-taxonomy packages directly from GitHub as documented.

---

**Test Date**: October 15, 2025  
**Repository**: github.com/zavgorodnii/pentagi-taxonomy  
**Commit**: 1f08a0b5955af22ada3732575ba82093a0494800

