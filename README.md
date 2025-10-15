# Pentagi Taxonomy

A versioned, multi-language entity taxonomy for penetration testing and security assessment tools. Define your entity schema once in YAML, and automatically generate type-safe code for Python, Go, and TypeScript.

## Overview

Pentagi Taxonomy is a code generation framework that helps you maintain consistent entity definitions across multiple programming languages. It's designed for penetration testing tools but can be adapted for any domain that requires versioned entity schemas.

**Key Features:**
- 🔄 **Single Source of Truth**: Define entities, fields, and relationships once in YAML
- 🛡️ **Type Safety**: Generate Pydantic models (Python), structs with validation (Go), and Zod schemas (TypeScript)
- 📦 **Multi-Version Support**: Maintain multiple schema versions simultaneously
- ✅ **Built-in Validation**: Comprehensive schema validation with field constraints
- 🚀 **Easy to Use**: Simple Makefile-based workflow

## Project Structure

```
pentagi-taxonomy/
├── version.yml              # Current global taxonomy version
├── v1/                      # Version 1 of the taxonomy
│   ├── entities.yml         # Entity definitions (nodes, edges, relationships)
│   ├── python/              # Generated Python package
│   ├── go/                  # Generated Go package
│   └── typescript/          # Generated TypeScript package
├── v2/                      # Version 2 of the taxonomy
│   ├── entities.yml
│   ├── python/
│   ├── go/
│   └── typescript/
├── codegen/                 # Code generation infrastructure
│   ├── python/
│   │   └── generate.py      # Python code generator
│   ├── go/
│   │   └── generate.py      # Go code generator
│   ├── typescript/
│   │   └── generate.py      # TypeScript code generator
│   ├── shared/
│   │   └── validator.py     # Schema validation logic
│   └── templates/           # Jinja2 templates for each language
│       ├── python/
│       ├── go/
│       └── typescript/
└── Makefile                 # Convenience commands for common tasks
```

## How It Works

1. **Define Schema**: Create or modify `entities.yml` in a version directory (e.g., `v2/entities.yml`)
2. **Validate**: Run validation to ensure schema correctness
3. **Generate Code**: Generate type-safe code for Python, Go, and TypeScript
4. **Use**: Import and use the generated packages in your projects

### Entity Schema Format

The `entities.yml` file defines three main sections:

#### 1. Nodes (Entities)

Nodes represent primary entities in your domain:

```yaml
nodes:
  Target:
    description: "A target system being assessed"
    fields:
      uuid:
        type: string
        description: "Unique identifier"
      hostname:
        type: string
        description: "DNS hostname if known"
      ip_address:
        type: string
        description: "IP address"
        regex: "^(?:[0-9]{1,3}\\.){3}[0-9]{1,3}$"
      status:
        type: string
        description: "Current status"
        enum: [active, inactive, scanning]
      risk_score:
        type: float
        description: "Risk score"
        min: 0.0
        max: 10.0
```

#### 2. Edges (Relationships)

Edges represent relationships between nodes:

```yaml
edges:
  HAS_PORT:
    description: "A target has a port"
    fields:
      timestamp:
        type: timestamp
        description: "When association was established"
  
  AFFECTS:
    description: "A vulnerability affects a target"
    fields:
      timestamp:
        type: timestamp
        description: "When identified"
      impact:
        type: string
        enum: [direct, indirect]
```

#### 3. Relationships

Define which nodes can be connected by which edges:

```yaml
relationships:
  - source: Target
    target: Port
    edges: [HAS_PORT]
  
  - source: Vulnerability
    target: Target
    edges: [AFFECTS]
```

### Supported Field Types

- `string` - Text values
- `int` - Integer numbers
- `float` - Floating-point numbers
- `boolean` - True/false values
- `timestamp` - Unix timestamps (float)
- Arrays: Add `[]` suffix (e.g., `string[]`, `int[]`)

### Field Constraints

- `enum: [value1, value2]` - Restrict to enumerated values (string only)
- `regex: "pattern"` - Validate against regex pattern (string only)
- `min: value` - Minimum value (numeric types only)
- `max: value` - Maximum value (numeric types only)
- `description: "text"` - Field documentation

