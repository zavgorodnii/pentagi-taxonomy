"""
Auto-generated entity mappings for pentagi-taxonomy.
DO NOT EDIT - this file is generated from entities.yml
"""

from .nodes import Target, Port, Vulnerability
from .edges import HasPort, Discovered, Affects

ENTITY_TYPES = {
    'Target': Target,
    'Port': Port,
    'Vulnerability': Vulnerability,
}

EDGE_TYPES = {
    'HAS_PORT': HasPort,
    'DISCOVERED': Discovered,
    'AFFECTS': Affects,
}

EDGE_TYPE_MAP = {
    ('Target', 'Port'): ['HAS_PORT'],
    ('Vulnerability', 'Target'): ['AFFECTS'],
}
