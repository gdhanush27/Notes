# Networks
- manage people and devices

--- 

## contains :
- broadcast domain
- Collision domain

---

## Devices :
- Hub - does not break both domain
- Switch - breaks only collision domain
- Router - breaks both domain
- If there are n devices connected on a

| devices | Broadcast domain | Collision Domain |
|--------|--------|--------|
| Hub | 1 | 1 |
| Switch | 1 | n |
| Router | n | n |
---

## OSI Layers
- Application Layer
    - User Interface
    - Gift Card
- Presentation Layer
    - Wrapping in cover
    - It can travel in a medium - Encryption / formatting / standard
    - Travel to destination
- Session Layer
    - Communicate with other party
    - Receive back
    - Sessions seperate
    - Half Duplex
- Transport Layer
    - Segment / Protocol (tcp/udp) port (21,22,80,443) 
    - TCP - Connection Oriented, Phone call, ACK 3 way handshake
    - UDP - Connection Oriented, Delivery Encapsulation, Decapsulation
- Network Layer
    - Packet / IP address / delivering packet to street ( common ) Encapsulation / Decapsulation
    - Router
- Datalink layer
    - Frames / mac addr / delivering to the right address 
    - Switchs
- Physical Layer
    - Bits 
    - Phycical layer 
    - 1s and 0s
    - hubs
---

## Subnets

- SubNetworks
- Dividing an IP into multiple segments
- Improve efficiency in 
    - IP management
    - Improved security
    - Better Performance ( Reducing congession by limiting broadcast domain )
    - Easier troubleshooting

### Formule in subnets

#### 🔹 **1. Number of Subnets**

**🧾 Formula:**  
Number of Subnets = 2^(n - original prefix)

**📌 Explanation:**
- `n` = new CIDR (e.g., /26)  
- `original prefix` = starting network CIDR (e.g., /24)  
- You are **borrowing** bits from the host portion to create subnets.

**✅ Example:**  
From /24 to /26 → Borrowed bits = 26 - 24 = 2 → Subnets = 2^2 = 4


#### 🔹 **2. Usable Hosts per Subnet**

**🧾 Formula:**  
Usable Hosts = 2^(32 - n) - 2

**📌 Explanation:**
- `n` = CIDR  
- `32 - n` = number of host bits

**✅ Example:**  
For /26: 32 - 26 = 6 → 2^6 - 2 = 64 - 2 = 62 hosts


#### 🔹 **3. Total IPs per Subnet (including network + broadcast)**

**🧾 Formula:**  
Total IPs = 2^(32 - n)

**✅ Example:**  
For /27: 2^(32 - 27) = 2^5 = 32 total IPs


#### 🔹 **4. Subnet Increment (Block Size)**

**🧾 Formula:**  
Increment = 256 - value in subnet mask where subnetting happens

**✅ Example:**  
/26 = 255.255.255.192 → subnetting happens in 4th octet → 256 - 192 = 64


#### 🔹 **5. CIDR → Subnet Mask**

**🧾 Steps:**
- Write `n` ones followed by `32 - n` zeros in binary
- Break into 4 octets, convert to decimal

**✅ Example:**  
/26 → Binary: 11111111.11111111.11111111.11000000  
→ Mask: 255.255.255.192


#### 🔹 **6. Subnet Mask → CIDR**

**🧾 Steps:**
- Convert mask to binary  
- Count the number of 1s = `n`

**✅ Example:**  
255.255.255.224 → 27 ones → /27


#### 🔹 **7. Wildcard Mask**

**🧾 Formula:**  
Wildcard Mask = 255.255.255.255 - Subnet Mask

**✅ Example:**  
255.255.255.0 → 0.0.0.255


#### 🔹 **8. Network Address**

**🧾 Formula:**  
Network Address = IP Address AND Subnet Mask

**✅ Example:**  
192.168.1.130 AND 255.255.255.192 → Network: 192.168.1.128


#### 🔹 **9. Broadcast Address**

**🧾 Formula:**  
Broadcast = Network Address + 2^(32 - n) - 1

**✅ Example:**  
Network: 192.168.1.128, /26 → 2^6 = 64 IPs  
→ Broadcast = 192.168.1.128 + 63 = 192.168.1.191


