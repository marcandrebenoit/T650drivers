# Logitech T650 Implementation Guide (2025 Master)

This guide summarizes the successful "Fruitful Arc" for enabling 5-finger multi-touch on the Logitech T650.

## 1. Hardware Overview
- **Device:** Logitech T650 Rechargeable Touchpad
- **Receiver:** Unifying Receiver (VID: `0x046D`, PID: `0xC52B`)
- **Firmware Tested:** 038
- **Unlock Feature Index:** `0x10` (HID++ 2.0 Multi-touch)

## 2. The Unlock Handshake (Key A)
To switch the device from "Mouse Mode" to "Raw Reporting Mode," send the following 20-byte packet to **Interface 2**:

`11 01 10 21 02 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00`

---

## 3. Linux Implementation: Solaar Rules
Once unlocked, use Solaar to map gestures natively without background scripts.

### 3rd-Finger Gesture Rule
- **Condition (Feature):** `TOUCHPAD RAW XY (6100)`
- **Condition (Test Bytes):**
    - **Begin (inclusive):** `0`
    - **End (exclusive):** `1`
    - **Type:** `mask`
    - **Mask:** `4`
- **Action (Key Press):**
    - **Key:** `Super_L`
    - **Type:** `click` (⚠️ NEVER use 'press' or 'depress')

---

## 4. Windows Implementation: Python Bridge
For Windows 10/11, use a user-space listener to translate raw HID++ packets.

### Core Logic (Pseudo-code)
```python
# Report ID 0x20 parsing
mask = data[4]
is_3_fingers = (mask & 0x04) # Check bit 2

if is_3_fingers:
    # Average Y of all active slots
    y_coords = [get_y(i) for i in active_slots]
    avg_y = sum(y_coords) / len(y_coords)
    
    # Calculate Delta
    if (avg_y - start_y) < -threshold:
        trigger("Win+Tab")

5. Troubleshooting
​Mouse Jams: If the Super key gets stuck, tap it once on your physical keyboard to send the release signal.
​KVM USB: This implementation is designed for host-level access. Virtualized USB stacks may drop high-frequency reports.