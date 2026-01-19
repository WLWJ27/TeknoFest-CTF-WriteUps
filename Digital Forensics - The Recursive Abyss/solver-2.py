from scapy.all import *
import base64

def solve_challenge(pcap_file):
    """
    Solve the recursive encapsulation challenge
    """
    print("[+] Loading PCAP file...")
    packets = rdpcap(pcap_file)
    print(f"[+] Total packets: {len(packets)}")
    
    print("\n[*] Traffic Analysis:")
    gre_count = len([p for p in packets if p.haslayer(GRE)])
    icmp_count = len([p for p in packets if p.haslayer(ICMP)])
    dns_count = len([p for p in packets if p.haslayer(DNS)])
    tcp_count = len([p for p in packets if p.haslayer(TCP)])
    
    print(f"    GRE packets: {gre_count}")
    print(f"    ICMP packets: {icmp_count}")
    print(f"    DNS packets: {dns_count}")
    print(f"    TCP packets: {tcp_count}")

    print("\n[*] Step 1: Filtering GRE packets...")
    gre_packets = [pkt for pkt in packets if pkt.haslayer(GRE)]
    print(f"    Found {len(gre_packets)} GRE packets")
    
    if not gre_packets:
        print("[-] No GRE packets found!")
        return

    print("\n[*] Analyzing GRE destinations...")
    gre_dests = {}
    for pkt in gre_packets:
        dest = pkt[IP].dst
        gre_dests[dest] = gre_dests.get(dest, 0) + 1
    
    print("    GRE Destination Distribution:")
    for dest, count in sorted(gre_dests.items(), key=lambda x: x[1], reverse=True):
        print(f"      {dest}: {count} packets")
    
    main_dest = max(gre_dests.items(), key=lambda x: x[1])[0]
    print(f"\n[*] Focusing on GRE packets to {main_dest}...")
    gre_packets = [pkt for pkt in gre_packets if pkt[IP].dst == main_dest]
    print(f"    Filtered to {len(gre_packets)} GRE packets")

    print("\n[*] Step 2: Extracting ICMP from GRE tunnel...")
    icmp_packets = []
    
    for pkt in gre_packets:
        if pkt.haslayer(GRE):
            gre_payload = pkt[GRE].payload
            if gre_payload.haslayer(ICMP):
                icmp_packets.append(gre_payload)
    
    print(f"    Found {len(icmp_packets)} ICMP packets inside GRE")
    
    if not icmp_packets:
        print("[-] No ICMP packets found in GRE tunnel!")
        return

    print("\n[*] Analyzing ICMP packet IDs...")
    icmp_ids = {}
    for pkt in icmp_packets:
        if pkt.haslayer(ICMP):
            icmp_id = pkt[ICMP].id
            icmp_ids[icmp_id] = icmp_ids.get(icmp_id, 0) + 1
    
    print("    ICMP ID Distribution:")
    for icmp_id, count in sorted(icmp_ids.items(), key=lambda x: x[1], reverse=True)[:5]:
        print(f"      0x{icmp_id:04x}: {count} packets")
    
    target_id = 0x1337
    if target_id in icmp_ids:
        print(f"\n[*] Found suspicious ICMP ID: 0x{target_id:04x} ({icmp_ids[target_id]} packets)")
        print(f"    This looks interesting... (0x1337 = 'leet' in hexspeak)")
        icmp_packets = [pkt for pkt in icmp_packets if pkt[ICMP].id == target_id]
    
    print("\n[*] Step 3: Extracting DNS from ICMP payloads...")
    dns_data = []
    
    for pkt in icmp_packets:
        if pkt.haslayer(ICMP) and pkt.haslayer(Raw):
            icmp_payload = pkt[Raw].load
            
            try:
                dns_pkt = DNS(icmp_payload)
                if dns_pkt.haslayer(DNSQR):
                    query_name = dns_pkt[DNSQR].qname.decode()
                    seq = pkt[ICMP].seq
                    dns_data.append((seq, query_name))
                    print(f"    [Seq {seq}] DNS query: {query_name}")
            except:
                pass
    
    print(f"\n    Total DNS queries extracted: {len(dns_data)}")
    
    if not dns_data:
        print("[-] No DNS queries found!")
        return
    
    dns_data.sort(key=lambda x: x[0])
    dns_queries = [query for seq, query in dns_data]
    
    print("\n[*] Step 4: Decoding flag from DNS queries...")
    
    encoded_parts = []
    for query in dns_queries:
        subdomain = query.split('.')[0]
        encoded_parts.append(subdomain)
        print(f"    Extracted part: {subdomain}")
    
    full_encoded = ''.join(encoded_parts)
    print(f"\n    Complete Base64 string: {full_encoded}")
    
    try:
        decoded_flag = base64.b64decode(full_encoded).decode()
        print(f"\n{'='*60}")
        print(f"[+] FLAG FOUND: {decoded_flag}")
        print(f"{'='*60}")
        return decoded_flag
    except Exception as e:
        print(f"[-] Failed to decode: {e}")
        return None

