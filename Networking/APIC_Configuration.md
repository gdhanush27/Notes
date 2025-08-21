## APIC Access Methods

### GUI Access
- **URL**: `https://<APIC_IP_ADDRESS>`
- **Default Port**: 443 (HTTPS)
- **Authentication**: Local user or external AAA
- **Session Timeout**: Configurable (default 1200 seconds)

### REST API Access
- **Base URL**: `https://<APIC_IP_ADDRESS>/api`
- **Content Type**: `application/json` or `application/xml`
- **Authentication**: Token-based or session cookie
- **Rate Limits**: 90 seconds maximum response time

## Authentication

### GUI Login
1. Navigate to `https://<APIC_IP_ADDRESS>`
2. Enter username and password
3. Select authentication domain (if applicable)
4. Click "Login"

### REST API Authentication
```bash
# Login Request
POST /api/aaaLogin.json
Content-Type: application/json

{
  "aaaUser": {
    "attributes": {
      "name": "username",
      "pwd": "password"
    }
  }
}

# Response includes token
{
  "imdata": [{
    "aaaLogin": {
      "attributes": {
        "token": "token_string_here",
        "version": "6.1(1.263c)",
        "buildTime": "timestamp"
      }
    }
  }]
}
```

## Configuration Hierarchy and Navigation

### GUI Navigation Structure
```
APIC GUI Root
├── Tenants
│   ├── {Tenant Name}
│   │   ├── Networking
│   │   │   ├── VRFs
│   │   │   ├── Bridge Domains
│   │   │   └── L3Outs
│   │   ├── Application Profiles
│   │   │   └── Application EPGs
│   │   └── Security Policies
│   │       ├── Contracts
│   │       └── Filters
├── Fabric
│   ├── Access Policies
│   │   ├── Policies
│   │   ├── Pools
│   │   └── Domains
│   └── Inventory
└── Admin
    ├── AAA
    └── System
```

## Tenant Configuration

### GUI Method: Creating a Tenant
**Navigation Path**: `Tenants → Add Tenant`

**Steps**:
1. Right-click "Tenants" in navigation
2. Select "Create Tenant"
3. Enter tenant details:
   - **Name**: Required (64 chars max)
   - **Description**: Optional (128 chars max)
   - **Security Domains**: Optional
4. Click "Submit"

### REST API Method: Creating a Tenant
```json
POST /api/mo/uni.json
Content-Type: application/json
Cookie: APIC-cookie=<token>

{
  "fvTenant": {
    "attributes": {
      "name": "PRODUCTION_TENANT",
      "descr": "Production environment for web applications",
      "dn": "uni/tn-PRODUCTION_TENANT"
    }
  }
}
```

**Response**:
```json
{
  "imdata": [{
    "fvTenant": {
      "attributes": {
        "childAction": "",
        "dn": "uni/tn-PRODUCTION_TENANT",
        "name": "PRODUCTION_TENANT",
        "status": "created"
      }
    }
  }]
}
```

## VRF/Context Configuration

### GUI Method: Creating a VRF
**Navigation Path**: `Tenants → [Tenant] → Networking → VRFs → Create VRF`

**Steps**:
1. Navigate to tenant
2. Expand "Networking"
3. Right-click "VRFs" → "Create VRF"
4. Configure parameters:
   - **Name**: Required
   - **Policy Control Enforcement**: Enforced/Unenforced
   - **Policy Control Direction**: Ingress/Egress
   - **IP Data-plane Learning**: Enabled/Disabled
   - **Preferred Group**: Include/Exclude
5. Click "Submit"

### REST API Method: Creating a VRF
```json
POST /api/mo/uni/tn-PRODUCTION_TENANT.json
Content-Type: application/json

{
  "fvCtx": {
    "attributes": {
      "name": "PROD_VRF",
      "descr": "Production VRF for web tier",
      "pcEnfPref": "enforced",
      "pcEnfDir": "ingress",
      "ipDataPlaneLearning": "enabled",
      "prefGrMemb": "disabled",
      "bdEnforcedEnable": "no"
    }
  }
}
```

