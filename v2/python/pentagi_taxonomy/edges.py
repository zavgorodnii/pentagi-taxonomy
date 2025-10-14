"""
Auto-generated edge models for pentagi-taxonomy.
DO NOT EDIT - this file is generated from entities.yml
"""

from pydantic import BaseModel, Field
from typing import Literal

class HasPort(BaseModel):
    """A target has a port"""
    version: int | None = Field(None, description='Taxonomy schema version (auto-injected by Graphiti fork)')
    timestamp: float | None = Field(None, description='When association was established')

class Discovered(BaseModel):
    """An action discovered an entity"""
    version: int | None = Field(None, description='Taxonomy schema version (auto-injected by Graphiti fork)')
    timestamp: float | None = Field(None, description='Discovery timestamp')
    confidence: float | None = Field(None, description='Confidence score', ge=0.0, le=1.0)
    method: Literal['active', 'passive'] | None = Field(None, description='Discovery method')

class Affects(BaseModel):
    """A vulnerability affects a target or service"""
    version: int | None = Field(None, description='Taxonomy schema version (auto-injected by Graphiti fork)')
    timestamp: float | None = Field(None, description='When the relationship was identified')
    impact: Literal['direct', 'indirect'] | None = Field(None, description='Type of impact')