## Quick Start

### Prerequisites

- Python 3.8+ (for code generation)
- Make (for convenience commands)
- Language-specific tools for using generated code:
  - Python: `pip`
  - Go: Go 1.19+
  - TypeScript: Node.js 16+

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourorg/pentagi-taxonomy.git
cd pentagi-taxonomy
```

2. Install code generation dependencies:
```bash
pip install -r codegen/requirements.txt
```

### Basic Usage

Generate code for the latest version (v2):

```bash
# Full workflow: validate → generate → test
make all VERSION=2

# Or step by step:
make validate VERSION=2      # Validate schema
make generate VERSION=2      # Generate code for all languages
make test VERSION=2          # Run tests
```

Generate code for a specific language:

```bash
make generate-python VERSION=2
make generate-go VERSION=2
make generate-typescript VERSION=2
```

## Makefile Commands

| Command | Description | Example |
|---------|-------------|---------|
| `make help` | Show all available commands | `make help` |
| `make all VERSION=N` | Run full cycle (validate → generate → test) | `make all VERSION=2` |
| `make validate VERSION=N` | Validate schema for version N | `make validate VERSION=2` |
| `make validate-all` | Validate all version schemas | `make validate-all` |
| `make generate VERSION=N` | Generate code for all languages | `make generate VERSION=2` |
| `make generate-python VERSION=N` | Generate only Python code | `make generate-python VERSION=2` |
| `make generate-go VERSION=N` | Generate only Go code | `make generate-go VERSION=2` |
| `make generate-typescript VERSION=N` | Generate only TypeScript code | `make generate-typescript VERSION=2` |
| `make test VERSION=N` | Run Python tests | `make test VERSION=2` |
| `make test-all` | Run tests for all versions | `make test-all` |
| `make clean VERSION=N` | Remove generated files for version N | `make clean VERSION=2` |
| `make clean-all` | Remove all generated files | `make clean-all` |
| `make bump-version` | Create new major version | `make bump-version` |

## Using Generated Code

### Python

```python
from pentagi_taxonomy import TAXONOMY_VERSION
from pentagi_taxonomy.nodes import Target, Port, Vulnerability
from pentagi_taxonomy.edges import HasPort, Affects

# Create entities with type checking and validation
target = Target(
    uuid="target-123",
    hostname="example.com",
    ip_address="192.168.1.1",
    status="active",
    risk_score=7.5
)

vulnerability = Vulnerability(
    uuid="vuln-456",
    title="SQL Injection",
    severity="critical",
    cvss_score=9.8,
    exploitable=True
)

# Validation happens automatically
print(f"Using taxonomy version: {TAXONOMY_VERSION}")
print(target.model_dump_json())
```

Install the Python package:
```bash
# Development mode
cd v2/python
pip install -e .

# Or from Git
pip install git+https://github.com/yourorg/pentagi-taxonomy.git#subdirectory=v2/python
```

### Go

```go
package main

import (
    "fmt"
    "github.com/yourorg/pentagi-taxonomy/v2/go/entities"
)

func main() {
    target := entities.Target{
        UUID:      "target-123",
        Hostname:  "example.com",
        IPAddress: "192.168.1.1",
        Status:    "active",
        RiskScore: 7.5,
    }
    
    // Validate the entity
    if err := target.Validate(); err != nil {
        panic(err)
    }
    
    fmt.Printf("Target: %+v\n", target)
}
```

### TypeScript

```typescript
import { Target, Vulnerability } from 'pentagi-taxonomy';
import { TargetSchema, VulnerabilitySchema } from 'pentagi-taxonomy/schemas';

// Create and validate entities
const target = TargetSchema.parse({
    uuid: "target-123",
    hostname: "example.com",
    ip_address: "192.168.1.1",
    status: "active",
    risk_score: 7.5
});

const vuln = VulnerabilitySchema.parse({
    uuid: "vuln-456",
    title: "SQL Injection",
    severity: "critical",
    cvss_score: 9.8,
    exploitable: true
});

