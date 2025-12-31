import hid
import time

def persistent_debug():
    try:
        target = next(d for d in hid.enumerate(0x046d, 0xc52b) if d['usage_page'] == 0xff00)
        device = hid.device()
        device.open_path(target['path'])
        device.set_nonblocking(True)
        
        print("Sending heartbeat pings... Move your finger now!")

        while True:
            # Send a 'Get Protocol Version' ping to keep the device awake
            # [ReportID, DevIndex, Feature, Function, ...]
            device.write([0x11, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00])
            
            report = device.read(20)
            if report:
                # We want to see if any packet starts with 11 01
                hex_line = bytes(report).hex(' ')
                print(f"Data: {hex_line}")
                
                # If you see 11 01, that is your finger movement!
                if hex_line.startswith("11 01"):
                    print(">>> TOUCH DATA DETECTED! <<<")
            
            time.sleep(0.01)

    except Exception as e:
        print(f"Error: {e}")
    finally:
        device.close()

if __name__ == "__main__":
    persistent_debug()