## Bridge Domain Configuration

### GUI Method: Creating a Bridge Domain
**Navigation Path**: `Tenants → [Tenant] → Networking → Bridge Domains → Create Bridge Domain`

**Steps**:
1. Navigate to Bridge Domains
2. Click "Create Bridge Domain"
3. General Tab:
   - **Name**: Required
   - **VRF**: Select from dropdown
   - **L2 Unknown Unicast**: Hardware Proxy/Flood
   - **L3 Unknown Multicast Flooding**: Flood/Optimize Flood
4. Advanced/L3 Configurations Tab:
   - **Unicast Routing**: Enable/Disable
   - **ARP Flooding**: Enable/Disable
   - **Endpoint Dataplane Learning**: Enable/Disable
5. Subnets Tab:
   - Add gateway subnets with scope (Public/Private/Shared)

### REST API Method: Bridge Domain with Subnet
```json
POST /api/mo/uni/tn-PRODUCTION_TENANT.json
Content-Type: application/json

{
  "fvBD": {
    "attributes": {
      "name": "WEB_BD",
      "descr": "Bridge domain for web servers",
      "arpFlood": "yes",
      "unicastRoute": "yes",
      "unkMcastAct": "flood",
      "unkMacUcastAct": "proxy"
    },
    "children": [
      {
        "fvRsCtx": {
          "attributes": {
            "tnFvCtxName": "PROD_VRF"
          }
        }
      },
      {
        "fvSubnet": {
          "attributes": {
            "ip": "192.168.10.1/24",
            "scope": "public,shared",
            "preferred": "no"
          }
        }
      }
    ]
  }
}
```

## Application Profile and EPG Configuration

### GUI Method: Creating Application Profile and EPG
**Navigation Path**: `Tenants → [Tenant] → Application Profiles → Create Application Profile`

**Application Profile Steps**:
1. Right-click "Application Profiles"
2. Select "Create Application Profile"
3. Enter name and description
4. Click "Submit"

**EPG Steps**:
1. Navigate to created Application Profile
2. Right-click "Application EPGs" → "Create Application EPG"
3. General Tab:
   - **Name**: Required
   - **Bridge Domain**: Select from dropdown
   - **Priority**: Level 1-3 or Unspecified
   - **Intra EPG Isolation**: Enforced/Unenforced
4. Domains Tab:
   - Add Physical/VMM domains
5. Contracts Tab:
   - Add Provider/Consumer contracts

### REST API Method: Application Profile with EPG
```json
POST /api/mo/uni/tn-PRODUCTION_TENANT.json
Content-Type: application/json

{
  "fvAp": {
    "attributes": {
      "name": "WEB_APP_PROFILE",
      "descr": "Web application profile"
    },
    "children": [
      {
        "fvAEPg": {
          "attributes": {
            "name": "WEB_EPG",
            "descr": "Web server endpoint group",
            "prio": "level2"
          },
          "children": [
            {
              "fvRsBd": {
                "attributes": {
                  "tnFvBDName": "WEB_BD"
                }
              }
            },
            {
              "fvRsDomAtt": {
                "attributes": {
                  "tDn": "uni/phys-PHYS_DOMAIN"
                }
              }
            },
            {
              "fvRsCons": {
                "attributes": {
                  "tnVzBrCPName": "WEB_CONTRACT"
                }
              }
            }
          ]
        }
      }
    ]
  }
}
```

## Contract and Filter Configuration

### GUI Method: Creating Contract and Filter
**Contract Navigation**: `Tenants → [Tenant] → Security Policies → Contracts → Create Contract`

**Contract Steps**:
1. Create Contract:
   - **Name**: Required
   - **Scope**: Application Profile/Tenant/VRF/Global
   - **Priority**: Level 1-3 or Unspecified
