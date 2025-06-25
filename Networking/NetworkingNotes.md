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

1. **Number of Subnets**

    **🧾 Formula:**  
    Number of Subnets = 2^(n - original prefix)

    **📌 Explanation:**
    - `n` = new CIDR (e.g., /26)  
    - `original prefix` = starting network CIDR (e.g., /24)  
    - You are **borrowing** bits from the host portion to create subnets.

    **✅ Example:**  
    From /24 to /26 → Borrowed bits = 26 - 24 = 2 → Subnets = 2^2 = 4


2. **Usable Hosts per Subnet**

    **🧾 Formula:**  
    Usable Hosts = 2^(32 - n) - 2

    **📌 Explanation:**
    - `n` = CIDR  
    - `32 - n` = number of host bits

    **✅ Example:**  
    For /26: 32 - 26 = 6 → 2^6 - 2 = 64 - 2 = 62 hosts


3. **Total IPs per Subnet (including network + broadcast)**

    **🧾 Formula:**  
    Total IPs = 2^(32 - n)

    **✅ Example:**  
    For /27: 2^(32 - 27) = 2^5 = 32 total IPs


4. **Subnet Increment (Block Size)**

    **🧾 Formula:**  
    Increment = 256 - value in subnet mask where subnetting happens

    **✅ Example:**  
    /26 = 255.255.255.192 → subnetting happens in 4th octet → 256 - 192 = 64


5. **CIDR → Subnet Mask**

    **🧾 Steps:**
    - Write `n` ones followed by `32 - n` zeros in binary
    - Break into 4 octets, convert to decimal

    **✅ Example:**  
    /26 → Binary: 11111111.11111111.11111111.11000000  
    → Mask: 255.255.255.192


6. **Subnet Mask → CIDR**

    **🧾 Steps:**
    - Convert mask to binary  
    - Count the number of 1s = `n`

    **✅ Example:**  
    255.255.255.224 → 27 ones → /27


7. **Wildcard Mask**

    **🧾 Formula:**  
    Wildcard Mask = 255.255.255.255 - Subnet Mask

    **✅ Example:**  
    255.255.255.0 → 0.0.0.255


8. **Network Address**

    **🧾 Formula:**  
    Network Address = IP Address AND Subnet Mask

    **✅ Example:**  
    192.168.1.130 AND 255.255.255.192 → Network: 192.168.1.128


9. **Broadcast Address**

    **🧾 Formula:**  
    Broadcast = Network Address + 2^(32 - n) - 1

    **✅ Example:**  
    Network: 192.168.1.128, /26 → 2^6 = 64 IPs  
    → Broadcast = 192.168.1.128 + 63 = 192.168.1.191


10. **Host Range**

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

## RIP

```markdown
R1 -- R2 -- R3 -- R4 -- R5
 |                     |
  -------< >-----------
```

- Step 1 - **Router Initialization**
    - Routers boots and starts RIP
    - Router adds it connected network ( Routers ) to its router DB
    - For example, 
        - R1 has interfaces to:
            - 10.0.12.0/30 (to R2)
            -  10.0.15.0/30 (to R5)
        - R1’s routing table at this point:
            - 10.0.12.0/30 — directly connected
            - 10.0.15.0/30 — directly connected
- Step 2 - **RIP sends routing updates**
    - Distance vector
    - Each router sends its full routing table to directly connected neighbors
        - Every 30 seconds
        - UDP port 520
    - R1 sends to R2:
        - 10.0.12.0/30 — metric 0
        - 10.0.15.0/30 — metric 0
    - R2 sends to R1:
        - 10.0.23.0/30 — metric 1
        - 10.0.12.0/30 — metric 0

- Step 3 - **R1 Receives Update from R2**
    - R1 receives R2’s update
    - R1 adds R2’s networks to its routing table
        - 10.0.23.0/30 — metric 1
        - 10.0.12.0/30 — metric 0
    - R1 updates its routing table(Hop count)
        - 10.0.23.0/30 — metric 2 via R2
        - 10.0.12.0/30 — metric 1 `(R2–R3 link)`
- Step 4 - **Information Propagation**
    - R2 sends R3's networks to R1
    - R3's route (10.0.34.0/30) comes to R2
    - R2 updates its routing table
        - R3 advertised to R2: 10.0.34.0/30 → 1 hop
        - R2 advertises to R1: 10.0.34.0/30 → 2 hops
    - R1 adds 1 hop: 10.0.34.0/30 → 3 hops via R2
        - R1 → R2 → R3 → R4 = 3 hops to R4’s network

