# ACI Packet Flow: EPG to EPG — Complete Deep Dive
> Underlay · Overlay · Protocol Stack · Packet Formats · Control Plane · Data Plane

---

## Table of Contents

1. [ACI Architecture Primer](#1-aci-architecture-primer)
2. [Key Addressing Concepts](#2-key-addressing-concepts)
3. [Underlay Network — IS-IS](#3-underlay-network--is-is)
4. [Overlay Network — VXLAN](#4-overlay-network--vxlan)
5. [Control Plane Protocols](#5-control-plane-protocols)
   - 5.1 OpFlex (APIC → Leaf)
   - 5.2 LLDP (Fabric Discovery)
   - 5.3 COOP (Spine Oracle)
   - 5.4 MP-BGP EVPN (Spine Route Reflector)
6. [Endpoint Learning](#6-endpoint-learning)
7. [Scenario A — Intra-Leaf, Same EPG/BD](#7-scenario-a--intra-leaf-same-epgbd)
8. [Scenario B — Inter-Leaf, Known Unicast (Same VRF)](#8-scenario-b--inter-leaf-known-unicast-same-vrf)
9. [Scenario C — Inter-Leaf, Unknown Unicast (Spine Proxy)](#9-scenario-c--inter-leaf-unknown-unicast-spine-proxy)
10. [Scenario D — Inter-VRF / Inter-EPG with Contract](#10-scenario-d--inter-vrf--inter-epg-with-contract)
11. [ARP Flows in ACI](#11-arp-flows-in-aci)
12. [Complete Packet Walk — Full Stack](#12-complete-packet-walk--full-stack)
13. [Quick Reference Tables](#13-quick-reference-tables)

---

## 1. ACI Architecture Primer

```
                          ┌──────────────────────────────────┐
                          │           APIC Cluster           │
                          │   (Policy, REST, OpFlex Server)  │
                          └──────────┬───────────────────────┘
                                     │ OpFlex (over fabric)
              ┌──────────────────────┼──────────────────────┐
              │                      │                       │
       ┌──────▼──────┐        ┌──────▼──────┐        ┌──────▼──────┐
       │   Spine 1   │        │   Spine 2   │        │   Spine N   │
       │  (IS-IS/BGP │        │  (IS-IS/BGP │        │  (IS-IS/BGP │
       │  RR + COOP) │        │  RR + COOP) │        │  RR + COOP) │
       └──────┬───┬──┘        └──────┬──────┘        └──────┬──────┘
              │   └──────────────────┤                       │
      ┌───────┘               ┌──────┘                ┌──────┘
      │                       │                       │
┌─────▼──────┐          ┌─────▼──────┐          ┌─────▼──────┐
│   Leaf 1   │          │   Leaf 2   │          │   Leaf N   │
│ (VTEP/TEP) │          │ (VTEP/TEP) │          │ (VTEP/TEP) │
└──────┬─────┘          └──────┬─────┘          └────────────┘
       │                       │
  ┌────┴────┐             ┌────┴────┐
  │  EPG-A  │             │  EPG-B  │
  │ 10.1.1.x│             │ 10.1.2.x│
  └─────────┘             └─────────┘
```

### Component Roles

| Component | Role |
|-----------|------|
| **APIC** | SDN controller; pushes policy via OpFlex; does NOT forward data-plane traffic |
| **Spine** | Pure L3 forwarding; IS-IS underlay; BGP route-reflector; COOP oracle; no EPG attachment |
| **Leaf** | Edge forwarding; endpoint learning; VTEP (VXLAN tunnel endpoint); policy enforcement (contracts) |
| **EPG** | Logical group of endpoints sharing policy; mapped to BD VNID and VRF VNID |
| **BD** | Bridge Domain — L2 domain; one or more subnets; associated to one VRF |
| **VRF** | Virtual Routing and Forwarding — L3 domain; isolation boundary |

---

## 2. Key Addressing Concepts

### TEP — Tunnel Endpoint

Every leaf and spine has a **TEP IP** (Tunnel Endpoint), assigned from the Infra TEP Pool (typically `10.0.0.0/16`). This is the **VXLAN source/destination IP** for all encapsulated traffic.

```
Leaf-1  TEP: 10.0.16.65/32   (loopback, announced via IS-IS)
Leaf-2  TEP: 10.0.16.66/32
Spine-1 TEP: 10.0.16.1/32
Spine-2 TEP: 10.0.16.2/32
```

### VNID — Virtual Network Identifier (24-bit)

ACI uses **two levels of VNIDs** inside VXLAN headers:

| VNID Type | Purpose | Scope |
|-----------|---------|-------|
| **BD VNID** | Identifies the Bridge Domain (L2 segment) | Intra-fabric flooding domain |
| **VRF VNID** | Identifies the VRF / tenant network | Used in spine proxy and inter-VRF routing |

### PTEP — Physical TEP vs. VTEP

- **PTEP**: The physical TEP of the leaf node
- **VTEP**: Can also refer to per-vPC/per-anycast TEP for vPC pairs
- **Anycast TEP**: vPC leaf pairs share a single anycast TEP so traffic can arrive at either switch

### Class ID (sclass/dclass)

Every EPG is assigned a **14-bit class ID (sclass)**. This is carried inside the VXLAN header (inner VLAN or Cisco extension) and used for **contract enforcement** at the destination leaf.

```
EPG-A (Web)   → sclass 0x8003 (32771)
EPG-B (App)   → sclass 0x8004 (32772)
EPG-C (DB)    → sclass 0x8005 (32773)
```

---

## 3. Underlay Network — IS-IS

ACI uses **IS-IS (Intermediate System to Intermediate System)** as its sole underlay IGP. No OSPF. No eBGP for underlay.

### Why IS-IS?

- Protocol-agnostic (works at L2, not reliant on IP for adjacency)
- Fast convergence
- Supports large-scale fabric (Cisco Nexus 9000 series)
- Dedicated to ACI fabric; not customer-visible

### IS-IS Topology in ACI

```
IS-IS Level-2 only (all nodes in one area: 49.0000.0000.0000.00)

Leaf-1 ─────── Spine-1 ─────── Leaf-2
               │
               Spine-2
```

All links are point-to-point IS-IS adjacencies between leaf ↔ spine. No leaf ↔ leaf IS-IS (leaf nodes never connect directly in ACI spine-leaf).

### IS-IS PDU Formats

#### IIH — IS-IS Hello (Adjacency Formation)

```
 0                   1                   2                   3
 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
├────────────────┬───────────────────────────────────────────────┤
│   Intra-Domain │ PDU Type (P2P IIH = 0x11)                     │
│   Routing PDU  │                                               │
├────────────────┴───────────────────────────────────────────────┤
│ Version/Proto ID Ext (0x01)                                    │
├────────────────────────────────────────────────────────────────┤
│ ID Length (6)                                                  │
├────────────────────────────────────────────────────────────────┤
│ R R R PDU Type (00010001)                                      │
├────────────────────────────────────────────────────────────────┤
│ Version (0x01)                                                 │
├────────────────────────────────────────────────────────────────┤
│ Reserved (0x00)                                                │
├────────────────────────────────────────────────────────────────┤
│ Max Area Addresses (0x00 = 3)                                  │
├────────────────────────────────────────────────────────────────┤
│ Circuit Type (L2 = 0x02)                                       │
├────────────────────────────────────────────────────────────────┤
│ Source ID (6 bytes: MAC-derived System ID)                     │
│                                                                │
├────────────────────────────────────────────────────────────────┤
│ Holding Time (30 seconds default in ACI)                       │
├────────────────────────────────────────────────────────────────┤
│ PDU Length                                                     │
├────────────────────────────────────────────────────────────────┤
│ Local Circuit ID (1 byte)                                      │
├────────────────────────────────────────────────────────────────┤
│ TLVs:                                                          │
│  ├─ TLV 132: IP Interface Address (leaf TEP IP)                │
│  ├─ TLV 240: P2P 3-Way Adjacency State                         │
│  └─ TLV 129: Supported Protocols (NLPID 0xCC = IPv4)           │
└────────────────────────────────────────────────────────────────┘
```

#### LSP — Link State PDU (Route Advertisement)

Each leaf advertises its TEP loopback as a host route (`/32`) via IS-IS LSP:

```
IS-IS LSP:
  LSP ID:        0000.0000.0065.00-00   (Leaf-1 system ID)
  Sequence Num:  0x00000001
  Checksum:      0xABCD
  Lifetime:      1200s

  TLVs:
    TLV 1  (Area Address):  49.0000.0000.0000
    TLV 22 (Extended IS Reachability):
            Neighbor: Spine-1 system ID, Metric: 40
            Neighbor: Spine-2 system ID, Metric: 40
    TLV 135 (Extended IP Reachability):
            Prefix: 10.0.16.65/32, Metric: 0   ← leaf TEP loopback
            Prefix: 10.0.0.65/32,  Metric: 0   ← infra VLAN SVI
    TLV 232 (IPv6 Reachability): [if IPv6 fabric]
```

### IS-IS SPF and FIB Population

After IS-IS converges, every leaf has full reachability to every other leaf TEP:

```
Leaf-1 routing table (underlay):
  10.0.16.1/32  via 10.0.0.1 (Spine-1 p2p link)   [IS-IS L2]
  10.0.16.2/32  via 10.0.0.3 (Spine-2 p2p link)   [IS-IS L2]
  10.0.16.66/32 via 10.0.0.1 ECMP 10.0.0.3         [IS-IS L2, ECMP]
```

---

## 4. Overlay Network — VXLAN

ACI uses **VXLAN** (Virtual eXtensible LAN, RFC 7348) as its overlay encapsulation with **Cisco-specific extensions**.

### Standard VXLAN Packet Format

```
Outer Ethernet Frame:
┌──────────────────────────────────────────────────────────────┐
│ Outer Dst MAC  (Next-hop MAC: Spine or Leaf)  [6 bytes]      │
│ Outer Src MAC  (Sending Leaf MAC)             [6 bytes]      │
│ EtherType 0x0800                              [2 bytes]      │
├──────────────────────────────────────────────────────────────┤
│ Outer IPv4 Header                             [20 bytes]     │
│  ├─ IP Protocol: UDP (0x11)                                  │
│  ├─ Src IP: Local Leaf TEP  (e.g., 10.0.16.65)               │
│  └─ Dst IP: Remote Leaf TEP (e.g., 10.0.16.66)               │
├──────────────────────────────────────────────────────────────┤
│ Outer UDP Header                              [8 bytes]      │
│  ├─ Src Port: Entropy Hash (inner flow hash)  [2 bytes]      │
│  └─ Dst Port: 4789 (VXLAN) or 8472 (Cisco)   [2 bytes]       │
├──────────────────────────────────────────────────────────────┤
│ VXLAN Header (Cisco ACI Extension)            [8 bytes]      │
│  0                   1                   2                 3 │
│  0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8   │
│  ├─ Flags: I=1, D=1 (VNI valid, Policy applied)              │
│  ├─ VNID: 24-bit BD VNID or VRF VNID                         │
│  └─ Reserved / sclass (src class ID in Cisco extension)      │
├──────────────────────────────────────────────────────────────┤
│ Inner Ethernet Frame                          [variable]     │
│  ├─ Inner Dst MAC  (endpoint MAC or router MAC)              │
│  ├─ Inner Src MAC  (sending endpoint MAC)                    │
│  └─ Inner EtherType                                          │
├──────────────────────────────────────────────────────────────┤
│ Inner IP Header + Payload                     [variable]     │
└──────────────────────────────────────────────────────────────┘

Total overhead: 6+6+2 + 20 + 8 + 8 = 50 bytes
(MTU on ACI fabric links set to 9150 bytes by default)
```

### Cisco ACI VXLAN Header (Detailed 8 bytes)

```
 Byte 0       Byte 1-3              Byte 4-7
┌────────────┬────────────────────┬────────────────────────────┐
│  Flags     │     Reserved       │  VNID (24-bit)  │ Reserved │
│  IDRSPPO   │                    │                 │  sclass  │
│  10110000  │  00 00 00          │  0x0ABCDE       │  0x8003  │
└────────────┴────────────────────┴────────────────────────────┘

Flag bits:
  I = 1  → VNID field is valid
  D = 1  → Policy (contract) has already been applied
           (set by src leaf; dst leaf skips re-enforcement if set)
  R/S/P/O = reserved/policy-related

sclass (source class): 14-bit EPG identifier carried in the low
        bytes of the VXLAN reserved field (Cisco proprietary).
```

---

## 5. Control Plane Protocols

### 5.1 OpFlex — APIC to Leaf Policy Push

**OpFlex** is an open, declarative policy protocol (RFC draft) used by APIC to push policy (contracts, EPG bindings, VLANs, VNIDs) to leaf nodes.

```
Transport: TCP port 8070 (TLS-encrypted)
Format:    JSON-RPC over TLS

APIC → Leaf message flow:
  1. APIC declares "policy universe" (EPG, BD, VRF, Contract)
  2. Leaf resolves policy objects it needs
  3. Leaf requests specific MOs (Managed Objects) from APIC
  4. APIC resolves and sends back

Example OpFlex message (simplified):
{
  "method": "policy_resolve",
  "params": [{
    "subject": "GbpEpGroup",
    "uri": "/PolicyUniverse/PolicySpace/Tenant1/GbpEpGroup/EPG-A/",
    "data": {
      "flood-domain": "BD-1",
      "network-domain": "VRF-1",
      "class-id": 32771
    }
  }]
}

Leaf programs:
  - Local VLAN → VNID mapping
  - EPG sclass binding
  - Contract (TCAM ACL) entries
  - BD flood list (remote TEPs)
```

### 5.2 LLDP — Fabric Topology Discovery

ACI uses **LLDP** on all fabric links to:
- Discover physical topology (which leaf port connects to which spine)
- Validate cabling against intended topology
- Enable APIC to build IS-IS/BGP configuration

```
LLDP Frame Format:
┌──────────────────────────────────────────────────────┐
│ Dst MAC: 01:80:C2:00:00:0E (LLDP multicast)          │
│ Src MAC: Interface MAC                               │
│ EtherType: 0x88CC                                    │
├──────────────────────────────────────────────────────┤
│ TLV: Chassis ID (MAC)                                │
│ TLV: Port ID (interface name)                        │
│ TLV: TTL (120s default)                              │
│ TLV: System Name ("leaf-1", "spine-1")               │
│ TLV: System Description (NX-OS version)              │
│ TLV: Cisco-proprietary OUI TLVs:                     │
│   └─ Node ID, TEP IP, Fabric ID, Pod ID              │
└──────────────────────────────────────────────────────┘
```

### 5.3 COOP — Council of Oracle Protocol (Spine Proxy)

**COOP** is Cisco-proprietary. All spines collectively maintain a **distributed endpoint database** (oracle). Every leaf reports its locally-learned endpoints to all spines via COOP. This allows spine to act as a proxy for unknown destinations.

```
COOP Transport: TCP port 5000 (ZeroMQ-based)
Direction: Leaf → All Spines

COOP endpoint registration message:
{
  endpoint_ip:   "10.1.1.10",
  endpoint_mac:  "00:50:56:AA:BB:CC",
  epg_sclass:    32771,
  bd_vnid:       0x0ABC01,
  vrf_vnid:      0x0ABC00,
  leaf_tep:      "10.0.16.65",
  flags:         ACTIVE
}

COOP consistency:
  - All spines sync endpoint DB with each other (COOP peer protocol)
  - Spines respond to VXLAN proxy requests from leaves
  - If EP moves: new leaf sends COOP update; old entry evicted
```

### 5.4 MP-BGP EVPN — Spine Route Reflector

ACI spines act as **MP-BGP route reflectors** (RR). Leaves establish iBGP sessions to spines.

```
BGP AS: single AS for entire ACI fabric (e.g., AS 65000)

BGP Address Families used:
  - L2VPN EVPN (AFI 25, SAFI 70)    → MAC/IP routes (Type 2)
  - IPv4 VPN (AFI 1, SAFI 128)      → L3 external routes (for L3Out)
  - IPv6 VPN (AFI 2, SAFI 128)      → IPv6 L3 routes

BGP EVPN Route Type 2 (MAC/IP Advertisement):
  - Used to advertise endpoint MAC + IP
  - Leaf-1 originates; Spine RR reflects to all peers

BGP Update — EVPN Type 2:
  NLRI:
    Route Type: 2
    Length:     varies
    RD:         10.0.16.65:32771   (Leaf-1 TEP : sclass)
    ESI:        00:00:00:00:00:00:00:00:00:00 (single-homed)
    Eth Tag ID: 0
    MAC Length: 48
    MAC:        00:50:56:AA:BB:CC
    IP Length:  32
    IP:         10.1.1.10
    MPLS Label1: BD-VNID (encoded as label)
    MPLS Label2: VRF-VNID (encoded as label)

  Ext Communities:
    RT:         65000:VNID       (import policy)
    Encap:      VXLAN (0x0008)
    MAC Mob:    seq 0

BGP EVPN Route Type 5 (IP Prefix):
  - Used for L3 routes (external prefixes via L3Out)
  - Spine RR reflects prefix + next-hop TEP
```

---

## 6. Endpoint Learning

Endpoint learning happens **in hardware on the leaf** using two mechanisms:

### 6.1 Data-Plane Learning

When a frame arrives on an access port:

```
Step 1: Frame ingresses leaf access port
Step 2: Leaf identifies VLAN → maps to BD VNID + VRF VNID + sclass (via OpFlex policy)
Step 3: Leaf records:
         Local EP Table entry:
           MAC:  00:50:56:AA:BB:CC
           IP:   10.1.1.10  (from ARP/GARP or IP header inspection)
           VLAN: 100 (access VLAN)
           BD:   BD-1 (VNID 0x0ABC01)
           VRF:  VRF-1 (VNID 0x0ABC00)
           Port: Eth1/1
           sclass: 32771 (EPG-A)
Step 4: Leaf sends COOP registration to all spines
Step 5: Leaf sends BGP EVPN Type-2 update (via spine RR)
```

### 6.2 Control-Plane Learning (ARP Gleaning)

For IP-to-MAC binding, the leaf can:
- Glean from ARP Request / ARP Reply packets
- Glean from GARP (Gratuitous ARP)
- Use IP endpoint detection (SVI ARP proxy)

### 6.3 EP Mobility

When an endpoint moves from Leaf-1 to Leaf-2:

```
1. Leaf-2 learns new MAC/IP from data plane
2. Leaf-2 sends COOP update (ACTIVE flag) → Spines update EP DB
3. Leaf-2 sends BGP EVPN Type-2 with higher MAC Mobility sequence
4. Leaf-1 receives BGP update → flushes local stale entry
5. All remote leaves pull updated EVPN route
```

---

## 7. Scenario A — Intra-Leaf, Same EPG/BD

**Topology:**  
`EP-A (10.1.1.10, VLAN 100) → Leaf-1 Eth1/1`  
`EP-B (10.1.1.20, VLAN 100) → Leaf-1 Eth1/2`  
Both in same EPG-A and same BD-1.

```
EP-A ──Eth1/1──► Leaf-1 ──Eth1/2──► EP-B
```

### Step-by-Step Packet Walk

**Step 1: EP-A generates Ethernet frame**

```
[EP-A → EP-B]
Inner Frame (as EP-A sends):
┌─────────────────────────────────────────────┐
│ Dst MAC:  00:50:56:BB:CC:DD  (EP-B MAC)     │
│ Src MAC:  00:50:56:AA:BB:CC  (EP-A MAC)     │
│ VLAN Tag: 100 (dot1q if trunk)              │
│ EtherType: 0x0800 (IPv4)                    │
├─────────────────────────────────────────────┤
│ IP Src: 10.1.1.10                           │
│ IP Dst: 10.1.1.20                           │
│ Protocol: TCP (0x06)                        │
├─────────────────────────────────────────────┤
│ TCP Src Port: 54321                         │
│ TCP Dst Port: 80                            │
│ Payload: HTTP data...                       │
└─────────────────────────────────────────────┘
```

**Step 2: Frame arrives on Leaf-1 Eth1/1**

```
Leaf-1 hardware pipeline (ASIC — Nexus 9000 Tahoe/Trident):

  a) Port ingress processing:
     - Strip 802.1q VLAN tag (VLAN 100)
     - Identify BD: VLAN 100 → BD-1 (VNID 0x0ABC01)
     - Identify VRF: BD-1 → VRF-1 (VNID 0x0ABC00)
     - Assign sclass: VLAN 100 + port Eth1/1 → EPG-A → sclass 32771

  b) Source endpoint learning:
     - Src MAC 00:50:56:AA:BB:CC not in local EP table → LEARN
     - Record: MAC → Port Eth1/1, BD BD-1, sclass 32771
     - Async: notify COOP, BGP EVPN

  c) Destination lookup:
     - Dst MAC 00:50:56:BB:CC:DD → lookup local EP table
     - FOUND: Port Eth1/2, BD BD-1
     - Both ports in same BD → L2 local switching

  d) Contract enforcement:
     - Src sclass: 32771 (EPG-A), Dst sclass: 32771 (EPG-A)
     - Intra-EPG: contract check → permit (intra-EPG allow by default
       unless "intra-EPG isolation" policy enabled)

  e) Egress:
     - Tag with VLAN 100 (if EP-B port is trunk), or strip (access)
     - Forward out Eth1/2
```

**Step 3: Frame egresses to EP-B — No VXLAN encapsulation needed.**

> For same-leaf L2 switching, there is **zero VXLAN overhead**. The frame is switched in hardware at line rate.

---

## 8. Scenario B — Inter-Leaf, Known Unicast (Same VRF)

**Topology:**  
`EP-A (10.1.1.10) → Leaf-1` — EPG-A, BD-1  
`EP-B (10.1.2.10) → Leaf-2` — EPG-B, BD-2  
Both in **VRF-1**. A **contract permits** traffic between EPG-A and EPG-B.

EP-B is already known to Leaf-1 (received via BGP EVPN from Spine RR).

```
EP-A → Leaf-1 ═══[VXLAN/IS-IS underlay]══► Leaf-2 → EP-B
                       (via Spine)
```

### Step-by-Step Packet Walk

**Step 1: EP-A sends frame**

EP-A is in subnet 10.1.1.0/24. EP-B is in subnet 10.1.2.0/24 (different BD, different subnet). EP-A **cannot send directly** to EP-B's MAC — it must ARP for the gateway.

In ACI, the **pervasive gateway (Anycast GW)** is distributed on every leaf that has BD-1 configured:

```
ACI Distributed Gateway:
  BD-1 subnet: 10.1.1.