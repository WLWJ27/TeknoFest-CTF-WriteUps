import csv

CSV_FILE = "icmp-4.csv"
SIGNAL_LENGTH = "64" 

bits = []
last_signal_time = 0.0
cumulative_time = 0.0
first_packet = True

with open(CSV_FILE, mode='r') as f:
    reader = csv.DictReader(f)
    
    for row in reader:
        raw_delta = row["Time"].strip()
        delta_val = float(raw_delta) if raw_delta else 0.0
        cumulative_time += delta_val

        if row["Length"] != SIGNAL_LENGTH:
            continue

        if first_packet:
            last_signal_time = cumulative_time
            first_packet = False
            continue

        # 4. Calculate the gap between THIS signal ping and the LAST signal ping
        actual_gap = cumulative_time - last_signal_time
        
        # Use a mid-point (1.5s) to decide between 0 and 1
        # This is more robust than strict rounding
        if 0.5 <= actual_gap < 1.5:
            bits.append("0")
        elif 1.5 <= actual_gap < 3.0:
            bits.append("1")
        
        last_signal_time = cumulative_time

# --- DECODING ---
bitstream = "".join(bits)

# We often miss the very first bit because it has no 'gap' before it.
# If the stream starts with the pattern for 'S' (1010011) missing the lead 0:
if bitstream.startswith("1010011"):
    bitstream = "0" + bitstream

flag = ""
for i in range(0, len(bitstream), 8):
    byte = bitstream[i:i+8]
    if len(byte) == 8:
        flag += chr(int(byte, 2))

print(f"Total bits: {len(bits)}")
print(f"Decoded Flag: {flag}")