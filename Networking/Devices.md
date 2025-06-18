
# Complete Notes: Network Devices, Layers & Tables

---

## 1. **Physical Layer Devices (Layer 1)**

| Device       | Function                                        | Communication Type       | Addressing | Tables Used |
| ------------ | ----------------------------------------------- | ------------------------ | ---------- | ----------- |
| **Hub**      | Repeats raw electrical signals to all ports     | Broadcast (no filtering) | None       | None        |
| **Repeater** | Amplifies or regenerates signals                | Signal boosting only     | None       | None        |
| **Cables**   | Transmit raw bits as electrical/optical signals | Physical media           | None       | None        |

* **Data Units:** Bits (0s and 1s)
* **Purpose:** Transmit raw bits without any filtering or processing.
* **Communication:** Broadcast to all connected devices; no intelligence.

---

## 2. **Data Link Layer Devices (Layer 2)**

| Device                           | Function                                                   | Communication Type            | Addressing    | Tables Used                       |
| -------------------------------- | ---------------------------------------------------------- | ----------------------------- | ------------- | --------------------------------- |
| **Switch**                       | Forwards frames based on MAC addresses to correct port     | Unicast, multicast, broadcast | MAC addresses | **MAC Address Table (CAM table)** |
| **Bridge**                       | Connects two LAN segments and filters traffic based on MAC | Unicast, multicast, broadcast | MAC addresses | MAC Address Table                 |
| **NIC (Network Interface Card)** | Physical interface for device on LAN                       | Sends/receives frames         | MAC addresses | ARP Cache (locally)               |

* **Data Units:** Frames
* **Addressing:** Uses **MAC addresses** (48-bit hardware address)
* **Key Functions:** Frame forwarding, filtering, error detection (CRC)
* **Important Table:**

  * **MAC Address Table:** Maps MAC addresses to switch ports; updated dynamically as frames pass through.
  * **ARP Table (on hosts):** Maps IP addresses to MAC addresses to enable local delivery.

---

## 3. **Network Layer Devices (Layer 3)**

| Device             | Function                                     | Communication Type | Addressing   | Tables Used                                                           |
| ------------------ | -------------------------------------------- | ------------------ | ------------ | --------------------------------------------------------------------- |
| **Router**         | Routes packets between different IP networks | Unicast, multicast | IP addresses | **Routing Table**, **ARP Table**, **NAT Table**, **Connection Table** |
| **Layer 3 Switch** | Combines switching and routing functions     | Unicast, multicast | IP addresses | Routing Table, MAC Address Table                                      |

* **Data Units:** Packets
* **Addressing:** Uses **IP addresses** (IPv4 or IPv6)
* **Key Functions:** Packet forwarding, routing, subnetting, traffic management.
* **Important Tables:**

  * **Routing Table:** Contains routes to destination networks, next hops, and metrics.
  * **ARP Table:** Resolves IP to MAC for local delivery.
  * **NAT Table:** Translates private IP/port to public IP/port in networks using NAT.
  * **Connection Table:** Used in stateful devices (routers/firewalls) to track active connections.

---

## 4. **Other Common Network Devices**

| Device           | Function                                                           | Layer(s) Used           | Notes                                                         |
| ---------------- | ------------------------------------------------------------------ | ----------------------- | ------------------------------------------------------------- |
| **Firewall**     | Filters traffic based on rules, may do NAT and stateful inspection | Layer 3/4 (sometimes 7) | Uses **ACLs** and **Connection Table** for stateful filtering |
| **Access Point** | Connects wireless clients to wired LAN                             | Layer 2 (and 1)         | Uses MAC addresses; acts like a wireless switch               |
| **Modem**        | Converts digital signals to analog for ISP connection              | Layer 1/2               | Connects home network to ISP                                  |

---

# Summary of Important Tables in Devices

| Table Name                    | Purpose                                                           | Used In Devices             |
| ----------------------------- | ----------------------------------------------------------------- | --------------------------- |
| **Routing Table**             | IP routes and next hops for packet forwarding                     | Routers, Layer 3 Switches   |
| **MAC Address Table**         | Map MAC addresses to switch ports for frame forwarding            | Switches, Bridges           |
| **ARP Table**                 | Map IP addresses to MAC addresses for local delivery              | Hosts, Routers              |
| **NAT Table**                 | Track private-to-public IP and port mappings                      | Routers, Firewalls          |
| **Connection Table**          | Track active connections for stateful filtering                   | Firewalls, Stateful Routers |
| **Access Control List (ACL)** | Rules for allowing or denying traffic based on IP, port, protocol | Routers, Firewalls          |

---

# Communication Flow Example

| Step                         | Device/Layer            | Action                                   |
| ---------------------------- | ----------------------- | ---------------------------------------- |
| 1. Bit transmission          | Layer 1 (Hub, Repeater) | Send raw electrical/optical signals      |
| 2. Frame forwarding          | Layer 2 (Switch)        | Forward frame based on MAC address       |
| 3. Packet routing            | Layer 3 (Router)        | Forward packet based on IP routing table |
| 4. NAT translation (if used) | Router/Firewall         | Translate private IP to public IP        |
| 5. Stateful filtering        | Firewall                | Check connection table and filter        |

---