2. Create Subject within Contract:
   - **Name**: Required
   - **Priority**: Inherit or specify
   - **Apply Both Directions**: Yes/No
3. Associate Filters to Subject

**Filter Navigation**: `Tenants → [Tenant] → Security Policies → Filters → Create Filter`

**Filter Steps**:
1. Create Filter with name
2. Add Filter Entry:
   - **Name**: Required
   - **EtherType**: IP/ARP/IPv4/IPv6
   - **IP Protocol**: TCP/UDP/ICMP/etc.
   - **Destination Port**: Specific ports or ranges
   - **TCP Session Rules**: Established/ACK/etc.

### REST API Method: Complete Contract with Filter
```json
POST /api/mo/uni/tn-PRODUCTION_TENANT.json
Content-Type: application/json

{
  "vzBrCP": {
    "attributes": {
      "name": "WEB_CONTRACT",
      "descr": "Web traffic contract",
      "scope": "tenant",
      "prio": "level1"
    },
    "children": [
      {
        "vzSubj": {
          "attributes": {
            "name": "HTTP_HTTPS_SUBJECT",
            "descr": "Allow HTTP and HTTPS traffic"
          },
          "children": [
            {
              "vzRsSubjFiltAtt": {
                "attributes": {
                  "tnVzFilterName": "WEB_FILTER"
                }
              }
            }
          ]
        }
      }
    ]
  }
}

# Separate call to create filter
POST /api/mo/uni/tn-PRODUCTION_TENANT.json
Content-Type: application/json

{
  "vzFilter": {
    "attributes": {
      "name": "WEB_FILTER",
      "descr": "Web traffic filter"
    },
    "children": [
      {
        "vzEntry": {
          "attributes": {
            "name": "HTTP",
            "etherT": "ip",
            "prot": "tcp",
            "dFromPort": "80",
            "dToPort": "80"
          }
        }
      },
      {
        "vzEntry": {
          "attributes": {
            "name": "HTTPS",
            "etherT": "ip", 
            "prot": "tcp",
            "dFromPort": "443",
            "dToPort": "443"
          }
        }
      }
    ]
  }
}
```

## Layer 3 Outside (L3Out) Configuration

### GUI Method: Creating L3Out
**Navigation Path**: `Tenants → [Tenant] → Networking → L3Outs → Create L3Out`

**Steps**:
1. General Tab:
   - **Name**: Required
   - **VRF**: Select associated VRF
   - **L3 Domain**: Select routed domain
2. Nodes and Interfaces Tab:
   - Add Node Profile
   - Configure Interface Profile
   - Set IP addresses and routing
3. Networks Tab:
   - Configure external networks
   - Set subnet scope and route control
4. Protocols Tab:
   - Configure BGP/OSPF parameters

### REST API Method: Basic L3Out Configuration
```json
POST /api/mo/uni/tn-PRODUCTION_TENANT.json
Content-Type: application/json

{
  "l3extOut": {
    "attributes": {
      "name": "EXTERNAL_L3OUT",
      "descr": "External connectivity L3Out"
    },
    "children": [
      {
        "l3extRsEctx": {
          "attributes": {
            "tnFvCtxName": "PROD_VRF"
          }
        }
      },
      {
        "l3extRsL3DomAtt": {
          "attributes": {
            "tDn": "uni/l3dom-ROUTED_DOMAIN"
          }
        }
      },
      {
        "l3extLNodeP": {
          "attributes": {
            "name": "NODE_PROFILE"
          },
          "children": [
            {
              "l3extRsNodeL3OutAtt": {
                "attributes": {
                  "tDn": "topology/pod-1/node-101",
                  "rtrId": "10.1.1.1"
                }
              }
            }
          ]
        }
      }
    ]
  }
}
```

## Access Policies Configuration

