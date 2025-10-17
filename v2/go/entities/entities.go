// Auto-generated entity definitions for pentagi-taxonomy.
// DO NOT EDIT - this file is generated from entities.yml

package entities

// Target A target system being assessed during penetration testing
type Target struct {
	Version *int `json:"version,omitempty"` // Taxonomy schema version (auto-injected by Graphiti fork)
	EntityUuid *string `json:"entity_uuid,omitempty"` // Unique identifier
	Hostname *string `json:"hostname,omitempty"` // DNS hostname if known
	IpAddress *string `json:"ip_address,omitempty" validate:"omitempty,ipv4"` // IP address of the target
	TargetType *string `json:"target_type,omitempty" validate:"omitempty,oneof=host web_service api domain"` // Classification of target
	RiskScore *float64 `json:"risk_score,omitempty" validate:"omitempty,min=0.0,max=10.0"` // Calculated risk score
	Status *string `json:"status,omitempty" validate:"omitempty,oneof=active inactive scanning"` // Current status
	DiscoveredAt *float64 `json:"discovered_at,omitempty"` // When the target was first discovered
}

// Port A network port on a target system
type Port struct {
	Version *int `json:"version,omitempty"` // Taxonomy schema version (auto-injected by Graphiti fork)
	EntityUuid *string `json:"entity_uuid,omitempty"` // Unique identifier
	PortNumber *int `json:"port_number,omitempty" validate:"omitempty,min=1,max=65535"` // Port number
	Protocol *string `json:"protocol,omitempty" validate:"omitempty,oneof=tcp udp"` // Network protocol
	State *string `json:"state,omitempty" validate:"omitempty,oneof=open closed filtered"` // Port state
	DiscoveredAt *float64 `json:"discovered_at,omitempty"` // Discovery timestamp
}

// Vulnerability A security vulnerability identified during assessment
type Vulnerability struct {
	Version *int `json:"version,omitempty"` // Taxonomy schema version (auto-injected by Graphiti fork)
	EntityUuid *string `json:"entity_uuid,omitempty"` // Unique identifier
	VulnId *string `json:"vuln_id,omitempty"` // Custom vulnerability identifier
	Title *string `json:"title,omitempty"` // Vulnerability title
	Severity *string `json:"severity,omitempty" validate:"omitempty,oneof=critical high medium low info"` // Severity classification
	CvssScore *float64 `json:"cvss_score,omitempty" validate:"omitempty,min=0.0,max=10.0"` // CVSS score
	Exploitable *bool `json:"exploitable,omitempty"` // Whether the vulnerability is exploitable
	DiscoveredAt *float64 `json:"discovered_at,omitempty"` // Discovery timestamp
}

// HasPort A target has a port
type HasPort struct {
	Version *int `json:"version,omitempty"` // Taxonomy schema version (auto-injected by Graphiti fork)
	Timestamp *float64 `json:"timestamp,omitempty"` // When association was established
}

// Discovered An action discovered an entity
type Discovered struct {
	Version *int `json:"version,omitempty"` // Taxonomy schema version (auto-injected by Graphiti fork)
	Timestamp *float64 `json:"timestamp,omitempty"` // Discovery timestamp
	Confidence *float64 `json:"confidence,omitempty" validate:"omitempty,min=0.0,max=1.0"` // Confidence score
	Method *string `json:"method,omitempty" validate:"omitempty,oneof=active passive"` // Discovery method
}

// Affects A vulnerability affects a target or service
type Affects struct {
	Version *int `json:"version,omitempty"` // Taxonomy schema version (auto-injected by Graphiti fork)
	Timestamp *float64 `json:"timestamp,omitempty"` // When the relationship was identified
	Impact *string `json:"impact,omitempty" validate:"omitempty,oneof=direct indirect"` // Type of impact
}