console.log('Validated:', target);
```

Install the TypeScript package:
```bash
cd v2/typescript
npm install
npm run build
```

## TypeScript Installation with gitpkg

### Why gitpkg is Required

Standard npm and yarn **cannot** install packages from GitHub subdirectories. This is a limitation of npm's GitHub integration:

```bash
# ❌ Doesn't work - npm tries to install from repo root
npm install github:yourorg/pentagi-taxonomy/v2/typescript

# ❌ Doesn't work - invalid syntax
npm install github:yourorg/pentagi-taxonomy#main:v2/typescript
```

**Solution:** [gitpkg](https://gitpkg.vercel.app/) creates virtual packages from GitHub subdirectories, enabling the monorepo structure while maintaining separate versioned TypeScript packages. Python and Go have native subdirectory support, so they don't need this workaround.

### gitpkg URL Format

```
https://gitpkg.now.sh/<owner>/<repo>/<path/to/package>?<branch-or-tag>&<custom-scripts>
```

**Components:**
- `<owner>/<repo>` - GitHub repository (e.g., `yourorg/pentagi-taxonomy`)
- `<path/to/package>` - Subdirectory path containing `package.json` (e.g., `v2/typescript`)
- `?<branch-or-tag>` - Git reference: branch name (`main`) or tag (`v2.1.0`)
- `&<custom-scripts>` - Optional custom npm scripts to run after installation

### Automatic Build Configuration

Since gitpkg fetches source code (not compiled JavaScript), we use the `scripts.postinstall` parameter to automatically build the package after installation:

```
scripts.postinstall=npm%20install%20--ignore-scripts%20%26%26%20npm%20run%20build
```

**URL encoding:**
- Space → `%20`
- `&&` → `%26%26`

This eliminates manual build steps - the package compiles automatically after `npm install`.

### Installation Examples

```bash
# Install from main branch with automatic build
npm install 'https://gitpkg.now.sh/yourorg/pentagi-taxonomy/v2/typescript?main&scripts.postinstall=npm%20install%20--ignore-scripts%20%26%26%20npm%20run%20build'

# Install from specific tag (pinned version) with automatic build
npm install 'https://gitpkg.now.sh/yourorg/pentagi-taxonomy/v2/typescript?v2.1.0&scripts.postinstall=npm%20install%20--ignore-scripts%20%26%26%20npm%20run%20build'

# Install from feature branch with automatic build
npm install 'https://gitpkg.now.sh/yourorg/pentagi-taxonomy/v2/typescript?feature/new-fields&scripts.postinstall=npm%20install%20--ignore-scripts%20%26%26%20npm%20run%20build'
```

### Using Multiple Versions with Aliases

Add to your `package.json` with npm aliases to use multiple versions simultaneously:

```json
{
  "dependencies": {
    "@pentagi/taxonomy-v1": "https://gitpkg.now.sh/yourorg/pentagi-taxonomy/v1/typescript?main&scripts.postinstall=npm%20install%20--ignore-scripts%20%26%26%20npm%20run%20build",
    "@pentagi/taxonomy-v2": "https://gitpkg.now.sh/yourorg/pentagi-taxonomy/v2/typescript?main&scripts.postinstall=npm%20install%20--ignore-scripts%20%26%26%20npm%20run%20build"
  }
}
```

Then import from aliased packages:

```typescript
import { TargetSchema as TargetV1 } from '@pentagi/taxonomy-v1';
import { TargetSchema as TargetV2 } from '@pentagi/taxonomy-v2';

// Handle entities by version
function validateTarget(data: any) {
  if (data.version === 1) {
    return TargetV1.parse(data);
  } else if (data.version === 2) {
    return TargetV2.parse(data);
  }
  throw new Error(`Unknown version: ${data.version}`);
}
```

### Updating Packages

When the taxonomy is updated on GitHub, refresh your installation:

```bash
# Clear npm cache (gitpkg caches packages)
npm cache clean --force