### GUI Method: VLAN Pool Creation
**Navigation Path**: `Fabric → Access Policies → Pools → VLAN → Create VLAN Pool`

**Steps**:
1. General Tab:
   - **Name**: Required
   - **Allocation Mode**: Static/Dynamic
   - **Description**: Optional
2. Encap Blocks Tab:
   - **VLAN Range**: Start-End (e.g., 100-200)
   - **Allocation Mode**: Inherit/Static/Dynamic
   - **Role**: Internal/External

### REST API Method: VLAN Pool with Range
```json
POST /api/mo/uni/infra.json
Content-Type: application/json

{
  "fvnsVlanInstP": {
    "attributes": {
      "name": "PROD_VLAN_POOL",
      "descr": "Production VLAN pool",
      "allocMode": "static"
    },
    "children": [
      {
        "fvnsEncapBlk": {
          "attributes": {
            "name": "encap",
            "from": "vlan-100",
            "to": "vlan-200",
            "role": "external"
          }
        }
      }
    ]
  }
}
```

### GUI Method: Physical Domain Creation
**Navigation Path**: `Fabric → Access Policies → Physical and External Domains → Physical Domains → Create Physical Domain`

**Steps**:
1. **Name**: Required
2. **VLAN Pool**: Select from dropdown
3. **AAEP**: Select Attachable Access Entity Profile

### REST API Method: Physical Domain
```json
POST /api/mo/uni/phys-PHYS_DOMAIN.json
Content-Type: application/json

{
  "physDomP": {
    "attributes": {
      "name": "PHYS_DOMAIN",
      "descr": "Physical domain for bare metal servers"
    },
    "children": [
      {
        "infraRsVlanNs": {
          "attributes": {
            "tDn": "uni/infra/vlanns-[PROD_VLAN_POOL]-static"
          }
        }
      }
    ]
  }
}
```

## Monitoring and Verification

### GUI Monitoring Locations
- **System → Health**: Overall fabric health
- **Tenants → [Tenant] → Operational → Endpoint**: Endpoint learning
- **Fabric → Inventory**: Physical inventory
- **Operations → Faults**: Active faults and events

### REST API Monitoring Queries
```bash
# Get tenant health
GET /api/mo/uni/tn-PRODUCTION_TENANT/health.json

# Get EPG endpoints
GET /api/mo/uni/tn-PRODUCTION_TENANT/ap-WEB_APP_PROFILE/epg-WEB_EPG.json?query-target=children&target-subtree-class=fvCEp

# Get fabric health
GET /api/mo/topology/health.json

# Get active faults
GET /api/class/faultInst.json?query-target-filter=eq(faultInst.severity,"critical")
```

## Error Handling and Best Practices

### REST API Error Handling
APIC allows maximum 90 seconds response time and may return "destination not available" on timeout.

**Retry Strategy**:
```python
import requests
import time

def apic_request_with_retry(url, data, headers, max_retries=3):
    for attempt in range(max_retries):
        try:
            response = requests.post(url, json=data, headers=headers, timeout=90)
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 503:  # Service unavailable
                time.sleep(5)  # Wait before retry
                continue
        except requests.exceptions.Timeout:
            if attempt < max_retries - 1:
                time.sleep(5)
                continue
            raise
    return None
```

### JSON Validation Examples
```json
# Successful response format
{
  "imdata": [{
    "fvTenant": {
      "attributes": {
        "dn": "uni/tn-PRODUCTION_TENANT",
        "status": "created"
      }
    }
  }]
}

# Error response format
{
  "imdata": [{
    "error": {
      "attributes": {
        "code": "103",
        "text": "DN exceeds supported depth/length"
      }
    }
  }]
}
```

## Security Best Practices

### Authentication Security
- Use certificate-based authentication for automation
- Implement proper session management
- Rotate credentials regularly
- Use least privilege principle

