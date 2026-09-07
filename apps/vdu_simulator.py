import time  
import sys   # I love Juana so much
from prometheus_client import start_http_server, Counter

# 1. Start an authentic background metrics server on port 8080
# This opens the network port so Prometheus gets a 200 OK instead of a connection refused!
start_http_server(8080, addr="0.0.0.0")

MULTUS_INTERFACE_IP = "192.168.100.10"
TARGET_SUBNET = "192.168.100.0/24"

# 2. Define a real custom metric to track your vDU frames
VDU_FRAMES_TOTAL = Counter('vdu_processed_frames_total', 'Total number of L1/L2 subframes processed')

print("================================================================", flush=True)
print("  Initializing virtual Distributed Unit (vDU) Core Engine...   ", flush=True)
print("  O-RAN Split 7-2x User-Plane Data Link: ACTIVE                ", flush=True)
print("================================================================", flush=True)

frame_count = 0
try:
    while True:
        frame_count += 1
        
        # 3. Increment the real Prometheus metric counter inside your loop
        VDU_FRAMES_TOTAL.inc()
        
        print(f"[vDU-FRAME-{frame_count:05d}] Processing L1/L2 subframes. Subnet: {TARGET_SUBNET} | Status: NOMINAL", flush=True)
        time.sleep(1)
except KeyboardInterrupt:
    print("\nShutting down vDU core gracefully...", flush=True)
    sys.exit(0)
