import hid
import time
from pynput.keyboard import Key, Controller

keyboard = Controller()

def start_gestures():
    try:
        # Connect to the 0xff00 usage page
        target = next(d for d in hid.enumerate(0x046d, 0xc52b) if d['usage_page'] == 0xff00)
        device = hid.device()
        device.open_path(target['path'])
        device.set_nonblocking(True)
        
        print("T650 Link: DIRECT. Ready for gestures.")

        is_gesturing = False
        start_y = None

        while True:
            # Heartbeat to keep the T650 from 'sleeping'
            device.write([0x11, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00] + [0]*13)
            
            # Read until the buffer is empty to get the most recent data
            report = None
            while True:
                last_read = device.read(20)
                if not last_read:
                    break
                report = last_read

            if report and report[0] == 0x11:
                finger_count = report[4] & 0x0F
                # Y-coordinate from your successful trace
                current_y = (report[5] << 8) | report[6]

                if finger_count == 3:
                    if not is_gesturing:
                        start_y = current_y
                        is_gesturing = True
                        print("3 Fingers - Tracking...")
                    elif start_y - current_y > 80: # Swipe UP
                        print(">>> TRIGGER: Task View <<<")
                        keyboard.press(Key.cmd); keyboard.press(Key.tab)
                        keyboard.release(Key.tab); keyboard.release(Key.cmd)
                        is_gesturing = False
                        time.sleep(1.0) # Prevent multi-firing
                else:
                    is_gesturing = False
            
            time.sleep(0.005) # 200Hz polling

    except Exception as e:
        print(f"Connection Lost: {e}")
    finally:
        device.close()

if __name__ == "__main__":
    start_gestures()