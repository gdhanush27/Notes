## Configuration Hierarchy
```
Fabric
├── Tenants
│   ├── VRF/Context
│   ├── Bridge Domains (BD)
│   ├── Application Profiles
│   │   └── Endpoint Groups (EPG)
│   ├── Contracts
│   │   ├── Subjects
│   │   └── Filters
│   └── Layer 3 Outside (L3Out)
└── Fabric Access Policies
    ├── Interface Policies
    ├── Switch Policies
    └── VLAN/VXLAN Pools
```

## Tenant Configuration

### Creating a Tenant
**GUI Path:** `Tenants → Add Tenant`

**CLI Syntax:**
```bash
configure terminal
tenant <TENANT_NAME>
```

**Parameters:**
- **Name** (Required): Alphanumeric string, max 64 characters
- **Description** (Optional): Text description, max 128 characters
- **Security Domains** (Optional): Array of security domain names

**REST API JSON:**
```json
{
  "fvTenant": {
    "attributes": {
      "name": "TENANT_NAME",
      "descr": "Description",
      "dn": "uni/tn-TENANT_NAME"
    }
  }
}
```

## VRF/Context Configuration

### Creating a VRF
**GUI Path:** `Tenants → [Tenant] → Networking → VRFs → Create VRF`

**CLI Syntax:**
```bash
configure terminal
tenant <TENANT_NAME>
vrf context <VRF_NAME>
```

**Required Parameters:**
- **Name**: VRF identifier (max 64 chars)

**Optional Parameters:**
- **Policy Control Enforcement**: `enforced` | `unenforced`
- **Policy Control Direction**: `ingress` | `egress`
- **IP Data-plane Learning**: `enabled` | `disabled`
- **Preferred Group**: `enabled` | `disabled`
- **BD Enforcement**: `enabled` | `disabled`

**CLI Configuration Example:**
```bash
(config-tenant-vrf)# contract enforce ingress egress
(config-tenant-vrf)# ip data-plane learning disable
(config-tenant-vrf)# preferred-group enable
```

## Bridge Domain (BD) Configuration

### Creating a Bridge Domain
**GUI Path:** `Tenants → [Tenant] → Networking → Bridge Domains → Create Bridge Domain`

**CLI Syntax:**
```bash
configure terminal
tenant <TENANT_NAME>
bridge-domain <BD_NAME>
```

**Required Parameters:**
- **Name**: Bridge Domain identifier
- **VRF**: Associated VRF/Context name

**Optional Parameters:**
- **Subnet**: Gateway IP addresses
- **L2 Unknown Unicast**: `flood` | `proxy`
- **L3 Unknown Multicast Flooding**: `flood` | `opt-flood`
- **Multi Destination Flooding**: `bd-flood` | `drop` | `encap-flood`
- **ARP Flooding**: `enabled` | `disabled`
- **Unicast Routing**: `enabled` | `disabled`
- **Endpoint Dataplane Learning**: `enabled` | `disabled`
- **IP Learning**: `enabled` | `disabled`

**CLI Configuration Example:**
```bash
(config-tenant-bd)# vrf member <VRF_NAME>
(config-tenant-bd)# subnet <IP_ADDRESS/MASK> scope public
(config-tenant-bd)# subnet <IP_ADDRESS/MASK> scope private
(config-tenant-bd)# arp flooding enable
(config-tenant-bd)# unicast-routing enable
(config-tenant-bd)# l2-unknown-unicast proxy
```

**Subnet Scope Options:**
- **public**: Advertised externally
- **private**: Internal to fabric
- **shared**: Shared between VRFs

## Application Profile Configuration

### Creating Application Profile
**GUI Path:** `Tenants → [Tenant] → Application Profiles → Create Application Profile`

**CLI Syntax:**
```bash
configure terminal
tenant <TENANT_NAME>
application <APP_PROFILE_NAME>
```

**Parameters:**
- **Name** (Required): Application profile identifier
- **Description** (Optional): Text description
- **Priority**: `unspecified` | `level1` | `level2` | `level3`

## Endpoint Group (EPG) Configuration

### Creating EPG
**GUI Path:** `Tenants → [Tenant] → Application Profiles → [App Profile] → Application EPGs → Create Application EPG`

**CLI Syntax:**
```bash
configure terminal
tenant <TENANT_NAME>
application <APP_PROFILE_NAME>
epg <EPG_NAME>
```

**Required Parameters:**
- **Name**: EPG identifier
- **Bridge Domain**: Associated BD name

**Optional Parameters:**
- **Priority**: `unspecified` | `level1` | `level2` | `level3`
- **Intra EPG Isolation**: `enforced` | `unenforced`
- **Preferred Group Member**: `include` | `exclude`
- **Custom QoS Policy**: Policy name
- **Flood on Encapsulation**: `enabled` | `disabled`
- **PC Enforcement Preference**: `enforced` | `unenforced`

**CLI Configuration Example:**
```bash
(config-tenant-app-epg)# bridge-domain member <BD_NAME>
(config-tenant-app-epg)# contract provider <CONTRACT_NAME>
(config-tenant-app-epg)# contract consumer <CONTRACT_NAME>
(config-tenant-app-epg)# domain member <DOMAIN_NAME>
```

**Domain Types:**
- **Physical Domain**: `phys <DOMAIN_NAME>`
- **VMware Domain**: `vmware <DOMAIN_NAME>`
- **L3 Domain**: `l3dom <DOMAIN_NAME>`

## Contract Configuration

### Creating Contract
**GUI Path:** `Tenants → [Tenant] → Security Policies → Contracts → Create Contract`

