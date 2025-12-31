import hid
import time
from pynput.mouse import Controller

mouse = Controller()

def start_driver():
    try:
        # Connect to the T650 raw interface
        info = next(d for d in hid.enumerate(0x046d, 0xc52b) if d['usage_page'] == 0xff00)
        device = hid.device()
        device.open_path(info['path'])
        device.set_nonblocking(True)
        
        print("T650 Virtual Driver Active. Move your finger!")

        last_x, last_y = None, None
        # Sensitivity: Increase this if the cursor moves too slow
        sensitivity = 1.5 

        while True:
            report = device.read(20)
            if report and report[0] == 0x11:
                finger_count = report[4] & 0x0F
                
                if finger_count > 0:
                    # Decode coordinates
                    current_x = (report[5] << 8) | report[6]
                    current_y = (report[7] << 8) | report[8]

                    if last_x is not None and last_y is not None:
                        # Calculate the movement delta
                        dx = (current_x - last_x) * sensitivity
                        dy = (current_y - last_y) * sensitivity
                        
                        # Move the Windows cursor
                        # Note: Y is usually inverted on trackpads
                        mouse.move(dx, dy)

                    last_x, last_y = current_x, current_y
                else:
                    # Finger lifted, reset tracking
                    last_x, last_y = None, None
            
            time.sleep(0.005) # Lower sleep = smoother movement

    except Exception as e:
        print(f"Driver Error: {e}")
    finally:
        device.close()

if __name__ == "__main__":
    start_driver()