#### 🔹 **10. Host Range**

**🧾 Formula:**  
First Host = Network Address + 1  
Last Host = Broadcast Address - 1

**✅ Example:**  
Network: 192.168.1.128  
Broadcast: 192.168.1.191  
→ Host range: 192.168.1.129 – 192.168.1.190


#### 📌 Final Summary Table (All in terms of `/n`)

| What You Want     | Formula / Logic                            |
| ----------------- | ------------------------------------------ |
| Subnets           | 2^(n - original CIDR)                      |
| Usable Hosts      | 2^(32 - n) - 2                             |
| Total IPs         | 2^(32 - n)                                 |
| Subnet Increment  | 256 - subnet mask octet                   |
| Wildcard Mask     | 255.255.255.255 - subnet mask              |
| Broadcast Address | Network + 2^(32 - n) - 1                   |
| First/Last Host   | Network + 1, Broadcast - 1                 |

---

## VLANs

- Logical grouping of physical devical
- Single physical network into multiple logical networks

### Limitations of LAN

- Too much broadcast traffic
- Security issues
- Lack of segmanetation

### Advantags of VLAN

- Each VLAN can be isolated
- Reducing broadcast traffic
- Better Management ( Organise by VLAN )
- No need for Multiple switchs to seperate network

---

## STP ( Spanning Tree Protocol )

- Layer 2 protocol 
- Prevent loops in network 

### Building STP

Consider the below connection for STP:

```markdown
  SW1 ─ SW2 ─ SW3 ─ SW4 ─ SW5
   \_______________________/
```

#### Find the Root Bridge

- Each switch has a priority and a MAC address
- Select the lowest priority 
- If some has the same priority, choose the switch with lowest MAC as Root Bridge

| Switch | Priority | MAC Address       | Bridge ID (Priority.MAC) |
| ------ | -------- | ----------------- | ------------------------ |
| SW1    | 32768    | 00:11:22:33:44:01 | 32768.00:11:22:33:44:01  |
| SW2    | 32768    | 00:11:22:33:44:02 | 32768.00:11:22:33:44:02  |
| SW3    | 32768    | 00:11:22:33:44:03 | 32768.00:11:22:33:44:03  |
| SW4    | 32768    | 00:11:22:33:44:04 | 32768.00:11:22:33:44:04  |
| SW5    | 32768    | 00:11:22:33:44:05 | 32768.00:11:22:33:44:05  |


#### Select the Root Port for Other Switchs

- Find the best path to Root Bridge
- assume all link are 1 Gbps = 4 cost

| Switch | Path to Root    | Total Cost | Root Port |
| ------ | --------------- | ---------- | --------- |
| SW2    | SW2 → SW1       | 4          | SW2 → SW1 |
| SW5    | SW5 → SW1       | 4          | SW5 → SW1 |
| SW3    | SW3 → SW2 → SW1 | 8          | SW3 → SW2 |
| SW4    | SW4 → SW5 → SW1 | 8          | SW4 → SW5 |


#### Designate Port to each Link

- Root as DP ( eg, in two links SW1–SW2 and SW1–SW5 )
- SW3–SW4	SW3 vs SW4? Tie → use MAC
    - Both have equal cost (8)
    - Compare MACs
    - SW3 has lower MAC → becomes DP

| Link    | DP Decision               |
| ------- | ------------------------- |
| SW1–SW2 | SW1 is Root → DP          |
| SW1–SW5 | SW1 is Root → DP          |
| SW2–SW3 | SW2 has lower cost → DP   |
| SW3–SW4 | SW3 vs SW4? Tie → use MAC |
| SW4–SW5 | SW5 has lower cost → DP   |


#### Identify Blocked Ports

- Any port that is not a Root Port (RP) or Designated Port (DP) must be Blocked.

#### Final Summary

| Link    | SW1 Port | SW2 Port | STP Status     |
| ------- | -------- | -------- | -------------- |
| SW1–SW2 | DP       | RP       | Active         |
| SW1–SW5 | DP       | RP       | Active         |
| SW2–SW3 | DP       | RP       | Active         |
| SW3–SW4 | DP       | Blocked  | Loop prevented |
| SW4–SW5 | RP       | DP       | Active         |

---


Client server
Application port
