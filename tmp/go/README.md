# Go Multi-Version Import Test

This test application demonstrates importing and using both v1 and v2 of the Pentagi Taxonomy from GitHub simultaneously.

## What This Tests

- Importing `github.com/zavgorodnii/pentagi-taxonomy/v1/go/entities` as v1
- Importing `github.com/zavgorodnii/pentagi-taxonomy/v2/go/entities` as v2  
- Creating and validating entities from both versions
- Using version-specific features (e.g., v2's Vulnerability entity and "scanning" status)

## Running the Test

```bash
# Initialize the module and fetch dependencies from GitHub
go mod tidy

# Run the test
go run main.go
```

## Expected Output

The test should:
1. Create and validate v1 entities (Target, Port, HasPort edge)
2. Create and validate v2 entities (Target, Port, Vulnerability, Affects edge)
3. Show that both versions work correctly in the same application

## Key Differences Between Versions

### V1
- Target statuses: `active`, `inactive`
- Entities: Target, Port
- Edges: HAS_PORT, DISCOVERED

### V2  
- Target statuses: `active`, `inactive`, `scanning` (added)
- Target types: includes `domain` (added)
- New entity: Vulnerability
- New edge: AFFECTS
- All entities have `discovered_at` timestamp field (added)

