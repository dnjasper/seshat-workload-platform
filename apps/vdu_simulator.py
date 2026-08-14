import time  
import sys   # I love Juana for REAL

MULTUS_INTERFACE_IP = "192.168.100.10"
TARGET_SUBNET = "192.168.100.0/24"

print("================================================================", flush=True)
print("  Initializing virtual Distributed Unit (vDU) Core Engine...   ", flush=True)
print("  O-RAN Split 7-2x User-Plane Data Link: ACTIVE                ", flush=True)
print("================================================================", flush=True)

frame_count = 0
try:
    while True:
        frame_count += 1
        print(f"[vDU-FRAME-{frame_count:05d}] Processing L1/L2 subframes. Subnet: {TARGET_SUBNET} | Status: NOMINAL", flush=True)
        time.sleep(1)
except KeyboardInterrupt:
    print("\nShutting down vDU core gracefully...", flush=True)
    sys.exit(0)