def show_hints():
    """
    Display progressive hints for solvers
    """
    print("\n" + "="*60)
    print("PROGRESSIVE HINTS (use these if stuck)")
    print("="*60)
    
    hints = [
        "Hint 1: Start by looking at unusual protocols in Wireshark. What protocol is uncommon in typical traffic?",
        "Hint 2: GRE (Generic Routing Encapsulation) is a tunneling protocol. Maybe something is hidden inside?",
        "Hint 3: Not all GRE packets are created equal. Check their destination IPs - is one destination more common?",
        "Hint 4: Once you extract the inner packets from GRE, what protocol do you see? ICMP perhaps?",
        "Hint 5: ICMP packets have an 'id' field. Is there a suspicious or non-random ID being used? (Think hexspeak)",
        "Hint 6: 0x1337 is 'leet' speak. These ICMP packets with ID 0x1337 seem special. What's in their payload?",
        "Hint 7: The ICMP payload contains binary data. Try parsing it as another protocol... maybe DNS?",
        "Hint 8: DNS queries have domain names. Look at the subdomains - do they look like encoded data?",
        "Hint 9: The subdomains look like Base64. Try extracting and concatenating them in order (use ICMP seq numbers).",
        "Hint 10: Base64 decode the concatenated string to get your flag!"
    ]
    
    for hint in hints:
        print(f"\n{hint}")

def quick_analysis(pcap_file):
    """
    Quick analysis for challenge creators to verify
    """
    print("\n" + "="*60)
    print("QUICK ANALYSIS FOR CHALLENGE VERIFICATION")
    print("="*60)
    
    packets = rdpcap(pcap_file)
    
    print(f"\nTotal packets: {len(packets)}")
    
    protocols = {}
    for pkt in packets:
        if pkt.haslayer(GRE):
            protocols['GRE'] = protocols.get('GRE', 0) + 1
        elif pkt.haslayer(ICMP):
            protocols['ICMP'] = protocols.get('ICMP', 0) + 1
        elif pkt.haslayer(DNS):
            protocols['DNS'] = protocols.get('DNS', 0) + 1
        elif pkt.haslayer(TCP):
            protocols['TCP'] = protocols.get('TCP', 0) + 1
        elif pkt.haslayer(UDP):
            protocols['UDP'] = protocols.get('UDP', 0) + 1
        elif pkt.haslayer(ARP):
            protocols['ARP'] = protocols.get('ARP', 0) + 1
    
    print("\nProtocol Distribution:")
    for proto, count in sorted(protocols.items(), key=lambda x: x[1], reverse=True):
        percentage = (count / len(packets)) * 100
        print(f"  {proto:8s}: {count:4d} packets ({percentage:.1f}%)")
    
    gre_packets = [p for p in packets if p.haslayer(GRE)]
    flag_gre = [p for p in gre_packets if p[IP].dst == "192.168.1.200"]
    
    print(f"\nGRE Analysis:")
    print(f"  Total GRE packets: {len(gre_packets)}")
    print(f"  Flag GRE packets (to 192.168.1.200): {len(flag_gre)}")
    print(f"  Decoy GRE packets: {len(gre_packets) - len(flag_gre)}")
    
    icmp_1337 = 0
    for pkt in flag_gre:
        if pkt.haslayer(GRE):
            inner = pkt[GRE].payload
            if inner.haslayer(ICMP) and inner[ICMP].id == 0x1337:
                icmp_1337 += 1
    
    print(f"\nFlag Traffic:")
    print(f"  ICMP packets with ID 0x1337: {icmp_1337}")
    print(f"  This is your flag traffic!")

if __name__ == "__main__":
    pcap_file = "challenge-2.pcap"
    
    print("="*60)
    print("RECURSIVE ENCAPSULATION CHALLENGE SOLVER")
    print("="*60)
    
    quick_analysis(pcap_file)
    
    print("\n")
    flag = solve_challenge(pcap_file)
    
    if flag:
        print("\n[+] Challenge solved successfully!")
    else:
        print("\n[-] Failed to solve challenge")
    
    show_hints()