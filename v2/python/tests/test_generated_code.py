"""
Tests for generated Python code.
"""

import pytest
from pydantic import ValidationError
from pentagi_taxonomy import TAXONOMY_VERSION, ENTITY_TYPES, EDGE_TYPES, EDGE_TYPE_MAP
from pentagi_taxonomy.nodes import Target, Port, Vulnerability
from pentagi_taxonomy.edges import HasPort, Discovered, Affects


def test_taxonomy_version():
    """Test that TAXONOMY_VERSION is correctly set."""
    assert TAXONOMY_VERSION == 2


def test_entity_types_exported():
    """Test that entity type mappings are exported."""
    assert 'Target' in ENTITY_TYPES
    assert 'Port' in ENTITY_TYPES
    assert 'Vulnerability' in ENTITY_TYPES
    assert ENTITY_TYPES['Target'] == Target


def test_edge_types_exported():
    """Test that edge type mappings are exported."""
    assert 'HAS_PORT' in EDGE_TYPES
    assert 'DISCOVERED' in EDGE_TYPES
    assert 'AFFECTS' in EDGE_TYPES


def test_edge_type_map():
    """Test relationship mappings."""
    assert ('Target', 'Port') in EDGE_TYPE_MAP
    assert 'HAS_PORT' in EDGE_TYPE_MAP[('Target', 'Port')]


def test_target_validation_valid():
    """Test valid Target creation."""
    target = Target(
        hostname="example.com",
        ip_address="192.168.1.1",
        target_type="host",
        risk_score=5.0,
        status="active"
    )
    assert target.hostname == "example.com"
    assert target.risk_score == 5.0


def test_target_enum_validation():
    """Test enum validation on Target."""
    # Valid enum value
    target = Target(target_type="host")
    assert target.target_type == "host"
    
    # Invalid enum value should fail
    with pytest.raises(ValidationError):
        Target(target_type="invalid_type")


def test_target_risk_score_range():
    """Test min/max validation on risk_score."""
    # Valid range
    target = Target(risk_score=0.0)
    assert target.risk_score == 0.0
    
    target = Target(risk_score=10.0)
    assert target.risk_score == 10.0
    
    # Out of range
    with pytest.raises(ValidationError):
        Target(risk_score=-1.0)
    
    with pytest.raises(ValidationError):
        Target(risk_score=11.0)


def test_port_validation():
    """Test Port validation."""
    port = Port(
        port_number=443,
        protocol="tcp",
        state="open"
    )
    assert port.port_number == 443
    
    # Port number out of range
    with pytest.raises(ValidationError):
        Port(port_number=0)
    
    with pytest.raises(ValidationError):
        Port(port_number=70000)


def test_vulnerability_validation():
    """Test Vulnerability validation."""
    vuln = Vulnerability(
        vuln_id="VULN-001",
        title="SQL Injection",
        severity="high",
        cvss_score=7.5,
        exploitable=True
    )
    assert vuln.severity == "high"
    assert vuln.exploitable == True


def test_edge_validation():
    """Test edge model validation."""
    discovered = Discovered(
        timestamp=1234567890.0,
        confidence=0.95,
        method="active"
    )
    assert discovered.confidence == 0.95
    
    # Confidence out of range
    with pytest.raises(ValidationError):
        Discovered(confidence=1.5)


def test_all_fields_optional():
    """Test that all fields are optional (can create empty entities)."""
    target = Target()
    assert target.version is None
    assert target.hostname is None
    
    port = Port()
    assert port.port_number is None
    
    vuln = Vulnerability()
    assert vuln.title is None

