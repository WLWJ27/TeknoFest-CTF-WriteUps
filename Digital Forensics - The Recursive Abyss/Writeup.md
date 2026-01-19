# 🌊 The Recursive Abyss

> *"In the darkest depths of Davy Jones' Locker, secrets are buried beneath layers of ocean floor, each layer deeper than the last. Only those who dare to dive through every stratum shall find the treasure that lies at the heart of the abyss."*

**Challenge Author: Aman Shahid**

## 📋 Challenge Overview

**The Recursive Abyss** is an advanced network forensics CTF challenge that simulates real-world data exfiltration techniques used by Advanced Persistent Threat (APT) groups. Participants must analyze a PCAP file containing approximately 1,000 packets of mixed network traffic to locate and extract a hidden flag that has been recursively encapsulated through multiple protocol layers.

---

## 🎯 Challenge Details

| Property | Value |
|----------|-------|
| **Category** | Network Forensics / PCAP Analysis |
| **Difficulty** | Hard |
| **Points** | 500 |
| **Estimated Time** | 2-4 hours |
| **Skills Required** | Protocol Analysis, Traffic Filtering, Data Decoding |
| **Flag Format** | `FLAG{...}` |

---

## 📖 Story & Context

Captain Jack Sparrow's ship, the *Black Pearl*, was intercepted by the Royal Navy while attempting to transmit secret coordinates to hidden treasure. The Navy captured network traffic containing roughly a thousand packets, each analogous to bottles thrown overboard with sealed messages.

However, the cunning pirate didn't simply write his secrets in plain text. Using an old technique passed down from Bootstrap Bill, Jack employed **recursive protocol encapsulation** - messages hidden within messages, sealed within bottles, placed in chests, buried in other chests.

The Navy's finest cryptographers have been stumped for weeks. They see the packets, they see the protocols, but they cannot comprehend the *depth* of the deception.

**Your mission**: Analyze this captured maritime traffic, dive deep through the layers of deception, peel back each protocol layer, and retrieve the coordinates to Jack's treasure.

⚠️ **Beware**: Not all packets contain treasure. Many are decoys thrown to mislead pursuers.

---

## 🏗️ Technical Architecture

### The Encapsulation Stack

The challenge implements a four-layer recursive encapsulation scheme:

```
┌─────────────────────────────────────────────┐
│  Layer 0: PCAP File (~1000 packets)         │
│  ├─ HTTP/HTTPS Traffic (300 packets)        │
│  ├─ DNS Queries (200 packets)               │
│  ├─ ICMP Pings (150 packets)                │
│  ├─ ARP, SMB, NTP, mDNS (140 packets)       │
│  ├─ Decoy GRE Traffic (20 packets)          │
│  └─ FLAG GRE Traffic (7 packets) ← TARGET   │
└─────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────┐
│  Layer 1: GRE Tunnel                        │
│  (Generic Routing Encapsulation)            │
│  • Protocol: 47                             │
│  • Destination: 192.168.1.200               │
│  • Contains: Encapsulated IP packets        │
└─────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────┐
│  Layer 2: ICMP Echo Requests                │
│  • Type: 8 (Echo Request)                   │
│  • ID: 0x1337 (Elite marker) ← HINT         │
│  • Payload: Contains DNS packets            │
└─────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────┐
│  Layer 3: DNS Queries                       │
│  • Query Type: A Record                     │
│  • Domain Pattern: *.partN.challenge.ctf    │
│  • Subdomain: Base64 encoded data           │
└─────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────┐
│  Layer 4: Base64 Encoded Flag               │
│  • Encoding: Standard Base64                │
│  • Chunked: Across multiple packets         │
│  • Ordering: By ICMP sequence number        │
└─────────────────────────────────────────────┘
                    ↓
              🏆 FLAG{...}
```

### Key Indicators of Compromise (IoCs)

Participants must identify these specific markers to locate the flag traffic:

1. **GRE Destination**: `192.168.1.200` (legitimate destination for flag packets)
2. **ICMP Identifier**: `0x1337` (hexspeak for "leet" - elite/secret traffic)
3. **DNS Domain Pattern**: `*.challenge.ctf` (non-existent TLD indicates covert channel)
4. **Subdomain Format**: Base64-encoded chunks (unusual for legitimate DNS)

