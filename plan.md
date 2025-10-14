# Custom Graphiti Implementation Plan

## Overview

This document outlines the plan for creating a custom Graphiti deployment with domain-specific entity types for pentesting workflows. The approach uses **two repositories** that work together:

1. **pentagi-taxonomy** - Monorepo containing the YAML schema, all code generators, and versioned generated code for Python, Go, and TypeScript. Supports side-by-side versioning allowing multiple major versions to coexist.
2. **graphiti (fork)** - Fork of the main Graphiti repository with custom entity injection, automatic version tracking, and tests.

The pentagi-taxonomy repository serves as both the schema definition and the distribution mechanism for all language bindings. Generated code is committed to versioned subdirectories (v1/, v2/, etc.), allowing consumers to import specific versions directly from GitHub while coexisting peacefully.

**Note on TypeScript:** TypeScript packages use [gitpkg](https://gitpkg.vercel.app/) for installation since npm doesn't natively support GitHub subdirectory imports. Python and Go use their native subdirectory support. gitpkg's custom script feature enables automatic TypeScript compilation during installation, eliminating manual build steps.

This architecture ensures:
- **Side-by-side versioning** - multiple major versions coexist, allowing gradual migration
- **Automatic version tracking** - all stored entities automatically tagged with taxonomy version
- **Single source of truth** for entity definitions and generated code
- **Language-specific optimization** with dedicated generators in one place
- **Easy adoption** - direct GitHub imports for specific versions (Python/Go native, TypeScript via gitpkg)
- **Simplified maintenance** - fork approach allows deep integration with Graphiti

---

## Repository Structure

### 1. Taxonomy Repository (`pentagi-taxonomy`)

```
pentagi-taxonomy/
├── README.md
├── LICENSE
├── CHANGELOG.md
├── Makefile                              # Generate all, test all, validate schema
├── version.yml                           # Current global version (e.g., version: 2)
├── v1/
│   ├── entities.yml                      # YAML schema for v1 entities
│   ├── python/
│   │   ├── pyproject.toml                # Python v1 package config
│   │   ├── README.md
│   │   └── pentagi_taxonomy/
│   │       ├── __init__.py               # GENERATED: Package init with TAXONOMY_VERSION
│   │       ├── nodes.py                  # GENERATED: v1 Pydantic node models
│   │       ├── edges.py                  # GENERATED: v1 Pydantic edge models
│   │       └── entity_map.py             # GENERATED: v1 entity mappings
│   ├── go/
│   │   ├── go.mod                        # Go v1 module config (includes validator/v10 dependency)
│   │   ├── go.sum
│   │   ├── README.md
│   │   └── entities/
│   │       ├── entities.go               # GENERATED: v1 Go structs with validation tags
│   │       ├── validators.go             # GENERATED: v1 validator instance and Validate() methods
│   │       └── types.go                  # GENERATED: v1 helper types
│   └── typescript/
│       ├── package.json                  # npm v1 config
│       ├── tsconfig.json
│       ├── README.md
│       └── src/
│           ├── index.ts                  # GENERATED: v1 main export
│           ├── entities.ts               # GENERATED: v1 TypeScript types
│           ├── schemas.ts                # GENERATED: v1 Zod schemas
│           └── validators.ts             # GENERATED: v1 validation helpers
├── v2/
│   ├── entities.yml                      # YAML schema for v2 entities (latest)
│   ├── python/
│   │   ├── pyproject.toml
│   │   ├── README.md
│   │   └── pentagi_taxonomy/
│   │       ├── __init__.py               # GENERATED: Package init with TAXONOMY_VERSION
│   │       ├── nodes.py                  # GENERATED: v2 Pydantic node models
│   │       ├── edges.py                  # GENERATED: v2 Pydantic edge models
│   │       └── entity_map.py             # GENERATED: v2 entity mappings
│   ├── go/
│   │   ├── go.mod                        # Go v2 module config (includes validator/v10 dependency)
│   │   ├── go.sum
│   │   ├── README.md
│   │   └── entities/
│   │       ├── entities.go               # GENERATED: v2 Go structs with validation tags
│   │       ├── validators.go             # GENERATED: v2 validator instance and Validate() methods
│   │       └── types.go                  # GENERATED: v2 helper types
│   └── typescript/
│       ├── package.json
│       ├── tsconfig.json
│       ├── README.md
│       └── src/
│           ├── index.ts                  # GENERATED: v2 main export
│           ├── entities.ts               # GENERATED: v2 TypeScript types
│           ├── schemas.ts                # GENERATED: v2 Zod schemas
│           └── validators.ts             # GENERATED: v2 validation helpers
├── codegen/
│   ├── shared/
│   │   └── validator.py                  # Shared schema validation logic
│   ├── python/
│   │   ├── generate.py                   # Python code generator (YAML → Pydantic)
│   │   └── templates/                    # Python code templates
│   ├── go/
│   │   ├── main.go                       # Go code generator (YAML → Go structs)
│   │   ├── parser.go                     # YAML parsing logic
│   │   └── templates/                    # Go code templates
│   └── typescript/
│       ├── generate.ts                   # TypeScript code generator (YAML → Zod)
│       ├── parser.ts                     # YAML parsing logic
│       └── templates/                    # TypeScript code templates
└── docs/
    ├── schema-reference.md               # Documentation for entity definitions
    ├── adding-entities.md                # Guide for adding new entity types
    ├── versioning.md                     # Guide for version management
    └── usage/
        ├── python.md                     # Python installation and usage guide
        ├── go.md                         # Go installation and usage guide
        └── typescript.md                 # TypeScript installation and usage guide
```

**Purpose:** Monorepo serving as both the entity schema definition and the distribution mechanism for all language bindings. Generated code is committed to versioned subdirectories, allowing side-by-side versions to coexist.

**Key characteristics:**
- Single source of truth for schema and all generated code
- Side-by-side versioning: v1/, v2/, etc. directories coexist in the same repo
- Each version can be consumed independently by pip, go get, and npm via GitHub
- All code generators in one place for consistency
- Major version bumps create new versioned directories
- No separate publication step required

**Key workflows:**
- `make validate VERSION=2` - Validates YAML schema structure for specific version
- `make generate VERSION=2` - Runs all three code generators for specific version
- `make generate-python VERSION=2` - Generates only Python code for specific version
- `make generate-go VERSION=2` - Generates only Go code for specific version
- `make generate-typescript VERSION=2` - Generates only TypeScript code for specific version
- `make test VERSION=2` - Runs tests for specific version's generated code
- `make test-all` - Runs tests for all versions
- `make bump-version` - Creates new major version directory and updates version.yml
- `make clean VERSION=2` - Removes generated files for specific version

**Installation by consumers:**
```bash
# Python v1 (via pip from GitHub)
pip install git+https://github.com/yourorg/pentagi-taxonomy.git#subdirectory=v1/python

# Python v2 (latest via pip from GitHub)
pip install git+https://github.com/yourorg/pentagi-taxonomy.git#subdirectory=v2/python

# Go v1 (via go get from GitHub)
go get github.com/yourorg/pentagi-taxonomy/v1/go/entities

# Go v2 (via go get from GitHub)
go get github.com/yourorg/pentagi-taxonomy/v2/go/entities

# TypeScript v1 (via gitpkg with automatic build - npm doesn't support subdirectories natively)
npm install 'https://gitpkg.now.sh/yourorg/pentagi-taxonomy/v1/typescript?main&scripts.postinstall=npm%20install%20--ignore-scripts%20%26%26%20npm%20run%20build'

# TypeScript v2 (via gitpkg with automatic build)
npm install 'https://gitpkg.now.sh/yourorg/pentagi-taxonomy/v2/typescript?main&scripts.postinstall=npm%20install%20--ignore-scripts%20%26%26%20npm%20run%20build'
```

**Why gitpkg for TypeScript?** Standard npm cannot install packages from GitHub subdirectories. [gitpkg](https://gitpkg.vercel.app/) creates virtual packages from subdirectories, enabling the monorepo structure. Python and Go have native subdirectory support. The custom `scripts.postinstall` parameter automatically builds the TypeScript package after installation, eliminating manual build steps.

---

### 2. Graphiti Fork (`graphiti`)

```
graphiti/                                 # Fork of getzep/graphiti
├── (all original Graphiti files)
├── PENTAGI_FORK.md                       # Documentation of fork-specific changes
├── graphiti_core/
│   ├── nodes.py                          # MODIFIED: Auto-inject version field
│   ├── edges.py                          # MODIFIED: Auto-inject version field
│   └── graphiti.py                       # MODIFIED: Auto-load latest taxonomy
├── server/
│   └── graph_service/
│       └── routers/
├── tests/
│   ├── (all original Graphiti tests)
│   ├── test_version_injection.py         # NEW: Test automatic version tracking
│   └── test_custom_entities_fork.py      # NEW: Test custom entity integration
└── .github/
    └── workflows/
        ├── ci.yml                         # MODIFIED: Include custom entity tests
        └── publish.yml                    # MODIFIED: Publish fork image
```

**Purpose:** Fork of the main Graphiti repository with deep integration of custom entities and automatic version tracking. Allows modification of core files for seamless taxonomy integration.

**Key characteristics:**
- Fork approach allows modifying any Graphiti files as needed
- Imports pentagi-taxonomy Python package (latest version) during installation
- Automatic version field injection for all nodes and edges
- Version loaded from pentagi-taxonomy at runtime
- Custom entities always provided by default
- Can sync upstream changes and reapply modifications
- Comprehensive test suite for fork-specific features

**Key workflows:**
- `make install` - Installs Graphiti fork with pentagi-taxonomy (latest version)
- `make test` - Runs all tests including fork-specific tests
- `make build-docker` - Builds Docker image with fork
- `make publish-docker` - Pushes Docker image to registry
- `make sync-upstream` - Syncs changes from upstream Graphiti
- `make clean` - Removes test containers and local images

**Installation process:**
1. Install pentagi-taxonomy Python package (latest version from v{N}/python/)
2. Install Graphiti fork with modified core files
3. Fork imports `TAXONOMY_VERSION` constant from pentagi-taxonomy
4. All entities automatically tagged with version on creation

---

## Automatic Version Tracking

### Version Field Injection

All nodes and edges stored in Graphiti are automatically tagged with a `version` field that corresponds to the current global taxonomy version. This ensures that entities can be traced back to the schema version they were created with, enabling safe migration and backwards compatibility.

**Version determination:**
- The Python code generator reads `version.yml` from the taxonomy repo root during generation
- `version.yml` contains a single field: `version: N` (where N is the current major version)
- This version number is embedded as a constant in the generated Python package
- The fork imports this constant and uses it to tag all nodes and edges
- All created nodes and edges automatically receive this version field

**Critical design principle:** Version injection happens AFTER LLM extraction and attribute population, but BEFORE database write. This ensures that even if the LLM mistakenly includes a `version` field in its output, it will be overwritten by the fork's forced injection.

**Implementation approach:**

1. **Version constant generation** (during code generation):
   - Python generator reads `version.yml` from repo root
   - Generates `TAXONOMY_VERSION` constant in `pentagi_taxonomy/__init__.py`
   - Version is embedded at generation time, not runtime

2. **Node modification** (`graphiti_core/nodes.py`):
   - Modified to automatically add `version` field to node attributes in `EntityNode.save()` method
   - Imports `TAXONOMY_VERSION` directly from `pentagi_taxonomy`
   - Version injected RIGHT BEFORE database write (after all LLM work is complete)
   - Force-assignment ensures LLM output cannot override it
   - See detailed implementation in Fork Modifications section below

3. **Edge modification** (`graphiti_core/edges.py`):
   - Modified to automatically add `version` field to edge attributes in `EntityEdge.save()` method
   - Imports `TAXONOMY_VERSION` directly from `pentagi_taxonomy`
   - Version injected RIGHT BEFORE database write (after all LLM work is complete)
   - Force-assignment ensures LLM output cannot override it
   - See detailed implementation in Fork Modifications section below

4. **Entity type injection** (`graphiti_core/graphiti.py`):
   - Modified to always load and inject custom entities from pentagi-taxonomy
   - Uses latest version (vN/) from pentagi-taxonomy automatically
   - No need for consumers to pass entity_types manually

**Version field characteristics:**
- Type: `int` (corresponds to major version number)
- Automatically set by fork code at save time, never extracted by LLM
- Injected AFTER LLM populates attributes but BEFORE database write
- Stored in the `attributes` dict alongside domain-specific fields
- Read-only after creation (immutable on stored entities)
- Enables querying entities by version: `MATCH (n:Entity {version: 1})`
- Allows safe coexistence of entities from different schema versions
- Protected from LLM override by force-assignment in `save()` method

**Example entity stored in graph:**
```json
{
  "uuid": "target-123",
  "name": "Production Server",
  "labels": ["Entity", "Target"],
  "summary": "Production web server",
  "created_at": "2025-10-09T12:00:00Z",
  "attributes": {
    "hostname": "prod.example.com",
    "ip_address": "192.168.1.100",
    "target_type": "host",
    "risk_score": 7.5,
    "version": 2
  }
}
```

The `version: 2` field inside `attributes` is automatically injected by the fork's `save()` method right before database write, indicating this entity was created using taxonomy v2. Even if the LLM mistakenly included a version field in its extracted attributes, it would be overwritten by this forced injection.

**Migration scenario:**
When taxonomy schema evolves from v1 to v2 with breaking changes:
1. Existing graph contains entities with `version: 1`
2. Fork is updated to use pentagi-taxonomy v2
3. New entities automatically tagged with `version: 2`
4. Backend/frontend can query by version to handle both schemas
5. Migration scripts can gradually update v1 entities to v2 format

---

## Entity Schema Definition

### `entities.yml`

All entity types, their fields, relationships, validation rules, and metadata are defined in a single YAML schema file. This schema serves as the single source of truth and drives code generation for Python, TypeScript, and Go.

**Version declaration:**
Each `entities.yml` file must declare its schema version at the top. This version is used by code generators and for documentation purposes, but the actual runtime version injection is handled by the Graphiti fork reading from the repo root `version.yml`.

```yaml
# Schema version (must match parent version directory)
version: 2
```

### Supported Primitive Types

Nodes and edges must be flat—attributes can only be primitive types or arrays of primitives:
- `string` - text values
- `int` - integer numbers
- `float` - floating-point numbers
- `boolean` - true/false values
- `timestamp` - Unix timestamp as float
- Arrays of any above: `string[]`, `int[]`, `float[]`, `boolean[]`, `timestamp[]`

### Validation Rules

Each field can optionally define validation constraints. The YAML schema supports three validation types:

**Enum validation** - Restricts values to a predefined set:
```yaml
status:
  type: string
  enum: [active, inactive, scanning]
```

**Regex validation** (TypeScript/Go only) - Pattern matching for strings:
```yaml
cve_id:
  type: string
  regex: "^CVE-\\d{4}-\\d{4,}$"
```

For regex patterns in Go, the generator can use built-in validators (e.g., `ipv4`, `email`, `url`) or register custom validators for complex patterns. The YAML `regex` field maps to either:
- Built-in validators: `validate:"omitempty,ipv4"` for IP addresses
- Custom validators: `validate:"omitempty,cve_id"` with a registered validator function

**Mapping common regex patterns to built-in validator/v10 validators:**
- `^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$` → `ipv4`
- `^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$` → `email`
- `^https?://.*` → `url`
- Custom patterns (e.g., `^CVE-\d{4}-\d{4,}$`) → Generate custom validator function

**Example YAML to Go struct tag mapping:**
```yaml
# YAML field definition
ip_address:
  type: string
  regex: "^(?:[0-9]{1,3}\\.){3}[0-9]{1,3}$"

# Generated Go struct field
IPAddress *string `json:"ip_address,omitempty" validate:"omitempty,ipv4"`

# YAML field definition
status:
  type: string
  enum: [active, inactive, scanning]

# Generated Go struct field
Status *string `json:"status,omitempty" validate:"omitempty,oneof=active inactive scanning"`

# YAML field definition
risk_score:
  type: float
  min: 0.0
  max: 10.0

# Generated Go struct field
RiskScore *float64 `json:"risk_score,omitempty" validate:"omitempty,min=0.0,max=10.0"`
```

**Numeric constraints** - Min/max boundaries for int/float/timestamp:
```yaml
risk_score:
  type: float
  min: 0.0
  max: 10.0

port_number:
  type: int
  min: 1
  max: 65535
```

**Implementation notes:**
- Python Pydantic models: enums and min/max constraints (no regex)
- Go validator/v10 struct tags: all three validation types (enums via `oneof`, regex via custom validators, min/max via `min`/`max` tags)
- TypeScript Zod schemas: all three validation types (enums, regex, min/max)

### Complete Schema Structure

**Important:** The `version` field **MUST** be defined in the YAML schema for all nodes and edges. This ensures:
- TypeScript/Go models properly type the version field for deserialization from database
- All three languages (Python/TypeScript/Go) have consistent type definitions
- Type safety when reading entities back from the graph database

Although defined in YAML, the version field is **never extracted by the LLM**. The Graphiti fork force-overwrites this field in the `save()` method right before database write, ensuring the LLM cannot corrupt it.

**Node definitions with validation:**
```yaml
# Schema version declaration
version: 2

nodes:
  Target:
    description: "A target system being assessed during penetration testing"
    fields:
      version:
        type: int
        description: "Taxonomy schema version (auto-injected by Graphiti fork)"
      uuid:
        type: string
        description: "Unique identifier"
      hostname:
        type: string
        description: "DNS hostname if known"
      ip_address:
        type: string
        description: "IP address of the target"
        regex: "^(?:[0-9]{1,3}\\.){3}[0-9]{1,3}$"  # Basic IPv4 pattern
      target_type:
        type: string
        description: "Classification of target"
        enum: [host, web_service, api, domain]
      risk_score:
        type: float
        description: "Calculated risk score"
        min: 0.0
        max: 10.0
      status:
        type: string
        description: "Current status"
        enum: [active, inactive, scanning]
      discovered_at:
        type: timestamp
        description: "When the target was first discovered"

  Port:
    description: "A network port on a target system"
    fields:
      version:
        type: int
        description: "Taxonomy schema version (auto-injected by Graphiti fork)"
      uuid:
        type: string
        description: "Unique identifier"
      port_number:
        type: int
        description: "Port number"
        min: 1
        max: 65535
      protocol:
        type: string
        description: "Network protocol"
        enum: [tcp, udp]
      state:
        type: string
        description: "Port state"
        enum: [open, closed, filtered]
      discovered_at:
        type: timestamp
        description: "Discovery timestamp"

  Vulnerability:
    description: "A security vulnerability identified during assessment"
    fields:
      version:
        type: int
        description: "Taxonomy schema version (auto-injected by Graphiti fork)"
      uuid:
        type: string
        description: "Unique identifier"
      vuln_id:
        type: string
        description: "Custom vulnerability identifier"
      title:
        type: string
        description: "Vulnerability title"
      severity:
        type: string
        description: "Severity classification"
        enum: [critical, high, medium, low, info]
      cvss_score:
        type: float
        description: "CVSS score"
        min: 0.0
        max: 10.0
      exploitable:
        type: boolean
        description: "Whether the vulnerability is exploitable"
      discovered_at:
        type: timestamp
        description: "Discovery timestamp"
```

**Edge definitions with validation:**
```yaml
# (continued in same entities.yml file)
edges:
  EXECUTED:
    description: "An agent executed an action"
    fields:
      version:
        type: int
        description: "Taxonomy schema version (auto-injected by Graphiti fork)"
      timestamp:
        type: timestamp
        description: "When the execution occurred"
      duration:
        type: float
        description: "Execution duration in seconds"
        min: 0.0
      success:
        type: boolean
        description: "Whether execution succeeded"

  DISCOVERED:
    description: "An action discovered an entity"
    fields:
      version:
        type: int
        description: "Taxonomy schema version (auto-injected by Graphiti fork)"
      timestamp:
        type: timestamp
        description: "Discovery timestamp"
      confidence:
        type: float
        description: "Confidence score"
        min: 0.0
        max: 1.0
      method:
        type: string
        description: "Discovery method"
        enum: [active, passive]

  HAS_PORT:
    description: "A target has a port"
    fields:
      version:
        type: int
        description: "Taxonomy schema version (auto-injected by Graphiti fork)"
      timestamp:
        type: timestamp
        description: "When association was established"

  AFFECTS:
    description: "A vulnerability affects a target or service"
    fields:
      version:
        type: int
        description: "Taxonomy schema version (auto-injected by Graphiti fork)"
      timestamp:
        type: timestamp
        description: "When the relationship was identified"
      impact:
        type: string
        description: "Type of impact"
        enum: [direct, indirect]
```

**Relationship compatibility map:**
```yaml
relationships:
  - source: Agent
    target: Action
    edges: [EXECUTED]
  
  - source: Action
    target: Target
    edges: [DISCOVERED]
  
  - source: Action
    target: Port
    edges: [DISCOVERED]
  
  - source: Action
    target: Vulnerability
    edges: [DISCOVERED]
  
  - source: Target
    target: Port
    edges: [HAS_PORT]
  
  - source: Port
    target: Service
    edges: [RUNS_ON]
  
  - source: Vulnerability
    target: Target
    edges: [AFFECTS]
  
  - source: Vulnerability
    target: Service
    edges: [AFFECTS]
```

**Schema design principles:**
- **All fields are optional** - No field can be marked as required (including `version`)
- **Flat structure only** - Attributes cannot be nested objects or complex types
- **Validation is declarative** - All constraints defined in YAML, enforced by generated code
- **Description usage** - Entity descriptions become docstrings/comments for LLM consumption
- **Cross-language consistency** - Same validation logic across Python, Go, and TypeScript
- **Version field required** - All nodes and edges must include the `version: int` field for type consistency

---

## Code Generation Architecture

### Overview

The `pentagi-taxonomy` repository contains all three code generators (`codegen/python/`, `codegen/go/`, `codegen/typescript/`) in a single location. This enables:
- **Shared validation logic** - Common schema validation used by all generators
- **Consistent behavior** - All generators tested together against same schema
- **Simplified testing** - Single CI pipeline tests all generated code
- **Side-by-side versioning** - Generate code for specific version directories

All generators follow the same general workflow:

1. **Read `entities.yml`** from the specified version directory (e.g., `v2/entities.yml`)
2. **Parse and validate the YAML schema** using shared validation logic
3. **Generate language-specific code** using templates tailored to each language
4. **Write generated files** to versioned language-specific directories (e.g., `v2/python/`, `v2/go/`, `v2/typescript/`)
5. **Validate generated code** compiles/type-checks correctly

**Version-aware generation:**
- Generators accept a `VERSION` parameter specifying which version directory to target
- Each version directory has its own independent `entities.yml` schema
- Generated code is isolated in version-specific subdirectories
- Older versions remain unchanged when new versions are created

### Shared Schema Validation Logic

The shared validator (`codegen/shared/validator.py`) implements validation checks used by all generators:
- All referenced entities in `relationships` must be defined in `nodes`
- Field types must be supported primitives or arrays of primitives
- Validation rules must match field types (e.g., regex only on strings)
- Enum values must be non-empty arrays
- Min/max constraints must be logically consistent (min ≤ max)
- Clear error messages when schema is invalid

This ensures consistent validation behavior across all three generators.

### Language-Specific Generators

#### Python Generator (`codegen/python/generate.py`)

**Input:** `../../v{N}/entities.yml` (version-specific schema)  
**Output:** `../../v{N}/python/pentagi_taxonomy/{__init__.py, nodes.py, edges.py, entity_map.py}`

**Generation logic:**
- Parses YAML using PyYAML
- Reads version number from `../../version.yml` at repo root
- Generates `__init__.py` with `TAXONOMY_VERSION` constant
- Creates Pydantic models with `BaseModel` inheritance
- Converts field types to Python type hints with `| None` for optional fields
- Applies `Field()` with `ge`/`le` for numeric min/max constraints
- Converts enum values to `Literal` types for type safety
- Generates `entity_map.py` with dictionaries mapping names to classes
- Preserves entity descriptions as docstrings
- Skips regex validation (intentional - keeps LLM extraction flexible)

**Execution:**
```bash
cd pentagi-taxonomy
make generate-python VERSION=2  # Generate for v2
make generate-python VERSION=1  # Regenerate for v1 (if needed)
```

#### Go Generator (`codegen/go/main.go`)

**Input:** `../../v{N}/entities.yml` (version-specific schema)  
**Output:** `../../v{N}/go/entities/{entities.go, validators.go, types.go}`

**Generation logic:**
- Parses YAML using `gopkg.in/yaml.v3`
- Creates structs with pointer fields for all optional attributes
- Adds JSON tags in snake_case for API compatibility
- Adds validation tags using go-playground/validator/v10 struct tag syntax
- Generates enum validation using `validate:"omitempty,oneof=..."` tags
- Registers custom regex validators for string patterns
- Generates min/max boundary checks using `validate:"omitempty,min=X,max=Y"` tags
- Creates `validators.go` with validator instance and custom validator registration
- Creates type aliases and constants in `types.go`
- Preserves entity descriptions as Go doc comments

**Execution:**
```bash
cd pentagi-taxonomy
make generate-go VERSION=2  # Generate for v2
make generate-go VERSION=1  # Regenerate for v1 (if needed)
```

#### TypeScript Generator (`codegen/typescript/generate.ts`)

**Input:** `../../v{N}/entities.yml` (version-specific schema)  
**Output:** `../../v{N}/typescript/src/{index.ts, entities.ts, schemas.ts, validators.ts}`

**Generation logic:**
- Parses YAML using `js-yaml`
- Creates Zod schemas with `.optional()` for all fields
- Generates TypeScript types via `z.infer<typeof Schema>`
- Applies `.min()` and `.max()` for numeric constraints
- Applies `.regex()` for string pattern validation
- Converts enums to `.enum()` for value restriction
- Creates barrel export in `index.ts` for clean imports
- Generates validation helpers (parse, safeParse wrappers)
- Preserves entity descriptions as JSDoc comments
- **Important:** Schema exports must use explicit type annotations: `Record<string, z.ZodType<any>>` to avoid TypeScript compilation errors with Zod type inference

**Execution:**
```bash
cd pentagi-taxonomy
make generate-typescript VERSION=2  # Generate for v2
make generate-typescript VERSION=1  # Regenerate for v1 (if needed)
```

### Generator Design Principles

**Idiomatic code generation:**
- Python: Pydantic models with type hints and Field validators
- Go: Structs with go-playground/validator/v10 tags and pointer fields
- TypeScript: Zod schemas with inferred types and builder API

**Consistency guarantees:**
- All generators read from the same `entities.yml` file
- Shared validation logic ensures consistent schema interpretation
- Field names are preserved (converted to language conventions if needed)
- Validation semantics are equivalent across languages
- Entity descriptions become documentation in each language

**Maintenance strategy:**
- All generators in one repo simplifies cross-language updates
- Generators can add language-specific optimizations independently
- Schema validation logic shared in `codegen/shared/`
- Breaking changes to YAML schema updated atomically across all generators
- Single version tag covers schema + all generated code

---

## Generated Custom Entities Module

All generated code should **not be edited manually** - any changes must be made in `entities.yml` and regenerated. Each language directory within `pentagi-taxonomy` contains auto-generated files with a header comment indicating they are machine-generated.

### Python: `pentagi-taxonomy/python/pentagi_taxonomy/`

**Generated `python/pentagi_taxonomy/__init__.py`** - Package initialization with version constant:
```python
"""
Auto-generated Pentagi Taxonomy package.
DO NOT EDIT - this file is generated from entities.yml
"""

# Version constant (read from version.yml during generation)
TAXONOMY_VERSION: int = 2

# Re-export entity types for convenience
from .entity_map import ENTITY_TYPES, EDGE_TYPES, EDGE_TYPE_MAP

__all__ = [
    'TAXONOMY_VERSION',
    'ENTITY_TYPES',
    'EDGE_TYPES',
    'EDGE_TYPE_MAP',
]
```

**Generated `python/pentagi_taxonomy/nodes.py`** - Pydantic models with validation:
```python
from pydantic import BaseModel, Field
from typing import Literal

class Target(BaseModel):
    """A target system being assessed during penetration testing"""
    version: int | None = Field(None, description='Taxonomy schema version (auto-injected by Graphiti fork)')
    uuid: str | None = Field(None, description='Unique identifier')
    hostname: str | None = Field(None, description='DNS hostname if known')
    ip_address: str | None = Field(None, description='IP address of the target')
    target_type: Literal['host', 'web_service', 'api', 'domain'] | None = Field(
        None,
        description='Classification of target'
    )
    risk_score: float | None = Field(None, ge=0.0, le=10.0, description='Calculated risk score')
    status: Literal['active', 'inactive', 'scanning'] | None = Field(
        None,
        description='Current status'
    )
    discovered_at: float | None = Field(None, description='When the target was first discovered')

class Port(BaseModel):
    """A network port on a target system"""
    version: int | None = Field(None, description='Taxonomy schema version (auto-injected by Graphiti fork)')
    uuid: str | None = Field(None, description='Unique identifier')
    port_number: int | None = Field(None, ge=1, le=65535, description='Port number')
    protocol: Literal['tcp', 'udp'] | None = Field(None, description='Network protocol')
    state: Literal['open', 'closed', 'filtered'] | None = Field(None, description='Port state')
    discovered_at: float | None = Field(None, description='Discovery timestamp')
```

**Note:** Although `version` appears in the Pydantic model and LLM might try to extract it, the Graphiti fork **force-overwrites** this field in `EntityNode.save()` before database write, ensuring the correct taxonomy version is always stored.

**Generated `python/pentagi_taxonomy/edges.py`** - Edge models with validation:
```python
from pydantic import BaseModel, Field
from typing import Literal

class Executed(BaseModel):
    """An agent executed an action"""
    version: int | None = Field(None, description='Taxonomy schema version (auto-injected by Graphiti fork)')
    timestamp: float | None = Field(None, description='When the execution occurred')
    duration: float | None = Field(None, ge=0.0, description='Execution duration in seconds')
    success: bool | None = Field(None, description='Whether execution succeeded')

class Discovered(BaseModel):
    """An action discovered an entity"""
    version: int | None = Field(None, description='Taxonomy schema version (auto-injected by Graphiti fork)')
    timestamp: float | None = Field(None, description='Discovery timestamp')
    confidence: float | None = Field(None, ge=0.0, le=1.0, description='Confidence score')
    method: Literal['active', 'passive'] | None = Field(None, description='Discovery method')
```

**Note:** Although `version` appears in the Pydantic model and LLM might try to extract it, the Graphiti fork **force-overwrites** this field in `EntityEdge.save()` before database write, ensuring the correct taxonomy version is always stored.

**Generated `python/pentagi_taxonomy/entity_map.py`** - Graphiti integration mappings:
```python
from .nodes import Target, Port, Vulnerability, Agent, Action
from .edges import Executed, Discovered, HasPort, Affects

ENTITY_TYPES = {
    'Target': Target,
    'Port': Port,
    'Vulnerability': Vulnerability,
    'Agent': Agent,
    'Action': Action,
}

EDGE_TYPES = {
    'EXECUTED': Executed,
    'DISCOVERED': Discovered,
    'HAS_PORT': HasPort,
    'AFFECTS': Affects,
}

EDGE_TYPE_MAP = {
    ('Agent', 'Action'): ['EXECUTED'],
    ('Action', 'Target'): ['DISCOVERED'],
    ('Action', 'Port'): ['DISCOVERED'],
    ('Target', 'Port'): ['HAS_PORT'],
    ('Vulnerability', 'Target'): ['AFFECTS'],
}
```

### TypeScript: `pentagi-taxonomy/typescript/src/`

**Generated `typescript/src/entities.ts`** - Types and Zod schemas:
```typescript
import { z } from 'zod';

// Node schemas
export const TargetSchema = z.object({
  version: z.number().int().optional(),
  uuid: z.string().optional(),
  hostname: z.string().optional(),
  ip_address: z.string().regex(/^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$/).optional(),
  target_type: z.enum(['host', 'web_service', 'api', 'domain']).optional(),
  risk_score: z.number().min(0.0).max(10.0).optional(),
  status: z.enum(['active', 'inactive', 'scanning']).optional(),
  discovered_at: z.number().optional(),
});

export type Target = z.infer<typeof TargetSchema>;

export const PortSchema = z.object({
  version: z.number().int().optional(),
  uuid: z.string().optional(),
  port_number: z.number().int().min(1).max(65535).optional(),
  protocol: z.enum(['tcp', 'udp']).optional(),
  state: z.enum(['open', 'closed', 'filtered']).optional(),
  discovered_at: z.number().optional(),
});

export type Port = z.infer<typeof PortSchema>;

// Edge schemas
export const ExecutedSchema = z.object({
  version: z.number().int().optional(),
  timestamp: z.number().optional(),
  duration: z.number().min(0.0).optional(),
  success: z.boolean().optional(),
});

export type Executed = z.infer<typeof ExecutedSchema>;

export const DiscoveredSchema = z.object({
  version: z.number().int().optional(),
  timestamp: z.number().optional(),
  confidence: z.number().min(0.0).max(1.0).optional(),
  method: z.enum(['active', 'passive']).optional(),
});

export type Discovered = z.infer<typeof DiscoveredSchema>;
```

**Note:** The `version` field is properly typed, allowing TypeScript code to safely deserialize entities from the graph database.

### Go: `pentagi-taxonomy/go/entities/`

**Generated `go/entities/entities.go`** - Struct definitions with validation tags:
```go
package entities

// Target is a target system being assessed during penetration testing
type Target struct {
    Version      *int     `json:"version,omitempty"`
    UUID         *string  `json:"uuid,omitempty"`
    Hostname     *string  `json:"hostname,omitempty"`
    IPAddress    *string  `json:"ip_address,omitempty" validate:"omitempty,ipv4"`
    TargetType   *string  `json:"target_type,omitempty" validate:"omitempty,oneof=host web_service api domain"`
    RiskScore    *float64 `json:"risk_score,omitempty" validate:"omitempty,min=0.0,max=10.0"`
    Status       *string  `json:"status,omitempty" validate:"omitempty,oneof=active inactive scanning"`
    DiscoveredAt *float64 `json:"discovered_at,omitempty"`
}

// Port is a network port on a target system
type Port struct {
    Version      *int     `json:"version,omitempty"`
    UUID         *string  `json:"uuid,omitempty"`
    PortNumber   *int     `json:"port_number,omitempty" validate:"omitempty,min=1,max=65535"`
    Protocol     *string  `json:"protocol,omitempty" validate:"omitempty,oneof=tcp udp"`
    State        *string  `json:"state,omitempty" validate:"omitempty,oneof=open closed filtered"`
    DiscoveredAt *float64 `json:"discovered_at,omitempty"`
}

// Executed represents an agent executed an action edge
type Executed struct {
    Version   *int     `json:"version,omitempty"`
    Timestamp *float64 `json:"timestamp,omitempty"`
    Duration  *float64 `json:"duration,omitempty" validate:"omitempty,min=0.0"`
    Success   *bool    `json:"success,omitempty"`
}

// Discovered represents an action discovered an entity edge
type Discovered struct {
    Version    *int     `json:"version,omitempty"`
    Timestamp  *float64 `json:"timestamp,omitempty"`
    Confidence *float64 `json:"confidence,omitempty" validate:"omitempty,min=0.0,max=1.0"`
    Method     *string  `json:"method,omitempty" validate:"omitempty,oneof=active passive"`
}
```

**Note:** The `version` field is properly typed, allowing Go code to safely unmarshal entities from the graph database JSON. Validation tags use go-playground/validator/v10 syntax.

**Generated `go/entities/validators.go`** - Validator instance and custom validators:
```go
package entities

import (
    "github.com/go-playground/validator/v10"
    "regexp"
)

// Validator is the shared validator instance for all entities
var Validator *validator.Validate

func init() {
    Validator = validator.New()
    
    // Register custom validators for regex patterns defined in entities.yml
    // Example for CVE ID pattern: ^CVE-\d{4}-\d{4,}$
    // Validator.RegisterValidation("cve_id", cveIDValidator)
}

// Validate validates a Target entity
func (t *Target) Validate() error {
    return Validator.Struct(t)
}

// Validate validates a Port entity
func (p *Port) Validate() error {
    return Validator.Struct(p)
}

// Validate validates an Executed edge
func (e *Executed) Validate() error {
    return Validator.Struct(e)
}

// Validate validates a Discovered edge
func (d *Discovered) Validate() error {
    return Validator.Struct(d)
}

// Custom validator functions for complex regex patterns from YAML
// These are generated when a field has a 'regex' constraint that doesn't
// match a built-in validator (ipv4, email, url, etc.)
//
// func cveIDValidator(fl validator.FieldLevel) bool {
//     pattern := regexp.MustCompile(`^CVE-\d{4}-\d{4,}$`)
//     return pattern.MatchString(fl.Field().String())
// }
```

**Generated `go/go.mod`** - Module configuration with validator dependency:
```go
module github.com/yourorg/pentagi-taxonomy/v2/go

go 1.21

require (
    github.com/go-playground/validator/v10 v10.28.0
)
```

**Cross-language design notes:**
- All fields use pointer types (Go) or optional (TS/Python) since no fields are required
- `version` field included in all generated models for proper deserialization from database
- Enum validation uses `Literal` (Python), `z.enum()` (TypeScript), `oneof` struct tags (Go)
- Min/max validation uses `ge`/`le` (Python), `.min()`/`.max()` (TypeScript), `min`/`max` struct tags (Go)
- Regex validation skipped in Python, implemented in TypeScript (Zod) and Go (validator/v10)
- Go validation leverages go-playground/validator/v10 with declarative struct tags
- Entity descriptions preserved as docstrings/comments for LLM context
- `version` field auto-injected by Graphiti fork, but typed in models for reading from DB

---

## Fork Modifications

### Core Modifications in Graphiti Fork

The Graphiti fork contains several strategic modifications to seamlessly integrate custom entities and automatic version tracking.

### 1. Version Constant Generation (in `pentagi-taxonomy`)

**Purpose:** Embed the taxonomy version as a constant in the generated Python package.

**Implementation:**
- Python code generator reads `version.yml` from taxonomy repo root
- Generates `TAXONOMY_VERSION: int = N` constant in `pentagi_taxonomy/__init__.py`
- Version is embedded at code generation time, not runtime
- Simple, type-safe, and reliable

**Generated code example:**
```python
# In v2/python/pentagi_taxonomy/__init__.py (auto-generated)
TAXONOMY_VERSION: int = 2
```

### 2. Node Modification (`graphiti_core/nodes.py`)

**Purpose:** Automatically inject `version` field into all created nodes at save time, ensuring LLM-extracted attributes cannot overwrite it.

**Critical requirement:** Version injection must happen AFTER LLM extraction and attribute population, but BEFORE database write.

**Node creation pipeline in Graphiti:**
1. **LLM extracts entities** → `extract_nodes()` in `utils/maintenance/node_operations.py` (lines 88-208)
   - LLM parses episode content and returns entity names
   - Creates basic `EntityNode` objects with name, group_id, labels
   - LLM does NOT see or set version field at this stage

2. **Deduplication** → `resolve_extracted_nodes()` (lines 395-450)
   - Matches extracted nodes against existing nodes in graph
   - Resolves duplicates using similarity and LLM-based deduplication
   - Returns resolved node list

3. **Attribute extraction** → `extract_attributes_from_nodes()` (lines 453-483)
   - For each node, calls LLM to extract domain-specific attributes
   - LLM response populates `node.attributes` dict (line 504: `node.attributes.update(llm_response)`)
   - This is where custom entity attributes from pentagi-taxonomy are populated
   - LLM has NO knowledge of version field and cannot set it

4. **Save to database** → `EntityNode.save()` in `nodes.py` (lines 479-510) ← **VERSION INJECTION HAPPENS HERE**
   - Prepares `entity_data` dict with all node properties
   - **MODIFICATION POINT:** Inject version into attributes dict BEFORE database write
   - This ensures version is added AFTER all LLM work is complete

**Specific modification in `EntityNode.save()` method:**

```python
# In graphiti_core/nodes.py, EntityNode.save() method (around line 479)

from pentagi_taxonomy import TAXONOMY_VERSION

async def save(self, driver: GraphDriver):
    if driver.graph_operations_interface:
        return await driver.graph_operations_interface.node_save(self, driver)

    entity_data: dict[str, Any] = {
        'uuid': self.uuid,
        'name': self.name,
        'name_embedding': self.name_embedding,
        'group_id': self.group_id,
        'summary': self.summary,
        'created_at': self.created_at,
    }

    # **MODIFICATION:** Force-inject version into attributes BEFORE database write
    # This happens AFTER LLM has populated self.attributes, ensuring LLM cannot override it
    self.attributes['version'] = TAXONOMY_VERSION

    if driver.provider == GraphProvider.KUZU:
        entity_data['attributes'] = json.dumps(self.attributes)
        entity_data['labels'] = list(set(self.labels + ['Entity']))
        result = await driver.execute_query(
            get_entity_node_save_query(driver.provider, labels=''),
            **entity_data,
        )
    else:
        entity_data.update(self.attributes or {})
        labels = ':'.join(self.labels + ['Entity'])

        result = await driver.execute_query(
            get_entity_node_save_query(driver.provider, labels),
            entity_data=entity_data,
        )

    logger.debug(f'Saved Node to Graph: {self.uuid}')
    return result
```

**Why this approach is safe:**
- Version injection happens in `save()` method, which is the last step before database write
- At this point, all LLM work is complete (extraction, deduplication, attribute population)
- Even if LLM mistakenly included `version` in extracted attributes, it gets overwritten here
- The `self.attributes['version'] = TAXONOMY_VERSION` assignment is done right before the dict is written to DB
- For non-KUZU drivers, `entity_data.update(self.attributes)` copies all attributes including the injected version
- For KUZU driver, attributes dict (with injected version) is JSON-serialized and stored

**Note on graph_operations_interface:**
Some graph drivers use a `graph_operations_interface` abstraction (line 480-481 in nodes.py). The same version injection logic must be applied in the corresponding interface implementation if this path is used. Check driver-specific implementations in `graphiti_core/driver/graph_operations/` to ensure consistent version injection.

### 3. Edge Modification (`graphiti_core/edges.py`)

**Purpose:** Automatically inject `version` field into all created edges at save time, ensuring LLM-extracted attributes cannot overwrite it.

**Critical requirement:** Version injection must happen AFTER LLM extraction and attribute population, but BEFORE database write.

**Edge creation pipeline in Graphiti:**
1. **LLM extracts relationships** → `extract_edges()` in `utils/maintenance/edge_operations.py`
   - LLM identifies relationships between entities from episode content
   - Creates basic `EntityEdge` objects with source, target, name, fact
   - LLM does NOT see or set version field at this stage

2. **Attribute extraction** → Similar to nodes, custom edge attributes are extracted by LLM
   - LLM response populates `edge.attributes` dict
   - This is where custom edge attributes from pentagi-taxonomy are populated
   - LLM has NO knowledge of version field and cannot set it

3. **Deduplication and resolution** → Edges are deduplicated against existing edges
   - Resolves duplicate relationships in the graph

4. **Save to database** → `EntityEdge.save()` in `edges.py` (lines 285-316) ← **VERSION INJECTION HAPPENS HERE**
   - Prepares `edge_data` dict with all edge properties
   - **MODIFICATION POINT:** Inject version into attributes dict BEFORE database write
   - This ensures version is added AFTER all LLM work is complete

**Specific modification in `EntityEdge.save()` method:**

```python
# In graphiti_core/edges.py, EntityEdge.save() method (around line 285)

from pentagi_taxonomy import TAXONOMY_VERSION

async def save(self, driver: GraphDriver):
    edge_data: dict[str, Any] = {
        'source_uuid': self.source_node_uuid,
        'target_uuid': self.target_node_uuid,
        'uuid': self.uuid,
        'name': self.name,
        'group_id': self.group_id,
        'fact': self.fact,
        'fact_embedding': self.fact_embedding,
        'episodes': self.episodes,
        'created_at': self.created_at,
        'expired_at': self.expired_at,
        'valid_at': self.valid_at,
        'invalid_at': self.invalid_at,
    }

    # **MODIFICATION:** Force-inject version into attributes BEFORE database write
    # This happens AFTER LLM has populated self.attributes, ensuring LLM cannot override it
    self.attributes['version'] = TAXONOMY_VERSION

    if driver.provider == GraphProvider.KUZU:
        edge_data['attributes'] = json.dumps(self.attributes)
        result = await driver.execute_query(
            get_entity_edge_save_query(driver.provider),
            **edge_data,
        )
    else:
        edge_data.update(self.attributes or {})
        result = await driver.execute_query(
            get_entity_edge_save_query(driver.provider),
            edge_data=edge_data,
        )

    logger.debug(f'Saved edge to Graph: {self.uuid}')
    return result
```

**Why this approach is safe:**
- Version injection happens in `save()` method, which is the last step before database write
- At this point, all LLM work is complete (extraction, attribute population, deduplication)
- Even if LLM mistakenly included `version` in extracted attributes, it gets overwritten here
- The `self.attributes['version'] = TAXONOMY_VERSION` assignment is done right before the dict is written to DB
- For non-KUZU drivers, `edge_data.update(self.attributes)` copies all attributes including the injected version
- For KUZU driver, attributes dict (with injected version) is JSON-serialized and stored

**Note on graph_operations_interface:**
Some graph drivers use a `graph_operations_interface` abstraction (line 56-57 in edges.py). The same version injection logic must be applied in the corresponding interface implementation if this path is used. Check driver-specific implementations in `graphiti_core/driver/graph_operations/` to ensure consistent version injection.

### 4. Graphiti Core (`graphiti_core/graphiti.py`)

**Purpose:** Always load and use custom entities from pentagi-taxonomy (latest version).

**Key modifications:**
- Import custom entities at module load time
- Default `entity_types`, `edge_types`, and `edge_type_map` parameters to custom entities
- Use latest version directory from pentagi-taxonomy

**Example modification:**
```python
# Add near top of file
from pentagi_taxonomy.entity_map import ENTITY_TYPES, EDGE_TYPES, EDGE_TYPE_MAP

# Modify add_episode() signature to default to custom entities
async def add_episode(
    self,
    # ... existing parameters ...
    entity_types: dict | None = None,
    edge_types: dict | None = None,
    edge_type_map: dict | None = None,
):
    # Use custom entities if not explicitly provided
    entity_types = entity_types or ENTITY_TYPES
    edge_types = edge_types or EDGE_TYPES
    edge_type_map = edge_type_map or EDGE_TYPE_MAP
    
    # ... rest of method implementation
```

### 5. Fork Documentation (`PENTAGI_FORK.md`)

**Purpose:** Document all fork-specific changes for maintainability.

**Contents:**
- List of all modified files with rationale
- How to sync upstream changes
- How to update pentagi-taxonomy version
- Testing strategy for fork-specific features
- Migration guide for moving between taxonomy versions

---

## Fork Installation and Deployment

### Installation Process

**Installing the fork locally:**
```bash
# Clone the fork
git clone https://github.com/yourorg/graphiti.git
cd graphiti

# Install pentagi-taxonomy (latest version)
LATEST_VERSION=$(cat pentagi-taxonomy-version.txt)  # Track preferred version
pip install git+https://github.com/yourorg/pentagi-taxonomy.git#subdirectory=v${LATEST_VERSION}/python

# Install Graphiti fork
pip install -e .
```

**Docker deployment:**
```dockerfile
FROM python:3.11-slim AS base

# Install pentagi-taxonomy (latest version)
ARG TAXONOMY_VERSION=2
RUN pip install git+https://github.com/yourorg/pentagi-taxonomy.git#subdirectory=v${TAXONOMY_VERSION}/python

# Clone and install Graphiti fork
RUN git clone --depth 1 --branch v0.1.0-fork https://github.com/yourorg/graphiti.git /app/graphiti
WORKDIR /app/graphiti
RUN pip install -e .

# ... rest of configuration
```

**Version tracking:**
- Fork repository tracks which pentagi-taxonomy version it's designed for in `pentagi-taxonomy-version.txt`
- Docker builds specify taxonomy version via build arg
- CI tests fork against multiple taxonomy versions to ensure compatibility

### Syncing Upstream Changes

**Workflow for incorporating upstream Graphiti updates:**
```bash
# Add upstream remote if not already added
git remote add upstream https://github.com/getzep/graphiti.git

# Fetch upstream changes
git fetch upstream

# Create branch for sync
git checkout -b sync-upstream-v0.3.12

# Merge or rebase upstream changes
git merge upstream/main

# Resolve conflicts in modified files (nodes.py, edges.py, graphiti.py)
# Reapply fork-specific modifications

# Test thoroughly
make test

# Commit and push
git commit -m "Sync upstream Graphiti v0.3.12"
git push origin sync-upstream-v0.3.12
```

**Key files requiring manual conflict resolution:**
- `graphiti_core/nodes.py` - version injection logic (imports `TAXONOMY_VERSION`)
- `graphiti_core/edges.py` - version injection logic (imports `TAXONOMY_VERSION`)
- `graphiti_core/graphiti.py` - custom entity defaults

### Fork Versioning Strategy

Fork versions track both the upstream Graphiti version and fork-specific changes:

**Version format:** `v<fork-version>-graphiti-<upstream-version>`

**Examples:**
- `v0.1.0-graphiti-0.3.10` - First fork release based on Graphiti v0.3.10
- `v0.2.0-graphiti-0.3.10` - Fork improvements (no upstream change)
- `v0.3.0-graphiti-0.3.12` - Updated to upstream Graphiti v0.3.12

**Maintenance notes:**
- Fork version increments for fork-specific improvements
- Upstream version increments when syncing with new Graphiti release
- Clear tagging strategy enables tracking both lineages

---

## Testing Strategy

### Purpose

Comprehensive testing ensures that the fork maintains compatibility with custom entities and automatic version tracking. Tests verify:
- Custom entities load without import errors
- Version constant can be imported from pentagi-taxonomy
- Version fields are automatically injected into all nodes and edges
- Episodes can be added and processed with custom entity extraction
- Search functionality works with the custom graph schema
- The entire stack (database + fork + custom entities) integrates properly

### Test Infrastructure

**Docker Compose Environment** - Defines a complete test stack with FalkorDB (graph database) and the Graphiti fork. Both services include healthchecks to ensure readiness before tests run. Environment variables configure database connections and API keys.

**Pytest Fixtures** (`tests/conftest.py`) - Provides shared test setup including an async HTTP client that waits for the Graphiti server to be healthy before running tests. This ensures tests don't fail due to startup timing.

**Fork-Specific Test Suites:**

**Version Injection Tests** (`tests/test_version_injection.py`) - New test suite for version tracking:
- **Version constant test** - Verifies `TAXONOMY_VERSION` can be imported from pentagi-taxonomy and has correct value
- **Node version test** - Creates nodes and verifies `version` field is automatically added with correct value
- **Edge version test** - Creates edges and verifies `version` field is automatically added with correct value
- **Graph query test** - Queries graph by version to verify version field is properly indexed
- **LLM extraction test** - Ensures LLM does not set version field (only code sets it)

**Custom Entity Tests** (`tests/test_custom_entities_fork.py`) - New test suite for entity integration:
- **Entity import test** - Verifies custom entities can be imported from pentagi-taxonomy
- **Episode processing test** - Posts episodes with domain-specific content and verifies custom entities are extracted
- **Entity validation test** - Ensures extracted entities validate according to Pydantic models
- **Entity type coverage test** - Verifies all defined entity types can be extracted

**Smoke Tests** (`tests/test_smoke.py`) - Existing smoke tests extended with fork checks:
- **Healthcheck test** - Verifies the server starts correctly with fork modifications
- **Episode addition test** - Posts episodes and verifies processing with version injection
- **Search test** - Queries entities and verifies version fields present
- **Cleanup test** - Verifies the graph can be cleared between test runs

**Test Runner Script** (`scripts/test.sh`) - Orchestrates the complete test workflow: starts docker-compose, waits for services, runs pytest with fork-specific tests, captures results, cleans up containers, and exits with appropriate status codes.

### Running Tests

**Local testing:**
```bash
# Run all tests
make test

# Run only fork-specific tests
pytest tests/test_version_injection.py tests/test_custom_entities_fork.py

# Run with specific taxonomy version
TAXONOMY_VERSION=2 make test
```

**CI testing:**
- Tests run on every commit
- Matrix testing: multiple taxonomy versions × fork versions
- Upstream sync branch testing before merging

---

## Build & Publish Workflows

### Taxonomy Repository (`pentagi-taxonomy`)

**Makefile targets:**
- **`validate VERSION=N`** - Validates YAML schema structure for version N
- **`validate-all`** - Validates all version schemas
- **`generate VERSION=N`** - Runs all three code generators for version N
- **`generate-python VERSION=N`** - Generates only Python code for version N
- **`generate-go VERSION=N`** - Generates only Go code for version N
- **`generate-typescript VERSION=N`** - Generates only TypeScript code for version N
- **`test VERSION=N`** - Runs tests for version N's generated code
- **`test-all`** - Runs tests for all versions
- **`test-python VERSION=N`** - Tests Python package for version N
- **`test-go VERSION=N`** - Tests Go module for version N
- **`test-typescript VERSION=N`** - Tests TypeScript package for version N
- **`bump-version`** - Creates new major version directory and updates version.yml
- **`clean VERSION=N`** - Removes generated files for version N
- **`clean-all`** - Removes all generated files

**Typical workflow for schema changes (backward-compatible):**
```bash
# Edit current version entities.yml
vim v2/entities.yml

# Validate schema
make validate VERSION=2

# Generate code for all languages
make generate VERSION=2

# Review all generated code
git diff v2/python/ v2/go/ v2/typescript/

# Test all packages
make test VERSION=2

# Commit and push (no new version needed for backward-compatible changes)
git add v2/
git commit -m "Add port_status field to Port entity"
git push origin main
```

**Typical workflow for breaking schema changes (new major version):**
```bash
# Create new major version
make bump-version  # Creates v3/ directory, copies v2/entities.yml, updates version.yml

# Edit new version entities.yml with breaking changes
vim v3/entities.yml

# Validate schema
make validate VERSION=3

# Generate code for all languages
make generate VERSION=3

# Review all generated code
git diff v3/

# Test new version
make test VERSION=3

# Also ensure old versions still work
make test VERSION=2
make test VERSION=1

# Commit and push
git add v3/ version.yml
git commit -m "Add v3 schema with refactored entity structure"
git push origin main
```

**Typical workflow for generator improvements:**
```bash
# Improve Python generator templates
vim codegen/python/templates/nodes.py.jinja

# Regenerate Python code for all versions
make generate-python VERSION=1
make generate-python VERSION=2
make generate-python VERSION=3

# Test all versions
make test-all

# Review changes
git diff v1/python/ v2/python/ v3/python/

# If satisfied, commit
git commit -m "Improve Python docstring generation across all versions"
git push origin main
```

**Package consumption:**

Consumers can import any version they need:

```bash
# Python v1
pip install git+https://github.com/yourorg/pentagi-taxonomy.git#subdirectory=v1/python

# Python v2
pip install git+https://github.com/yourorg/pentagi-taxonomy.git#subdirectory=v2/python

# Go v1
go get github.com/yourorg/pentagi-taxonomy/v1/go/entities

# Go v2
go get github.com/yourorg/pentagi-taxonomy/v2/go/entities

# TypeScript v1 (via gitpkg with automatic build)
npm install 'https://gitpkg.now.sh/yourorg/pentagi-taxonomy/v1/typescript?main&scripts.postinstall=npm%20install%20--ignore-scripts%20%26%26%20npm%20run%20build'

# TypeScript v2 (via gitpkg with automatic build)
npm install 'https://gitpkg.now.sh/yourorg/pentagi-taxonomy/v2/typescript?main&scripts.postinstall=npm%20install%20--ignore-scripts%20%26%26%20npm%20run%20build'
```

**TypeScript package.json with aliases:**
```json
{
  "dependencies": {
    "@pentagi/taxonomy-v1": "https://gitpkg.now.sh/yourorg/pentagi-taxonomy/v1/typescript?main&scripts.postinstall=npm%20install%20--ignore-scripts%20%26%26%20npm%20run%20build",
    "@pentagi/taxonomy-v2": "https://gitpkg.now.sh/yourorg/pentagi-taxonomy/v2/typescript?main&scripts.postinstall=npm%20install%20--ignore-scripts%20%26%26%20npm%20run%20build"
  }
}
```

**Note:** The `scripts.postinstall` parameter in the gitpkg URL automatically runs `npm install --ignore-scripts && npm run build` after fetching the package, so no manual build step is required.

---

### Graphiti Fork Repository (`graphiti`)

**Makefile targets:**
- **`install`** - Installs Graphiti fork locally with pentagi-taxonomy (latest version)
- **`test`** - Runs all tests including fork-specific tests
- **`test-fork`** - Runs only fork-specific tests (version injection, custom entities)
- **`build-docker`** - Builds Docker image with fork
- **`publish-docker`** - Pushes Docker image to registry
- **`sync-upstream`** - Syncs changes from upstream Graphiti and creates merge branch
- **`clean`** - Removes test containers and local images

**Typical workflow for taxonomy version updates:**
```bash
# Update taxonomy version tracking file
echo "3" > pentagi-taxonomy-version.txt

# Rebuild and test locally
pip install git+https://github.com/yourorg/pentagi-taxonomy.git#subdirectory=v3/python
make test

# Build Docker image
make build-docker TAXONOMY_VERSION=3

# Run comprehensive tests
make test

# Publish if tests pass
make publish-docker

# Commit and tag
git add pentagi-taxonomy-version.txt
git commit -m "Update to pentagi-taxonomy v3"
git tag v0.2.0-graphiti-0.3.11
git push origin main --tags
```

**Typical workflow for syncing upstream Graphiti:**
```bash
# Sync upstream changes
make sync-upstream UPSTREAM_VERSION=v0.3.12

# This creates a branch and attempts merge
# Manually resolve conflicts in modified files

# Reapply fork modifications if needed
# - graphiti_core/nodes.py (version injection)
# - graphiti_core/edges.py (version injection)
# - graphiti_core/graphiti.py (custom entity defaults)

# Test thoroughly
make test

# If tests pass, merge
git checkout main
git merge sync-upstream-v0.3.12

# Tag with new upstream version
git tag v0.3.0-graphiti-0.3.12
git push origin main --tags

# Build and publish Docker image
make build-docker publish-docker
```

**Typical workflow for fork-specific improvements:**
```bash
# Modify fork-specific code (e.g., improve version injection logic)
vim graphiti_core/nodes.py

# Test changes
make test-fork

# Commit and tag
git commit -m "Improve version injection logic"
git tag v0.2.1-graphiti-0.3.11  # Fork version bump, same upstream
git push origin main --tags
```

---

## Version Management Strategy

### Major Version Directories

The `pentagi-taxonomy` repository uses **directory-based major versioning**:

**Version structure:**
- Each major version lives in its own directory: `v1/`, `v2/`, `v3/`, etc.
- Each version directory contains independent schema and generated code for all languages
- The `version.yml` file at repo root specifies the current/latest major version
- Consumers can import any version they need via subdirectory paths

**Version semantics:**
- **Major version (directory)**: Breaking schema changes requiring new directory
  - Removed fields, changed field types, removed entity types
  - Incompatible validation changes
  - Structural refactoring requiring migration
- **Minor changes (same directory)**: Backward-compatible changes to existing version
  - New optional fields
  - New entity types
  - Additional validation rules (stricter)
- **Patch changes (same directory)**: Non-breaking improvements
  - Documentation updates
  - Generator improvements
  - Bug fixes

**Examples of breaking changes requiring new major version:**
- Renaming a field: `ip_address` → `ipAddress`
- Changing field type: `port_number: string` → `port_number: int`
- Removing an entity type: deleting `Service` entity
- Changing enum values: `status: [active, inactive]` → `status: [running, stopped]`

**Examples of compatible changes within same major version:**
- Adding new optional field: `Service.version: string`
- Adding new entity type: `Credential` entity
- Tightening validation: `risk_score` min/max constraints

### Version.yml File

The `version.yml` file at the repository root tracks the current/latest major version:

```yaml
version: 2
```

**Purpose:**
- Indicates which version directory is considered "latest" and "active"
- Used by Graphiti fork to determine which version to install
- Updated when a new major version is created via `make bump-version`

**Workflow:**
1. When creating v3: `make bump-version` creates `v3/` directory and updates `version.yml` to `version: 3`
2. Graphiti fork reads this file to install the latest version
3. Old versions (v1, v2) remain in repo for consumers still using them

### Graphiti Fork Versioning

Fork versions track both the fork-specific version and upstream Graphiti version:

**Version format:** `v<fork-major>.<fork-minor>.<fork-patch>-graphiti-<upstream-version>`

**Examples:**
- `v0.1.0-graphiti-0.3.10` - First fork release based on Graphiti v0.3.10
- `v0.1.1-graphiti-0.3.10` - Fork bug fix (same upstream)
- `v0.2.0-graphiti-0.3.10` - Fork feature (same upstream)
- `v0.3.0-graphiti-0.3.12` - Synced to upstream Graphiti v0.3.12

**Fork version semantics:**
- **MAJOR**: Breaking changes to fork behavior or taxonomy integration
- **MINOR**: New fork features, taxonomy version updates
- **PATCH**: Bug fixes, documentation, minor improvements

### Upgrade Workflows

**Workflow 1: Backward-compatible schema change (no new major version)**
```bash
# In pentagi-taxonomy repo
vim v2/entities.yml  # Add new optional field
make validate VERSION=2
make generate VERSION=2
make test VERSION=2
git commit -m "Add optional description field to Target entity"
git push origin main

# No action needed in Graphiti fork - it already uses v2
```

**Workflow 2: Breaking schema change (new major version)**
```bash
# In pentagi-taxonomy repo
make bump-version  # Creates v3/, updates version.yml to 3
vim v3/entities.yml  # Make breaking changes
make generate VERSION=3
make test-all  # Test all versions
git commit -m "Add v3 with refactored entity structure"
git push origin main

# In Graphiti fork repo
echo "3" > pentagi-taxonomy-version.txt
pip install git+https://github.com/yourorg/pentagi-taxonomy.git#subdirectory=v3/python
make test
git commit -m "Update to pentagi-taxonomy v3"
git tag v0.2.0-graphiti-0.3.11
git push origin main --tags
make build-docker publish-docker
```

**Workflow 3: Sync upstream Graphiti**
```bash
# In Graphiti fork repo
git fetch upstream
git checkout -b sync-upstream-v0.3.12
git merge upstream/main
# Resolve conflicts in modified files
make test
git checkout main
git merge sync-upstream-v0.3.12
git tag v0.3.0-graphiti-0.3.12
git push origin main --tags
make build-docker publish-docker
```

### Multi-Version Support Benefits

**For backend/frontend developers:**
- Backend can use v1 while frontend migrates to v2
- Gradual migration without coordinated "big bang" release
- Test new schema version before full rollout
- No forced upgrades

**For Graphiti deployments:**
- Always uses latest version (from version.yml)
- Entities stored with version field for tracking
- Can query both v1 and v2 entities in same graph
- Migration scripts can update entities version-by-version

**Example multi-version deployment:**
```
Graph database contains:
- Target entities with version: 1 (old schema)
- Target entities with version: 2 (new schema)

Backend API (Go):
- Imports v1/go/entities for reading old entities
- Imports v2/go/entities for reading new entities
- Handles both schemas gracefully

Frontend (TypeScript):
- Still using v1/typescript package
- Can migrate to v2 when ready
- No breaking changes forced

Graphiti fork:
- Uses v2/python package (latest)
- All new entities created with version: 2
- Version field enables querying by schema version
```

This approach provides maximum flexibility for gradual migration across distributed systems.

---

## Multi-Language Integration Strategy

### Versioned Package Architecture

The `pentagi-taxonomy` repository contains all three language bindings for multiple major versions, each consumable directly from GitHub:

**Python (versioned directories: `v1/python/`, `v2/python/`, etc.):**
- Installed via pip from GitHub subdirectory: `pip install git+https://github.com/yourorg/pentagi-taxonomy.git#subdirectory=v2/python`
- Used by Graphiti fork (always latest version from version.yml)
- Can also be installed directly in other Python projects (any version)
- Package name: `pentagi_taxonomy` (same across all versions)

**Go (versioned directories: `v1/go/`, `v2/go/`, etc.):**
- Imported as Go module: `go get github.com/yourorg/pentagi-taxonomy/v2/go/entities`
- Uses Go's native GitHub integration
- No separate publication needed - Go fetches directly from GitHub
- Import path: `github.com/yourorg/pentagi-taxonomy/v2/go/entities`
- Can import multiple versions in same project

**TypeScript (versioned directories: `v1/typescript/`, `v2/typescript/`, etc.):**
- Installed via **gitpkg** with automatic build: `npm install 'https://gitpkg.now.sh/yourorg/pentagi-taxonomy/v2/typescript?main&scripts.postinstall=npm%20install%20--ignore-scripts%20%26%26%20npm%20run%20build'`
- gitpkg required because npm doesn't natively support GitHub subdirectory imports
- Can be used in frontend projects, Node.js backends, or serverless functions
- No npm registry publication needed - gitpkg fetches directly from GitHub subdirectories
- Package provides TypeScript types and Zod schemas
- Automatic build via `scripts.postinstall` parameter - no manual build step required

**Version coexistence:**
- Go and TypeScript projects can import multiple versions simultaneously
- Python projects typically use one version (can use aliasing for multiple versions if needed)
- Backend can use v1 while frontend uses v2 during migration

### Language-Specific Integration

#### Python (Graphiti Fork)

**Installation:**
```bash
# Install latest taxonomy version (determined by version.yml)
LATEST_VERSION=$(curl -s https://raw.githubusercontent.com/yourorg/pentagi-taxonomy/main/version.yml | grep version | cut -d' ' -f2)
pip install git+https://github.com/yourorg/pentagi-taxonomy.git#subdirectory=v${LATEST_VERSION}/python

# Or install specific version
pip install git+https://github.com/yourorg/pentagi-taxonomy.git#subdirectory=v2/python
```

**Integration approach:**
- Generated Pydantic models imported from `pentagi_taxonomy` package
- Fork modifications automatically inject entity types at module level
- Modified `graphiti.py` defaults to custom entities
- Version loader reads taxonomy version and injects into all nodes/edges
- No manual integration required from consumers

**Validation characteristics:**
- Automatic during Pydantic model instantiation
- Invalid data raises `ValidationError`
- Enum validation via `Literal` types for type safety
- Min/max validation enforced by `ge`/`le` parameters
- Regex validation intentionally omitted (keeps LLM extraction flexible)

**Example usage (internal to Graphiti fork):**
```python
# In graphiti_core/graphiti.py (fork modification)
from pentagi_taxonomy.entity_map import ENTITY_TYPES, EDGE_TYPES, EDGE_TYPE_MAP

async def add_episode(
    self,
    # ... existing parameters ...
    entity_types: dict | None = None,
    edge_types: dict | None = None,
    edge_type_map: dict | None = None,
):
    # Use custom entities if not explicitly provided
    entity_types = entity_types or ENTITY_TYPES
    edge_types = edge_types or EDGE_TYPES
    edge_type_map = edge_type_map or EDGE_TYPE_MAP
    
    # ... rest of method
```

**Version injection (automatic in fork):**
```python
# In graphiti_core/nodes.py (fork modification)
from pentagi_taxonomy import TAXONOMY_VERSION

async def save(self, driver: GraphDriver):
    # ... prepare entity_data dict ...
    
    # Automatically inject version field RIGHT BEFORE database write
    # This happens AFTER LLM has populated self.attributes
    self.attributes['version'] = TAXONOMY_VERSION
    
    # ... write to database with version included in attributes ...
```

See the Fork Modifications section above for complete implementation details.

---

#### TypeScript (Frontend)

**Installation:**
```bash
# Install specific version via gitpkg (with automatic build)
npm install 'https://gitpkg.now.sh/yourorg/pentagi-taxonomy/v2/typescript?main&scripts.postinstall=npm%20install%20--ignore-scripts%20%26%26%20npm%20run%20build'

# Or install v1 for backward compatibility (with automatic build)
npm install 'https://gitpkg.now.sh/yourorg/pentagi-taxonomy/v1/typescript?main&scripts.postinstall=npm%20install%20--ignore-scripts%20%26%26%20npm%20run%20build'
```

**Integration approach:**
- Import types and schemas from pentagi-taxonomy package
- Use with form libraries (React Hook Form, Formik) or API clients
- Validate API responses, form inputs, or persisted data
- Can install multiple versions side-by-side (using npm aliases)

**Validation characteristics:**
- Explicit validation via `.parse()` or `.safeParse()` methods
- All three validation types supported: enums, regex, min/max
- `.safeParse()` returns structured error objects instead of throwing
- Version field present in entities retrieved from Graphiti

**Example usage (single version):**
```typescript
import { TargetSchema, Target, PortSchema } from 'pentagi-taxonomy-v2';

// Type-safe variable (note: version field added by Graphiti, not required for creation)
const target: Target = {
  hostname: 'example.com',
  ip_address: '192.168.1.1',
  target_type: 'host',
  risk_score: 7.5
};

// Runtime validation
try {
  TargetSchema.parse(target);
  console.log('Valid target');
} catch (error) {
  console.error('Validation failed:', error);
}

// Safe validation (no throw)
const result = PortSchema.safeParse(data);
if (result.success) {
  console.log('Valid port:', result.data);
} else {
  console.error('Validation errors:', result.error.errors);
}
```

**Example usage (multi-version):**
```typescript
// Install both versions with aliases in package.json:
// "@pentagi/taxonomy-v1": "https://gitpkg.now.sh/yourorg/pentagi-taxonomy/v1/typescript?main&scripts.postinstall=npm%20install%20--ignore-scripts%20%26%26%20npm%20run%20build"
// "@pentagi/taxonomy-v2": "https://gitpkg.now.sh/yourorg/pentagi-taxonomy/v2/typescript?main&scripts.postinstall=npm%20install%20--ignore-scripts%20%26%26%20npm%20run%20build"

import { TargetSchema as TargetSchemaV1 } from '@pentagi/taxonomy-v1';
import { TargetSchema as TargetSchemaV2 } from '@pentagi/taxonomy-v2';

// Handle entities by version
function validateTarget(data: any) {
  if (data.version === 1) {
    return TargetSchemaV1.parse(data);
  } else if (data.version === 2) {
    return TargetSchemaV2.parse(data);
  }
  throw new Error(`Unknown version: ${data.version}`);
}
```

---

#### Go (Backend API)

**Installation:**
```bash
# Install specific version
go get github.com/yourorg/pentagi-taxonomy/v2/go/entities

# Install multiple versions side-by-side
go get github.com/yourorg/pentagi-taxonomy/v1/go/entities
go get github.com/yourorg/pentagi-taxonomy/v2/go/entities
```

**Integration approach:**
- Import package directly from GitHub pentagi-taxonomy repo
- Use structs for API request/response types
- Explicit validation via `Validate()` methods
- Can import multiple versions in same project (different import paths)

**Validation characteristics:**
- Explicit validation via `Validate() error` method (wraps validator/v10)
- All three validation types supported via struct tags: enums (`oneof`), regex (custom validators), min/max
- Returns `error` on failure, `nil` on success
- Validation rules declared in struct tags for clarity and maintainability
- JSON tags in snake_case for consistency with Python/TypeScript
- Version field present in entities retrieved from Graphiti

**Example usage (single version):**
```go
import (
    "encoding/json"
    "github.com/yourorg/pentagi-taxonomy/v2/go/entities"
)

// Unmarshal from JSON
var target entities.Target
if err := json.Unmarshal(data, &target); err != nil {
    return err
}

// Explicit validation
if err := target.Validate(); err != nil {
    return fmt.Errorf("invalid target: %w", err)
}

// Use validated data
fmt.Printf("Target: %s at %s (version %d)\n", 
    safeDeref(target.Hostname), 
    safeDeref(target.IPAddress),
    safeDeref(target.Version))
```

**Example usage (multi-version):**
```go
import (
    entitiesv1 "github.com/yourorg/pentagi-taxonomy/v1/go/entities"
    entitiesv2 "github.com/yourorg/pentagi-taxonomy/v2/go/entities"
)

// Handle entities by version
func validateTarget(data []byte) (interface{}, error) {
    // First, unmarshal just to check version
    var versionCheck struct {
        Version *int `json:"version"`
    }
    if err := json.Unmarshal(data, &versionCheck); err != nil {
        return nil, err
    }

    switch safeDeref(versionCheck.Version) {
    case 1:
        var target entitiesv1.Target
        if err := json.Unmarshal(data, &target); err != nil {
            return nil, err
        }
        if err := target.Validate(); err != nil {
            return nil, err
        }
        return &target, nil
    case 2:
        var target entitiesv2.Target
        if err := json.Unmarshal(data, &target); err != nil {
            return nil, err
        }
        if err := target.Validate(); err != nil {
            return nil, err
        }
        return &target, nil
    default:
        return nil, fmt.Errorf("unsupported version: %d", safeDeref(versionCheck.Version))
    }
}
```

---

### Type Mapping Across Languages

| YAML Type    | Python          | TypeScript      | Go              |
|--------------|-----------------|-----------------|-----------------|
| `string`     | `str \| None`   | `string?`       | `*string`       |
| `int`        | `int \| None`   | `number?`       | `*int`          |
| `float`      | `float \| None` | `number?`       | `*float64`      |
| `boolean`    | `bool \| None`  | `boolean?`      | `*bool`         |
| `timestamp`  | `float \| None` | `number?`       | `*float64`      |
| `string[]`   | `list[str] \| None` | `string[]?` | `*[]string`     |

### Cross-Language Consistency Guarantees

**Field names:**
- Preserved from YAML schema (snake_case)
- Consistent across all languages
- JSON serialization uses snake_case in all languages

**Validation logic:**
- Semantically equivalent across languages
- Same constraints enforced (enum values, min/max, regex)
- Different implementation but identical behavior

**Entity descriptions:**
- Preserved as docstrings (Python), JSDoc (TypeScript), Go doc comments
- Provides context for developers and LLMs
- Included in IDE autocomplete/hover information

**Type safety:**
- Maintained through each language's native type system
- Pydantic (Python), Zod (TypeScript), structs (Go)
- Compile-time or runtime type checking

**Optional fields:**
- All fields are optional in all languages
- No required fields (Graphiti design principle)
- Consistent nullable/optional representation

### System-Wide Integration Example

**End-to-end flow:**

1. **Agent discovers a target:**
```typescript
// Frontend TypeScript (using pentagi-taxonomy)
import { TargetSchema } from 'pentagi-taxonomy';

const scanResult = await runNmapScan(ipAddress);
const target = TargetSchema.parse(scanResult);
await api.ingestEpisode({ content: `Discovered target: ${target.hostname}` });
```

2. **Graphiti extracts entities:**
```python
# Python (internal pentagi-graphiti processing)
# pentagi_taxonomy.entity_map provides custom entity types
# LLM extracts Target entity with ip_address, hostname, risk_score
# Pydantic validates against Target model from pentagi_taxonomy
# Entity persisted to graph
```

3. **Backend retrieves and validates:**
```go
// Go backend API (using pentagi-taxonomy)
import "github.com/yourorg/pentagi-taxonomy/go/entities"

targets, err := graphitiClient.Search(ctx, "targets with high risk")
for _, node := range targets {
    var target entities.Target
    json.Unmarshal(node.Properties, &target)
    if err := target.Validate(); err != nil {
        log.Warn("Invalid target in graph: %v", err)
        continue
    }
    // Process validated target
}
```

4. **Frontend displays:**
```typescript
// Frontend TypeScript (using pentagi-taxonomy)
import { TargetSchema } from 'pentagi-taxonomy';

const targets = await api.getHighRiskTargets();
targets.forEach(t => {
  const validated = TargetSchema.parse(t);  // Runtime validation
  renderTargetCard(validated);
});
```

**All three languages import from the same `pentagi-taxonomy` repository at the same version, ensuring consistency.**

### Testing Strategy

**pentagi-taxonomy repo:**
- Schema validation: YAML syntax, type definitions, relationship consistency
- Python tests: Unit tests for Pydantic models, validation boundary cases
- Go tests: Table-driven tests for `Validate()` methods using validator/v10, JSON marshal/unmarshal, struct tag correctness
- TypeScript tests: Zod schema validation, type inference correctness
- Cross-language consistency tests: Same data validates equivalently in all three languages
- CI runs all three test suites on every commit

**Example Go test structure:**
```go
func TestTargetValidation(t *testing.T) {
    tests := []struct {
        name    string
        target  entities.Target
        wantErr bool
    }{
        {
            name: "valid target",
            target: entities.Target{
                IPAddress: ptr("192.168.1.1"),
                TargetType: ptr("host"),
                RiskScore: ptr(5.0),
                Status: ptr("active"),
            },
            wantErr: false,
        },
        {
            name: "invalid IP address",
            target: entities.Target{
                IPAddress: ptr("999.999.999.999"),
            },
            wantErr: true,
        },
        {
            name: "invalid enum value",
            target: entities.Target{
                TargetType: ptr("invalid_type"),
            },
            wantErr: true,
        },
        {
            name: "risk score out of range",
            target: entities.Target{
                RiskScore: ptr(15.0),
            },
            wantErr: true,
        },
    }
    
    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            err := tt.target.Validate()
            if (err != nil) != tt.wantErr {
                t.Errorf("Validate() error = %v, wantErr %v", err, tt.wantErr)
            }
        })
    }
}
```

**pentagi-graphiti repo:**
- Smoke tests: End-to-end episode ingestion with custom entities
- Integration tests: Verify Graphiti extracts and validates custom entities from pentagi-taxonomy
- Compatibility matrix: Test multiple Graphiti × pentagi-taxonomy version combinations
- Patch validation: Ensure patches apply cleanly to target Graphiti versions

### Benefits of Two-Repository Architecture

**Simplified maintenance:**
- All generators and generated code in one repo (pentagi-taxonomy)
- Atomic updates: schema changes, code generation, and tests in single commit
- No need to coordinate releases across multiple repos
- Single version tag covers all language bindings

**Clear separation of concerns:**
- pentagi-taxonomy: Pure entity definitions and language bindings
- pentagi-graphiti: Graphiti-specific integration and deployment
- Schema evolution independent of Graphiti upgrades

**Easy consumption:**
- All package managers support direct GitHub installation
- No publication step required (no npm publish, no Docker registry for taxonomy)
- Consumers simply update version tag in their install command
- Same version tag works for Python, Go, and TypeScript

**Unified testing:**
- Single CI pipeline tests all three language bindings together
- Ensures cross-language consistency
- Easier to catch regressions across languages
- Simpler test matrix (pentagi-graphiti tests Graphiti × taxonomy combinations)

**Version simplicity:**
- pentagi-taxonomy: Single version covers all languages
- pentagi-graphiti: Combined version (taxonomy + Graphiti) clearly documented
- No confusion about which language binding version to use
- Easier to track what schema version is deployed

This two-repository monorepo approach balances simplicity (unified taxonomy) with separation of concerns (Graphiti patches separate), while eliminating the overhead of managing four separate repos.

---

## TypeScript Installation with gitpkg

### Why gitpkg is Required

Standard npm and yarn **cannot** install packages from GitHub subdirectories. The following approaches don't work:

```bash
# ❌ Doesn't work - npm tries to install from repo root
npm install github:yourorg/pentagi-taxonomy/v2/typescript

# ❌ Doesn't work - invalid syntax
npm install github:yourorg/pentagi-taxonomy#main:v2/typescript
```

**Solution:** [gitpkg](https://gitpkg.vercel.app/) creates virtual packages from GitHub subdirectories, enabling the monorepo structure while maintaining separate versioned TypeScript packages.

### gitpkg URL Format

```
https://gitpkg.now.sh/<owner>/<repo>/<path/to/package>?<branch-or-tag>&<custom-scripts>
```

**Components:**
- `<owner>/<repo>` - GitHub repository (e.g., `yourorg/pentagi-taxonomy`)
- `<path/to/package>` - Subdirectory path containing `package.json` (e.g., `v2/typescript`)
- `?<branch-or-tag>` - Git reference: branch name (`main`) or tag (`v2.1.0`)
- `&<custom-scripts>` - Optional custom npm scripts to run after installation

**Custom scripts for automatic build:**
Since gitpkg fetches source code (not compiled JavaScript), we use the `scripts.postinstall` parameter to automatically build the package after installation:

```
scripts.postinstall=npm%20install%20--ignore-scripts%20%26%26%20npm%20run%20build
```

URL encoding:
- Space: `%20`
- `&&`: `%26%26`

**Examples:**
```bash
# Install from main branch with automatic build
npm install 'https://gitpkg.now.sh/yourorg/pentagi-taxonomy/v2/typescript?main&scripts.postinstall=npm%20install%20--ignore-scripts%20%26%26%20npm%20run%20build'

# Install from specific tag (pinned version) with automatic build
npm install 'https://gitpkg.now.sh/yourorg/pentagi-taxonomy/v2/typescript?v2.1.0&scripts.postinstall=npm%20install%20--ignore-scripts%20%26%26%20npm%20run%20build'

# Install from feature branch with automatic build
npm install 'https://gitpkg.now.sh/yourorg/pentagi-taxonomy/v2/typescript?feature/new-fields&scripts.postinstall=npm%20install%20--ignore-scripts%20%26%26%20npm%20run%20build'
```

### Installation Workflow

**1. Add to package.json with aliases (including automatic build):**
```json
{
  "dependencies": {
    "@pentagi/taxonomy-v1": "https://gitpkg.now.sh/yourorg/pentagi-taxonomy/v1/typescript?main&scripts.postinstall=npm%20install%20--ignore-scripts%20%26%26%20npm%20run%20build",
    "@pentagi/taxonomy-v2": "https://gitpkg.now.sh/yourorg/pentagi-taxonomy/v2/typescript?main&scripts.postinstall=npm%20install%20--ignore-scripts%20%26%26%20npm%20run%20build"
  }
}
```

**2. Install packages:**
```bash
npm install
```

The `scripts.postinstall` parameter automatically runs `npm install --ignore-scripts && npm run build` after fetching each package, so no manual build step is required.

**3. Use in your code:**
```typescript
import { TargetSchema, Target } from '@pentagi/taxonomy-v2';

const target: Target = {
  hostname: 'example.com',
  target_type: 'cloud_resource',
  risk_score: 8.5,
};

TargetSchema.parse(target); // Runtime validation
```

### Updating Packages

When taxonomy is updated on GitHub:

```bash
# Clear npm cache (gitpkg caches packages)
npm cache clean --force

# Remove node_modules and reinstall
rm -rf node_modules package-lock.json
npm install
```

The `scripts.postinstall` parameter in the gitpkg URL automatically rebuilds the packages after installation, so no manual build step is required.

### Version Pinning Strategies

**Using branches (auto-updates):**
```json
{
  "@pentagi/taxonomy-v2": "https://gitpkg.now.sh/yourorg/pentagi-taxonomy/v2/typescript?main&scripts.postinstall=npm%20install%20--ignore-scripts%20%26%26%20npm%20run%20build"
}
```
- Fetches latest from `main` branch
- Running `npm update` pulls new commits
- Automatic build via `scripts.postinstall`
- Good for: development, always getting latest patches

**Using tags (pinned):**
```json
{
  "@pentagi/taxonomy-v2": "https://gitpkg.now.sh/yourorg/pentagi-taxonomy/v2/typescript?v2.1.0&scripts.postinstall=npm%20install%20--ignore-scripts%20%26%26%20npm%20run%20build"
}
```
- Fetches specific tagged version
- Won't change until you manually update the tag
- Automatic build via `scripts.postinstall`
- Good for: production, reproducible builds
