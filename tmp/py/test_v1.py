#!/usr/bin/env python3
"""
Test script for pentagi-taxonomy v1 from GitHub
"""

print("=" * 60)
print("Testing pentagi-taxonomy Version 1 from GitHub")
print("=" * 60)

from pentagi_taxonomy import TAXONOMY_VERSION
from pentagi_taxonomy.nodes import Target, Port
from pentagi_taxonomy.edges import HasPort, Discovered

print(f"\n✓ Successfully imported from pentagi_taxonomy v{TAXONOMY_VERSION}")

# Test creating a Target entity (v1 only has active/inactive status)
target = Target(
    version=1,
    uuid="target-123",
    hostname="example.com",
    ip_address="192.168.1.1",
    target_type="host",
    status="active",
    risk_score=7.5
)
print(f"\n✓ Created Target entity:")
print(f"  UUID: {target.uuid}")
print(f"  Hostname: {target.hostname}")
print(f"  IP Address: {target.ip_address}")
print(f"  Target Type: {target.target_type}")
print(f"  Status: {target.status}")
print(f"  Risk Score: {target.risk_score}")

# Test creating a Port entity (v1 doesn't have service field)
port = Port(
    version=1,
    uuid="port-456",
    port_number=443,
    protocol="tcp",
    state="open"
)
print(f"\n✓ Created Port entity:")
print(f"  UUID: {port.uuid}")
print(f"  Port Number: {port.port_number}")
print(f"  Protocol: {port.protocol}")
print(f"  State: {port.state}")

# Test creating edge relationships
has_port = HasPort(version=1, timestamp=1634567890.5)
print(f"\n✓ Created HAS_PORT edge:")
print(f"  Timestamp: {has_port.timestamp}")

discovered = Discovered(
    version=1,
    timestamp=1634567900.0,
    confidence=0.95,
    method="active"
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
print("✓ All Version 1 tests passed successfully!")
print("=" * 60)