**CLI Syntax:**
```bash
configure terminal
tenant <TENANT_NAME>
contract <CONTRACT_NAME>
```

**Parameters:**
- **Name** (Required): Contract identifier
- **Scope**: `application-profile` | `tenant` | `context` | `global`
- **Priority**: `unspecified` | `level1` | `level2` | `level3`
- **Target DSCP**: `unspecified` | `CS0-CS7` | `AF11-AF43` | `EF`

**Subject Configuration:**
```bash
(config-tenant-contract)# subject <SUBJECT_NAME>
(config-tenant-contract-subj)# access-group <FILTER_NAME>
```

### Creating Filter
**GUI Path:** `Tenants → [Tenant] → Security Policies → Filters → Create Filter`

**CLI Syntax:**
```bash
configure terminal
tenant <TENANT_NAME>
filter <FILTER_NAME>
```

**Filter Entry Parameters:**
- **Name**: Entry identifier
- **EtherType**: `ip` | `arp` | `ipv4` | `ipv6` | Custom
- **IP Protocol**: `tcp` | `udp` | `icmp` | `eigrp` | `ospf` | Custom
- **Source Port Range**: `unspecified` | `dns` | `ftp` | `http` | `https` | `smtp` | `ssh` | Custom
- **Destination Port Range**: Same as source port options
- **TCP Session Rules**: `unspecified` | `ack` | `est` | `fin` | `rst` | `syn`

**CLI Filter Entry Example:**
```bash
(config-tenant-filter)# entry <ENTRY_NAME>
(config-tenant-filter-entry)# ethertype ip
(config-tenant-filter-entry)# protocol tcp
(config-tenant-filter-entry)# source-port unspecified
(config-tenant-filter-entry)# destination-port https
(config-tenant-filter-entry)# tcp-session-rules established
```

## Layer 3 Outside (L3Out) Configuration

### Creating L3Out
**GUI Path:** `Tenants → [Tenant] → Networking → L3Outs → Create L3Out`

**CLI Syntax:**
```bash
configure terminal
tenant <TENANT_NAME>
l3out <L3OUT_NAME>
```

**Parameters:**
- **Name** (Required): L3Out identifier
- **VRF**: Associated VRF name
- **L3 Domain**: External routed domain
- **OSPF/BGP Area**: Routing protocol configuration

**Node Profile Configuration:**
```bash
(config-tenant-l3out)# node-profile <PROFILE_NAME>
(config-tenant-l3out-node)# node <NODE_ID> router-id <ROUTER_ID>
(config-tenant-l3out-node)# interface-profile <INTERFACE_PROFILE_NAME>
```

## Access Policies Configuration

### VLAN Pool
**GUI Path:** `Fabric → Access Policies → Pools → VLAN → Create VLAN Pool`

**Parameters:**
- **Name** (Required): Pool identifier
- **Allocation Mode**: `static` | `dynamic`
- **VLAN Range**: Start and End VLAN IDs
- **Role**: `internal` | `external`

### Domain Configuration
**GUI Path:** `Fabric → Access Policies → Physical and External Domains`

**Types and Parameters:**
- **Physical Domain**:
  - VLAN Pool association
  - AAEP (Attachable Access Entity Profile)
- **VMware VMM Domain**:
  - vCenter credentials
  - Datacenter name
  - VLAN Pool
  - VXLAN Pool

### Interface Policy Groups
**GUI Path:** `Fabric → Access Policies → Interface → Policy Groups`

**Types:**
- **Leaf Access Port**: For server connections
- **PC/vPC Interface**: For port channels
- **Leaf Breakout Port**: For breakout cables

## Common CLI Show Commands (Read-Only)

```bash
# Fabric topology
show controller
show topology
show fabric node-status

# Tenant information
show tenant <TENANT_NAME>
show tenant <TENANT_NAME> brief

# EPG and endpoint information
show epg <EPG_NAME>
show endpoint
show endpoint epg <EPG_NAME>

# Bridge domain information
show bridge-domain <BD_NAME>
show bridge-domain <BD_NAME> detail

# Contract information
show contract <CONTRACT_NAME>
show contract usage

# Health monitoring
show system internal health-stats
show health-stats system
```

## Best Practices

### Naming Conventions
- Use descriptive, consistent naming
- Include environment prefix (PROD, DEV, TEST)
- Avoid special characters except hyphens and underscores
- Maximum length considerations for GUI compatibility

### Security
- Follow least privilege principle in contracts
- Use specific filters instead of "any/any" rules
- Implement proper microsegmentation
- Regular audit of contract usage

### Performance
- Limit the number of EPGs per BD (recommended < 100)
- Use appropriate flooding settings for BD
- Monitor contract rule utilization
- Plan VRF boundaries carefully

## Troubleshooting Commands

```bash
# Fabric health
show health-stats fabric
show health-stats fabric detail

# Endpoint learning
show endpoint tracking
show endpoint learning-log

# Contract debugging
show contract usage
show policy-element contract <CONTRACT_NAME>

# Fault monitoring
show fault critical
show fault major
show fault minor
```

## REST API Examples

### Tenant Creation
```json
POST: https://<APIC_IP>/api/mo/uni.json
{
  "fvTenant": {
    "attributes": {
      "name": "PRODUCTION_TENANT",
      "descr": "Production environment tenant"
    }
  }
}
```

### EPG with Contract
```json
{
  "fvAEPg": {
    "attributes": {
      "name": "WEB_EPG",
      "prio": "unspecified"
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
        "fvRsCons": {
          "attributes": {
            "tnVzBrCPName": "WEB_CONTRACT"
          }
        }
      }
    ]
  }
}
```