---

## 🔍 Challenge Components

### Traffic Composition

The PCAP file contains realistic network noise to simulate a production environment:

| Traffic Type | Packet Count | Purpose |
|--------------|--------------|---------|
| HTTP/HTTPS | ~300 | Web browsing simulation |
| DNS Queries | ~200 | Normal domain resolution |
| ICMP Pings | ~150 | Network diagnostics |
| ARP Requests | ~50 | Local network discovery |
| SMB Traffic | ~30 | File sharing activity |
| NTP Sync | ~20 | Time synchronization |
| mDNS | ~40 | Multicast DNS discovery |
| **Decoy GRE** | ~20 | Red herring tunnels |
| **FLAG GRE** | **~7** | **Actual flag traffic** |
| **TOTAL** | **~1000** | |

### Signal-to-Noise Ratio

- **Flag Packets**: 7 out of ~1000 (**0.7%**)
- **Decoy Complexity**: Multiple false positives (decoy GRE, normal ICMP)
- **Realistic Timestamps**: Packets distributed over time
- **Protocol Diversity**: 8+ different protocols in mix

---

## 🛠️ Required Tools & Technologies

### Essential Tools

1. **Wireshark** (Primary Analysis Tool)
   - Version: 3.0+
   - Purpose: Packet visualization, filtering, protocol dissection
   - Download: https://www.wireshark.org/

2. **Python 3** (Scripting & Automation)
   - Version: 3.8+
   - Libraries: Scapy, base64 (standard library)
   - Purpose: Automated extraction and decoding

3. **Scapy** (Packet Manipulation)
   - Installation: `pip install scapy`
   - Purpose: Programmatic packet parsing
   - Documentation: https://scapy.net/

### Optional Tools

