#!/usr/bin/env python3
"""
Test script for pentagi-taxonomy v2 from GitHub
"""

print("=" * 60)
print("Testing pentagi-taxonomy Version 2 from GitHub")
print("=" * 60)

from pentagi_taxonomy import TAXONOMY_VERSION
from pentagi_taxonomy.nodes import Target, Port, Vulnerability
from pentagi_taxonomy.edges import HasPort, Affects, Discovered

print(f"\n✓ Successfully imported from pentagi_taxonomy v{TAXONOMY_VERSION}")

# Test creating a Target entity (v2 has additional fields like discovered_at)
target = Target(
    version=2,
    uuid="target-123",
    hostname="example.com",
    ip_address="192.168.1.1",
    target_type="host",
    status="active",
    risk_score=7.5,
    discovered_at=1634567800.0
)
print(f"\n✓ Created Target entity:")
print(f"  UUID: {target.uuid}")
print(f"  Hostname: {target.hostname}")
print(f"  IP Address: {target.ip_address}")
print(f"  Target Type: {target.target_type}")
print(f"  Status: {target.status}")
print(f"  Risk Score: {target.risk_score}")
print(f"  Discovered At: {target.discovered_at}")

# Test creating a Port entity (v2 has discovered_at field)
port = Port(
    version=2,
    uuid="port-456",
    port_number=443,
    protocol="tcp",
    state="open",
    discovered_at=1634567850.0
)
print(f"\n✓ Created Port entity:")
print(f"  UUID: {port.uuid}")
print(f"  Port Number: {port.port_number}")
print(f"  Protocol: {port.protocol}")
print(f"  State: {port.state}")
print(f"  Discovered At: {port.discovered_at}")

# Test creating a Vulnerability entity (NEW in v2!)
vulnerability = Vulnerability(
    version=2,
    uuid="vuln-789",
    vuln_id="CVE-2024-1234",
    title="SQL Injection",
    severity="critical",
    cvss_score=9.8,
    exploitable=True,
    discovered_at=1634567900.0
)
print(f"\n✓ Created Vulnerability entity (NEW in v2):")
print(f"  UUID: {vulnerability.uuid}")
print(f"  Vuln ID: {vulnerability.vuln_id}")
print(f"  Title: {vulnerability.title}")
print(f"  Severity: {vulnerability.severity}")
print(f"  CVSS Score: {vulnerability.cvss_score}")
print(f"  Exploitable: {vulnerability.exploitable}")
print(f"  Discovered At: {vulnerability.discovered_at}")

# Test creating edge relationships
has_port = HasPort(version=2, timestamp=1634567890.5)
print(f"\n✓ Created HAS_PORT edge:")
print(f"  Timestamp: {has_port.timestamp}")

affects = Affects(
    version=2,
    timestamp=1634567900.0,
    impact="direct"
)
print(f"\n✓ Created AFFECTS edge (NEW in v2):")
print(f"  Timestamp: {affects.timestamp}")
print(f"  Impact: {affects.impact}")

discovered = Discovered(
    version=2,
    timestamp=1634567950.0,
    confidence=0.98,
    method="passive"
)
print(f"\n✓ Created DISCOVERED edge:")
print(f"  Timestamp: {discovered.timestamp}")
print(f"  Confidence: {discovered.confidence}")
print(f"  Method: {discovered.method}")

# Test JSON serialization
print(f"\n✓ JSON serialization test:")
json_output = target.model_dump_json(indent=2)
print(f"  {json_output}")

print("\n" + "=" * 60)
print("✓ All Version 2 tests passed successfully!")
print("=" * 60)