### API Security
```bash
# Use HTTPS only
https://<apic_ip>/api/...

# Include proper headers
Content-Type: application/json
Accept: application/json
Cookie: APIC-cookie=<token>
```

### Configuration Security
- Validate all input parameters
- Use specific contracts instead of "any/any" rules
- Implement proper microsegmentation
- Regular backup of configurations

## Complete Configuration Example

### Scenario: Web Application Deployment
This example creates a complete tenant with web and database tiers.

#### GUI Workflow Summary
1. Create Tenant → Create VRF → Create Bridge Domains
2. Create Application Profile → Create EPGs → Associate to Bridge Domains
3. Create Contracts and Filters → Associate to EPGs
4. Configure Access Policies → Associate Domains to EPGs

#### REST API Complete Workflow
```json
# 1. Create Tenant
POST /api/mo/uni.json
{
  "fvTenant": {
    "attributes": {"name": "WEB_APP_TENANT"}
  }
}

# 2. Create VRF, Bridge Domains, and Application constructs in single call
POST /api/mo/uni/tn-WEB_APP_TENANT.json
{
  "fvTenant": {
    "children": [
      {
        "fvCtx": {
          "attributes": {
            "name": "WEB_VRF",
            "pcEnfPref": "enforced"
          }
        }
      },
      {
        "fvBD": {
          "attributes": {
            "name": "WEB_BD",
            "unicastRoute": "yes"
          },
          "children": [
            {
              "fvRsCtx": {
                "attributes": {"tnFvCtxName": "WEB_VRF"}
              }
            },
            {
              "fvSubnet": {
                "attributes": {
                  "ip": "192.168.10.1/24",
                  "scope": "public"
                }
              }
            }
          ]
        }
      },
      {
        "fvBD": {
          "attributes": {
            "name": "DB_BD",
            "unicastRoute": "yes"
          },
          "children": [
            {
              "fvRsCtx": {
                "attributes": {"tnFvCtxName": "WEB_VRF"}
              }
            },
            {
              "fvSubnet": {
                "attributes": {
                  "ip": "192.168.20.1/24", 
                  "scope": "private"
                }
              }
            }
          ]
        }
      },
      {
        "fvAp": {
          "attributes": {"name": "THREE_TIER_APP"},
          "children": [
            {
              "fvAEPg": {
                "attributes": {"name": "WEB_EPG"},
                "children": [
                  {
                    "fvRsBd": {
                      "attributes": {"tnFvBDName": "WEB_BD"}
                    }
                  },
                  {
                    "fvRsProv": {
                      "attributes": {"tnVzBrCPName": "WEB_CONTRACT"}
                    }
                  }
                ]
              }
            },
            {
              "fvAEPg": {
                "attributes": {"name": "DB_EPG"},
                "children": [
                  {
                    "fvRsBd": {
                      "attributes": {"tnFvBDName": "DB_BD"}
                    }
                  },
                  {
                    "fvRsCons": {
                      "attributes": {"tnVzBrCPName": "DB_CONTRACT"}
                    }
                  }
                ]
              }
            }
          ]
        }
      }
    ]
  }
}
```

## Troubleshooting Guide

### Common GUI Issues
- **Slow loading**: Check APIC cluster health and browser cache
- **Configuration not applying**: Verify fault conditions and policy resolution
- **Missing options**: Check user permissions and role-based access

### Common REST API Issues
- **Authentication failures**: Verify token validity and permissions
- **Timeout errors**: Implement retry logic and check system load
- **Validation errors**: Verify JSON syntax and required attributes

### Diagnostic Commands via REST API
```bash
# Check APIC cluster status
GET /api/node/class/topSystem.json

# Verify policy resolution
GET /api/mo/uni/tn-TENANT/ap-APP/epg-EPG.json?query-target=children&target-subtree-class=fvRtdEpP

# Check endpoint learning
GET /api/class/fvCEp.json?query-target-filter=wcard(fvCEp.dn,"TENANT")
```
