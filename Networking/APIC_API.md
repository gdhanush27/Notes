# Cisco APIC API Reference Documentation

A comprehensive collection of official Cisco APIC (Application Policy Infrastructure Controller) REST API documentation, references, and developer resources. This repository serves as a centralized guide for network engineers and developers working with Cisco ACI programmability.

## 📚 Table of Contents
- [Introduction](#introduction)
- [Official API Configuration Guides](#official-api-configuration-guides)
- [Management Information Model (MIM) References](#management-information-model-mim-references)
- [Developer Resources and Tools](#developer-resources-and-tools)
- [Additional Reference Materials](#additional-reference-materials)
- [Tools and Utilities](#tools-and-utilities)
- [Community and Learning Resources](#community-and-learning-resources)
- [API Reference and Examples](#api-reference-and-examples)
  - [Authentication](#authentication)
  - [Tenant Management](#tenant-management)
  - [Network Configuration](#network-configuration)
  - [Application Profiles and EPGs](#application-profiles-and-epgs)
  - [Contracts and Filters](#contracts-and-filters)
  - [Contract Association](#contract-association)
  - [Querying Objects](#querying-objects)
- [Quick Start Guide](#quick-start-guide)

## 🌟 Introduction

Cisco ACI provides a comprehensive REST API for automating network configuration, management, and monitoring. This documentation collection covers everything from basic API concepts to advanced object model references and practical implementation guides.

**Key Concepts:**
- **REST API**: Programmatic interface using HTTP/HTTPS with JSON/XML payloads
- **Management Information Model (MIM)**: Hierarchical tree of managed objects (MOs)
- **Object-Oriented Model**: Complete configuration and runtime state representation
- **Policy-Based Configuration**: Intent-driven network automation

## 📖 Official API Configuration Guides

### Primary Documentation
| Document | Format | Description | Link |
|----------|--------|-------------|------|
| **Cisco APIC REST API Configuration Guide (4.2x+)** | [HTML](https://www.cisco.com/c/en/us/td/docs/dcn/aci/apic/all/apic-rest-api-configuration-guide/cisco-apic-rest-api-configuration-guide-42x-and-later.html) / [PDF](https://www.cisco.com/c/en/us/td/docs/dcn/aci/apic/all/apic-rest-api-configuration-guide/cisco-apic-rest-api-configuration-guide-42x-and-later.pdf) | Comprehensive REST API reference with examples | [Direct Usage Section](https://www.cisco.com/c/en/us/td/docs/dcn/aci/apic/all/apic-rest-api-configuration-guide/cisco-apic-rest-api-configuration-guide-42x-and-later/m_using_the_rest_api.html) |
| **Cisco APIC REST API User Guide** | [HTML](https://www.cisco.com/c/en/us/td/docs/switches/datacenter/aci/apic/sw/1-x/api/rest/b_APIC_RESTful_API_User_Guide/overview_of_the.html) | Introduction to REST API concepts and architecture | [Link](https://www.cisco.com/c/en/us/td/docs/switches/datacenter/aci/apic/sw/1-x/api/rest/b_APIC_RESTful_API_User_Guide/overview_of_the.html) |

### Key Sections in Configuration Guides
- **Authentication**: Token-based authentication with aaaLogin
- **REST Methods**: POST, GET, DELETE operations
- **Payload Formats**: JSON and XML encoding examples
- **Object Management**: Creating, reading, updating, deleting MOs
- **Error Handling**: Fault codes and troubleshooting

## 🏗️ Management Information Model (MIM) References

### Object Model Documentation
| Resource | Description | Link |
|----------|-------------|------|
| **Cisco DevNet APIC Object Model Reference** | Complete MO reference with properties, relationships, and containment | [Latest](https://developer.cisco.com/docs/apic-mim/latest/) |
| **API Version Selector** | Choose specific APIC MIM release (6.1x to 2.2x) | [Selector](https://developer.cisco.com/site/apic-mim-ref-api/) |
| **MIM Reference Guide** | Official comprehensive MO reference (PDF typically available with software) | Referenced in [Fundamentals Guide](https://www.cisco.com/c/en/us/td/docs/dcn/aci/apic/6x/aci-fundamentals/cisco-aci-fundamentals-60x.html) |

### Understanding the MIM
- **Hierarchical Structure**: Root → Parent → Child objects
- **Distinguished Names (DN)**: Unique object identifiers
- **Managed Objects (MOs)**: Represent physical and logical components
- **Relationships**: Parent-child, association, and composition relationships

## 🛠️ Developer Resources and Tools

### Cisco DevNet ACI Portal
| Resource | Description | Link |
|----------|-------------|------|
| **ACI Programmability Portal** | Central hub for ACI development resources | [Portal](https://developer.cisco.com/site/aci/) |
| **ACI API Configuration Guide** | Developer-focused API documentation | [Guide](https://developer.cisco.com/docs/aci/) |
| **Python SDK Documentation** | Cobra SDK API reference and examples | [API Ref](https://cobra.readthedocs.io/en/latest/api-ref/) / [Main Docs](https://cobra.readthedocs.io/en/latest/) |

### SDKs and Libraries
- **Cobra SDK**: Python library for ACI automation
- **REST API Clients**: Direct HTTP/HTTPS integration
- **Ansible Modules**: ACI automation with Ansible
- **Terraform Providers**: Infrastructure as Code for ACI

## 📚 Additional Reference Materials

### Architecture and Concepts
| Document | Description | Link |
|----------|-------------|------|
| **Cisco ACI Policy Model Guide** | Understanding ACI policy constructs | [HTML](https://www.cisco.com/c/en/us/td/docs/switches/datacenter/aci/apic/sw/policy-model-guide/b-Cisco-ACI-Policy-Model-Guide.html) |
| **ACI Fundamentals (6.0x)** | Core concepts and architecture | [HTML](https://www.cisco.com/c/en/us/td/docs/dcn/aci/apic/6x/aci-fundamentals/cisco-aci-fundamentals-60x.html) / [PDF](https://www.cisco.com/c/en/us/td/docs/dcn/aci/apic/6x/aci-fundamentals/cisco-aci-fundamentals-60x.pdf) |
| **APIC CLI Reference** | Command-line interface for object management | [CLI Guide](https://www.cisco.com/c/en/us/td/docs/switches/datacenter/aci/apic/sw/1-x/cli/b_APIC_CLI_User_Guide/b_APIC_CLI_User_Guide_chapter_011.html) |

### Key Topics
- **Contract Model**: EPG communication through contracts
- **Tenant Configuration**: Multi-tenancy concepts
- **VRF and Bridge Domains**: L3 and L2 networking
- **Application Profiles**: Grouping EPGs and policies

## 🧰 Tools and Utilities

### Object Browsers and Explorers
| Tool | Description | Link |
|------|-------------|------|
| **APIC Managed Object Browser** | Third-party graphical MO tree browser | [DC App Center](https://dcappcenter.cisco.com/apic-managed-object-browser.html) / [Alternative](https://haystacknetworks.com/cisco-apic-managed-object-browser) |
| **Built-in APIC API Documentation** | Real-time API docs on your APIC controller | `https://<APIC_IP>/api/doc` |
| **API Inspector** | GUI tool for viewing API calls | Available in APIC GUI (System Tools → Show API Inspector) |

### Development Tools
- **Postman Collections**: API testing and exploration
- **Visore**: Built-in MO browser (APIC GUI)
- **moquery**: CLI tool for querying MOs
- **ACI Toolkit**: Development and testing utilities

## 👥 Community and Learning Resources

### Learning and Training
| Resource | Description | Link |
|----------|-------------|------|
| **Cisco Learning Labs** | Hands-on ACI API labs | [DevNet Labs](https://developer.cisco.com/site/aci/) |
| **Cisco Live Presentations** | Conference sessions on ACI programmability | [Videos](https://developer.cisco.com/site/aci/) |
| **ACI Developer Videos** | Tutorial and demonstration videos | [Video Series](https://developer.cisco.com/site/aci/) |

### Community Support
| Resource | Description | Link |
|----------|-------------|------|
| **Cisco Community Forums** | ACI discussion and support | [ACI Forum](https://community.cisco.com/t5/application-centric-infrastructure/bd-p/7600-discussions-application-centric-infrastructure) |
| **Stack Overflow** | Developer Q&A with ACI tags | [ACI Questions](https://stackoverflow.com/questions/tagged/cisco-aci) |
| **GitHub Repositories** | Sample code and examples | [CiscoDevNet/aci](https://github.com/CiscoDevNet/aci) |

### Sample Code and Examples
- **GitHub**: ACI automation scripts and examples
- **DevNet Code Exchange**: Community-contributed code
- **Cisco Live Labs**: Hands-on workshop materials

## 🔧 API Reference and Examples

### Authentication

All API calls require authentication. The APIC uses token-based authentication with a session cookie.

#### Login and Get Token
```bash
curl -k -X POST https://<APIC_IP>/api/mo/aaaLogin.json \
  -H "Content-Type: application/json" \
  -d '{
    "aaaUser": {
      "attributes": {
        "name": "admin",
        "pwd": "password"
      }
    }
  }'
```

**Response:**
```json
{
  "imdata": [
    {
      "aaaLogin": {
        "attributes": {
          "token": "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9..."
        }
      }
    }
  ]
}
```

#### Using the Token
Include the token in subsequent requests:
```bash
curl -k -X GET https://<APIC_IP>/api/mo/uni.json \
  -H "Cookie: APIC-cookie=<token>"
```

---

### Tenant Management

#### Create a Tenant
```bash
curl -k -X POST https://<APIC_IP>/api/mo/uni.json \
  -H "Content-Type: application/json" \
  -H "Cookie: APIC-cookie=<token>" \
  -d '{
    "fvTenant": {
      "attributes": {
        "name": "Tenant_Practice",
        "descr": "Practice EPG Communication",
        "status": "created"
      }
    }
  }'
```

#### Get Tenant Information
```bash
curl -k -X GET https://<APIC_IP>/api/mo/uni/tn-Tenant_Practice.json \
  -H "Cookie: APIC-cookie=<token>"
```

#### Delete a Tenant
```bash
curl -k -X POST https://<APIC_IP>/api/mo/uni.json \
  -H "Content-Type: application/json" \
  -H "Cookie: APIC-cookie=<token>" \
  -d '{
    "fvTenant": {
      "attributes": {
        "name": "Tenant_Practice",
        "status": "deleted"
      }
    }
  }'
```

---

### Network Configuration

#### Create a VRF (Context)
```bash
curl -k -X POST https://<APIC_IP>/api/mo/uni/tn-Tenant_Practice.json \
  -H "Content-Type: application/json" \
  -H "Cookie: APIC-cookie=<token>" \
  -d '{
    "fvCtx": {
      "attributes": {
        "name": "VRF_Practice",
        "descr": "VRF for EPG Communication",
        "status": "created"
      }
    }
  }'
```

#### Create a Bridge Domain with Subnet
```bash
curl -k -X POST https://<APIC_IP>/api/mo/uni/tn-Tenant_Practice.json \
  -H "Content-Type: application/json" \
  -H "Cookie: APIC-cookie=<token>" \
  -d '{
    "fvBD": {
      "attributes": {
        "name": "BD_Practice",
        "descr": "Bridge Domain for Practice",
        "status": "created"
      },
      "children": [
        {
          "fvRsCtx": {
            "attributes": {
              "tnFvCtxName": "VRF_Practice"
            }
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
  }'
```

---

### Application Profiles and EPGs

#### Create an Application Profile
```bash
curl -k -X POST https://<APIC_IP>/api/mo/uni/tn-Tenant_Practice.json \
  -H "Content-Type: application/json" \
  -H "Cookie: APIC-cookie=<token>" \
  -d '{
    "fvAp": {
      "attributes": {
        "name": "AppProfile_Practice",
        "descr": "Application Profile for Practice",
        "status": "created"
      }
    }
  }'
```

#### Create an EPG
```bash
curl -k -X POST https://<APIC_IP>/api/mo/uni/tn-Tenant_Practice/ap-AppProfile_Practice.json \
  -H "Content-Type: application/json" \
  -H "Cookie: APIC-cookie=<token>" \
  -d '{
    "fvAEPg": {
      "attributes": {
        "name": "EPG_Web",
        "descr": "Web Server EPG",
        "status": "created"
      },
      "children": [
        {
          "fvRsBd": {
            "attributes": {
              "tnFvBDName": "BD_Practice"
            }
          }
        }
      ]
    }
  }'
```

#### Create Multiple EPGs
```bash
# EPG for Application Servers
curl -k -X POST https://<APIC_IP>/api/mo/uni/tn-Tenant_Practice/ap-AppProfile_Practice.json \
  -H "Content-Type: application/json" \
  -H "Cookie: APIC-cookie=<token>" \
  -d '{
    "fvAEPg": {
      "attributes": {
        "name": "EPG_App",
        "descr": "Application Server EPG",
        "status": "created"
      },
      "children": [
        {
          "fvRsBd": {
            "attributes": {
              "tnFvBDName": "BD_Practice"
            }
          }
        }
      ]
    }
  }'
```

---

### Contracts and Filters

#### Create a Filter
```bash
curl -k -X POST https://<APIC_IP>/api/mo/uni/tn-Tenant_Practice.json \
  -H "Content-Type: application/json" \
  -H "Cookie: APIC-cookie=<token>" \
  -d '{
    "vzFilter": {
      "attributes": {
        "name": "Filter_WebApp",
        "status": "created"
      },
      "children": [
        {
          "vzEntry": {
            "attributes": {
              "name": "Allow_HTTP",
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
              "name": "Allow_HTTPS",
              "etherT": "ip",
              "prot": "tcp",
              "dFromPort": "443",
              "dToPort": "443"
            }
          }
        }
      ]
    }
  }'
```

#### Create a Contract
```bash
curl -k -X POST https://<APIC_IP>/api/mo/uni/tn-Tenant_Practice.json \
  -H "Content-Type: application/json" \
  -H "Cookie: APIC-cookie=<token>" \
  -d '{
    "vzBrCP": {
      "attributes": {
        "name": "Contract_WebApp",
        "descr": "Contract for Web to App Communication",
        "status": "created"
      },
      "children": [
        {
          "vzSubj": {
            "attributes": {
              "name": "Subject_WebApp"
            },
            "children": [
              {
                "vzRsSubjFiltAtt": {
                  "attributes": {
                    "tnVzFilterName": "Filter_WebApp",
                    "status": "created"
                  }
                }
              }
            ]
          }
        }
      ]
    }
  }'
```

---

### Contract Association

#### Configure EPG as Contract Provider
```bash
curl -k -X POST https://<APIC_IP>/api/mo/uni/tn-Tenant_Practice/ap-AppProfile_Practice/epg-EPG_Web.json \
  -H "Content-Type: application/json" \
  -H "Cookie: APIC-cookie=<token>" \
  -d '{
    "fvRsProv": {
      "attributes": {
        "tnVzBrCPName": "Contract_WebApp",
        "status": "created"
      }
    }
  }'
```

#### Configure EPG as Contract Consumer
```bash
curl -k -X POST https://<APIC_IP>/api/mo/uni/tn-Tenant_Practice/ap-AppProfile_Practice/epg-EPG_App.json \
  -H "Content-Type: application/json" \
  -H "Cookie: APIC-cookie=<token>" \
  -d '{
    "fvRsCons": {
      "attributes": {
        "tnVzBrCPName": "Contract_WebApp",
        "status": "created"
      }
    }
  }'
```

---

### Querying Objects

#### Get All Tenants
```bash
curl -k -X GET https://<APIC_IP>/api/class/fvTenant.json \
  -H "Cookie: APIC-cookie=<token>"
```

#### Get Specific Tenant with Children
```bash
curl -k -X GET https://<APIC_IP>/api/mo/uni/tn-Tenant_Practice.json?rsp-subtree=full \
  -H "Cookie: APIC-cookie=<token>"
```

#### Get All EPGs in a Tenant
```bash
curl -k -X GET https://<APIC_IP>/api/class/fvAEPg.json?query-target-filter=eq(fvTenant.name,"Tenant_Practice") \
  -H "Cookie: APIC-cookie=<token>"
```

#### Get EPG Contract Associations
```bash
curl -k -X GET https://<APIC_IP>/api/mo/uni/tn-Tenant_Practice/ap-AppProfile_Practice/epg-EPG_Web.json?rsp-subtree=children \
  -H "Cookie: APIC-cookie=<token>"
```

#### Search for Objects by Name
```bash
curl -k -X GET https://<APIC_IP>/api/class/fvAEPg.json?query-target-filter=wcard(fvAEPg.name,"EPG") \
  -H "Cookie: APIC-cookie=<token>"
```

---

## 🚀 Quick Start Guide

### 1. First Steps
1. **Access Your APIC**: Log in to your APIC GUI
2. **API Inspector**: Enable API Inspector to see GUI operations as API calls
3. **Built-in Docs**: Visit `https://<APIC_IP>/api/doc` for version-specific documentation

### 2. Essential Reading Order
1. Start with **REST API User Guide** for basic concepts
2. Review **REST API Configuration Guide** for detailed operations
3. Use **Object Model Reference** for MO-specific information
4. Explore **DevNet resources** for practical examples

### 3. Development Setup
```bash
# Install Python SDK
pip install cobra-sdk

# Basic API call example
from cobra.mit.access import MoDirectory
from cobra.mit.session import LoginSession
from cobra.mit.request import DnQuery

session = LoginSession('https://<APIC_IP>', '<username>', '<password>')
mo_dir = MoDirectory(session)
mo_dir.login()

# Query a tenant
tenant = mo_dir.lookupByDn('uni/tn-Tenant_Practice')
print(tenant)
```

### 4. Common API Patterns
- **Authentication**: POST to `/api/mo/aaaLogin.json`
- **Object Creation**: POST to `/api/mo/<parent_dn>.json`
- **Object Retrieval**: GET from `/api/mo/<object_dn>.json`
- **Object Deletion**: DELETE to `/api/mo/<object_dn>.json`
- **Class Queries**: GET from `/api/class/<class_name>.json`

### 5. Complete EPG-to-EPG Setup Example
```bash
#!/bin/bash

APIC_IP="192.168.1.1"
USERNAME="admin"
PASSWORD="password"
TENANT="Tenant_Practice"
VRF="VRF_Practice"
BD="BD_Practice"
APP_PROFILE="AppProfile_Practice"
EPG_WEB="EPG_Web"
EPG_APP="EPG_App"
FILTER="Filter_WebApp"
CONTRACT="Contract_WebApp"

# Login
TOKEN=$(curl -sk -X POST https://$APIC_IP/api/mo/aaaLogin.json \
  -H "Content-Type: application/json" \
  -d "{\"aaaUser\":{\"attributes\":{\"name\":\"$USERNAME\",\"pwd\":\"$PASSWORD\"}}}" | \
  jq -r '.imdata[0].aaaLogin.attributes.token')

# Create Tenant
curl -sk -X POST https://$APIC_IP/api/mo/uni.json \
  -H "Content-Type: application/json" \
  -H "Cookie: APIC-cookie=$TOKEN" \
  -d "{\"fvTenant\":{\"attributes\":{\"name\":\"$TENANT\",\"status\":\"created\"}}}"

# Create VRF
curl -sk -X POST https://$APIC_IP/api/mo/uni/tn-$TENANT.json \
  -H "Content-Type: application/json" \
  -H "Cookie: APIC-cookie=$TOKEN" \
  -d "{\"fvCtx\":{\"attributes\":{\"name\":\"$VRF\",\"status\":\"created\"}}}"

# Create Bridge Domain with Subnet
curl -sk -X POST https://$APIC_IP/api/mo/uni/tn-$TENANT.json \
  -H "Content-Type: application/json" \
  -H "Cookie: APIC-cookie=$TOKEN" \
  -d "{
    \"fvBD\":{
      \"attributes\":{\"name\":\"$BD\",\"status\":\"created\"},
      \"children\":[
        {\"fvRsCtx\":{\"attributes\":{\"tnFvCtxName\":\"$VRF\"}}},
        {\"fvSubnet\":{\"attributes\":{\"ip\":\"192.168.10.1/24\"}}}
      ]
    }
  }"

# Create Application Profile
curl -sk -X POST https://$APIC_IP/api/mo/uni/tn-$TENANT.json \
  -H "Content-Type: application/json" \
  -H "Cookie: APIC-cookie=$TOKEN" \
  -d "{\"fvAp\":{\"attributes\":{\"name\":\"$APP_PROFILE\",\"status\":\"created\"}}}"

# Create EPGs
for EPG in $EPG_WEB $EPG_APP; do
  curl -sk -X POST https://$APIC_IP/api/mo/uni/tn-$TENANT/ap-$APP_PROFILE.json \
    -H "Content-Type: application/json" \
    -H "Cookie: APIC-cookie=$TOKEN" \
    -d "{
      \"fvAEPg\":{
        \"attributes\":{\"name\":\"$EPG\",\"status\":\"created\"},
        \"children\":[
          {\"fvRsBd\":{\"attributes\":{\"tnFvBDName\":\"$BD\"}}}
        ]
      }
    }"
done

# Create Filter
curl -sk -X POST https://$APIC_IP/api/mo/uni/tn-$TENANT.json \
  -H "Content-Type: application/json" \
  -H "Cookie: APIC-cookie=$TOKEN" \
  -d "{
    \"vzFilter\":{
      \"attributes\":{\"name\":\"$FILTER\",\"status\":\"created\"},
      \"children\":[
        {\"vzEntry\":{\"attributes\":{\"name\":\"Allow_HTTP\",\"etherT\":\"ip\",\"prot\":\"tcp\",\"dFromPort\":\"80\",\"dToPort\":\"80\"}}}
      ]
    }
  }"

# Create Contract
curl -sk -X POST https://$APIC_IP/api/mo/uni/tn-$TENANT.json \
  -H "Content-Type: application/json" \
  -H "Cookie: APIC-cookie=$TOKEN" \
  -d "{
    \"vzBrCP\":{
      \"attributes\":{\"name\":\"$CONTRACT\",\"status\":\"created\"},
      \"children\":[
        {\"vzSubj\":{\"attributes\":{\"name\":\"Subject_WebApp\"},
          \"children\":[
            {\"vzRsSubjFiltAtt\":{\"attributes\":{\"tnVzFilterName\":\"$FILTER\",\"status\":\"created\"}}}
          ]
        }
      ]
    }
  }"

# Associate Contract with EPGs
curl -sk -X POST https://$APIC_IP/api/mo/uni/tn-$TENANT/ap-$APP_PROFILE/epg-$EPG_WEB.json \
  -H "Content-Type: application/json" \
  -H "Cookie: APIC-cookie=$TOKEN" \
  -d "{\"fvRsProv\":{\"attributes\":{\"tnVzBrCPName\":\"$CONTRACT\",\"status\":\"created\"}}}"

curl -sk -X POST https://$APIC_IP/api/mo/uni/tn-$TENANT/ap-$APP_PROFILE/epg-$EPG_APP.json \
  -H "Content-Type: application/json" \
  -H "Cookie: APIC-cookie=$TOKEN" \
  -d "{\"fvRsCons\":{\"attributes\":{\"tnVzBrCPName\":\"$CONTRACT\",\"status\":\"created\"}}}"

echo "EPG-to-EPG communication setup completed!"
```

## 📝 Contributing

This documentation collection is maintained by the Cisco ACI community. To contribute:
1. Fork this repository
2. Create a feature branch
3. Add or update documentation links
4. Submit a pull request

## 🔗 Related Resources

- [Cisco ACI Product Page](https://www.cisco.com/c/en/us/solutions/data-center-virtualization/application-centric-infrastructure/index.html)
- [Cisco DevNet ACI Sandbox](https://developer.cisco.com/site/sandbox/aci/)
- [Cisco ACI YouTube Channel](https://www.youtube.com/c/ciscoaci)

> This documentation collection is provided for educational purposes. All Cisco documentation is subject to Cisco's terms of use and copyright.
