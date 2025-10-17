"""
Auto-generated node models for pentagi-taxonomy.
DO NOT EDIT - this file is generated from entities.yml
"""

from pydantic import BaseModel, Field
from typing import Literal

class Target(BaseModel):
    """A target system being assessed during penetration testing"""
    version: int | None = Field(None, description='Taxonomy schema version (auto-injected by Graphiti fork)')
    entity_uuid: str | None = Field(None, description='Unique identifier')
    hostname: str | None = Field(None, description='DNS hostname if known')
    ip_address: str | None = Field(None, description='IP address of the target')
    target_type: Literal['host', 'web_service', 'api', 'domain'] | None = Field(None, description='Classification of target')
    risk_score: float | None = Field(None, description='Calculated risk score', ge=0.0, le=10.0)
    status: Literal['active', 'inactive', 'scanning'] | None = Field(None, description='Current status')
    discovered_at: float | None = Field(None, description='When the target was first discovered')

class Port(BaseModel):
    """A network port on a target system"""
    version: int | None = Field(None, description='Taxonomy schema version (auto-injected by Graphiti fork)')
    entity_uuid: str | None = Field(None, description='Unique identifier')
    port_number: int | None = Field(None, description='Port number', ge=1, le=65535)
    protocol: Literal['tcp', 'udp'] | None = Field(None, description='Network protocol')
    state: Literal['open', 'closed', 'filtered'] | None = Field(None, description='Port state')
    discovered_at: float | None = Field(None, description='Discovery timestamp')

class Vulnerability(BaseModel):
    """A security vulnerability identified during assessment"""
    version: int | None = Field(None, description='Taxonomy schema version (auto-injected by Graphiti fork)')
    entity_uuid: str | None = Field(None, description='Unique identifier')
    vuln_id: str | None = Field(None, description='Custom vulnerability identifier')
    title: str | None = Field(None, description='Vulnerability title')
    severity: Literal['critical', 'high', 'medium', 'low', 'info'] | None = Field(None, description='Severity classification')
    cvss_score: float | None = Field(None, description='CVSS score', ge=0.0, le=10.0)
    exploitable: bool | None = Field(None, description='Whether the vulnerability is exploitable')
    discovered_at: float | None = Field(None, description='Discovery timestamp')

