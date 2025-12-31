import hid
import time

# Hardware Constants
VID, PID = 0x046D, 0xC52B  # Logitech Unifying Receiver
T650_IDX = 1               # Device index on the receiver

def discover_features():
    # Target Interface 2 (HID++ Protocol)
    path = next((d['path'] for d in hid.enumerate(VID, PID) if d['interface_number'] == 2), None)
    
    if not path:
        print("[!] Could not find Unifying Receiver Interface 2.")
        return

    h = hid.device()
    h.open_path(path)
    
    print(f"--- Logitech T650 Feature Discovery ---")
    print(f"Device: {h.get_product_string()}")
    print("-" * 40)

    # We iterate through indices 0x00 to 0x20 to find Feature 0x6100 (Touchpad)
    # The command is: [ReportID, DevIndex, FeatureIndex, Function(GetID), Params...]
    for i in range(0x01, 0x25):
        # Function 0x00 on any feature index usually returns the Feature ID
        cmd = [0x11, T650_IDX, 0x00, 0x00, i] + [0]*15
        h.write(cmd)
        
        res = h.read(20, timeout_ms=100)
        if res and len(res) >= 6:
            # Bytes 4 and 5 contain the 16-bit Feature ID
            feature_id = (res[4] << 8) | res[5]
            
            if feature_id == 0x6100:
                print(f"[FOUND] Multi-Touch Feature (0x6100) at Index: {hex(i)}")
            elif feature_id != 0x0000:
                print(f"Index {hex(i)}: Feature {hex(feature_id)}")
        
        time.sleep(0.01)

    h.close()

if __name__ == "__main__":
    discover_features()
