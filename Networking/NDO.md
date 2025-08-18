# Cisco Nexus Dashboard Orchestrator Configuration Guide - README

> **Version**: ACI Fabrics, Release 4.2(x)  
> **Last Updated**: January 15, 2024

## 📋 Table of Contents

1. [Overview](#overview)
2. [Dashboard Navigation](#dashboard-navigation)
3. [Templates Overview](#templates-overview)
4. [Getting Started Workflow](#getting-started-workflow)
5. [Application & Fabric Management](#application--fabric-management)
6. [Operations](#operations)
7. [Infrastructure Management](#infrastructure-management)
8. [Features and Use Cases](#features-and-use-cases)
9. [Best Practices](#best-practices)

---

## 🔍 Overview

Cisco Nexus Dashboard Orchestrator (NDO) is a centralized management platform for configuring and monitoring Cisco APIC, Cloud Network Controller, and NDFC deployments across multiple sites.

### Key Components
- **Multi-Site Management**: Configure policies across multiple ACI fabrics
- **Template-Based Deployment**: Use templates for consistent policy deployment
- **Configuration Drift Detection**: Monitor and reconcile configuration differences
- **Version Control**: Track and rollback template changes

---

## 🎛️ Dashboard Navigation

### Main Navigation Areas

#### 1. Overview
**Purpose**: Global view of multi-site implementations and health status

**Steps to Access**:
1. Login to Nexus Dashboard Orchestrator
2. Click **Overview** from main navigation
3. Toggle between **Global View** and **Journey** modes

**Key Features**:
- Site health status visualization
- Audit logs summary
- Fabric interconnect status
- Template sync status

#### 2. Operate
**Purpose**: Perform operational functions on sites and tenants

**Available Functions**:
- **Sites Management**: View site status, add new sites, access audit logs
- **Tenant Operations**: Manage tenant associations and permissions

#### 3. Configure
**Purpose**: Configure connectivity and templates

**Main Sections**:
- **Site to Site Connectivity**: Manage inter-site connections
- **Tenant Templates**: Application, L3Out, Monitoring, Service Device, Tenant Policies
- **Fabric Templates**: Fabric Policies, Resources, Monitoring Access

#### 4. Admin
**Purpose**: Administrative functions

**Available Options**:
- Software Management
- Backup & Restore
- System Configuration
- Integrations (SD-WAN, DNA Center)
- Tech Support

---

## 📋 Templates Overview

### Template Types

#### 1. Application Templates (ACI Multi-Cloud)
- **Multi-Site**: Templates for stretched or site-local policies with inter-site connectivity
- **Autonomous**: Templates for isolated sites without inter-site connectivity

#### 2. Tenant Policy Templates
- Route Map Policies (Multicast/Route Control)
- Custom QoS Policies
- DHCP Relay/Option Policies
- IGMP Interface/Snooping Policies

#### 3. Fabric Policy Templates
- VLAN Pools, Physical Domains
- Interface/Node/Pod Settings
- QoS Policies, NTP/PTP Policies

### Template Design Patterns

#### Single Template Deployment
```
Schema1
└── Template1 (All objects: VRFs, BDs, EPGs, Contracts)
    ├── Site1 ✓
    ├── Site2 ✓
    └── Site3 ✓
```

#### Network/Policy Separation
```
Schema1 (Networking)
└── NetworkTemplate (VRFs, BDs, Subnets)

Schema2 (Applications)  
└── AppTemplate (EPGs, Contracts, Filters)
    └── References: Schema1.NetworkTemplate
```

#### Site-Based Separation
```
Schema1
├── Site1Template (Site1-specific objects)
├── Site2Template (Site2-specific objects)
├── SharedTemplate (Cross-site objects)
└── Site1-Site2-SharedTemplate (Specific sharing)
```

---

## 🚀 Getting Started Workflow

### Step 1: Initial Setup

#### Add Sites
1. Navigate to **Operate > Sites**
2. Click **Add Site**
3. Provide site details:
   - Site Name and Type
   - Controller IP/Credentials
   - Site Role (Spine/Leaf configuration)
4. Click **Save**

#### Create/Import Tenants
**Option A - Create New Tenant**:
1. Go to **Operate > Tenants**
2. Click **Create Tenant**
3. Configure:
   - Display Name and Description
   - Associated Sites
   - Security Domains (optional)
   - Associated Users
4. Click **Save**

**Option B - Import Existing Tenant**:
1. Go to **Operate > Sites**
2. Find site → Click **⋯** → **Import Tenants**
3. Select tenants to import
4. Click **OK**

### Step 2: Configure Site-to-Site Connectivity

1. Navigate to **Configure > Site to Site Connectivity**
2. Review current settings:
   - BGP Peering Type
   - Keep alive/Hold/Stale intervals
   - Graceful Restart settings
3. Click **Configure** to modify settings
4. Click **Deploy** to apply changes

### Step 3: Create and Deploy Templates

#### Create Application Template
1. Go to **Configure > Tenant Templates > Applications**
2. Click **Add Schema**
3. Provide schema name and template details
4. Add template objects as needed
5. Associate template with sites
6. Deploy template

---

## 🏗️ Application & Fabric Management

### Schema and Template Operations

#### Creating Schemas and Templates

**Steps**:
1. **Configure > Tenant Templates > Applications**
2. Click **Add Schema**
3. Configure schema properties:
   - Schema Name
   - Template Name  
   - Associated Tenant
4. Add template objects:
   - VRFs
   - Bridge Domains
   - EPGs
   - Contracts and Filters

#### Template Assignment to Sites

**Steps**:
1. Select template in schema view
2. Click **Actions > Add/Remove Sites**
3. Select target sites
4. Click **OK**

#### Deploying Templates

**Pre-deployment Checklist**:
- [ ] All dependent objects exist
- [ ] Template assigned to sites
- [ ] Review deployment plan
- [ ] Template approved (if change control enabled)

**Deployment Steps**:
1. Select template
2. Click **Deploy Template**
3. Review **Deployment Plan**:
   - Verify objects to be created/modified/deleted
   - Check site-specific configurations
   - Review XML payload if needed
4. Click **Deploy**

#### Template Versioning and Management

**Version Control Features**:
- Maximum 20 Deployed + 20 Intermediate versions per template
- Deployed versions: Successfully deployed to sites
- Intermediate versions: Saved but not deployed

**Version Operations**:
1. **View History**: Actions → **View Version History**
2. **Tag Golden Version**: Actions → **Tag**
3. **Rollback**: Actions → **Rollback Versions**
4. **Compare Versions**: Select version in history view

#### Configuration Drift Management

**Causes of Configuration Drift**:
- Template modified in NDO but not deployed
- Configuration changed directly in APIC
- NDO restored from backup
- NDO upgrade with new properties

**Drift Reconciliation Steps**:
1. Navigate to drifted template (shows "Out of Sync")
2. Actions → **Reconcile Configuration Drift**
3. Review template-level differences
4. Choose NDO or site configuration for each difference
5. Review site-specific properties
6. Click **Preview Changes**
7. Click **Deploy to Sites** to reconcile

### Bulk Update Operations

**Supported Objects**: EPGs, Bridge Domains, Contracts, VRFs, External EPGs

**Steps**:
1. Navigate to template
2. Click **Select** mode
3. Select multiple objects of same type
4. Click **⋯** → **Edit**
5. Configure bulk properties:
   - EPG: Bridge Domain, Contracts, EPG Type, etc.
   - BD: VRF, L2 Stretch, Unicast Routing, etc.
   - Contracts: Scope, Filter Chain, QoS Level
6. Click **Save**

---

## ⚙️ Operations

### Audit Logs
**Access**: **Operate > Sites** → **Audit Logs**
- View system events and changes
- Filter by time range and severity
- Export logs for analysis

### Backup and Restore

#### Create Backup
1. **Admin > Backup & Restore**
2. Click **Create Backup**
3. Configure:
   - Backup name and description
   - Include configuration/audit logs
   - Remote location (optional)
4. Click **Create**

#### Restore Configuration
1. **Admin > Backup & Restore**
2. Select backup
3. Click **Restore**
4. Confirm restoration

#### Schedule Backups
1. **Admin > Backup & Restore**
2. Click **No Schedule** → **Create Schedule**
3. Configure:
   - Schedule frequency
   - Backup retention
   - Remote location
4. Click **Save**

### Site Upgrades

#### Download Firmware
1. **Admin > Software Management**
2. Click **Setup Download**
3. Select sites and firmware version
4. Click **Download**

#### Upgrade Controllers
1. **Software Management** → Select site
2. **Set Update** → **Controllers**
3. Select firmware version
4. Configure maintenance window
5. Click **Upgrade**

#### Upgrade Switches
1. **Software Management** → Select site  
2. **Set Update** → **Switches**
3. Select switch group and firmware
4. Configure upgrade parameters
5. Click **Upgrade**

---

## 🏢 Infrastructure Management

### Adding and Managing Sites

#### Add APIC Site
1. **Operate > Sites** → **Add Site**
2. Configure site details:
   - **Name**: Unique site identifier
   - **URL**: APIC management IP/FQDN
   - **Username/Password**: APIC credentials
   - **Login Domain**: Authentication domain
3. Click **Save**
4. Verify site connectivity

#### Site Configuration

**Infra Settings**:
1. **Configure > Site to Site Connectivity**
2. Select site → **Configure**
3. Configure:
   - Pod settings
   - Spine switch configurations  
   - BGP settings
4. **Deploy** configuration

### CloudSec Encryption

#### Requirements
- APIC release 5.2(1) or later
- Supported hardware platforms
- Proper network connectivity

#### Configuration Steps

**1. APIC Configuration**:
```bash
# Enable CloudSec on APIC
configure
crypto pki trustpoint CloudSec
crypto pki authenticate CloudSec
```

**2. NDO Configuration**:
1. **Configure > Site to Site Connectivity**
2. **General Settings** → Enable **CloudSec Encryption**
3. Configure encryption parameters
4. **Deploy** to sites

**3. Verification**:
```bash
# Verify on switch
show crypto engine brief
show crypto session brief
```

---

## 🌟 Features and Use Cases

### DHCP Relay Configuration

#### Create DHCP Relay Policy
1. **Configure > Tenant Templates > Tenant Policies**
2. **Create Tenant Policy Template**
3. **+Create Object** → **DHCP Relay Policy**
4. Configure providers:
   - **Application EPG** or **L3 External Network**
   - DHCP server IP address
   - VRF preference (if needed)
5. **Save** policy

#### Create DHCP Option Policy  
1. In same template → **+Create Object** → **DHCP Option Policy**
2. **Add Option**:
   - Name (e.g., "Name Server")
   - ID and Data values
3. **Save** policy

#### Assign DHCP Policies
1. Navigate to Bridge Domain in application template
2. **DHCP Configuration** section
3. Select DHCP Relay and Option policies
4. **Deploy** template

### External Connectivity (L3Out)

#### Create L3Out Template
1. **Configure > Tenant Templates > L3Out**
2. **Create L3Out Template**
3. Configure L3Out properties:
   - Name and VRF association
   - Route Map policies
   - External EPGs
4. Add site-specific configurations:
   - Physical interfaces
   - SVI configurations
   - BGP/OSPF settings
5. **Deploy** template

### Inter-site L3Out

#### Configure External TEP Pool
1. **Configure > Site to Site Connectivity**
2. **General Settings** → **External TEP Pool**
3. Specify IP range for external connectivity
4. **Deploy** configuration

#### Create Inter-site External EPG
1. In L3Out template → **External EPGs**
2. Enable **Inter-site L3Out**
3. Configure subnet mappings
4. **Deploy** template

### QoS Configuration

#### Global DSCP Policy
1. **Configure > Site to Site Connectivity**
2. **General Settings** → **Global DSCP Policy**
3. Configure DSCP-to-priority mappings
4. **Deploy** to sites

#### Custom QoS Policy
1. **Tenant Policy Template** → **Custom QoS Policy**
2. Configure DSCP/CoS mappings:
   - DSCP range and target values
   - CoS range and target values  
   - Priority assignments
3. **Deploy** template

### Layer 3 Multicast

#### Create Multicast Route Map
1. **Tenant Policy Template** → **Route Map Policy for Multicast**
2. **Add Route Map Entries**:
   - Group IP range (224.0.0.0-239.255.255.255)
   - Source IP (for filtering)
   - RP IP (for RP configuration)
   - Action (Permit/Deny)
3. **Deploy** template

#### Enable ASM/SSM Multicast
1. In VRF configuration → **Multicast**
2. Configure:
   - **ASM**: Any-Source Multicast settings
   - **SSM**: Source-Specific Multicast range
   - Route Map association
3. **Deploy** template

### SD-Access Integration

#### Onboard DNA Center
1. **Admin > Integrations** → **SD-Access**
2. **Add DNA Center**:
   - Management IP and credentials
   - Trust certificates
3. **Save** integration

#### Configure Connectivity
1. **L3Out Template** → External EPG
2. Enable **SD-Access** connectivity
3. Configure Virtual Network mappings
4. **Deploy** template

### Service Chaining with PBR

#### Create Service Device Template  
1. **Configure > Tenant Templates > Service Device**
2. **Create Service Device Template**
3. Configure service device:
   - Device type and interfaces
   - Service graph template
   - Device clustering (if applicable)
4. **Deploy** template

#### Add Service Chaining to Contract
1. In Application template → **Contract**
2. **Service Graph** section
3. Select service device template
4. Configure connector mappings
5. **Deploy** template

---

## 📝 Best Practices

### Template Design
1. **Follow Dependencies**: Deploy objects in correct dependency order
2. **Avoid Cycles**: No circular dependencies across templates  
3. **Plan Scale**: Consider verified scalability limits
4. **Use Separation**: Separate network and policy objects when beneficial

### Configuration Management
1. **Version Control**: Tag golden versions and track changes
2. **Change Control**: Enable template approval for production
3. **Drift Monitoring**: Regularly check and reconcile configuration drifts
4. **Backup Strategy**: Schedule regular backups with retention

### Deployment Strategy
1. **Test First**: Deploy to test sites before production
2. **Review Plans**: Always review deployment plans before deploying
3. **Staged Rollouts**: Deploy to sites incrementally
4. **Rollback Plan**: Keep previous working versions tagged

### Security and Access
1. **Role-Based Access**: Use appropriate user roles (Designer/Approver/Deployer)
2. **Security Domains**: Implement tenant isolation where needed
3. **Audit Trails**: Monitor audit logs for unauthorized changes
4. **Regular Updates**: Keep NDO and site controllers updated

### Monitoring and Maintenance
1. **Health Monitoring**: Regularly check site and fabric health
2. **Performance**: Monitor template deployment times and success rates
3. **Capacity Planning**: Track object counts against scale limits
4. **Documentation**: Maintain documentation of template purposes and dependencies

### Troubleshooting
1. **Logs Analysis**: Use audit logs and system logs for troubleshooting
2. **Configuration Validation**: Use deployment plans to validate changes
3. **Site Connectivity**: Verify inter-site connectivity before deployments
4. **Version Comparison**: Use version history to identify problematic changes

---

## 🔧 Common Commands and Operations

### Template Operations
```bash
# View template deployment status
GET /api/v1/templates/{template-id}/deployment-status

# Deploy template with version check
PUT /api/v1/templates/{template-id}/deploy?enableVersionCheck=true

# Get template version history  
GET /api/v1/templates/{template-id}/versions
```

### Site Operations
```bash
# Check site connectivity
GET /api/v1/sites/{site-id}/health

# Import tenant from site
POST /api/v1/sites/{site-id}/tenants/import

# Refresh site information
POST /api/v1/sites/{site-id}/refresh
```

---

## 📚 Additional Resources

- **Cisco Nexus Dashboard Orchestrator Documentation**: [docs.cisco.com](https://docs.cisco.com)
- **APIC Configuration Guides**: Platform-specific configuration details
- **NDO Verified Scalability Guides**: Scale limits and recommendations  
- **Community Forums**: Cisco Community for NDO discussions
- **TAC Support**: Technical Assistance Center for production issues

---

*This README provides a comprehensive guide to Cisco Nexus Dashboard Orchestrator configuration and operations. For detailed technical specifications and advanced configurations, refer to the official Cisco documentation.*
