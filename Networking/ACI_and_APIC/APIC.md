# APIC GUI Complete Guide - EPG to EPG Communication Setup

## 🎯 Objective
Learn APIC GUI elements and create EPG-to-EPG communication for hands-on practice.

---

## 🔍 Part 1: APIC GUI Exploration and Elements

### Accessing APIC GUI
1. **Open Browser** and navigate to your APIC IP: `https://<APIC-IP>`
2. **Login** with your credentials
3. **Accept Certificate** if prompted

### Main GUI Elements Overview

#### 1. Top Navigation Bar
```
[CISCO LOGO] [Search Box] [User Menu] [Help] [Settings]
```
- **Search Box**: Global search for objects and configurations
- **User Menu**: User preferences, logout, change password
- **Help**: Documentation and guided tours
- **Settings**: Display preferences and system settings

#### 2. Left Navigation Panel (Menu Tree)
```
📁 FABRIC
   ├── 📊 Fabric Membership
   ├── 🔗 Access Policies  
   ├── ⚙️ Fabric Policies
   └── 📈 Inventory

📁 TENANTS
   ├── 🏢 Tenant (common)
   ├── 🏢 Tenant (infra) 
   └── ➕ Create Tenant

📁 VIRTUAL NETWORKING
   ├── 🌐 Container Domains
   └── 🖥️ VMM Domains

📁 L4-L7 SERVICES
   ├── 📦 Device Packages
   └── 🔧 Service Graph Templates

📁 ADMIN
   ├── 👤 AAA
   ├── 🔒 Import/Export
   └── ⚙️ System
```

#### 3. Main Content Area
- **Breadcrumb Navigation**: Shows current location
- **Action Bar**: Create, Delete, Edit buttons
- **Object Tables**: Displays configuration objects
- **Property Panels**: Configuration details on the right

#### 4. Right Properties Panel
- **General Properties**: Basic object information
- **Policy Configuration**: Detailed settings
- **Operational Data**: Status and statistics

---

## 🏗️ Part 2: Understanding Fabric Infrastructure

### Leaf Nodes and Fabric Discovery

#### Step 1: Explore Fabric Membership
1. **Navigate**: `Fabric > Fabric Membership`
2. **Observe**:
   - **Discovered Nodes**: All switches detected by APIC
   - **Node ID**: Unique identifier for each switch
   - **Serial Number**: Hardware serial number
   - **Model**: Switch hardware model
   - **Role**: Spine or Leaf designation
   - **Status**: Registered, Unregistered, etc.

#### Step 2: Register Leaf Switches (if needed)
1. **Select Unregistered Node**
2. **Right-click** → **Register**
3. **Configure**:
   - **Node ID**: Assign unique ID (101, 102, etc.)
   - **Node Name**: Descriptive name (leaf-101, leaf-102)
   - **Pod ID**: Usually Pod-1 for single pod
4. **Click Submit**

#### Step 3: Verify Fabric Topology
1. **Navigate**: `Fabric > Inventory > Fabric Membership`
2. **Click Topology Tab**
3. **Observe**:
   - Visual representation of spine-leaf topology
   - Link states between switches
   - Node health status

---

## 🏢 Part 3: Creating Tenant and Basic Structure

### Step 1: Create a New Tenant
1. **Navigate**: `Tenants`
2. **Right-click** on tenant area → **Create Tenant**
3. **Configure Tenant**:
   ```
   Name: Lab-Tenant
   Description: Learning Lab for EPG Communication
   Security Domains: [Leave default]
   ```
4. **Click Submit**

### Step 2: Explore Tenant Structure
After creating tenant, expand `Tenants > Lab-Tenant` to see:
```
📁 Lab-Tenant
   ├── 🌐 Networking
   │   ├── VRFs
   │   ├── Bridge Domains  
   │   └── Subnets
   ├── 📱 Application Profiles
   │   └── Application EPGs
   ├── 🔗 Contracts
   │   ├── Standard
   │   ├── Filters
   │   └── Subjects
   ├── 🔒 Security Policies
   └── 📊 Policies
```

