# Complete ACI Configuration Guide with Sample Configs

## Prerequisites and Lab Setup

**Sample Lab Environment:**
- APIC IP: 10.1.1.100
- Leaf-101: Interfaces eth1/1, eth1/2 for Ixia connections
- Leaf-102: Interface eth1/3 for additional connectivity
- VLAN Pool: 100-199
- Physical Domain: "PhysDom_Lab"

## Part 1: Infrastructure Setup

### Step 1: Create VLAN Pool
1. Navigate to **Fabric** → **Access Policies** → **Pools** → **VLAN**
2. Right-click and select **Create VLAN Pool**
3. Configuration:
   ```
   Name: VLAN_Pool_Lab
   Allocation Mode: Static Allocation
   - From: vlan-100
   - To: vlan-199
   - Allocation Mode: Static Allocation
   ```
4. Click **Submit**

### Step 2: Create Physical Domain
1. Navigate to **Fabric** → **Access Policies** → **Physical and External Domains** → **Physical Domains**
2. Right-click and select **Create Physical Domain**
3. Configuration:
   ```
   Name: PhysDom_Lab
   VLAN Pool: VLAN_Pool_Lab
   ```
4. Click **Submit**

### Step 3: Create Interface Policy Group
1. Navigate to **Fabric** → **Access Policies** → **Interfaces** → **Leaf Interfaces** → **Policy Groups** → **Leaf Access Port**
2. Right-click and select **Create Leaf Access Port Policy Group**
3. Configuration:
   ```
   Name: IntPolGrp_Lab
   Link Level Policy: default (or create custom)
   CDP Policy: default
   LLDP Policy: default
   Attached Entity Profile: Create new AEP (see next step)
   ```

### Step 4: Create Attachable Entity Profile (AEP)
1. Navigate to **Fabric** → **Access Policies** → **Global Policies** → **Attachable Entity Profiles**
2. Right-click and select **Create Attachable Entity Profile**
3. Configuration:
   ```
   Name: AEP_Lab
   Domains:
   - Domain Type: Physical Domain
   - Domain: PhysDom_Lab
   ```
4. Go back and update Interface Policy Group with this AEP

### Step 5: Create Interface Profiles and Selectors
1. Navigate to **Fabric** → **Access Policies** → **Interfaces** → **Leaf Interfaces** → **Profiles**
2. Right-click and select **Create Leaf Interface Profile**
3. Configuration:
   ```
   Name: IntProf_Leaf101
   ```

4. Expand the profile and right-click **Access Port Selectors** → **Create Access Port Selector**
5. Configuration for Ixia Port 1:
   ```
   Name: Ixia_Port1
   Interface IDs: 1/1
   Interface Policy Group: IntPolGrp_Lab
   ```

6. Create another selector for Ixia Port 2:
   ```
   Name: Ixia_Port2  
   Interface IDs: 1/2
   Interface Policy Group: IntPolGrp_Lab
   ```

### Step 6: Create Switch Profile
1. Navigate to **Fabric** → **Access Policies** → **Switches** → **Leaf Switches** → **Profiles**
2. Right-click and select **Create Leaf Profile**
3. Configuration:
   ```
   Name: SwitchProf_Leaf101
   Leaf Selectors:
   - Name: Leaf101_Selector
   - Blocks: 101-101 (Node ID range)
   Associated Interface Selector Profiles: IntProf_Leaf101
   ```

## Part 2: Tenant and Networking Configuration

### Step 7: Create Tenant
1. Navigate to **Tenants**
2. Right-click and select **Create Tenant**
3. Configuration:
   ```
   Name: LAB_TENANT
   Description: Lab tenant for EPG testing
   ```

### Step 8: Create VRF
1. Expand **LAB_TENANT** → **Networking** → **VRFs**
2. Right-click and select **Create VRF**
3. Configuration:
   ```
   Name: LAB_VRF
   Policy Control Enforcement: Enforced
   Policy Control Direction: Ingress
   ```

### Step 9: Create Bridge Domain
1. Under **LAB_TENANT** → **Networking** → **Bridge Domains**
2. Right-click and select **Create Bridge Domain**
3. Configuration:
   ```
   Name: LAB_BD
   VRF: LAB_VRF
   
   Subnets:
   - Gateway IP: 192.168.100.1/24
   - Scope: Public, Shared
   - Preferred: Yes
   
   L2 Configuration:
   - L2 Unknown Unicast: Hardware Proxy
   - ARP Flooding: Enabled
   - Unicast Routing: Enabled
   - Limit IP Learning to Subnet: Enabled
   ```

### Step 10: Create Application Profile
1. Under **LAB_TENANT** → **Application Profiles**
2. Right-click and select **Create Application Profile**
3. Configuration:
   ```
   Name: LAB_APP
   Description: Application profile for web and database tiers
   ```

