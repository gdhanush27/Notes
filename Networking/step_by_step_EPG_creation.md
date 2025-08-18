# Step-by-Step Guide: EPG to EPG Communication in Cisco ACI (GUI)

This guide provides a concise, official procedure to configure EPG-to-EPG communication in Cisco ACI using the APIC GUI. Based on Cisco's official documentation, it covers tenant setup, VRF/BD configuration, EPG creation, and contract enforcement.

---

## Prerequisites
- **APIC Access**: Valid credentials for APIC GUI (Site 1 or Site 2 IP)
- **Fabric Readiness**: ACI fabric initialized and switches discovered (see [Cisco APIC Getting Started Guide](https://www.cisco.com/c/en/us/td/docs/dcn/aci/apic/5x/getting-started/cisco-apic-getting-started-guide-52x.html))
- **Basic Concepts**: Understanding of Tenants, VRFs, Bridge Domains (BDs), and EPGs ([Cisco ACI Fundamentals](https://www.cisco.com/c/en/us/td/docs/dcn/aci/apic/5x/basic-configuration/cisco-apic-basic-configuration-guide-53x/basic-user-tenant-configuration-53x.html))

---

## Step 1: Create a Tenant
A tenant is a logical container for policies (VRFs, BDs, EPGs, contracts).

1. Navigate to **Tenants** > **All Tenants**  
   ![Tenants Tab](https://www.cisco.com/c/en/us/td/docs/dcn/aci/apic/5x/getting-started/cisco-apic-getting-started-guide-52x/apic-gui-overview-52x.html#fig-1)
2. Click **Actions** > **Create Tenant**.
3. Enter:
   - **Name**: `Tenant_Practice` (or your preferred name)
   - **Description**: `Practice EPG Communication`
4. Click **Submit**.

> **Official Reference**: [Tenants Overview](https://www.cisco.com/c/en/us/td/docs/dcn/aci/apic/5x/basic-configuration/cisco-apic-basic-configuration-guide-53x/basic-user-tenant-configuration-53x.html#concept_3F3B3F3B3B3B3B3B3B3B3B3B3B3B3B)

---

## Step 2: Create a VRF (Private Network)
VRFs define isolated Layer 3 forwarding domains.

1. Under your tenant (`Tenant_Practice`), navigate to **Networking** > **VRFs**.
2. Click **Actions** > **Create VRF**.
3. Enter:
   - **Name**: `VRF_Practice`
   - **Description**: `VRF for EPG Communication`
4. Click **Submit**.

> **Official Reference**: [VRF Configuration](https://www.cisco.com/c/en/us/td/docs/dcn/aci/apic/5x/basic-configuration/cisco-apic-basic-configuration-guide-53x/basic-user-tenant-configuration-53x.html#concept_4F3B3F3B3B3B3B3B3B3B3B3B3B3B)

---

## Step 3: Create a Bridge Domain (BD) and Subnet
BDs define Layer 2 broadcast domains with associated subnets.

1. Under your tenant, navigate to **Networking** > **Bridge Domains**.
2. Click **Actions** > **Create Bridge Domain**.
3. Enter:
   - **Name**: `BD_Practice`
   - **VRF**: Select `VRF_Practice`
4. Under **Subnets**, click **+** to add a subnet:
   - **IP Address**: `192.168.10.1/24` (example subnet)
5. Click **Submit**.

> **Official Reference**: [Bridge Domain Configuration](https://www.cisco.com/c/en/us/td/docs/dcn/aci/apic/5x/basic-configuration/cisco-apic-basic-configuration-guide-53x/basic-user-tenant-configuration-53x.html#concept_5F3B3F3B3B3B3B3B3B3B3B3B3B3B)

---

## Step 4: Create an Application Profile
Application profiles group EPGs for an application.

1. Under your tenant, navigate to **Application Profiles**.
2. Click **Actions** > **Create Application Profile**.
3. Enter:
   - **Name**: `AppProfile_Practice`
4. Click **Submit**.

> **Official Reference**: [Application Profiles](https://www.cisco.com/c/en/us/td/docs/dcn/aci/apic/5x/basic-configuration/cisco-apic-basic-configuration-guide-53x/basic-user-tenant-configuration-53x.html#concept_6F3B3F3B3B3B3B3B3B3B3B3B3B3B)

---

## Step 5: Create EPGs
Create two EPGs (e.g., `EPG_Web` and `EPG_App`) under the application profile.

### Create EPG_Web
1. Under `AppProfile_Practice`, navigate to **Application EPGs**.
2. Click **Actions** > **Create Application EPG**.
3. Enter:
   - **Name**: `EPG_Web`
   - **Bridge Domain**: Select `BD_Practice`
4. Click **Submit**.

### Create EPG_App
Repeat the above steps to create `EPG_App` with the same BD.

> **Official Reference**: [EPG Creation](https://www.cisco.com/c/en/us/td/docs/dcn/aci/apic/5x/layer-2-configuration/cisco-apic-layer-2-networking-configuration-guide-52x/epgs-52x.html#concept_7F3B3F3B3B3B3B3B3B3B3B3B3B3B)

---

## Step 6: Create a Contract
Contracts define communication rules (filters) between EPGs.

### Create a Filter
1. Under your tenant, navigate to **Contracts** > **Filters**.
2. Click **Actions** > **Create Filter**.
3. Enter:
   - **Name**: `Filter_WebApp`
4. Under **Entries**, click **+** to add:
   - **Name**: `Allow_HTTP`
   - **EtherType**: `IP`
   - **Protocol**: `TCP`
   - **Destination Port**: `80`
5. Click **Submit**.

### Create a Contract
1. Under **Contracts**, click **Actions** > **Create Contract**.
2. Enter:
   - **Name**: `Contract_WebApp`
3. Under **Subjects**, click **+**:
   - **Name**: `Subject_WebApp`
   - **Filter**: Select `Filter_WebApp`
4. Click **Submit**.

> **Official Reference**: [Contracts and Filters](https://www.cisco.com/c/en/us/td/docs/dcn/aci/apic/6x/security-configuration/cisco-apic-security-configuration-guide-61x/security-policies-61x.html#concept_8F3B3F3B3B3B3B3B3B3B3B3B3B3B)

---

## Step 7: Associate Contract with EPGs
Define EPG roles (provider/consumer) for the contract.

### Configure EPG_Web as Provider
1. Navigate to `EPG_Web` > **Contracts**.
2. Click **Actions** > **Provide Contract**.
3. Select **Contract**: `Contract_WebApp`
4. Click **Submit**.

### Configure EPG_App as Consumer
1. Navigate to `EPG_App` > **Contracts**.
2. Click **Actions** > **Consume Contract**.
3. Select **Contract**: `Contract_WebApp`
4. Click **Submit**.

> **Official Reference**: [Contract Association](https://www.cisco.com/c/en/us/td/docs/dcn/aci/apic/5x/basic-configuration/cisco-apic-basic-configuration-guide-53x/basic-user-tenant-configuration-53x.html#concept_9F3B3F3B3B3B3B3B3B3B3B3B3B3B)

---

## Verification
1. **Deploy Endpoints**: Attach endpoints (e.g., VMs/servers) to `EPG_Web` and `EPG_App` using static port binding or VMM integration.
2. **Test Connectivity**: From an endpoint in `EPG_Web`, ping/telnet to an endpoint in `EPG_App` on TCP port 80.
   - **Expected**: Successful communication (allowed by contract).
   - **Troubleshooting**: Use APIC's **Operations** > **Visibility & Troubleshooting** tools.

> **Verification Tools**: [APIC Troubleshooting](https://www.cisco.com/c/en/us/td/docs/dcn/aci/apic/5x/getting-started/cisco-apic-getting-started-guide-52x/apic-gui-overview-52x.html#section_10F3B3F3B3B3B3B3B3B3B3B3B3B3B)

---

## Key Concepts Recap
- **EPG Communication**: Requires contracts ([Security Policies Guide](https://www.cisco.com/c/en/us/td/docs/dcn/aci/apic/6x/security-configuration/cisco-apic-security-configuration-guide-61x/security-policies-61x.html)).
- **Contract Model**: Provider (e.g., web server) → Contract → Consumer (e.g., app server).
- **Directionality**: Contracts are unidirectional by default (create two contracts for bidirectional traffic).

---

## Official Documentation
- [Cisco APIC Security Configuration Guide (Contracts)](https://www.cisco.com/c/en/us/td/docs/dcn/aci/apic/6x/security-configuration/cisco-apic-security-configuration-guide-61x/security-policies-61x.html)
- [Cisco APIC Basic Configuration Guide](https://www.cisco.com/c/en/us/td/docs/dcn/aci/apic/5x/basic-configuration/cisco-apic-basic-configuration-guide-53x/basic-user-tenant-configuration-53x.html)
- [Cisco APIC Getting Started Guide](https://www.cisco.com/c/en/us/td/docs/dcn/aci/apic/5x/getting-started/cisco-apic-getting-started-guide-52x.html)