---

## 🌐 Part 4: Creating Network Infrastructure

### Step 1: Create VRF (Virtual Routing and Forwarding)
1. **Navigate**: `Tenants > Lab-Tenant > Networking > VRFs`
2. **Right-click** → **Create VRF**
3. **Configure**:
   ```
   Name: Lab-VRF
   Description: Lab VRF for EPG communication
   Policy Control Enforcement: Enforced
   Policy Control Direction: Ingress
   ```
4. **Click Submit**

### Step 2: Create Bridge Domain
1. **Navigate**: `Tenants > Lab-Tenant > Networking > Bridge Domains`
2. **Right-click** → **Create Bridge Domain**
3. **Configure**:
   ```
   Name: Lab-BD
   Description: Lab Bridge Domain
   VRF: Lab-VRF (select from dropdown)
   L2 Unknown Unicast: Hardware Proxy
   ARP Flooding: Enabled
   Unicast Routing: Enabled
   ```
4. **Click Submit**

### Step 3: Create Subnet for Bridge Domain
1. **Expand**: `Bridge Domains > Lab-BD`
2. **Right-click** on **Subnets** → **Create Subnet**
3. **Configure**:
   ```
   Gateway IP: 10.1.1.1/24
   Description: Lab subnet for EPGs
   Scope: Private to VRF
   Subnet Control: [Leave default]
   ```
4. **Click Submit**

---

## 📱 Part 5: Creating Application Profile and EPGs

### Step 1: Create Application Profile
1. **Navigate**: `Tenants > Lab-Tenant > Application Profiles`
2. **Right-click** → **Create Application Profile**
3. **Configure**:
   ```
   Name: Lab-App
   Description: Lab Application Profile for EPG testing
   ```
4. **Click Submit**

### Step 2: Create First EPG (Web Servers)
1. **Navigate**: `Tenants > Lab-Tenant > Application Profiles > Lab-App`
2. **Right-click** on **Application EPGs** → **Create Application EPG**
3. **Configure**:
   ```
   Name: Web-EPG
   Description: Web servers EPG
   Bridge Domain: Lab-BD (select from dropdown)
   ```
4. **Click Submit**

### Step 3: Create Second EPG (Database Servers)
1. **Right-click** on **Application EPGs** → **Create Application EPG**
2. **Configure**:
   ```
   Name: DB-EPG
   Description: Database servers EPG
   Bridge Domain: Lab-BD (select from dropdown)
   ```
3. **Click Submit**

---

## 🔗 Part 6: Creating Contracts for EPG Communication

### Step 1: Create Filter for HTTP Traffic
1. **Navigate**: `Tenants > Lab-Tenant > Contracts > Filters`
2. **Right-click** → **Create Filter**
3. **Configure**:
   ```
   Name: HTTP-Filter
   Description: Allow HTTP traffic
   ```
4. **Click Submit**

### Step 2: Add Filter Entry
1. **Expand**: `Filters > HTTP-Filter`
2. **Right-click** on **Entries** → **Create Filter Entry**
3. **Configure**:
   ```
   Name: HTTP-Entry
   EtherType: IP
   IP Protocol: TCP
   Destination Port Range From: 80
   Destination Port Range To: 80
   ```
4. **Click Submit**

### Step 3: Create Contract
1. **Navigate**: `Tenants > Lab-Tenant > Contracts > Standard`
2. **Right-click** → **Create Contract**
3. **Configure**:
   ```
   Name: Web-to-DB-Contract
   Description: Allow web to database communication
   Scope: Tenant (default)
   ```
4. **Click Submit**

### Step 4: Create Contract Subject
1. **Expand**: `Contracts > Standard > Web-to-DB-Contract`
2. **Right-click** on **Subjects** → **Create Contract Subject**
3. **Configure**:
   ```
   Name: HTTP-Subject
   Description: HTTP traffic subject
   Apply Both Directions: Yes
   Reverse Filter Ports: Yes
   ```
