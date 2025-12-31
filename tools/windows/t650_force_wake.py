import hid
import time

def force_wake():
    try:
        info = next(d for d in hid.enumerate(0x046d, 0xc52b) if d['usage_page'] == 0xff00)
        device = hid.device()
        device.open_path(info['path'])
        
        print(f"Force-initializing T650...")

        # 1. Ask for the 'Touchpad' feature index
        # [ID, DevIndex, RootFeature, GetFeatureCmd, FeatureID_MSB, FeatureID_LSB...]
        # 0x6010 is the ID for Touchpad gestures on HID++ 2.0
        msg = [0x11, 0x01, 0x00, 0x00, 0x60, 0x10] + [0]*14
        device.write(msg)
        time.sleep(0.1)

        # 2. Force Raw Mode (The "Magic" packet)
        # This specific sequence overrides the internal mouse emulator
        raw_mode = [0x11, 0x01, 0x01, 0x10, 0x01] + [0]*15
        device.write(raw_mode)
        
        print("Sent feature request and raw mode override.")
        device.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    force_wake()