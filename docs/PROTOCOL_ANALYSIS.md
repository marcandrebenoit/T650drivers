# HID++ 2.0 Multi-Finger Protocol Analysis

This document details the raw data structure used by the Logitech T650 (Firmware 038) to report multi-touch data after being unlocked into "Raw Mode."

## Data Packet Structure (Report ID 0x20)
When "Key A" (`11 01 10 21 02`) is accepted, the device begins streaming 20-byte Extra Long reports.

| Byte  | Name            | Description                                              |
| :---- | :-------------- | :------------------------------------------------------- |
| 0     | Report ID       | `0x20` (Extra Long HID++ Report)                         |
| 1     | Device Index    | `0x01` (The T650 index on the Unifying Receiver)         |
| 2     | Feature Index   | `0x10` (Multi-touch Feature)                             |
| 4     | Contact Mask    | Bitmask: Bit 0 (F1) to Bit 4 (F5). 1 = Down, 0 = Up.     |
| 5-7   | Finger 1 Data   | 12-bit X, 12-bit Y coordinates.                          |
| 8-10  | Finger 2 Data   | 12-bit X, 12-bit Y coordinates.                          |
| 11-13 | Finger 3 Data   | 12-bit X, 12-bit Y coordinates.                          |
| 14-16 | Finger 4 Data   | 12-bit X, 12-bit Y coordinates.                          |
| 17-19 | Finger 5 Data   | 12-bit X, 12-bit Y coordinates.                          |

## Coordinate Bit-Packing (12-bit)
Each finger occupies 3 bytes (24 bits) to store two 12-bit values.

- **Byte 0:** Lower 8 bits of X.
- **Byte 1:** Lower 4 bits of Y (High Nibble) | Upper 4 bits of X (Low Nibble).
- **Byte 2:** Upper 8 bits of Y.

### Python Parsing Logic
```python
def parse_12bit(data, offset):
    # Extract X (Bytes 0 and 1)
    x = data[offset] | ((data[offset + 1] & 0x0F) << 8)
    # Extract Y (Bytes 1 and 2)
    y = (data[offset + 1] >> 4) | (data[offset + 2] << 8)
    return x, y
