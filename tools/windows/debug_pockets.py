import hid

def debug_t650():
    try:
        # Connect to the raw interface (0xff00)
        info = next(d for d in hid.enumerate(0x046d, 0xc52b) if d['usage_page'] == 0xff00)
        device = hid.device()
        device.open_path(info['path'])
        device.set_nonblocking(True)
        print(f"Connected. Move your finger (especially 3 fingers) and watch...")

        while True:
            report = device.read(20)
            if report:
                # Convert list to bytes to use the .hex() method
                hex_data = bytes(report).hex(' ')
                print(f"Raw Hex: {hex_data}")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    debug_t650()