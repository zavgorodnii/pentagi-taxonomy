package main

import (
	"fmt"
	"time"

	// Import v1 entities with alias
	v1entities "github.com/zavgorodnii/pentagi-taxonomy/v1/go/entities"

	// Import v2 entities with alias
	v2entities "github.com/zavgorodnii/pentagi-taxonomy/v2/go/entities"
)

func main() {
	fmt.Println("=== Pentagi Taxonomy Multi-Version Test ===")
	fmt.Println()

	// Test Version 1
	fmt.Println("--- Testing Version 1 ---")
	testV1()
	fmt.Println()

	// Test Version 2
	fmt.Println("--- Testing Version 2 ---")
	testV2()
	fmt.Println()

	fmt.Println("✓ All tests passed! Both versions work correctly.")
}

func testV1() {
	// Helper functions to create pointers
	intPtr := func(i int) *int { return &i }
	strPtr := func(s string) *string { return &s }
	floatPtr := func(f float64) *float64 { return &f }

	// Create a Target entity from v1
	target := v1entities.Target{
		Version:    intPtr(1),
		Uuid:       strPtr("target-v1-123"),
		Hostname:   strPtr("example.com"),
		IpAddress:  strPtr("192.168.1.1"),
		TargetType: strPtr("host"),
		RiskScore:  floatPtr(7.5),
		Status:     strPtr("active"),
	}

	// Validate the entity
	if err := target.Validate(); err != nil {
		panic(fmt.Sprintf("V1 Target validation failed: %v", err))
	}
	fmt.Printf("✓ V1 Target created and validated: %s (%s)\n", *target.Hostname, *target.IpAddress)

	// Create a Port entity from v1
	port := v1entities.Port{
		Version:    intPtr(1),
		Uuid:       strPtr("port-v1-456"),
		PortNumber: intPtr(443),
		Protocol:   strPtr("tcp"),
		State:      strPtr("open"),
	}

	if err := port.Validate(); err != nil {
		panic(fmt.Sprintf("V1 Port validation failed: %v", err))
	}
	fmt.Printf("✓ V1 Port created and validated: %d/%s (%s)\n", *port.PortNumber, *port.Protocol, *port.State)

	// Create an edge relationship from v1
	hasPort := v1entities.HasPort{
		Version:   intPtr(1),
		Timestamp: floatPtr(float64(time.Now().Unix())),
	}

	if err := hasPort.Validate(); err != nil {
		panic(fmt.Sprintf("V1 HasPort validation failed: %v", err))
	}
	fmt.Printf("✓ V1 HasPort edge created and validated\n")
}

func testV2() {
	// Helper functions to create pointers
	intPtr := func(i int) *int { return &i }
	strPtr := func(s string) *string { return &s }
	floatPtr := func(f float64) *float64 { return &f }
	boolPtr := func(b bool) *bool { return &b }

	// Create a Target entity from v2 (note: v2 has additional fields)
	target := v2entities.Target{
		Version:      intPtr(2),
		Uuid:         strPtr("target-v2-789"),
		Hostname:     strPtr("newexample.com"),
		IpAddress:    strPtr("10.0.0.1"),
		TargetType:   strPtr("web_service"),
		RiskScore:    floatPtr(8.5),
		Status:       strPtr("scanning"), // v2 has "scanning" status
		DiscoveredAt: floatPtr(float64(time.Now().Unix())),
	}

	if err := target.Validate(); err != nil {
		panic(fmt.Sprintf("V2 Target validation failed: %v", err))
	}
	fmt.Printf("✓ V2 Target created and validated: %s (%s)\n", *target.Hostname, *target.IpAddress)

	// Create a Port entity from v2
	port := v2entities.Port{
		Version:      intPtr(2),
		Uuid:         strPtr("port-v2-101"),
		PortNumber:   intPtr(8080),
		Protocol:     strPtr("tcp"),
		State:        strPtr("open"),
		DiscoveredAt: floatPtr(float64(time.Now().Unix())),
	}

	if err := port.Validate(); err != nil {
		panic(fmt.Sprintf("V2 Port validation failed: %v", err))
	}
	fmt.Printf("✓ V2 Port created and validated: %d/%s (%s)\n", *port.PortNumber, *port.Protocol, *port.State)

	// Create a Vulnerability entity (new in v2)
	vuln := v2entities.Vulnerability{
		Version:      intPtr(2),
		Uuid:         strPtr("vuln-v2-202"),
		VulnId:       strPtr("CVE-2024-1234"),
		Title:        strPtr("SQL Injection Vulnerability"),
		Severity:     strPtr("critical"),
		CvssScore:    floatPtr(9.8),
		Exploitable:  boolPtr(true),
		DiscoveredAt: floatPtr(float64(time.Now().Unix())),
	}

	if err := vuln.Validate(); err != nil {
		panic(fmt.Sprintf("V2 Vulnerability validation failed: %v", err))
	}
	fmt.Printf("✓ V2 Vulnerability created and validated: %s (%s)\n", *vuln.VulnId, *vuln.Severity)

	// Create an AFFECTS edge (new in v2)
	affects := v2entities.Affects{
		Version:   intPtr(2),
		Timestamp: floatPtr(float64(time.Now().Unix())),
		Impact:    strPtr("direct"),
	}

	if err := affects.Validate(); err != nil {
		panic(fmt.Sprintf("V2 Affects validation failed: %v", err))
	}
	fmt.Printf("✓ V2 Affects edge created and validated\n")
}