4. **Click Submit**

### Step 5: Associate Filter to Subject
1. **Expand**: `Subjects > HTTP-Subject`
2. **Right-click** on **Filters** → **Create Filter**
3. **Configure**:
   ```
   Filter: HTTP-Filter (select from dropdown)
   Directive: [Leave default]
   ```
4. **Click Submit**

---

## 🤝 Part 7: Establishing EPG-to-EPG Communication

### Step 1: Configure Web-EPG as Consumer
1. **Navigate**: `Tenants > Lab-Tenant > Application Profiles > Lab-App > Application EPGs > Web-EPG`
2. **In Properties Panel**: Scroll to **Contracts** section
3. **In Consumed Contracts**: Click **+**
4. **Configure**:
   ```
   Contract: Web-to-DB-Contract
   ```
5. **Click Update**

### Step 2: Configure DB-EPG as Provider
1. **Navigate**: `Application EPGs > DB-EPG`
2. **In Properties Panel**: Scroll to **Contracts** section  
3. **In Provided Contracts**: Click **+**
4. **Configure**:
   ```
   Contract: Web-to-DB-Contract
   ```
5. **Click Update**

---

## 🔌 Part 8: Physical Connectivity (Static Path Binding)

### Step 1: Find Available Interfaces
1. **Navigate**: `Fabric > Inventory > Pod-1 > Leaf-101` (or your leaf node)
2. **Click** on **Interfaces**
3. **Note** available interfaces (e.g., eth1/1, eth1/2)

### Step 2: Bind Web-EPG to Physical Interface
1. **Navigate**: `Tenants > Lab-Tenant > Application Profiles > Lab-App > Application EPGs > Web-EPG`
2. **Right-click** on **Static Ports** → **Deploy Static EPG on PC, VPC or Interface**
3. **Configure**:
   ```
   Pod: Pod-1
   Node: 101 (your leaf node)
   Path: eth1/1 (available interface)
   VLAN: 100
   Mode: Regular 802.1P
   Deployment Immediacy: Immediate
   ```
4. **Click Submit**

### Step 3: Bind DB-EPG to Physical Interface  
1. **Navigate**: `Application EPGs > DB-EPG`
2. **Right-click** on **Static Ports** → **Deploy Static EPG on PC, VPC or Interface**
3. **Configure**:
   ```
   Pod: Pod-1
   Node: 101 (your leaf node)  
   Path: eth1/2 (different interface)
   VLAN: 200
   Mode: Regular 802.1P
   Deployment Immediacy: Immediate
   ```
4. **Click Submit**

---

## 🔍 Part 9: Verification and Testing

### Step 1: Verify Policy Deployment
1. **Navigate**: `Tenants > Lab-Tenant > Operational > Policy CAM`
2. **Check**:
   - VRF deployment status
   - Bridge Domain status
   - EPG policy programming

### Step 2: Check Contract Rules
1. **Navigate**: `Tenants > Lab-Tenant > Operational > Contract`
2. **Select**: Web-to-DB-Contract
3. **Verify**: Rule programming and statistics

### Step 3: Monitor Fabric Health
1. **Navigate**: `Fabric > Inventory`
2. **Check Health Scores**:
   - Fabric overall health
   - Individual node health
   - Interface status

### Step 4: View Endpoint Learning
1. **Navigate**: `Tenants > Lab-Tenant > Operational > Endpoints`
2. **Check**: Learned endpoints in each EPG
3. **Note**: MAC addresses and IP assignments

---

## 🧪 Part 10: Testing Communication

### Option 1: Using APIC Built-in Tools
1. **Navigate**: `Tenants > Lab-Tenant > Troubleshooting`
2. **Use Atomic Counters**: Track contract hit counters
3. **Use Contract Usage**: See active contract utilization

