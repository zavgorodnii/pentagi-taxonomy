import { TargetSchema as TargetV1, PortSchema as PortV1, DiscoveredSchema as DiscoveredV1, TAXONOMY_VERSION as VERSION_V1 } from '@pentagi/taxonomy-v1';
import { TargetSchema as TargetV2, PortSchema as PortV2, VulnerabilitySchema as VulnerabilityV2, AffectsSchema as AffectsV2, TAXONOMY_VERSION as VERSION_V2 } from '@pentagi/taxonomy-v2';

console.log('🚀 Testing Pentagi Taxonomy - Multiple Versions from GitHub');
console.log('=' .repeat(60));

async function testTaxonomyVersions() {
  try {
    console.log('\n📦 Testing Version 1 (V1) imports...');
    console.log(`📋 V1 Taxonomy version: ${VERSION_V1}`);
    
    // Test V1 Target creation and validation
    const targetV1Data = {
      uuid: "target-v1-123",
      hostname: "example-v1.com",
      ip_address: "192.168.1.100",  // Added back - should work with regex fix!
      status: "active",
      target_type: "host",
      risk_score: 7.5
    };

    const targetV1 = TargetV1.parse(targetV1Data);
    console.log('✅ V1 Target created and validated successfully:');
    console.log(JSON.stringify(targetV1, null, 2));

    // Test V1 Port creation and validation (V1 doesn't have VulnerabilitySchema)
    const portV1Data = {
      uuid: "port-v1-456",
      port_number: 22,
      protocol: "tcp",
      state: "open"
    };

    const portV1 = PortV1.parse(portV1Data);
    console.log('✅ V1 Port created and validated successfully:');
    console.log(JSON.stringify(portV1, null, 2));

    // Test V1 Discovered edge
    const discoveredV1Data = {
      timestamp: Date.now() / 1000,
      confidence: 0.95,
      method: "active"
    };

    const discoveredV1 = DiscoveredV1.parse(discoveredV1Data);
    console.log('✅ V1 Discovered edge created and validated successfully:');
    console.log(JSON.stringify(discoveredV1, null, 2));

    console.log('\n📦 Testing Version 2 (V2) imports...');
    console.log(`📋 V2 Taxonomy version: ${VERSION_V2}`);
    
    // Test V2 Target creation and validation (with new fields)
    const targetV2Data = {
      uuid: "target-v2-789",
      hostname: "example-v2.com",
      ip_address: "10.0.0.1",  // Added back - should work with regex fix!
      status: "scanning",  // V2 has "scanning" status
      target_type: "domain",  // V2 has "domain" type
      risk_score: 8.5,
      discovered_at: Date.now() / 1000  // V2 has discovered_at field
    };

    const targetV2 = TargetV2.parse(targetV2Data);
    console.log('✅ V2 Target created and validated successfully:');
    console.log(JSON.stringify(targetV2, null, 2));

    // Test V2 Port creation and validation (with new fields)
    const portV2Data = {
      uuid: "port-v2-012",
      port_number: 443,
      protocol: "tcp",
      state: "open",
      discovered_at: Date.now() / 1000  // V2 has discovered_at field
    };

    const portV2 = PortV2.parse(portV2Data);
    console.log('✅ V2 Port created and validated successfully:');
    console.log(JSON.stringify(portV2, null, 2));

    // Test V2 Vulnerability creation and validation (ONLY exists in V2!)
    const vulnV2Data = {
      uuid: "vuln-v2-345",
      vuln_id: "CVE-2023-12345",
      title: "Remote Code Execution (V2 only)",
      severity: "critical",
      cvss_score: 9.9,
      exploitable: true,
      discovered_at: Date.now() / 1000
    };

    const vulnV2 = VulnerabilityV2.parse(vulnV2Data);
    console.log('✅ V2 Vulnerability created and validated successfully:');
    console.log(JSON.stringify(vulnV2, null, 2));

    // Test V2 Affects edge (new in V2)
    const affectsV2Data = {
      timestamp: Date.now() / 1000,
      impact: "direct"
    };

    const affectsV2 = AffectsV2.parse(affectsV2Data);
    console.log('✅ V2 Affects edge created and validated successfully:');
    console.log(JSON.stringify(affectsV2, null, 2));

    console.log('\n🎯 Testing version-specific handling...');
    
    // Function to handle entities by version (as shown in README)
    function validateTarget(data: any, version: number) {
      if (version === 1) {
        return TargetV1.parse(data);
      } else if (version === 2) {
        return TargetV2.parse(data);
      }
      throw new Error(`Unknown version: ${version}`);
    }

    // Test version-specific validation with compatible data
    const testData = {
      uuid: "target-multi-version",
      hostname: "multi.example.com",
      ip_address: "172.16.0.1",  // Added back - should work with regex fix!  
      status: "active",  // Both V1 and V2 support "active"
      target_type: "host",  // Both V1 and V2 support "host"
      risk_score: 6.0
    };

    const targetFromV1 = validateTarget(testData, 1);
    const targetFromV2 = validateTarget(testData, 2);

    console.log('✅ Multi-version validation successful!');
    console.log('  V1 Target UUID:', targetFromV1.uuid);
    console.log('  V2 Target UUID:', targetFromV2.uuid);

    console.log('\n📊 Showing version differences...');
    console.log('🔹 V1 Features:');
    console.log('  - Target with basic fields');
    console.log('  - Port entities');
    console.log('  - HasPort and Discovered edges');
    console.log('  - Status: active, inactive');
    console.log('  - Target types: host, web_service, api');
    
    console.log('🔹 V2 Features (additions):');
    console.log('  - Vulnerability entities (NEW!)');
    console.log('  - Affects edges (NEW!)'); 
    console.log('  - discovered_at timestamps (NEW!)');
    console.log('  - Status: active, inactive, scanning (NEW!)');
    console.log('  - Target types: host, web_service, api, domain (NEW!)');

    console.log('\n✨ All tests passed! Both V1 and V2 schemas loaded from GitHub successfully.');
    console.log('🎉 gitpkg installation method works perfectly!');
    console.log(`🔖 Version summary: V${VERSION_V1} and V${VERSION_V2} working simultaneously`);

  } catch (error) {
    console.error('❌ Test failed:', error);
    process.exit(1);
  }
}

// Run the tests
testTaxonomyVersions();
