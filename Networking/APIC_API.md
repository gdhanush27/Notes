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
```

### 4. Common API Patterns
- **Authentication**: POST to `/api/mo/aaaLogin.json`
- **Object Creation**: POST to `/api/mo/<parent_dn>.json`
- **Object Retrieval**: GET from `/api/mo/<object_dn>.json`
- **Object Deletion**: DELETE to `/api/mo/<object_dn>.json`

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
