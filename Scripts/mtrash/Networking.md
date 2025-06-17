**NETWORKING**

**Definition:**
*   Connecting computers and other devices to communicate and share resources.
*   Connections can be:
    *   Wired
    *   Wireless
*   **Enables communication between devices using standardized protocols.**

**Types of Computer Networks:**
*   **PAN (Personal Area Network)** - Very small area, personal devices (e.g., Bluetooth).
*   **LAN (Local Area Network)** - Limited area like homes, schools, offices.
*   **MAN (Metropolitan Area Network)** - Large campus or city.
*   **WAN (Wide Area Network)** - Large geographical areas (e.g., the Internet).
*   **VPN (Virtual Private Network)** - Secure connection over a public network (e.g., internet).

**Why Networking?**
*   Resource sharing – files, printers, internet.
*   Communication – email, instant messaging, VoIP.
*   Efficiency and productivity.
*   Cost saving (shared resources).
*   Remote access – access resources from different locations.
*   Scalability and flexibility.
*   **Centralized data management and backup.**

**OSI – Open Systems Interconnection**
*   Developed by ISO (International Organization for Standardization).
*   A **conceptual framework** that explains how different computer systems communicate over a network.
*   Provides a clear structure for data transmission and managing network issues.
*   **Divides the communication process into 7 distinct layers.**

**Layers of OSI Model**

1.  **Physical Layer (L1)**
    *   Lowest Layer.
    *   Establishes actual physical connection between devices.
    *   Contains information in the form of **bits (1s and 0s)**.
    *   Transmits individual bits from one node to another.
    *   Transmits raw binary data over physical mediums (e.g., cables, radio waves, fiber).
    *   **Devices:** Hub, Repeater, Modem, **Cables (Ethernet, Fiber)**, **Network Interface Card (NIC - Physical Connector)**.
    *   **Functions:** Bit synchronization, Bit rate control, Physical topologies (Bus, Star, Ring, Mesh), Transmission mode (Simplex, Half-duplex, Full-duplex).

2.  **Data Link Layer (DLL) (L2)**
    *   Node-to-node delivery of message (**on the same network segment**).
    *   **Responsible for** error-free transmission **over the physical link**.
    *   Packet in DLL is called a **Frame**.
    *   Transmits frames **between directly connected devices** using MAC address.
    *   **Devices:** **Switches (Bridges largely superseded by switches)**, **Bridges (legacy)**, **NIC (logical controller)**.
    *   **Functions:** Framing, Physical addressing (adds source/dest **MAC address** in header), Error control (**detection** via CRC, not correction), Flow control, Access control (**MAC protocols like CSMA/CD for Ethernet**).

3.  **Network Layer (L3)**
    *   **Host-to-host delivery** - Connects one host to another located in **potentially** different networks.
    *   Handles packet routing – determines **the** shortest path to transmit.
    *   Data is **organized in** packets (**or datagrams**).
    *   Sender & receiver's **logical (IP)** address are placed in the header.
    *   **Devices:** **Routers**, **Layer 3 Switches**.
    *   **Functions:** **Path determination (Routing)**, Logical addressing (**IP addressing**), **Fragmentation (if needed)**.
    *   **Key Protocol: IP (Internet Protocol)**.

4.  **Transport Layer (L4)**
    *   **Process-to-process** delivery - End-to-end delivery **between applications**.
    *   Data is referred to as **Segments (TCP) or Datagrams (UDP)**.
    *   Adds **source and destination** port number in the header.
    *   **Protocols:** **TCP (Transmission Control Protocol - Connection-oriented, reliable)**, **UDP (User Datagram Protocol - Connectionless, best-effort)**, NetBIOS, PPTP.
    *   **Functions:** **Service-point addressing (Port numbers)**, Segmentation **and reassembly**, **Connection control (TCP)**, Flow control, **End-to-end** Error checking **and recovery (TCP)**.

5.  **Session Layer (L5)**
    *   Establish, manage, and terminate **dialogue** sessions between two **communicating** devices.
    *   Provides **dialog** authentication and **session** security.
    *   **Protocols:** NetBIOS, PPTP, **RPC (Remote Procedure Call)**.
    *   **Functions:** Session establishment/management/termination, Synchronization (**checkpoints**), Dialog controller (half-duplex, full-duplex).

6.  **Presentation Layer (L6)**
    *   **Data Representation/Translation** layer.
    *   Translates data between application **data structures** and network **transmission** formats.
    *   **Protocol:** **TLS/SSL (also provides encryption)**, **MIME**.
    *   **Functions:** Translation (e.g., ASCII to EBCDIC, **data compression formats**), Encryption / Decryption, **Data** Compression.

7.  **Application Layer (L7)**
    *   Top layer, closest to the user (**provides network services to end-user applications**).
    *   **Protocols:** **HTTP/HTTPS (Web)**, **FTP (File Transfer)**, **SMTP (Email Send)**, **POP3/IMAP (Email Retrieve)**, **DNS (Domain Name Resolution)**, **DHCP (IP Address Assignment)**, **SNMP (Network Management)**.
    *   **Functions:** **Provides user interfaces and network services:** Mail services, Directory services, Web browsing, File transfer, **Remote login (Telnet, SSH)**.

