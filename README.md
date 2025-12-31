# Logitech T650 Multi-Touch Driver Project

This repository provides the research, diagnostic tools, and driver implementation required to unlock the full 5-finger multi-touch capabilities of the Logitech T650 Rechargeable Touchpad on modern operating systems (Linux and Windows 10/11).



## 1. The Problem
By default, the T650 identifies as a "Generic HID Mouse" when connected via a Unifying Receiver. This legacy compatibility mode hides the high-resolution digitizer data, resulting in:
* **No Touchpad Settings:** The OS does not recognize the device as a touchpad.
* **Limited Gestures:** Only 1-finger movement and 2-finger basic scrolling are available.
* **Low Precision:** Movement is restricted to standard mouse resolution rather than the native 12-bit digitizer precision.

## 2. The Solution: HID++ 2.0 Unlock
Our research into the HID++ 2.0 protocol (specifically **Firmware 038**) revealed that the device requires a specific "Unlock Key" to enable Raw Reporting Mode.

### Hardware Constants
- **VID:** `0x046D` (Logitech)
- **PID:** `0xC52B` (Unifying Receiver)
- **Interface:** 2 (HID++ Protocol Interface)
- **Feature Index:** `0x10` (Multi-touch Feature)
- **Unlock Sequence (Key A):** `11 01 10 21 02`



## 3. Repository Structure

| Folder | Description |
| :--- | :--- |
| `/tools` | Diagnostic scripts to verify 5-finger coordinate data. |
| `/drivers` | User-space driver implementations (Linux `libevdev`). |
| `/docs` | Technical documentation of the 12-bit bit-packing and protocol. |

## 4. Getting Started

### Prerequisites
You must have Python 3.10+ installed along with the `hidapi` library:
```bash
pip install hidapi
