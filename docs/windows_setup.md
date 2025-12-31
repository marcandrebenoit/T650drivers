# Windows 10/11 Implementation Plan

Windows does not natively support the T650 as a "Precision Touchpad."
To enable multi-finger gestures on Windows, we must use a Python-based bridge that translates raw HID++ 2.0 packets into Windows shell commands.

## Prerequisites
- **Python 3.10+**
- **hidapi**: `pip install hidapi`
- **pynput**: For injecting keyboard shortcuts. `pip install pynput`

## The "Bridge" Architecture
Since Windows 10/11 will only see a standard mouse, our script runs in the background to:
1. **Unlock the T650** using the HID++ 2.0 Key A handshake.
2. **Sniff the 20-byte Extra Long reports** (Report ID `0x20`).
3. **Calculate Deltas:** Track the `Y` coordinate shift of 3 fingers.
4. **Trigger Shortcuts:** - **3-Finger Swipe Up:** Sends `Win + Tab` (Task View).
   - **3-Finger Swipe Left/Right:** Sends `Ctrl + Win + Left/Right` (Desktop Switching).

## Known Limitations
- **Cursor Conflict:** Windows may fight the script for control of the pointer.
We recommend letting Windows handle the 1-finger movement and using the script exclusively for 3+ finger "Gesture Injection."