### Option 2: Endpoint Testing (if endpoints are connected)
1. **Connect test devices** to configured interfaces
2. **Assign IPs** in the 10.1.1.0/24 range
3. **Test connectivity** between EPGs using ping/HTTP

---

## 📊 Part 11: GUI Navigation Tips and Tricks

### Useful GUI Features

#### Search Functionality
- **Global Search**: Use top search bar for any object
- **Quick Filters**: Use filter boxes in object tables
- **Advanced Search**: Use operators like `name==Web*`

#### View Options
- **List View**: Tabular display with sortable columns
- **Tree View**: Hierarchical object display  
- **Topology View**: Graphical representation

#### Shortcuts and Navigation
- **Breadcrumbs**: Click any level to navigate back
- **Recent Objects**: Access recently viewed configurations
- **Bookmarks**: Save frequently accessed locations
- **Multi-tab**: Open multiple configurations simultaneously

#### Property Panel Tips
- **Pin Panel**: Keep properties panel open while navigating
- **Expand/Collapse**: Use arrows to show/hide sections
- **Help Icons**: Hover over (i) icons for field explanations

### Common GUI Locations Quick Reference
```
📍 Fabric Health: Fabric > Inventory
📍 Interface Status: Fabric > Inventory > Pod-X > Node-X > Interfaces  
📍 Endpoint Learning: Tenants > [Tenant] > Operational > Endpoints
📍 Contract Statistics: Tenants > [Tenant] > Operational > Contract
📍 Policy Troubleshooting: Tenants > [Tenant] > Troubleshooting
📍 System Logs: Admin > Monitoring > Events
```

---

## ✅ Part 12: Verification Checklist

### Configuration Checklist
- [ ] Tenant created successfully
- [ ] VRF configured and deployed
- [ ] Bridge Domain created with subnet
- [ ] Application Profile created
- [ ] Both EPGs created and associated with BD
- [ ] Filter created with appropriate ports
- [ ] Contract created with subject and filter
- [ ] Web-EPG consuming contract
- [ ] DB-EPG providing contract
- [ ] Static ports bound to both EPGs
- [ ] All objects show "deployed" status

### Testing Checklist
- [ ] Policy CAM shows deployed policies
- [ ] Contract statistics show rule creation
- [ ] Endpoints learned in respective EPGs
- [ ] Health scores are green/acceptable
- [ ] No fault conditions present

---

## 🚨 Common Troubleshooting

### If EPGs Cannot Communicate
1. **Check Contract Direction**: Ensure consumer/provider roles are correct
2. **Verify Filter Rules**: Confirm ports and protocols match traffic
3. **Check Static Binding**: Ensure interfaces are properly configured
4. **Review Health Scores**: Look for fault conditions
5. **Verify Policy Deployment**: Check Policy CAM for rule programming

### GUI Navigation Issues
1. **Clear Browser Cache**: Refresh page and clear cache
2. **Check Browser Compatibility**: Use supported browsers
3. **Verify APIC Connectivity**: Ensure stable connection to APIC
4. **User Permissions**: Verify user has appropriate access rights

---

## 🎓 Learning Next Steps

### Expand Your Lab
1. **Add More EPGs**: Create additional application tiers
2. **Create Complex Contracts**: Multiple subjects and filters
3. **Implement Service Graphs**: Add L4-L7 services
4. **Configure VMM Integration**: Connect to hypervisors
5. **Set up External Connectivity**: Configure L3Out

### Advanced Topics to Explore
1. **Microsegmentation**: Create more granular security policies
2. **QoS Policies**: Implement quality of service
3. **Multicast Configuration**: Set up multicast routing
4. **Monitoring and Analytics**: Use fabric insights and analysis

---

This comprehensive guide provides hands-on experience with APIC GUI navigation and EPG-to-EPG communication setup. Practice these steps multiple times to become comfortable with the interface and ACI concepts!
