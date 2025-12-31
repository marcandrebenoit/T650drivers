import hid
import time

def decode_t650():
    # Vendor: Logitech (0x046d), Product: Unifying Receiver (0xc52b)
    try:
        # Find the raw HID++ interface
        info = next(d for d in hid.enumerate(0x046d, 0xc52b) if d['usage_page'] == 0xff00)
        device = hid.device()
        device.open_path(info['path'])
        device.set_nonblocking(True)
        
        print(f"Connected to T650 on {info['path']}")
        print("Tracking Finger 1... (Ctrl+C to exit)")

        while True:
            report = device.read(20)
            if report and report[0] == 0x11:  # Long Report
                # Byte 4: Finger contact info
                # The first 4 bits usually identify the finger ID
                # The last 4 bits are often the event type (Down/Move/Up)
                finger_count = report[4] & 0x0F
                
                if finger_count > 0:
                    # Combine High Byte (shifted 8 bits) and Low Byte
                    x = (report[5] << 8) | report[6]
                    y = (report[7] << 8) | report[8]
                    
                    print(f"Fingers: {finger_count} | X: {x:4} | Y: {y:4}", end='\r')
                else:
                    print("No fingers detected.                          ", end='\r')
            
            time.sleep(0.01) # 100Hz polling is plenty for a VM

    except StopIteration:
        print("Error: Could not find the HID++ usage page. Is the device passed through?")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        device.close()

if __name__ == "__main__":
    decode_t650()