- Step 5 - **R1 Learns Multiple Paths**
    - R1 also hears from R5
    - R1 receives R5’s update
        - 10.0.45.0/30 (R4–R5) via R5 → 2 hops
        - 10.0.34.0/30 (R3–R4) via R5 → 3 hops
    - R1 has two paths to R4’s network
        - R1 → R2 → R3 → R4 → 3 hops
        - R1 → R5 → R4 → 2 hops

- Step 6 - **Routing Table Convergence**

| Destination  | Next Hop | Metric (Hop Count) |
| ------------ | -------- | ------------------ |
| 10.0.12.0/30 | Direct   | 0                  |
| 10.0.15.0/30 | Direct   | 0                  |
| 10.0.23.0/30 | R2       | 1                  |
| 10.0.34.0/30 | R2 or R5 | 2 or 2             |
| 10.0.45.0/30 | R5       | 1                  |

- Step 7 - **Periodic Updates**
    - Every 30 seconds, all routers continue sending their full routing table to neighbors.
    - RIP automatically adjusts when a link goes down `(after 180 seconds → route is invalid)`. 

### Summary

| Step | Action                                   | Effect on R1                          |
| ---- | ---------------------------------------- | ------------------------------------- |
| 1    | RIP starts, adds directly connected nets | Knows only its links                  |
| 2    | Receives updates from R2 and R5          | Learns about R3, R4 via neighbors     |
| 3    | Updates routing table with hop count     | Chooses shortest path to all routers  |
| 4    | Receives better paths                    | Replaces entries with lower hop count |
| 5    | Periodically sends and receives updates  | Maintains table continuously          |

---

## OSPF
- Link State Protocol
- Uses Dijkstra's algorithm to find the shortest path

### OSPF Step-by-Step Workflow
1. **Initialization**
   - OSPF starts on each router.
   - Each router identifies its directly connected interfaces and their states.

2. **Hello Packets**
    - Routers send Hello packets to discover neighbors.
    - Hello packets contain information about the router's ID, priority, and other parameters.
        ```
        R1 ---- Hello ----> R2
        R1 <--- Hello ---- R2  
        ```
3. **Establishing Adjacency**
    - Routers form adjacency with certain neighbors (like DR/BDR on multi-access networks).

    - Once adjacent, they start exchanging LSAs.

4. **LSA Exchange (Database Synchronization)**
    - Routers exchange Link-State Advertisements (LSAs) using Database Description (DBD) packets.

    - Routers use LS Request, LS Update, LS Ack to synchronize their Link-State Databases (LSDBs).

5. **LSA Types (Important for OSPF Operation)**

    | LSA Type | Description                                                                   |
    | -------- | ----------------------------------------------------------------------------- |
    | Type 1   | **Router LSA** – Sent by each router within an area                           |
    | Type 2   | **Network LSA** – Sent by DR in a broadcast network                           |
    | Type 3   | **Summary LSA** – Sent by ABR to advertise routes between areas               |
    | Type 4   | **ASBR Summary LSA** – Info about ASBR to other areas                         |
    | Type 5   | **External LSA** – Routes to external networks (e.g., redistributed from BGP) |

6. **SPF Calculation (Shortest Path First)**
    - Each router builds a Link-State Database (LSDB).

    - It runs the Dijkstra's SPF algorithm on the LSDB to calculate the shortest path to all other routers/networks.
    
    ```
    SPF Tree (R1):
    - R1 → R2 (cost 10)
    - R1 → R3 (cost 20 via R2)
    ```

7. **Routing Table Formation**
    - After SPF calculation, each router creates its routing table based on the shortest paths found.
    
    ```
    Routing Table:
    Network 10.0.0.0/24 via R2, cost 10
    Network 192.168.1.0/24 via R3, cost 20
    ```

8. **Periodic and Triggered Updates**
- OSPF does not send periodic full updates.
- Only changes (like link down/up) trigger a new LSA.
- LSAs are flooded to all OSPF routers within the area.

### OSPF Summary Table

| Step | Description                              |
| ---- | ---------------------------------------- |
| 1    | Routers initialize and assign OSPF areas |
| 2    | Discover neighbors via Hello packets     |
| 3    | Form adjacencies                         |
| 4    | Exchange LSAs (DB sync)                  |
| 5    | Build the LSDB with LSA types            |
| 6    | Run SPF algorithm to find best paths     |
| 7    | Install routes in the routing table      |
| 8    | React to topology changes with new LSAs  |


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
