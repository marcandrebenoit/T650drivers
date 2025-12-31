import hid
import time

def deep_probe():
    try:
        # Find the Raw Vendor interface
        info = next(d for d in hid.enumerate(0x046d, 0xc52b) if d['usage_page'] == 0xff00)
        device = hid.device()
        device.open_path(info['path'])
        device.set_nonblocking(False) # Wait for a response
        
        print(f"Connected to {info['path']}")
        print("Probing T650... Move your fingers while this runs.")

        while True:
            # Command: Get Protocol Version (This is the most 'standard' HID++ query)
            # [ID, DevIndex, Feature, Function, ...]
            # We use 0x11 (Long Report) to force the device into that mode
            try:
                device.write([0x11, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00] + [0]*13)
                
                # Try to read for 100ms
                report = device.read(20)
                if report:
                    print(f"REPLY RECEIVED: {bytes(report).hex(' ')}")
                    if report[0] == 0x11 and report[4] != 0:
                        print(f"!!! MOTION DATA: Fingers={report[4] & 0x0F} !!!")
            except Exception as e:
                print(f"Write/Read error: {e}")
                break
            
            time.sleep(0.05)

    except StopIteration:
        print("Error: Unifying Receiver Raw Interface not found. Is it redirected?")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    deep_probe()