## Part 3: EPG Configuration

### Step 11: Create First EPG (Web Tier)
1. Expand **LAB_APP** → **Application EPGs**
2. Right-click and select **Create Application EPG**
3. Configuration:
   ```
   Name: WEB_EPG
   Bridge Domain: LAB_BD
   
   Domains:
   - Domain Type: Physical Domain
   - Domain: PhysDom_Lab
   - Deploy Immediacy: Immediate
   - Resolution Immediacy: Immediate
   - VLAN: 150 (Static)
   ```

### Step 12: Create Second EPG (Database Tier)
1. Right-click **Application EPGs** and select **Create Application EPG**
2. Configuration:
   ```
   Name: DB_EPG
   Bridge Domain: LAB_BD
   
   Domains:
   - Domain Type: Physical Domain  
   - Domain: PhysDom_Lab
   - Deploy Immediacy: Immediate
   - Resolution Immediacy: Immediate
   - VLAN: 160 (Static)
   ```

## Part 4: Security Policy Configuration

### Step 13: Create Filters
1. Under **LAB_TENANT** → **Security Policies** → **Filters**
2. Create HTTP Filter:
   ```
   Name: HTTP_FILTER
   
   Entries:
   - Name: HTTP_ENTRY
   - EtherType: IP
   - IP Protocol: TCP  
   - Destination Port: 80 to 80
   - Source Port: unspecified
   - Stateful: Yes
   ```

3. Create HTTPS Filter:
   ```
   Name: HTTPS_FILTER
   
   Entries:
   - Name: HTTPS_ENTRY
   - EtherType: IP
   - IP Protocol: TCP
   - Destination Port: 443 to 443
   - Source Port: unspecified
   - Stateful: Yes
   ```

4. Create MySQL Filter:
   ```
   Name: MYSQL_FILTER
   
   Entries:
   - Name: MYSQL_ENTRY
   - EtherType: IP
   - IP Protocol: TCP
   - Destination Port: 3306 to 3306
   - Source Port: unspecified
   - Stateful: Yes
   ```

5. Create ICMP Filter:
   ```
   Name: ICMP_FILTER
   
   Entries:
   - Name: ICMP_ENTRY
   - EtherType: IP
   - IP Protocol: ICMP
   - ICMP Type: unspecified
   ```

### Step 14: Create Contracts
1. Under **LAB_TENANT** → **Security Policies** → **Contracts**
2. Create Web-to-DB Contract:
   ```
   Name: WEB_TO_DB_CONTRACT
   Scope: Tenant
   
   Subjects:
   - Name: WEB_TO_DB_SUBJECT
   - Filters: MYSQL_FILTER, ICMP_FILTER
   - Service Graph: None
   - QoS Class: Unspecified
   ```

3. Create External-to-Web Contract:
   ```
   Name: EXT_TO_WEB_CONTRACT
   Scope: Tenant
   
   Subjects:
   - Name: EXT_TO_WEB_SUBJECT
   - Filters: HTTP_FILTER, HTTPS_FILTER, ICMP_FILTER
   ```

### Step 15: Apply Contracts to EPGs
1. Configure WEB_EPG:
   ```
   WEB_EPG Contracts:
   - Provided Contracts: EXT_TO_WEB_CONTRACT
   - Consumed Contracts: WEB_TO_DB_CONTRACT
   ```
   
   **Implementation:**
   - Navigate to **WEB_EPG** → **Contracts**
   - Right-click **Provided Contracts** → **Add Contract**
   - Select **EXT_TO_WEB_CONTRACT**
   - Right-click **Consumed Contracts** → **Add Contract** 
   - Select **WEB_TO_DB_CONTRACT**

2. Configure DB_EPG:
   ```
   DB_EPG Contracts:
   - Provided Contracts: WEB_TO_DB_CONTRACT
   - Consumed Contracts: None
   ```

   **Implementation:**
   - Navigate to **DB_EPG** → **Contracts**
   - Right-click **Provided Contracts** → **Add Contract**
   - Select **WEB_TO_DB_CONTRACT**

## Part 5: Ixia Configuration and Traffic Generation

### Step 16: Ixia Physical Setup
1. **Physical Connections:**
   ```
   Ixia Port 1/1 → Leaf-101 eth1/1 (WEB_EPG - VLAN 150)
   Ixia Port 1/2 → Leaf-101 eth1/2 (DB_EPG - VLAN 160)
   ```

2. **Verify Physical Connectivity:**
   - Check in APIC: **Fabric** → **Inventory** → **Pod-1** → **Leaf-101** → **Interfaces**
   - Confirm eth1/1 and eth1/2 are "up"

### Step 17: IxNetwork Configuration
1. **Open IxNetwork and Create New Configuration**
2. **Add Chassis and Ports:**
   ```
   Chassis IP: [Your Ixia Chassis IP]
   Ports: 1/1, 1/2
   ```

