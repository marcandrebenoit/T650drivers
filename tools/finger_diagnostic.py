import hid
import os

# Configuration for T650 Firmware 038
VID, PID = 0x046D, 0xC52B
T650_IDX = 1
MT_IDX = 0x10

def diagnostic():
    path = next((d['path'] for d in hid.enumerate(VID, PID) if d['interface_number'] == 2), None)
    h = hid.device()
    h.open_path(path)
    
    # Send Key A Unlock
    h.write([0x11, T650_IDX, MT_IDX, 0x21, 0x02] + [0]*15)
    
    print("--- T650 5-FINGER DIAGNOSTIC ---")
    print("Touch the pad with multiple fingers to see raw data.\n")

    try:
        while True:
            data = h.read(20)
            if data and data[0] in [0x11, 0x20] and data[2] == MT_IDX:
                mask = data[4]
                fingers = []
                
                for i in range(5):
                    if mask & (1 << i):
                        # Parse 12-bit coords for active finger
                        offset = 5 + (i * 3)
                        x = data[offset] | ((data[offset+1] & 0x0F) << 8)
                        y = (data[offset+1] >> 4) | (data[offset+2] << 8)
                        fingers.append(f"F{i+1}:({x:4},{y:4})")
                    else:
                        fingers.append(f"F{i+1}:[ UP ]")
                
                print(f"\r{' | '.join(fingers)} | Mask:{bin(mask)}", end="", flush=True)
    except KeyboardInterrupt:
        h.write([0x11, T650_IDX, MT_IDX, 0x21, 0x00] + [0]*15)
        print("\nResetting to Mouse Mode.")

if __name__ == "__main__":
    diagnostic()