- **tshark**: Command-line packet analysis
- **CyberChef**: Web-based decoding (https://gchq.github.io/CyberChef/)
- **NetworkMiner**: Alternative packet analyzer
- **tcpdump**: Quick packet filtering

---

## 🧭 Solution Methodology

### High-Level Approach

Participants should follow this investigative workflow:

```
1. Initial Reconnaissance
   └─> Identify unusual protocols in traffic mix

2. Protocol Isolation
   └─> Filter GRE packets and analyze destinations

3. Tunnel Extraction
   └─> Extract encapsulated packets from GRE payload

4. Pattern Recognition
   └─> Identify consistent ICMP ID values

5. Payload Analysis
   └─> Parse ICMP payload as DNS packets

6. Data Reconstruction
   └─> Extract Base64 chunks from DNS queries

7. Decoding
   └─> Concatenate and decode Base64 to reveal flag
```

### Wireshark Filter Progression

Participants will likely use these filters in sequence:

```bash
# Step 1: Find all GRE traffic
gre

# Step 2: Narrow to specific destination
gre and ip.dst == 192.168.1.200

# Step 3: Verify ICMP inside GRE
gre and ip.dst == 192.168.1.200 and icmp

# Step 4: Examine specific ICMP ID (after discovery)
icmp.ident == 0x1337
```

### Extraction Methods

**Method 1: Manual (Wireshark)**
1. Filter to target packets
2. Right-click → Follow → Stream
3. Export packet bytes
4. Parse manually or with hex editor

**Method 2: Semi-Automated (tshark)**
```bash
tshark -r challenge.pcap -Y "gre and ip.dst == 192.168.1.200" \
       -T fields -e data -e icmp.seq
```

**Method 3: Fully Automated (Scapy)**
```python
from scapy.all import *
import base64

# Load PCAP
packets = rdpcap("challenge.pcap")

# Filter GRE to specific destination
gre_pkts = [p for p in packets if p.haslayer(GRE) 
            and p[IP].dst == "192.168.1.200"]

# Extract DNS from ICMP in GRE
dns_queries = []
for pkt in gre_pkts:
    inner = pkt[GRE].payload
    if inner.haslayer(ICMP) and inner[ICMP].id == 0x1337:
        dns_pkt = DNS(inner[Raw].load)
        dns_queries.append((inner[ICMP].seq, dns_pkt[DNSQR].qname))

# Sort by sequence and decode
dns_queries.sort()
b64_data = ''.join([q.split(b'.')[0].decode() for _, q in dns_queries])
flag = base64.b64decode(b64_data).decode()
```

---

## 💡 Hint System

### Progressive Hints (Released Over Time)

**Hint 1 - The Kraken's Path** (Immediate)
> *"The Kraken doesn't attack every ship, only those sailing to specific waters. Filter your search to ships bound for the cursed coordinates: `192.168.1.200`"*

**Hint 2 - The Elite Crew Mark** (+2 hours)
> *"Captain Jack marks his trusted messages with a sacred number - 0x1337. In the world of ECHO requests, this be the Captain's signature."*

**Hint 3 - Bootstrap Bill's Wisdom** (+4 hours)
> *"Sometimes, lad, the treasure ain't in the answer - it's in the question. DNS queries be more than they appear."*

**Hint 4 - The Compass** (+6 hours)
> *"When lost at sea, use this bearing: `gre and ip.dst == 192.168.1.200 and icmp`"*

**Hint 5 - The Order of the Seas** (+8 hours)
> *"Every message has its place in the sequence. The Captain numbers his echoes for a reason."*

### Subtle Hints Embedded in Description

- "Four fathoms deep" → Four protocol layers
- "1337" repeatedly mentioned → Hexspeak indicator
- "Questions themselves" → DNS queries
- "Specific destination" → Filter by IP
- "Recursive" in title → Multiple layers

---

## 🎓 Learning Objectives

Upon completing this challenge, participants will gain understanding of:

### Technical Skills
- ✅ Network protocol analysis (OSI Layer 2-7)
- ✅ PCAP file structure and manipulation
- ✅ GRE tunneling mechanics
- ✅ ICMP protocol internals
- ✅ DNS packet structure
- ✅ Base64 encoding/decoding
- ✅ Wireshark advanced filtering
- ✅ Scapy packet parsing
- ✅ Data exfiltration techniques
- ✅ Covert channel detection

### Cybersecurity Concepts
- 🔒 Protocol encapsulation and tunneling
- 🔒 Signal-to-noise ratio in traffic analysis
- 🔒 Indicator of Compromise (IoC) identification
- 🔒 Behavioral analysis vs. signature detection
- 🔒 Red team evasion techniques
- 🔒 Blue team detection methodologies

### Real-World Applications
- 🌐 APT (Advanced Persistent Threat) tactics
- 🌐 Incident response procedures
- 🌐 Network forensics investigation
- 🌐 Malware communication analysis
- 🌐 Data Loss Prevention (DLP) bypass methods

---

## 🌍 Real-World Relevance

### Industry Techniques Simulated

This challenge mirrors actual techniques used in:

**Offensive Operations:**
- **APT Groups**: Turla, Equation Group, APT29 (Cozy Bear)
- **Malware Families**: DNSMessenger, PoisonIvy, Cobalt Strike
- **Red Team Engagements**: Standard covert channel testing

**Defensive Operations:**
- **SOC Analysis**: Daily traffic investigation tasks
- **Incident Response**: Breach investigation procedures
- **Threat Hunting**: Proactive anomaly detection

### Notable Real-World Incidents

1. **2013 Target Breach**: Multi-layer protocol manipulation for 40M+ credit card exfiltration
2. **2017 DNSMessenger**: PowerShell malware using DNS TXT records for C2
3. **2018 APT29 HAMMERTOSS**: Combined Twitter, GitHub, and DNS tunneling

### Tools Used in Production

**Offensive:**
- `dnscat2` - DNS tunneling
- `iodine` - IP over DNS
- `icmptunnel` - ICMP encapsulation
- `ptunnel` - TCP over ICMP

**Defensive:**
- `Suricata/Snort` - IDS tunnel detection
- `Zeek (Bro)` - Protocol anomaly detection
- `Wireshark` - Manual forensic analysis
- `NetworkMiner` - Traffic reconstruction

---

## 📊 Difficulty Analysis

### What Makes This Hard

1. **Extreme Signal-to-Noise**: 0.7% flag packets among 99.3% noise
2. **Multi-Layer Complexity**: Four distinct protocol layers to traverse
3. **Active Deception**: Decoy GRE traffic mimicking flag patterns
4. **Non-Standard Usage**: Protocols used outside normal specifications
5. **Fragmented Data**: Flag split across multiple sequential packets
6. **Time Investment**: Requires thorough, methodical analysis

### Skill Progression

```
Beginner → Can identify unusual protocols
    ↓
Intermediate → Can filter and isolate GRE traffic
    ↓
Advanced → Can extract nested protocols manually
    ↓
Expert → Can script automated extraction with Scapy
    ↓
Master → Understands real-world APT implications
```

### Expected Solve Rate

- **With No Hints**: ~15% (experienced CTF players)
- **With Early Hints**: ~40% (intermediate players)
- **With All Hints**: ~70% (determined beginners)

---

## 🚀 Deployment Instructions

### For Challenge Creators

#### Prerequisites
```bash
# Install Python 3.8+
python --version

# Install Scapy
pip install scapy

# Install Npcap (Windows) or libpcap (Linux)
# Windows: https://npcap.com/
# Linux: sudo apt-get install libpcap-dev
```

#### Generate Challenge
```bash
# Clone or download challenge files
cd recursive-abyss-challenge

# Generate the PCAP file
python generate_challenge.py

# Verify challenge is solvable
python solver.py

# Output: challenge.pcap (~1000 packets)
```

#### Customization Options

Edit `generate_challenge.py` to customize:

```python
# Change the flag
FLAG = "FLAG{your_custom_flag_here}"

# Adjust packet count
TARGET_PACKET_COUNT = 2000  # More noise

# Modify IoC indicators
ICMP_ID = 0x4242  # Different magic number
DST_IP = "10.0.0.100"  # Different destination

# Change encoding
# Add XOR cipher before Base64
def xor_encrypt(data, key=0x42):
    return bytes([b ^ key for b in data.encode()])
```

### For CTF Platforms

#### File Delivery
- **Filename**: `the_recursive_abyss.pcap` or `davy_jones_locker.pcap`
- **Filesize**: ~150-300 KB (depending on packet count)
- **MD5 Hash**: Generate and provide for integrity verification
- **Compression**: Optional `.zip` or `.tar.gz` (reduces by ~60%)

#### Challenge Metadata
```yaml
name: "The Recursive Abyss"
category: "Network Forensics"
difficulty: "Hard"
points: 500
files:
  - the_recursive_abyss.pcap
flag_format: "FLAG{...}"
hints:
  - cost: 50 points
    text: "The tunnel has a specific destination"
  - cost: 100 points
    text: "Look for ICMP ID 0x1337"
  - cost: 150 points
    text: "DNS queries contain Base64"
```

---

## 🏆 Scoring & Hints

### Point Distribution

| Milestone | Points | Cumulative |
|-----------|--------|------------|
| Identify GRE traffic | 50 | 50 |
| Filter to correct destination | 75 | 125 |
| Extract ICMP from GRE | 100 | 225 |
| Discover ICMP ID pattern | 100 | 325 |
| Parse DNS from ICMP | 100 | 425 |
| Decode Base64 flag | 75 | 500 |

### Hint Penalty Structure

- **Hint 1**: -50 points (425 max)
- **Hint 2**: -100 points (375 max)
- **Hint 3**: -150 points (325 max)
- **Full Solution**: -300 points (200 max)

---

## 📝 Solution Validation

### Flag Verification

The correct flag format will be:
```
FLAG{n3st3d_pr0t0c0ls_are_fun}
```

**Validation Regex:**
```regex
^FLAG\{[a-z0-9_]+\}$
```

### Common Mistakes

❌ **Incorrect decoding order**: Must sort by ICMP sequence number  
❌ **Wrong Base64 padding**: Ensure proper concatenation  
❌ **Including domain suffix**: Only extract subdomain portion  
❌ **Decoy GRE traffic**: Must filter to correct destination  
❌ **Wrong ICMP ID**: Only packets with 0x1337 contain flag  

---

## 🔧 Troubleshooting

### For Participants

**Problem**: "I can't find any GRE packets"
- **Solution**: Ensure Wireshark is decoding properly. Try filter: `ip.proto == 47`

**Problem**: "GRE payload shows as malformed"
- **Solution**: Right-click → Decode As → GRE

**Problem**: "ICMP payload is just hex data"
- **Solution**: Export bytes and parse as DNS manually or with Scapy

**Problem**: "Base64 decode fails"
- **Solution**: Check for proper ordering (ICMP seq), remove domain suffix

### For Challenge Creators

**Problem**: "Scapy won't install on Windows"
- **Solution**: Install Npcap first, then retry Scapy installation

**Problem**: "Generated PCAP has wrong packet count"
- **Solution**: Adjust `TARGET_PACKET_COUNT` in generate_challenge.py

**Problem**: "Solver script fails"
- **Solution**: Verify PCAP filename matches, check Python version 3.8+

---

## 📚 Additional Resources

### Recommended Reading

**Protocol Documentation:**
- [RFC 2784 - Generic Routing Encapsulation (GRE)](https://tools.ietf.org/html/rfc2784)
- [RFC 792 - Internet Control Message Protocol (ICMP)](https://tools.ietf.org/html/rfc792)
- [RFC 1035 - Domain Names (DNS)](https://tools.ietf.org/html/rfc1035)

**Tunneling & Covert Channels:**
- "The Art of Exploitation" by Jon Erickson
- "Network Forensics" by Sherri Davidoff
- "Practical Packet Analysis" by Chris Sanders

**Wireshark Mastery:**
- [Wireshark Official Documentation](https://www.wireshark.org/docs/)
- [Wireshark Network Analysis](https://www.wiresharkbook.com/)

### Video Tutorials

- Wireshark Tutorial Series (YouTube: NetworkChuck)
- Scapy Basics (YouTube: John Hammond)
- Network Forensics (YouTube: HackerSploit)

### Practice Platforms

- [PCAP Analysis on TryHackMe](https://tryhackme.com/)
- [Network Forensics on HackTheBox](https://www.hackthebox.eu/)
- [Malware Traffic Analysis](https://www.malware-traffic-analysis.net/)

---

## 🤝 Credits & Attribution

**Challenge Concept**: Inspired by real-world APT techniques and covert channel research

**Technical Implementation**: Based on legitimate network protocols (GRE, ICMP, DNS)

**Theming**: Pirates of the Caribbean franchise (Disney)

**Tools Used**:
- Scapy (Python packet manipulation library)
- Wireshark (Open source packet analyzer)
- Python 3 (Standard library)

**Special Thanks**:
- Anthropic Claude (Challenge development assistance)
- CTF Community (Continuous inspiration)
- Network Security Researchers (Real-world insights)

---

## 📄 License

This challenge is released for **educational and CTF purposes only**.

**Permitted Use:**
- ✅ CTF competitions
- ✅ Educational training
- ✅ Security awareness workshops
- ✅ Academic research

**Prohibited Use:**
- ❌ Malicious purposes
- ❌ Unauthorized network testing
- ❌ Production network deployment
- ❌ Commercial redistribution without permission

---

## 🎉 Conclusion

**The Recursive Abyss** is more than just a CTF challenge - it's a journey through the depths of network protocol analysis, mirroring real-world techniques used by both attackers and defenders in modern cybersecurity.

By completing this challenge, participants will have demonstrated:
- Advanced packet analysis skills
- Understanding of protocol encapsulation
- Ability to filter signal from noise
- Persistence in multi-layered investigation
- Real-world incident response capabilities

*"The problem is not the problem. The problem is your attitude about the problem."*  
— Captain Jack Sparrow (probably talking about PCAP analysis)

**Good luck, and may your filters be ever precise!** 🏴‍☠️🔍

---

**Version**: 1.0  
**Last Updated**: January 2026  
**Difficulty Rating**: ⭐⭐⭐⭐⚪ (4/5)  
**Estimated Solve Time**: 2-4 hours  

🌊 *Dive deep, brave analyst. The abyss awaits.* 🌊
