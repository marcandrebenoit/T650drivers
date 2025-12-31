import hid
import sys

# Hardware Constants
VID, PID = 0x046D, 0xC52B  # Logitech Unifying Receiver
T650_IDX = 1               # Standard index for the first device
MT_IDX = 0x10              # Multi-touch Feature Index (Firmware 038)

def unlock():
    # Target only the HID++ control interface (Interface 2)
    path = next((d['path'] for d in hid.enumerate(VID, PID) if d['interface_number'] == 2), None)
    
    if not path:
        print("[!] T650 Receiver Interface 2 not found.")
        return False

    try:
        h = hid.device()
        h.open_path(path)
        
        # Command: [LongReport, DevIndex, FeatureIdx, Function(SetMode), Mode(Advanced)]
        # Key A: 11 01 10 21 02
        cmd = [0x11, T650_IDX, MT_IDX, 0x21, 0x02] + [0]*15
        h.write(cmd)
        
        # Verify response (Optional but good for logs)
        res = h.read(20, timeout_ms=500)
        if res and res[3] == 0x21:
            print("[+] T650 successfully toggled to Advanced Mode.")
            return True
        else:
            print("[?] Unlock command sent, but no confirmation received.")
            return True # Often works even if response is missed
            
    except Exception as e:
        print(f"[!] Error: {e}")
        return False
    finally:
        h.close()

if __name__ == "__main__":
    if unlock():
        sys.exit(0)
    else:
        sys.exit(1)