**Transmission Modes:**

*   **Simplex Mode** – One-way communication.
    *   Sender can send data, but cannot receive.
    *   Example: Keyboard, **Traditional Broadcast TV/Radio**.
*   **Half-duplex Mode**
    *   Bidirectional communication, **but only one direction at a time**.
    *   Sender can send the data and also receive the data **but only one at a time**.
    *   Example: Walkie-Talkie, **Ethernet (CSMA/CD)**.
    *   **Illustration:** A is sending → B is receiving **then** A is receiving ← B is sending.
*   **Full-duplex Mode**
    *   **Simultaneous** bidirectional communication.
    *   Sender can send the data and also receive the data **at the same time**.
    *   Example: Telephone, **Modern Ethernet Switches**, **Web Browsing (HTTP over TCP)**.
    *   **Illustration:** A ⇄ B (Bidirectional, simultaneously).

**SOCKET**
*   Endpoint of a two-way communication link between two programs running on the network.
*   **Facilitates** realtime communication between devices **using IP addresses and port numbers**.
*   **Host Example IP:** 146.86.5.20
*   **Socket Example:** (146.86.5.28:1625) = IP + Port.
*   Used in client-server application **model**.
*   **TYPES OF SOCKETS:**
    *   **Datagram Socket (UDP)** - Connectionless, unreliable.
    *   **Stream Socket (TCP)** - Connection-oriented, reliable.

**PORTS**

*   **HARDWARE PORTS**
    *   Physical connection interface on a computer.
    *   Used to connect external devices:
        *   USB port
        *   HDMI port
        *   Ethernet port
        *   Audio jack
*   **SOFTWARE PORTS**
    *   Logical communication endpoint used by **a** software app to send and receive data over a network.
    *   Helps direct incoming and outgoing network traffic **to the correct application/service**.
    *   Represented by a **16-bit unsigned integer**, range **0 to 65535** (2^16 = 65536 ports).
*   **Port Ranges:**
    *   **0–1023:** Well-known ports (**System/Privileged ports**).
    *   **1024–49151:** Registered ports (**User ports, assigned by IANA for common services**).
    *   **49152–65535:** Dynamic/private ports (**Ephemeral ports, used by clients temporarily**).
*   **Common Ports:**
    *   20/21 – FTP (Data/Control)
    *   22 – SSH (Secure Shell)
    *   23 – Telnet (Insecure)
    *   25 – SMTP (Email Send)
    *   53 – DNS (Domain Name System)
    *   67/68 – DHCP (Server/Client)
    *   80 – HTTP (Web)
    *   110 – POP3 (Email Retrieve)
    *   143 – IMAP (Email Retrieve)
    *   443 – HTTPS (Secure Web)
    *   3389 – RDP (Remote Desktop)

**L1, L2, L3 Devices**
*   **L1 – Physical Layer:** Hubs, Repeaters, **Cables (Ethernet, Fiber)**, **Modems (Physical Signal Conversion)**.
*   **L2 – Data Link Layer:** **Switches (primary L2 device)**, Bridges (legacy), **Wireless Access Points (WAPs - primarily L2)**, NIC (logical controller).
*   **L3 – Network Layer:** **Routers (primary L3 device)**, **Layer 3 Switches (Switch with routing capabilities)**.

**FIREWALL**
*   Network security device (**can be** hardware/software/**cloud-based**).
*   Monitors **and controls** all incoming and outgoing **network** traffic **based on predefined security rules**.
*   **Acts** as a barrier between a **trusted internal network** (e.g., LAN) and an **untrusted external network** (e.g., WAN, internet).
*   **Actions:**
    *   **Allow/Accept** – Permit the traffic.
    *   **Deny/Reject** – Block the traffic **and typically send a rejection notification (e.g., TCP RST)**.
    *   **Drop** – Block the traffic **silently** with no reply.
*   **Firewall Types (Added for clarity):**
    *   **Packet-Filtering (Stateless):** Basic, rules based on IP/Port/Protocol.
    *   **Stateful Inspection:** Tracks active connections, more intelligent decisions.
    *   **Proxy Firewall:** Intermediary for connections, inspects application-layer traffic.
    *   **Next-Generation Firewall (NGFW):** Integrates deeper inspection (IPS, Application Control, Identity).
*   **Firewall rules (ACLs - Access Control Lists)** typically reside **on the firewall device**.
    *   **Rules check:** Source IP address, Destination IP address, **Source Port**, Destination Port number, Protocol (TCP, UDP, ICMP, etc.).
*   **ACLs (Access Control Lists):**
    *   **Ordered lists of permit/deny rules** used by routers **and firewalls** to control traffic flow.
    *   **Reside on network devices (Routers, Firewalls, L3 Switches)**.
    *   **Checks packet headers:** Primarily IP addresses **(Source/Destination)**, **Port numbers (Source/Destination)**, and **Protocol**.
