# Pentagi Taxonomy TypeScript Test Application

This TypeScript application successfully demonstrates importing and using **both version 1 and version 2** of the Pentagi Taxonomy from GitHub using the gitpkg installation method.

## What This Test Proves

✅ **gitpkg Installation Works**: Both v1 and v2 packages installed successfully from GitHub  
✅ **Simultaneous Version Usage**: Both versions imported and used in the same application  
✅ **Type Safety**: Zod schemas provide runtime validation for all entities  
✅ **Version Differences**: Clearly shows evolution from V1 to V2  

## Key Results

### V1 Features Successfully Tested
- TargetSchema with basic fields
- PortSchema with network port validation
- DiscoveredSchema edge relationships
- Status enums: `active`, `inactive`
- Target types: `host`, `web_service`, `api`

### V2 Features Successfully Tested  
- TargetSchema with **additional fields** (`discovered_at`)
- PortSchema with **additional fields** (`discovered_at`)
- **VulnerabilitySchema** (NEW in V2!)
- **AffectsSchema** edge (NEW in V2!)
- Status enums: `active`, `inactive`, **`scanning`** (NEW!)
- Target types: `host`, `web_service`, `api`, **`domain`** (NEW!)

### Multi-Version Validation
- Same data successfully validated against both V1 and V2 schemas
- Version-specific handling implemented as shown in README examples
- Taxonomy version constants working properly (V1=1, V2=2)

## Installation Method Used

```json
{
  "dependencies": {
    "@pentagi/taxonomy-v1": "https://gitpkg.now.sh/zavgorodnii/pentagi-taxonomy/v1/typescript?main&scripts.postinstall=npm%20install%20--ignore-scripts%20%26%26%20npm%20run%20build",
    "@pentagi/taxonomy-v2": "https://gitpkg.now.sh/zavgorodnii/pentagi-taxonomy/v2/typescript?main&scripts.postinstall=npm%20install%20--ignore-scripts%20%26%26%20npm%20run%20build"
  }
}
```

## Running the Test

```bash
npm install  # Installs packages from GitHub via gitpkg
npm run test # Runs the comprehensive test suite
```

## Test Output Summary

```
🚀 Testing Pentagi Taxonomy - Multiple Versions from GitHub
============================================================

📦 Testing Version 1 (V1) imports...
📋 V1 Taxonomy version: 1
✅ V1 Target created and validated successfully:
{
  "uuid": "target-v1-123",
  "hostname": "example-v1.com",
  "ip_address": "192.168.1.100",  ← IP validation now works!
  "target_type": "host",
  "risk_score": 7.5,
  "status": "active"
}

📦 Testing Version 2 (V2) imports...
📋 V2 Taxonomy version: 2
✅ V2 Target created and validated successfully:
{
  "uuid": "target-v2-789",
  "hostname": "example-v2.com", 
  "ip_address": "10.0.0.1",  ← IP validation works in V2 too!
  "target_type": "domain",
  "risk_score": 8.5,
  "status": "scanning",
  "discovered_at": 1760542715.158
}

🎯 Testing version-specific handling...
✅ Multi-version validation successful with IP addresses!

✨ All tests passed! Both V1 and V2 schemas loaded from GitHub successfully.
🎉 gitpkg installation method works perfectly!
🔧 Regex validation bug fixed - IP addresses now validate correctly!
```

## Bug Fix Validated

During testing, we discovered and fixed a bug in the TypeScript code generator (`codegen/typescript/generate.py`) where regex patterns were being double-escaped, causing IP address validation to fail. The fix was simple:

**Before (buggy):**
```python
regex = field_def["regex"].replace("\\", "\\\\")  # Double-escaping
```

**After (fixed):**
```python  
regex = field_def["regex"]  # Use regex as-is
```

This fix ensures that all `regex` constraints in the YAML schema work correctly in the generated TypeScript/Zod schemas.

## Conclusion

This test successfully validates the instructions in the main README about using gitpkg to install the Pentagi Taxonomy packages from GitHub subdirectories and use multiple versions simultaneously in a TypeScript application. It also confirms that regex validation (including IP addresses) works correctly after the bug fix.
