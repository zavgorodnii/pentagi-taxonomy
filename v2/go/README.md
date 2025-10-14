# Pentagi Taxonomy Go Package (v2)

Auto-generated Go package containing structs with validation for pentesting entities.

## Installation

```bash
go get github.com/yourorg/pentagi-taxonomy/v2/go/entities
```

## Usage

```go
package main

import (
    "fmt"
    "github.com/yourorg/pentagi-taxonomy/v2/go/entities"
)

func main() {
    hostname := "example.com"
    ipAddr := "192.168.1.1"
    targetType := "domain"
    riskScore := 7.5
    status := "scanning"
    
    target := entities.Target{
        Hostname:   &hostname,
        IPAddress:  &ipAddr,
        TargetType: &targetType,
        RiskScore:  &riskScore,
        Status:     &status,
    }
    
    // Validate the entity
    if err := target.Validate(); err != nil {
        fmt.Printf("Validation error: %v\n", err)
        return
    }
    
    fmt.Println("Target is valid!")
}
```

## Development

Run tests:

```bash
go test ./... -v
```

