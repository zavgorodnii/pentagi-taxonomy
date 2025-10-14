# Pentagi Taxonomy Python Package (v2)

Auto-generated Python package containing Pydantic models for pentesting entities.

## Installation

Install directly from GitHub:

```bash
pip install git+https://github.com/yourorg/pentagi-taxonomy.git#subdirectory=v2/python
```

## Usage

```python
from pentagi_taxonomy import TAXONOMY_VERSION
from pentagi_taxonomy.nodes import Target, Port, Vulnerability
from pentagi_taxonomy.edges import HasPort, Discovered, Affects

# Create a target
target = Target(
    hostname="example.com",
    ip_address="192.168.1.1",
    target_type="domain",
    risk_score=7.5,
    status="scanning"
)

# Create a vulnerability
vuln = Vulnerability(
    title="SQL Injection",
    severity="critical",
    cvss_score=9.8,
    exploitable=True
)

print(f"Using taxonomy version: {TAXONOMY_VERSION}")
```

## Development

Run tests:

```bash
pip install -e .[dev]
pytest tests/
```