### Step 18: Configure Traffic Endpoints
1. **Configure Port 1/1 (Web Server Simulation):**
   ```
   Port: 1/1
   Protocol Stack: Ethernet/VLAN/IPv4
   
   Ethernet Configuration:
   - MAC Address: 00:11:22:33:44:01
   - Auto MAC: Disabled
   
   VLAN Configuration:  
   - VLAN ID: 150
   - Priority: 0
   
   IPv4 Configuration:
   - Address: 192.168.100.10
   - Gateway: 192.168.100.1
   - Prefix: 24
   ```

2. **Configure Port 1/2 (Database Server Simulation):**
   ```
   Port: 1/2
   Protocol Stack: Ethernet/VLAN/IPv4
   
   Ethernet Configuration:
   - MAC Address: 00:11:22:33:44:02  
   - Auto MAC: Disabled
   
   VLAN Configuration:
   - VLAN ID: 160
   - Priority: 0
   
   IPv4 Configuration:
   - Address: 192.168.100.20
   - Gateway: 192.168.100.1
   - Prefix: 24
   ```

### Step 19: Create Traffic Items
1. **HTTP Traffic (External to Web):**
   ```
   Name: External_to_Web_HTTP
   Traffic Type: IPv4
   
   Source/Destination:
   - Bidirectional: No
   - Source Endpoints: Port 1/1 (192.168.100.10)
   - Destination Endpoints: Port 1/1 (192.168.100.10) [Loopback test]
   
   Frame:
   - Frame Size Type: Fixed
   - Frame Size: 1024 bytes
   
   Rate:
   - Rate Type: Packets Per Second
   - Rate: 1000 pps
   
   Protocol Configuration:
   - Ethernet: Default
   - VLAN: ID 150
   - IPv4: Source 192.168.100.10, Dest 192.168.100.10
   - TCP: Source Port 12345, Dest Port 80
   ```

2. **MySQL Traffic (Web to Database):**
   ```
   Name: Web_to_DB_MySQL  
   Traffic Type: IPv4
   
   Source/Destination:
   - Bidirectional: No
   - Source Endpoints: Port 1/1 (192.168.100.10)
   - Destination Endpoints: Port 1/2 (192.168.100.20)
   
   Frame:
   - Frame Size Type: Fixed
   - Frame Size: 512 bytes
   
   Rate:
   - Rate Type: Packets Per Second
   - Rate: 500 pps
   
   Protocol Configuration:
   - Ethernet: Default
   - VLAN: Source 150, Dest 160
   - IPv4: Source 192.168.100.10, Dest 192.168.100.20
   - TCP: Source Port 45678, Dest Port 3306
   ```

3. **ICMP Traffic (Connectivity Test):**
   ```
   Name: ICMP_Connectivity
   Traffic Type: IPv4
   
   Source/Destination:
   - Bidirectional: Yes
   - Source Endpoints: Port 1/1 (192.168.100.10)
   - Destination Endpoints: Port 1/2 (192.168.100.20)
   
   Frame:
   - Frame Size Type: Fixed  
   - Frame Size: 64 bytes
   
   Rate:
   - Rate Type: Packets Per Second
   - Rate: 10 pps
   
   Protocol Configuration:
   - Ethernet: Default
   - VLAN: Bidirectional 150<->160
   - IPv4: Source 192.168.100.10, Dest 192.168.100.20
   - ICMP: Echo Request/Reply
   ```

### Step 20: Start Traffic and Validate
1. **Start All Traffic Items**
2. **Monitor Real-time Statistics**
3. **Expected Results:**
   ```
   External_to_Web_HTTP: Should pass (contract allows HTTP)
   Web_to_DB_MySQL: Should pass (contract allows MySQL) 
   ICMP_Connectivity: Should pass (contract allows ICMP)
   ```

## Troubleshooting Common Issues

### Issue 1: Endpoints Not Learning
**Symptoms:** No endpoints visible in EPG operational tab
**Solution:**
1. Verify physical connectivity
2. Check VLAN configuration matches EPG domain
3. Ensure AEP is correctly associated
4. Verify switch and interface profiles

### Issue 2: Traffic Not Passing
**Symptoms:** TX packets > 0, RX packets = 0
**Solution:**
1. Verify contract configuration (provider/consumer)
2. Check filter entries match traffic characteristics  
3. Ensure EPG domain associations are correct
4. Verify VLAN encapsulation

### Issue 3: Contract Not Hit
**Symptoms:** Traffic passes but no contract statistics
**Solution:**
1. Verify contract scope (Tenant/VRF/Global)
2. Check subject and filter associations
3. Ensure EPG contract relationships are correct
4. Verify policy enforcement direction
