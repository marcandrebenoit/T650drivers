import hid
import time
from pynput.keyboard import Key, Controller

kb = Controller()

def start_gestures():
    print("--- T650 GENTLE DRIVER STARTED ---")
    print("Safety limits enabled to prevent USB bus lockup.")
    
    while True:
        device = None
        try:
            # Connect to the Raw interface
            target = next(d for d in hid.enumerate(0x046d, 0xc52b) if d['usage_page'] == 0xff00)
            device = hid.device()
            device.open_path(target['path'])
            device.set_nonblocking(True)
            print("Link Established. Monitoring gestures...")

            is_gesturing = False
            start_x, start_y = None, None
            last_heartbeat = 0

            while True:
                # GENTLE HEARTBEAT: Only once every 3 seconds
                # This keeps the T650 awake without flooding the USB bus
                if time.time() - last_heartbeat > 3.0:
                    try:
                        device.write([0x11, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00] + [0]*13)
                        last_heartbeat = time.time()
                    except: pass

                report = device.read(20)
                if report and report[0] == 0x11:
                    fingers = report[4] & 0x0F
                    # Finger 1 coordinates (High Byte << 8 | Low Byte)
                    curr_x = (report[5] << 8) | report[6]
                    curr_y = (report[7] << 8) | report[8]

                    if fingers >= 3:
                        if not is_gesturing:
                            start_x, start_y = curr_x, curr_y
                            is_gesturing = True
                        else:
                            dx = start_x - curr_x
                            dy = start_y - curr_y

                            # 3-FINGER UP -> Task View
                            if fingers == 3 and dy > 100:
                                print("Action: Task View")
                                with kb.pressed(Key.cmd): kb.tap(Key.tab)
                                is_gesturing = False; time.sleep(0.8)

                            # 4-FINGER SWIPE -> Change Virtual Desktop
                            elif fingers == 4:
                                if dx > 100:
                                    print("Action: Desktop Left")
                                    with kb.pressed(Key.cmd, Key.ctrl): kb.tap(Key.left)
                                    is_gesturing = False; time.sleep(0.6)
                                elif dx < -100:
                                    print("Action: Desktop Right")
                                    with kb.pressed(Key.cmd, Key.ctrl): kb.tap(Key.right)
                                    is_gesturing = False; time.sleep(0.6)
                    else:
                        is_gesturing = False

                # 0.01 = 100Hz. This is the 'Goldilocks' zone for stability.
                time.sleep(0.01) 

        except Exception as e:
            print(f"Waiting for T650... ({e})")
            if device: device.close()
            time.sleep(3) # Wait before retrying to let the USB bus rest

if __name__ == "__main__":
    start_gestures()
