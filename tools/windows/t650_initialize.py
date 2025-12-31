import hid
import time

def initialize_t650():
    try:
        # Connect via usage_page 0xff00 (Raw HID++)
        info = next(d for d in hid.enumerate(0x046d, 0xc52b) if d['usage_page'] == 0xff00)
        device = hid.device()
        device.open_path(info['path'])
        
        print(f"Initializing T650 on {info['path']}...")

        # HID++ 2.0 Command to enable "Raw" touch reporting
        # This tells the device: "Stop being a mouse, start being a touchpad."
        # [ReportID, DevIndex, FeatureIndex, Function/SoftwareID, Data...]
        # Note: 0x11 is the Long Report ID.
        msg = [0] * 20
        msg[0] = 0x11
        msg[1] = 0x01 # Device index (usually 0x01 for first device on receiver)
        msg[2] = 0x01 # Feature index for "Root"
        msg[3] = 0x00 # Function to get feature
        
        device.write(msg)
        print("Initialization packet sent. Now check the debug script again!")
        
        device.close()
    except Exception as e:
        print(f"Initialization Error: {e}")

if __name__ == "__main__":
    initialize_t650()