# Remove node_modules and reinstall
rm -rf node_modules package-lock.json
npm install
```

The `scripts.postinstall` parameter automatically rebuilds the packages after installation.

### Version Pinning Strategies

**Using branches (auto-updates):**
```json
{
  "@pentagi/taxonomy": "https://gitpkg.now.sh/yourorg/pentagi-taxonomy/v2/typescript?main&scripts.postinstall=npm%20install%20--ignore-scripts%20%26%26%20npm%20run%20build"
}
```
- Fetches latest from `main` branch
- Running `npm update` pulls new commits
- **Good for:** development, always getting latest patches

**Using tags (pinned):**
```json
{
  "@pentagi/taxonomy": "https://gitpkg.now.sh/yourorg/pentagi-taxonomy/v2/typescript?v2.1.0&scripts.postinstall=npm%20install%20--ignore-scripts%20%26%26%20npm%20run%20build"
}
```
- Fetches specific tagged version
- Won't change until you manually update the tag
- **Good for:** production, reproducible builds

## Version Management

### Creating a New Version

To create a new major version of the taxonomy:

```bash
make bump-version
```

This will:
1. Read the current version from `version.yml`
2. Create a new version directory (e.g., `v3/`)
3. Copy the previous version's `entities.yml` as a starting point
4. Update the version number in the new `entities.yml`
5. Update `version.yml` to point to the new version

After creating a new version:
1. Edit `vN/entities.yml` with your changes
2. Validate: `make validate VERSION=N`
3. Generate code: `make generate VERSION=N`
4. Test: `make test VERSION=N`
5. Commit the new version

### Version Compatibility

Each version is independent and can be used simultaneously. This allows:
- Gradual migration between versions
- Supporting multiple API versions
- Maintaining backward compatibility

## Development Workflow

### Adding a New Entity

1. Edit `vN/entities.yml` to add your node definition
2. Validate the schema:
   ```bash
   make validate VERSION=N
   ```
3. Generate code:
   ```bash
   make generate VERSION=N
   ```
4. Review generated code in `vN/python/`, `vN/go/`, and `vN/typescript/`
5. Run tests:
   ```bash
   make test VERSION=N
   ```

### Modifying Existing Entities

For **backward-compatible changes** (adding optional fields):
- Modify the current version's `entities.yml`
- Regenerate code

For **breaking changes** (removing fields, changing types):
- Create a new major version with `make bump-version`
- Make changes in the new version
- Keep the old version for backward compatibility

### Adding Custom Validation

You can extend the generated code with custom validation:

**Python**: Subclass the generated models and add Pydantic validators
**Go**: Add methods to the generated structs
**TypeScript**: Use Zod's refinement methods

## Testing

The Python packages include basic tests. Run them with:

```bash
# Test specific version
make test VERSION=2

# Test all versions
make test-all

# Or manually
cd v2/python
pytest tests/ -v
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes to the schema or code generators
4. Run validation and tests
5. Submit a pull request

### Code Generator Development

To modify the code generators:

1. Edit templates in `codegen/templates/<language>/`
2. Modify generator logic in `codegen/<language>/generate.py`
3. Test with: `make clean VERSION=2 && make generate VERSION=2`
4. Verify generated code works correctly

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Architecture Notes

### Why Code Generation?

Code generation provides several benefits over alternatives:

- **Type Safety**: Generate native types for each language
- **No Runtime Dependencies**: Generated code is standalone
- **IDE Support**: Full autocomplete and type checking
- **Performance**: No reflection or runtime parsing
- **Flexibility**: Easy to customize templates per language

### Validation Strategy

Validation happens at two levels:

1. **Schema Validation** (at generation time): Ensures `entities.yml` is well-formed
2. **Data Validation** (at runtime): Generated code validates entity instances

This approach catches errors early while maintaining runtime safety.

## FAQ

**Q: Can I use only one language?**
A: Yes! Generate only the language you need with `make generate-python VERSION=N`, etc.

**Q: How do I handle version migration?**
A: Keep both versions active during migration. Write migration code in your application to convert between versions.

**Q: Can I add custom fields to generated code?**
A: For minor additions, you can subclass/extend generated types. For major customizations, modify the templates or add to your schema.

**Q: What if I need a new field type?**
A: Edit `codegen/shared/validator.py` to add the type, then update all language generators and templates.

---

For questions or issues, please open a GitHub issue or contact the maintainers.

